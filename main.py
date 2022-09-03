# The framework used is from https://pypi.org/project/FlightRadarAPI/

import time

from FlightRadar24.api import FlightRadar24API
from logger import Location
from logger import FlightLogger
from logger import FlightsTracked
from data import BOUNDARY
from data import CENTRE_LATITUDE
from data import CENTRE_LONGITUDE
from data import DISTANCE_SQUARED

flightApi = FlightRadar24API()

trackerConfig = {
	"faa": "1",
	"satellite": "0",
	"mlat": "1",
	"flarm": "1",
	"adsb": "1",
	"gnd": "0",
	"air": "1",
	"vehicles": "0",
	"estimated": "0",
	"maxage": "14400",
	"gliders": "0",
	"stats": "1",
	"limit": "5000"
}


loggers = FlightsTracked()

def initialisation():
	flightApi.set_real_time_flight_tracker_config(config=trackerConfig)

def isNear(flight) -> bool:
	distSq = (flight.longitude - CENTRE_LONGITUDE)**2
	distSq += (flight.latitude - CENTRE_LATITUDE)**2

	return (distSq <= DISTANCE_SQUARED)

def isWithinArea(flightsWithinArea, flightToCheck) -> bool:
	for flightLogged in flightsWithinArea:
		if flightToCheck.id == flightLogged.id:
			return True

	return False

def main():
	initialisation()

	while True:
		# fetch flights, filter by area
		flightsWithinArea = flightApi.get_flights(bounds=BOUNDARY)

		for flight in flightsWithinArea:
			print("{:8s}: {:4s} -> {:4s}".format(flight.callsign, flight.origin_airport_iata, flight.destination_airport_iata))

		for i, flight in enumerate(flightsWithinArea):
			# update existing flights
			if loggers.has(flight):
				loggers.get(i).updateLocation(flight)
				print("existing: {:}".format(flight.callsign))
			
			# add new flights
			else:
				loggers.add(flight)
				print("added {:}".format(flight.callsign))

		# delete flights out of range
		for i, flightLogged in enumerate(loggers.getAll()):
			if isWithinArea(flightsWithinArea, flightLogged) == False:
				loggers.remove(i)
				print("outside {:}".format(flightLogged.id))

		for flight in flightsWithinArea:
			if isNear(flight):
				print("Flight {:} is near".format(flight.callsign))

		# identify flights coming closer
		# calculate time to reach

		# delay
		print("")
		time.sleep(5)

if __name__ == "__main__":
	main()