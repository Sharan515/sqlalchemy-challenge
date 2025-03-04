# Design Your Climate App

#Designing a Flask API based on the queries developed
##########################################33
#Import dependencies and reflect database
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///C:\\Users\\shara\\Desktop\\CLASSES\\Module 10\\Module 10 assignment due Mar3,25\\SurfsUp\\Resources\\hawaii.sqlite")

# Reflect Database into ORM classes

Base = automap_base()
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station




################# 1. / ################ 

#     Start at the homepage.
################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#  List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

#################  2. /api/v1.0/precipitation ################ 

#     Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all precipation queries"""
    # Query
    results = session.query(Measurement.prcp).all()

    session.close()


    # Convert list of tuples into normal list
    precip_data = list(np.ravel(results))

    

#     Return the JSON representation of your dictionary.
    return jsonify(precip_data)


################ 3. /api/v1.0/stations ################ 

#     Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station_list():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all precipation queries"""
    # Query
    results = session.query(Measurement.station).distinct().all()

    session.close()


    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    

#     Return the JSON representation of your dictionary.
    return jsonify(station_list)


#################  4. /api/v1.0/tobs ################ 
#@app.route("/api/v1.0/tobs")
#     Query the dates and temperature observations of the most-active station for the previous year of data.

#     Return a JSON list of temperature observations for the previous year.



#################  5. /api/v1.0/<start> and /api/v1.0/<start>/<end> ################ 
#@app.route("/api/v1.0")
#     Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#     For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#     For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)






if __name__ == '__main__':
    app.run(debug=True)
