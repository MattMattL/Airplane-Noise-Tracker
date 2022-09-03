
class Location:
	latitude = None
	longitude = None

class FlightLogger:

	def __init__(self, flight):
		self.locationsLogged: list[Location] = []

		self.id = flight.id
		self.updated: bool = True

	def updateLocation(self, flight):
		newLocation = Location()
		
		newLocation.latitude = flight.latitude
		newLocation.longitude = flight.longitude
		
		self.locationsLogged.append(newLocation)

class FlightsTracked:

	def __init__(self):
		self.loggers: list[FlightLogger] = []

	def get(self, index):
		return self.loggers[index]

	def getAll(self):
		return self.loggers

	def add(self, flight):
		newLogger = FlightLogger(flight)
		self.loggers.append(newLogger)

	def size(self):
		return len(self.loggers)

	def remove(self, i):
		# for i, logger in enumerate(loggers):
		# 	if logger.id == flight.id:
		self.loggers.pop(i)

	def has(self, flight):
		for loggedFlight in self.loggers:
			if loggedFlight.id == flight.id:
				return True

		return False