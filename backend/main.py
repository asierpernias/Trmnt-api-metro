from fastapi import FastAPI, HTTPException, Query
from metrovalencia import obtener_paradas, paradas, InvalidMetroResponse
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get('/parada/{id_parada}')
def parada(id_parada:int, limit: int = Query(5, ge=1, le= 10)):
    
    if str(id_parada) not in paradas:
        raise HTTPException(status_code=404, detail="Stop not found")

    try:
        trains, name, updated_at = obtener_paradas(id_parada)
    
    except requests.Timeout as e:
        logger.warning("Metro API timeout for stop %s, %s:", id_parada, e)
        raise HTTPException(status_code=504, detail="API Timeout")
    except requests.RequestException as e:
        logger.warning("Metro API error for stop %s, %s:", id_parada, e)
        raise HTTPException(status_code=502, detail="Metro API error")
    except InvalidMetroResponse as e:
        logger.warning("Invalid Metro respones for stop %s, %s:", id_parada, e)
        raise HTTPException(status_code=502, detail="Invalid answer from metro API")
    

    return {
        "station": name,
        "trains": trains[:limit],
        "updated_at": updated_at
    }

@app.get("/health")
def health():
    return {"status": "ok"}