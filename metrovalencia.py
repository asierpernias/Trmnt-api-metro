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
    resultado = recorrerDiccionario(previsiones, id_parada)
    return resultado


def recorrerDiccionario(previsiones, id_parada):
    datos = []
    if previsiones["previsiones"]:
        for i in  previsiones["previsiones"]:
            datos.append(
                {
                    "line": i['line'],
                    "hour": i['hora'],
                    "destination": i['destino'],
                    "left": i["seconds"]
                }
            )
            identificador = f"{id_parada}-{i['line']}-{i['destino']}-{i['hora']}"
        return datos
    else:
        return []

def conversionTiempo(seconds):
    minutes = seconds // 60
    secondsleft = seconds % 60
    return minutes, secondsleft
placeholderTime = 670
tiempoNotificatin = 5 #min
minutes, seconds = conversionTiempo(placeholderTime)
notifications = set()
def notificar(minutes, seconds, id):
    pass
def comprovarTime(seconds, identificador):
    if minutes < tiempoNotificatin and identificador not in notifications: 
        notificar(minutes, seconds)
        notifications.add(identificador)


datos1 = obtener_paradas(int(input("ID: ")))

print(datos1)