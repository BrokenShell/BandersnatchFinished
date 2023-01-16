import os

from Fortuna import random_int, random_float
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine

APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        monster=Monster().to_dict(),
    )


@APP.route("/data")
def data():
    db = Database()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("app", "model.joblib")
    retrain = request.values.get("retrain", type=bool)

    if retrain or not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)

    stats = (round(random_float(1, 250), 2) for _ in range(3))
    level = request.values.get("level", type=int) or random_int(1, 20)
    health = request.values.get("health", type=float) or next(stats)
    energy = request.values.get("energy", type=float) or next(stats)
    sanity = request.values.get("sanity", type=float) or next(stats)
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    info = machine.info()
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )
