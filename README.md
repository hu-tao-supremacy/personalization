## Direct connection to PosgresSQL

```
psql -U username -h localhost -p 5432 dbname
```

## Check for user ids that are ready to recommend (For testing)

SELECT user_id FROM user_event join event_recommendation on user_event.event_id = event_recommendation.event_id;

## First Time Setup

- install [python3](https://www.python.org/downloads/) and [pip3](https://pip.pypa.io/en/stable/installing/)
- Run Command

```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate.fish หรือ source env/bin/activate
```

- Install dependencies
  `pip3 install -r requirements.txt`
- add environment variables in env/bin/activate file
