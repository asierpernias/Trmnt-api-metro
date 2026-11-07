import requests
import json 
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
cache = {}
CONTACT = os.environ.get("METRO_CONTACT", "tu@email.com")
CACHE_TTL = int(os.environ.get("CACHE_TTL", "60"))
TIMEOUT = float(os.environ.get("METRO_TIMEOUT", "10"))
USER_AGENT = f"trmnl-metrovalencia/1 (contact={CONTACT})"
class InvalidMetroResponse(Exception):
    """The metro API returned an unexpected structure"""

PARADAS_PATH = Path(__file__).parent / "paradas.json"
with open(PARADAS_PATH, encoding="utf-8") as json_file:
    paradas = json.load(json_file)

def obtener_paradas(id_parada):
    parada = paradas[str(id_parada)]
    if id_parada in cache:
        time_saved, trains, updated_madrid = cache[id_parada]
        if time.monotonic() - time_saved < CACHE_TTL:
            logger.info("Cache hit for stop %s", id_parada)
            return trains, parada, updated_madrid
    logger.info("Querying metro API for stop %s", id_parada)
    url = f"https://metroapi.alexbadi.es/prevision/{id_parada}/parse"
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    }
    respones = requests.get(url, headers=headers, timeout=TIMEOUT)
    respones.raise_for_status()
    previsiones = respones.json()
    resultado = recorrerDiccionario(previsiones)
    updated_at = datetime.now(timezone.utc)
    updated_madrid = updated_at.astimezone(ZoneInfo("Europe/Madrid"))
    updated_madrid = updated_madrid.isoformat()
    cache[id_parada] = (time.monotonic(), resultado, updated_madrid)
    return resultado, parada, updated_madrid


def recorrerDiccionario(previsiones):
    if not isinstance(previsiones, dict):
        raise InvalidMetroResponse("The answer is not a dictionary")
    if "previsiones" not in previsiones:
        raise InvalidMetroResponse("The key 'previsiones' is missing")
    if not isinstance(previsiones["previsiones"], list):
        raise InvalidMetroResponse("'previsiones' is not a list")
    datos = []
    for i in  previsiones["previsiones"]:
        try:
            seconds = int(i['seconds'])
            if seconds < 0:
                raise ValueError("Seconds unexpected data")
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
        except (KeyError, TypeError, ValueError):
            logger.warning("Skipping bad train: %r", i)
            continue
    if previsiones["previsiones"] and not datos:
        raise InvalidMetroResponse("No train could be processed") 
    return datos
    
def conversionTiempo(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return minutes, seconds
