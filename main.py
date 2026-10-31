from fastapi import FastAPI, HTTPException
from metrovalencia import obtener_paradas
import json

app = FastAPI()

@app.get('/parada/{id_parada}')
def parada(id_parada:int):
    with open('paradas.json', encoding="utf-8") as json_file:
        comprobacion = json.load(json_file)
        if str(id_parada) not in str(comprobacion):
            raise HTTPException(status_code=404, detail="Stop not found")

    trains, name = obtener_paradas(id_parada)
    
    return {
        "station": name,
        "trains": trains,
    }