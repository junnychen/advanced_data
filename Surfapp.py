import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
import pandas as pd

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= '2016-08-23').all()
    #create dict using list comprehension 
    #d = dict((key, value) for (key, value) in iterable)
    #d = {key:value for key, value in iterable }
    prcp_list = dict((date, prcp) for (date, prcp) in precipitation)
    return jsonify(prcp_list)
  
@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    stations= session.query(Station.station,Station.name).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")

def temp():
    temp = dt.date(2017,8,23) -dt.timedelta(days=365)
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
    temp = session.query(Measurement.tobs).\
            filter(Measurement.date >= '2016-08-23').all()
    #list object
    temp = list(np.ravel(temp))
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end == None:
        dates = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        dates = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    normals = list(np.ravel(dates))
    return jsonify(normals)
        

if __name__ == '__main__':
    app.run()
