"""
Dutch Gas prices API
"""
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from gas_prices import gas_prices
from gas_map import gas_map
import os

app = FastAPI(
    title="Dutch Gas prices API",
    description="Dutch Gas prices API.",
    version="1.0",
)


@app.get("/")
async def root():
    """
    Gas prices API Status
    """
    return {"Status": "Online"}


@app.get("/api/v1/gas_prices/{station_id}",
         summary="Query the gas prices from a station",
         description="Returns Euro 95 e5/e10 and Diesel prices from directlease.nl \
             (Note: because it's using OCR technology it's not 100% accurate)",
         )
async def api_gas_prices(station_id: str = Query(None, \
                         description='Provide Station ID (number before .png)')):
    """
    Query the gas prices from a station
    """
    result = gas_prices(station_id)
    return result


@app.get("/api/v1/gas_maps",
         summary="Get ",
         description="Returns KML file with gas stations markers."
         )
async def api_gas_map():
    """
    Create a KML file with gas stations.
    """
    result = gas_map()
    return FileResponse(path=result, media_type='application/zip', filename=os.path.basename(result))
