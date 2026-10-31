import requests
import json 
import time

cache = {}
CACHE_TTL = 60

with open('paradas.json', encoding="utf-8") as json_file:
    paradas = json.load(json_file)

def obtener_paradas(id_parada):
    parada = paradas[str(id_parada)]
    if id_parada in cache:
        time_saved, trains = cache[id_parada]
        if time.monotonic() - time_saved < CACHE_TTL:
            return trains, parada
    url = f"https://metroapi.alexbadi.es/prevision/{id_parada}/parse"
    headers = {
        'User-Agent': 'postman-test/1 (Prueba; contact=example@example.com)',
        'Accept': 'application/json'
    }
    payload={}
    respones = requests.request("GET", url, headers=headers, data=payload, timeout=10.0)
    respones.raise_for_status()
    previsiones = respones.json()
    resultado = recorrerDiccionario(previsiones)
    cache[id_parada] = (time.monotonic(), resultado)
    return resultado, parada


def recorrerDiccionario(previsiones):
    datos = []
    if previsiones["previsiones"]:
        for i in  previsiones["previsiones"]:
            seconds = int(i['seconds'])
            minutes_left, seconds_left = conversionTiempo(seconds)
            datos.append(
                {
                    "line": i['line'],
                    "hour": i['hora'],
                    "destination": i['destino'],
                    "seconds_left": seconds_left, 
                    "minutes_left": minutes_left
                }
            )
        return datos
    else:
        return []

def conversionTiempo(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return minutes, seconds
