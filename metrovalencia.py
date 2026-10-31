import requests
import json 


with open('paradas.json', encoding="utf-8") as json_file:
    paradas = json.load(json_file)

def obtener_paradas(id_parada):
    url = f"https://metroapi.alexbadi.es/prevision/{id_parada}/parse"

    parada = paradas[str(id_parada)]
    headers = {
        'User-Agent': 'postman-test/1 (Prueba; contact=example@example.com)',
        'Accept': 'application/json'
    }
    payload={}
    respones = requests.request("GET", url, headers=headers, data=payload)
    previsiones = respones.json()
    resultado = recorrerDiccionario(previsiones)
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
