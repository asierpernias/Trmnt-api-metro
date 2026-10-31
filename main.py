from fastapi import FastAPI, HTTPException, Query
from metrovalencia import obtener_paradas, paradas
import requests

app = FastAPI()

@app.get('/parada/{id_parada}')
def parada(id_parada:int, limit: int = Query(5, ge=1, le= 10)):
    
    if str(id_parada) not in paradas:
        raise HTTPException(status_code=404, detail="Stop not found")

    try:
        trains, name = obtener_paradas(id_parada)
    
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="API Timeout")
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Metro API error")

    

    return {
        "station": name,
        "trains": trains[:limit],
    }