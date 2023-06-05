#Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: To be able to obtain data from the Start and End Dates, the date format must be YYYY-MM-DD/YYYY-MM-DD"
    )

##### Precipitation Analysis #####
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Design a query to retrieve the last 12 months of precipitation data
    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        all()

    session.close()

    # Create a dictionary from the row data and append to a list of 
    # all_precipitation_values
    all_precipitation_values = []
    for date, prcp  in precipitation_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_precipitation_values.append(prcp_dict)

    return jsonify(all_precipitation_values)

###### Return a JSON list of stations from the dataset #####
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Stations
    station_results = session.query(Station.station, Station.name).all()

    session.close()

     #Create a dictionary from the row data and append to a list of all_stations
    all_station_values = []
    for station, name  in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
                    
        all_station_values.append(station_dict)

    return jsonify(all_station_values)


##### Get the previous 12 months of Temperature Obervation (TOBS) data #####

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station 
    # for the previous year of data
    tobs_results = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date.desc()).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_tobs
    all_tobs_values = []
    for date,tobs, station in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["station"] = station
        
        all_tobs_values.append(tobs_dict)

    return jsonify(all_tobs_values)

##### Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query min, avg, and max for all the dates greater than or equal to the start date.
    start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs_values = []
    for min, avg, max in start_date_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs_values.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs_values)

@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Query min, avg, and max for the dates from the start date to the end date, inclusive

    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs_values = []
    for min, avg, max in start_end_results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs_values.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs_values)

if __name__ == "__main__":
    app.run(debug=True)