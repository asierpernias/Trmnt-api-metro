# MetroValencia Noticias
MetroValencia Noticias is  TRMNL plugin that polls a custom API (`backend/`) and renders the obtained data showing the exact time r the trains are supposed to arrive to the underground station you select, how many minutes there are left for it, which line the train will arrive operates on and its final destination.

**Disclaimer: The API gets its data from a third-party API [Alex Badi MetroValencia API](https://dash.metroapi.alexbadi.es/). It is not under my control so it can lack of some data and have issues at some point.**

## How it works

- `backend/`: A custom FastAPI API that gets the data from the station, formats it and returns it as a small JSON.
- `frontend`: The section that polls the data from the backend and renders it. It contains the Liquid files for each different available layout.

## API

#### `GET parada/{id_parada}?limit=5`

###### id_parada
`backend/paradas.json` contains a list of all the stations and the code asociated to them. 

###### limit (1-10, Default 5)
The amount of trains that will be returned in the JSON answer.

###### Answer example
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

#### Health
Returns `{"status": "ok"}`

#### Exceptions
- 404: Stop couldn't be found.
- 502: Unknown exception on the origina data source.
- 504: Timeout on the original data source.

## Running the backend

```
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Previewing the plugin

**Requires Ruby 4.0+ and [trmnlp](https://github.com/usetrmnl/trmnlp)**

```
gem install trmnl_preview
trmnlp serve -d frontend
```

Change the `stop_id` on `frontend/src/settings.yml` (`polling_url`) in order to change the station data that is displayed on the device.

## Following steps:
For now Ill stop working on the project but in a future I would like to add three things:
1. Fully controlled by me or more reliable/open source data source to avoid errors I cant tackle in any way.
2. Easier selection and change between different stations polling, as now it is just harcoded.
3. Compatibility with mobile phone (another project?) that actuates as a notifier.

## Screenshots

## LICENSE

This project is under the MIT License. Read `LICENSE.txt` for more info.