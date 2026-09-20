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
    texto = f"La proximas previsiones de la parada {parada} son Línea: {previsiones['previsiones'][0]['line']} - Hora: {previsiones['previsiones'][0]['hora']}"
    print(texto)

obtener_paradas(int(input("ID: ")))