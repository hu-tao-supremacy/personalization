from concurrent import futures
import logging
import os

import grpc
import hts.common.common_pb2 as common
import hts.personalization.service_pb2 as personalization_service
import hts.personalization.service_pb2_grpc as personalization_service_grpc
from db_model import (
    DBSession,
    UserEvent,
    EventRecommendation,
    Event,
    EventDuration
)
from helper import (
    getInt32Value,
    getStringValue,
    getTimeStamp,
)
from toolz.dicttoolz import merge_with
from scipy.special import softmax
from random import choices
import numpy as np 
from datetime import datetime
from sqlalchemy import func


class PersonalizationService(personalization_service_grpc.PersonalizationServiceServicer):
    def GetRecommendedEvents(self, request, context):
        session = DBSession()
        try:
            user_id = request.user_id
            k_events = request.k_events
            user_recommendation_score = session.query(UserEvent)\
            .filter(UserEvent.user_id == user_id, EventRecommendation.score.isnot(None))\
            .join(EventRecommendation, UserEvent.event_id == EventRecommendation.event_id)\
            .with_entities(EventRecommendation.score)

            dictionary = {}
            for item in user_recommendation_score:
                dictionary = merge_with(sum, dictionary, item[0])
            event_ids = list(dictionary.keys())
            
            # check durations 
            event_ids_future_query = session.query(EventDuration).filter(EventDuration.event_id.in_(event_ids))\
                .group_by(EventDuration.event_id)\
                .order_by(func.min(EventDuration.start))\
                .having(datetime.now() < func.min(EventDuration.start))\
                .with_entities(EventDuration.event_id)
            event_ids_future = []
            for item in event_ids_future_query:
                event_ids_future.append(str(item[0]))
            
            # get score and convert to prob using softmax
            events_score = [dictionary[x] for x in event_ids_future]
            if len(events_score) == 0:
                return personalization_service.GetRecommendedEventsResponse(event_collection=[])
            prob = softmax(events_score)

            # events to recommended
            size = min(k_events, len(event_ids_future))
            choice = np.random.choice(event_ids_future, p=prob, size=size, replace=False)
            query_events = session.query(Event).filter(Event.id.in_(choice)).all()

            data = map(
                lambda event: common.Event(
                    id=event.id,
                    organization_id=event.organization_id,
                    location_id=getInt32Value(event.location_id),
                    description=event.description,
                    name=event.name,
                    cover_image_url=getStringValue(event.cover_image_url),
                    cover_image_hash=getStringValue(event.cover_image_hash),
                    poster_image_url=getStringValue(event.poster_image_url),
                    poster_image_hash=getStringValue(event.poster_image_hash),
                    profile_image_url=getStringValue(event.profile_image_url),
                    profile_image_hash=getStringValue(event.profile_image_hash),
                    attendee_limit=event.attendee_limit,
                    contact=getStringValue(event.contact),
                    registration_due_date=getTimeStamp(event.registration_due_date),
                ),
                query_events,
            )
            return personalization_service.GetRecommendedEventsResponse(event_collection=data)
        except Exception as e:
            session.rollback()
            raise Exception(f"Something went wrong: {e}")
            return personalization_service.GetRecommendedEventsResponse(event_collection=[])
        finally:
            session.close()

port = os.environ.get("GRPC_PORT")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    personalization_service_grpc.add_PersonalizationServiceServicer_to_server(
        PersonalizationService(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print('service started')
    server.wait_for_termination()

serve()
