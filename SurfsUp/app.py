# Import the dependencies.
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve the last 12 months of precipitation data."""
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp)\
                     .filter(Measurement.date >= year_ago).all()
    session.close()

    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Retrieve a list of all the stations."""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    stations_list = list(np.ravel(results))
    return jsonify(stations=stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Retrieve temperature observations from the most-active station for the past year."""
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs)\
                     .filter(Measurement.station == 'USC00519281')\
                     .filter(Measurement.date >= year_ago).all()
    session.close()

    temps_list = list(np.ravel(results))
    return jsonify(temperatures=temps_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):
    """Return min, max, and avg temperature for the given date range."""
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    # Convert start and end dates from string to datetime format
    start = dt.datetime.strptime(start, "%Y-%m-%d")

    if end:
        end = dt.datetime.strptime(end, "%Y-%m-%d")
        results = session.query(*sel).filter(Measurement.date >= start)\
                                     .filter(Measurement.date <= end).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temperatures=temps)

if __name__ == "__main__":
    app.run(debug=True)
