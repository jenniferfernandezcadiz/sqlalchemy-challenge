# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
import pandas as pd

# setting the path 
engine = create_engine("sqlite:///../sqlalchemy-challenge/resources/hawaii.sqlite")


# reflecting an exisiting database into a new model
Base=automap_base()

# reflecting the tables
Base.prepare(engine, reflect=True)


# save references for each table
measurement=Base.classes.measurement
station=Base.classes.station


session=Session(engine)

#############################################

from flask import Flask, json, jsonify
import datetime as dt

###############################
#Flask setup 
###############################
app=Flask(__name__)
###############################


#Flask Routes
########################

@app.route('/')
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )

###########################
#Precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last_twelve_months).order_by(measurement.date).all()

    precip={date: prcp for date, prcp in prcp}

    return jsonify(precip)


###########################

#list of stations

@app.route("/api/v1.0/stations")
def stations():
    all_stations=session.query(station.station,station.name).all()

    return jsonify(all_stations)

###############################

#Most active station for last year of data 

@app.route("/api/v1.0/tobs")
def tobs():
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    temp = session.query(measurement.tobs).filter(measurement.station=="USC00519281").filter(measurement.date >=last_twelve_months).order_by(measurement.tobs).all()

    return jsonify(temp)

#############################

#start

@app.route('/api/v1.0/<start>')
def start(start=None):

    #start = measurement.date <='2010-01-01'
    #end = measurement.date >= '2017-08-23'

    tobs=session.query(measurement.tobs).filter(measurement.date.between(start,'2017-08-23')).all()

    tobs_df=pd.DataFrame(tobs)

    t_avg=tobs_df['tobs'].mean()
    t_min=tobs_df['tobs'].min()
    t_max=tobs_df['tobs'].max()

    return jsonify (t_avg,t_min,t_max)

####################################

# Start & End 
@app.route('/api/v1.0/<start>/<end>')
def startend(start=None, end=None):

    #start = measurement.date <='2010-01-01'
    #end = measurement.date >= '2017-08-23'

    tobs=session.query(measurement.tobs).filter(measurement.date.between(start,end)).all()

    tobs_df=pd.DataFrame(tobs)

    t_avg=tobs_df["tobs"].mean()
    t_max=tobs_df["tobs"].max()
    t_min=tobs_df["tobs"].min()

    return jsonify(t_avg,t_max,t_min)


if __name__=='__main__':
    app.run(debug=True)






