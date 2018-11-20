#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
# ---------------------------------------- SYSTEM DATABASE PARAMETERS -------------------------------------------------
# The name of the host where MongoDB is running.
mongodb_host = '127.0.0.1'
# The port where MongoDB is listening to.
mongodb_port = 27017

travel_requests_simulator_timeout = 100

travel_requests_simulator_max_operation_timeout = 600
travel_requests_simulator_min_number_of_documents = 10

travel_requests_simulator_max_number_of_documents = 100


travel_requests_simulator_datetime_distribution_weights = [
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1
]


maximum_bus_capacity = 100

average_waiting_time_threshold = 0
individual_waiting_time_threshold = 0
minimum_number_of_passengers_in_timetable = 10

look_ahead_timetables_generator_timeout = 100

look_ahead_timetables_generator_max_operation_timeout = 600


look_ahead_timetables_updater_timeout = 100

look_ahead_timetables_updater_max_operation_timeout = 600


testing_bus_stop_names = [
    
]

testing_bus_line_id = 1

now = datetime.now()
today = datetime(now.year, now.month, now.day, 0, 0, 0, 00000)
tomorrow = today + timedelta(days=1)

testing_travel_requests_min_departure_datetime = today
testing_travel_requests_max_departure_datetime = tomorrow

testing_timetables_starting_datetime = today
testing_timetables_ending_datetime = tomorrow
