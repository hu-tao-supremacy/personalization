## Direct connection to PosgresSQL

```
psql -U username -h localhost -p 5432 dbname
```

SELECT user_id FROM user_event join event_recommendation on user_event.event_id = event_recommendation.event_id;
