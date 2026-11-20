# MetroValencia Noticias
A TRMNL plugin that displays the following trains that will arrive to the station you select. It will display the exact time it is supposed to arrive, how many minutes are left for it, the line it works on and which is its destination.

## How it works

- `backend/`: a FastAPI service that fetches the schedule and returns a small JSON-
- `frontend/`: the TRMNL plugin (Liquid templates for all available layouts)

TRMNL polls the backend and later the templates on `frontend/` render the result from the obtained data.

## API

`GET /parada/{stop_id}?limit=5`

- limit: number of trains to return (1-10, default 5).
 
- Example of an API answer:

```json
{
  "station": "Colón",
  "trains": [
    {
      "line": 2,
      "hour": "16:11",
      "destination": "Torrent Avinguda",
      "minutes_left": 5,
      "seconds_left": 54
    }
  ],
  "updated_at": "2026-11-07T16:05:00+01:00"
}
```
Stop IDs are all listed in `backend/paradas.json`.

**Disclaimer:**
The arrival times come from a thrid-party API (`metroapi.alexbadi.es`) which is not under my control and has had down times before as some stations usually lack of data.


## Running the backend

```
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Previewing the pluging

**Requires Ruby 4.0+ and [trmnlp](https://github.com/usetrmnl/trmnlp)**

```
gem install trmnl_preview
trmnlp serve -d frontend
```

Set the stop in `frontend/src/settings.yml` (`polling_url`).

## Screenshots

## LICENSE

This project is under the MIT License. Reade `LICENSE.txt` for more info.