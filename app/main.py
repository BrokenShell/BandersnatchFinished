import os

from Fortuna import random_float, random_int
from MonsterLab import Monster
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
db = Database()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "monster": Monster().to_dict(),
        },
    )


@app.get("/data")
async def data(request: Request):
    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "count": db.count(),
            "table": db.html_table(),
        },
    )


@app.get("/view")
async def view_get(request: Request):
    default_x_axis = options[1]
    default_y_axis = options[2]
    default_target = options[4]
    graph = chart(
        df=db.dataframe(),
        x=default_x_axis,
        y=default_y_axis,
        target=default_target,
    ).to_json()
    return templates.TemplateResponse(
        "view.html",
        {
            "request": request,
            "options": options,
            "x_axis": default_x_axis,
            "y_axis": default_y_axis,
            "target": default_target,
            "count": db.count(),
            "graph": graph,
        },
    )


@app.post("/view")
async def view_post(request: Request,
                    x_axis: str = Form(...),
                    y_axis: str = Form(...),
                    target: str = Form(...)):
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return templates.TemplateResponse(
        "view.html",
        {
            "request": request,
            "options": options,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "target": target,
            "count": db.count(),
            "graph": graph,
        },
    )


@app.get("/model")
async def model_get(request: Request):
    filepath = os.path.join("app", "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    level = random_int(1, 20)
    health = round(random_float(1, 250), 2)
    energy = round(random_float(1, 250), 2)
    sanity = round(random_float(1, 250), 2)
    prediction, confidence = machine(
        DataFrame([dict(zip(options, (level, health, energy, sanity)))])
    )
    info = machine.info()
    return templates.TemplateResponse(
        "model.html",
        {
            "request": request,
            "info": info,
            "level": level,
            "health": health,
            "energy": energy,
            "sanity": sanity,
            "prediction": prediction,
            "confidence": f"{confidence:.2%}",
        },
    )


@app.post("/model")
async def model_post(request: Request,
                     retrain: str = Form("no"),
                     level: int = Form(...),
                     health: float = Form(...),
                     energy: float = Form(...),
                     sanity: float = Form(...)):
    filepath = os.path.join("app", "model.joblib")
    if retrain == "yes" or not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    prediction, confidence = machine(
        DataFrame([dict(zip(options, (level, health, energy, sanity)))])
    )
    info = machine.info()
    return templates.TemplateResponse(
        "model.html",
        {
            "request": request,
            "info": info,
            "level": level,
            "health": health,
            "energy": energy,
            "sanity": sanity,
            "prediction": prediction,
            "confidence": f"{confidence:.2%}",
        },
    )
