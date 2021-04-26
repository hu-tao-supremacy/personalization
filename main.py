from concurrent import futures
import logging
import os

import grpc
import hts.common.common_pb2 as common
import hts.personalization.service_pb2 as personalization_service
import hts.personalization.service_pb2_grpc as personalization_service_grpc

class PersonalizationService(personalization_service_grpc.PersonalizationServiceServicer):
    def GetRecommendedEvents(self, request, context):
        return personalization_service.GetRecommendedEventsResponse(eventCollection=[])

port = os.environ.get("GRPC_PORT")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    personalization_service_grpc.add_PersonalizationServiceServicer_to_server(
        PersonalizationService(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()

serve()
