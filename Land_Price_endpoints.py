import uvicorn

from joblib import dump, load
from fastapi import FastAPI
import osmnx as ox
from pydantic import BaseModel


class Land_Prediction(BaseModel):
    Latitude : float
    Longitude : float


app = FastAPI()

with open("price_predicition_0_1.joblib", "rb") as f:
    model = load(f)


@app.get('/')
async def index():
    return {'message': 'This is the homepage of the API '}


@app.post('/prediction')
async def get_land_feature(data: Land_Prediction):
    received = data.dict()

    tags = {'shop': True,
            'office': True,
            'landuse': True,
            'highway': True,
            'waterway': True,
            'water': True,
            'natural': True,
            'man_made': True,
            'tourism': True,
            'building': True,
            'amenity': True,
            }
    Latitude = received['Latitude']
    Longitude = received['Longitude']

    variable=[]

    value = {'shop': 0,
             'office': 0,
             'landuse': 0,
             'highway': 0,
             'waterway': 0,
             'water': 0,
             'natural': 0,
             'man_made': 0,
             'tourism': 0,
             'building': 0,
             'amenity': 0,
             }
    for rag in tags:
        tag = {rag: True}
        gdf = ox.geometries.geometries_from_point((Latitude, Longitude), dist=1500, tags=tag)
        value[rag] = len(gdf)
    shop = value['shop']
    office = value['office']
    landuse = value['landuse']
    highway = value['highway']
    waterway = value['waterway']
    water = value['water']
    natural = value['natural']
    man_made = value['man_made']
    tourism = value['tourism']
    building = value['building']
    amenity = value['amenity']



    pred_name = model.predict(
        [[shop, office, landuse, highway, waterway, water, natural, man_made, tourism, building, amenity]]).tolist()[0]

    return {'prediction': pred_name}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000)
