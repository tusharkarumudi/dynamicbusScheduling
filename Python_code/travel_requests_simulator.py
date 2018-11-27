import random
import numpy as npy
from datetime import timedelta
from mongodb_database_connection import MongodbDatabaseConnection
from parameters import mongodb_host, mongodb_port, travel_requests_simulator_datetime_distribution_weights

class TravelRequestsSimulator(object):
	def __init__(self):
		self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)

	def generate_travel_request_documents(self):

		number_of_travel_request_documents = np.random.poisson(0,40)
		#bus_line=None,
		bus_line_id = "100 Oaks"
		#if bus_line is None:
		#   bus_line = self.mongodb_database_connection.find_bus_line_document(bus_line_id=bus_line_id)


		#bus_stops = bus_line.get('bus_stops')
		bus_stops_array = ["100OAKS", "5AVGAYNN", "6AOAKSN", "6THLAFNN", "7AVCHUSN", "7AVCOMSN", "7AVUNISM", "8ABRONM", "8ABRONN", "8ABROSN"]
		number_of_bus_stops = len(bus_stops_array)


		#  distribution_weighted_datetimes = [
		# (initial_datetime + timedelta(hours=i),
		#   travel_requests_simulator_datetime_distribution_weights[i]) for i in range(0, 24)
		#]
		#datetime_population = [val for val, cnt in distribution_weighted_datetimes for i in range(cnt)]
		travel_request_documents = []

		for i in range(0, number_of_travel_request_documents):
			starting_bus_stop_index = npy.random.poisson(0, number_of_bus_stops - 2)
			starting_bus_stop = bus_stops_array[starting_bus_stop_index]
			ending_bus_stop_index = npy.random.poisson(starting_bus_stop_index + 1, number_of_bus_stops - 1)
			ending_bus_stop = bus_stops_array[ending_bus_stop_index]
			additional_departure_time_interval = npy.random.poisson(0, 59)
			departure_datetime = ("09:00"+timedelta(minutes=additional_departure_time_interval))

		travel_request_document = {
			'client_id': client_id,
			'bus_line_id': bus_line_id,
			'starting_bus_stop': {
			"stopid":starting_bus_stop, "name":"MUSIC CITY CENTRAL 5TH - BAY 11", "longitude":"-86.781996", "latitude":"36.166590"		
			},
			'ending_bus_stop': {
			"stopid":ending_bus_stop, "name":"CHARLOTTE AVE & 8TH AVE N WB", "longitude":"-86.785451", "latitude":"36.164393"
			},
			'departure_datetime': departure_datetime,
			'arrival_datetime': None,
			'starting_timetable_entry_index': None,
			'ending_timetable_entry_index': None
		}
		travel_request_documents.append(travel_request_document)

		# 4: The generated travel_request_documents are stored at the
		#    TravelRequests collection of the System Database.
		#
		self.mongodb_database_connection.insert_travel_request_documents(
		travel_request_documents=travel_request_documents
		)
