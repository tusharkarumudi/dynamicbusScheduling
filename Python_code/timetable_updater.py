#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# from datetime import timedelta
from timetable_generator import adjust_timetable_entries, ceil_datetime_minutes

class TimetableUpdater(object):
    def __init__(self, bus_stops, timetables, travel_requests):
        """
        Initialize the TimetableUpdater and send a request to the Route Generator in order to
        identify the less time-consuming route which connects the provided bus_stops.

        :param bus_stops: [bus_stop_document]
        :param timetables: [timetable_document]
        :param travel_requests: [travel_request_document]
        :return: None
        """
        self.bus_stops = bus_stops
        self.timetables = timetables
        self.travel_requests = travel_requests


def update_entries_of_timetable(timetable):
    """
    Update the timetable_entries of a timetable, taking into consideration the route_generator_response.

    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')
    number_of_timetable_entries = len(timetable_entries)
    ideal_departure_datetimes = [timetable_entry.get('departure_datetime') for timetable_entry in timetable_entries]
    # total_times = [intermediate_route.get('total_time') for intermediate_route in intermediate_routes]

    for i in range(0, number_of_timetable_entries):
        timetable_entry = timetable_entries[i]
        # total_time = timetable_entry.get('route').get('total_time')
        # # total_time = total_times[i]
        # departure_datetime = timetable_entry.get('departure_datetime')
        #
        # if i > 0:
        #     previous_timetable_entry = timetable_entries[i - 1]
        #     previous_arrival_datetime = previous_timetable_entry.get('arrival_datetime')
        #     # departure_datetime_based_on_previous_arrival_datetime = previous_arrival_datetime
        #     departure_datetime_based_on_previous_arrival_datetime = ceil_datetime_minutes(
        #         starting_datetime=previous_arrival_datetime
        #     )
        #     if departure_datetime_based_on_previous_arrival_datetime > departure_datetime:
        #         departure_datetime = departure_datetime_based_on_previous_arrival_datetime
        #         timetable_entry['departure_datetime'] = departure_datetime
        #
        # arrival_datetime = departure_datetime + timedelta(seconds=total_time)
        # timetable_entry['arrival_datetime'] = arrival_datetime

    adjust_timetable_entries(
        timetable=timetable,
        ideal_departure_datetimes=ideal_departure_datetimes
    )


def update_entries_of_timetables(timetables):
    """
    Update the timetable_entries of a list of timetables, taking into consideration the route_generator_response.

    :param timetables: [timetable_documents]
    :param route_generator_response: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: None (Updates timetables)
    """
    for timetable in timetables:
        update_entries_of_timetable(timetable=timetable)
