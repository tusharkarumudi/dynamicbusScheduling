#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from parameters import maximum_bus_capacity, average_waiting_time_threshold, \
    individual_waiting_time_threshold, minimum_number_of_passengers_in_timetable

class TimetableGenerator(object):
    def __init__(self, bus_line_id, bus_stops, travel_requests, maximum_timetable_id_in_database):
        """
        Initialize the TimetableGenerator, send a request to the RouteGenerator and receive the less time-consuming
        route which connects the provided bus stops.

        :param bus_line_id: int
        :param bus_stops: [bus_stop_document]
        :param travel_requests: [travel_request_document]
        :param maximum_timetable_id_in_database: int
        :return: None
        """
        self.maximum_timetable_id_in_database = maximum_timetable_id_in_database
        self.timetables = []
        self.bus_line_id = bus_line_id
        self.bus_stops = bus_stops
        self.travel_requests = travel_requests


def add_ideal_departure_datetimes_of_travel_request(ideal_departure_datetimes_of_travel_request,
                                                    ideal_departure_datetimes_of_travel_requests):
    """
    Add each one of the items in the ideal_departure_datetimes_of_travel_request list, to the
    corresponding list of the ideal_departure_datetimes_of_travel_requests double list.

    :param ideal_departure_datetimes_of_travel_request: [departure_datetime]
    :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
    :return: None (Updates ideal_departure_datetimes)
    """
    for index in range(0, len(ideal_departure_datetimes_of_travel_request)):
        ideal_departure_datetime_of_travel_request = ideal_departure_datetimes_of_travel_request[index]
        ideal_departure_datetimes_of_travel_requests[index].append(ideal_departure_datetime_of_travel_request)


def add_timetable_to_timetables_sorted_by_starting_datetime(timetable, timetables):
    """
    Add a provided timetable to the timetables list, sorted by its starting_datetime.

    :param timetable: timetable_document
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    number_of_timetables = len(timetables)
    insertion_index = number_of_timetables

    for i in range(0, number_of_timetables):
        current_timetable = timetables[i]
        starting_datetime_of_new_timetable = get_starting_datetime_of_timetable(timetable=timetable)
        starting_datetime_of_current_timetable = get_starting_datetime_of_timetable(timetable=current_timetable)

        if starting_datetime_of_new_timetable < starting_datetime_of_current_timetable:
            insertion_index = i
            break

    timetables.insert(insertion_index, timetable)

def add_travel_request_to_timetable_without_adjustments(travel_request, timetable):
    """
    Add a travel_request to the list of travel_requests of a timetable, without adjusting the timetable_entries.

    :param travel_request: travel_request_document
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests = timetable.get('travel_requests')
    travel_requests.append(travel_request)


def adjust_departure_datetimes_of_timetable(timetable):
    """
    Adjust the departure datetimes of a timetable, taking into consideration
    the departure datetimes of its corresponding travel requests.

    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests = timetable.get('travel_requests')
    timetable_entries = timetable.get('timetable_entries')
    total_times = [timetable_entry.get('route').get('total_time') for timetable_entry in timetable_entries]

    ideal_departure_datetimes_of_travel_requests = [
        [timetable_entry.get('departure_datetime')] for timetable_entry in timetable_entries
    ]

    for travel_request in travel_requests:
        if travel_request == 'ending_bus_stop':
            print (travel_requests)
        ideal_departure_datetimes_of_travel_request = estimate_ideal_departure_datetimes_of_travel_request(
            travel_request=travel_request,
            total_times=total_times
        )
        add_ideal_departure_datetimes_of_travel_request(
            ideal_departure_datetimes_of_travel_request=ideal_departure_datetimes_of_travel_request,
            ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests
        )

    ideal_departure_datetimes = estimate_ideal_departure_datetimes(
        ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests
    )

    adjust_timetable_entries(timetable=timetable, ideal_departure_datetimes=ideal_departure_datetimes)


def adjust_departure_datetimes_of_timetables(timetables):
    """
    Adjust the departure datetimes of each one of the timetables, taking into consideration
    the departure datetimes of its corresponding travel requests.

    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        adjust_departure_datetimes_of_timetable(timetable=timetable)


def adjust_timetable_entries(timetable, ideal_departure_datetimes):
    """
    Adjust the timetable entries, combining the ideal departure datetimes and
    the required traveling time from one bus stop to another.

    :param timetable: timetable_document
    :param ideal_departure_datetimes: [datetime]
    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')
    number_of_timetable_entries = len(timetable_entries)

    for i in range(0, number_of_timetable_entries):
        timetable_entry = timetable_entries[i]
        total_time = timetable_entry.get('route').get('total_time')
        ideal_departure_datetime = ideal_departure_datetimes[i]

        if i == 0:
            departure_datetime = ideal_departure_datetime
        else:
            previous_departure_datetime = timetable_entries[i - 1].get('departure_datetime')
            departure_datetime = previous_departure_datetime + timedelta(seconds=total_time)

            # if potential_departure_datetime < ideal_departure_datetime:
            #     departure_datetime = ideal_departure_datetime
            # else:
            #     departure_datetime = potential_departure_datetime

        # departure_datetime = ceil_datetime_minutes(starting_datetime=departure_datetime)
        arrival_datetime = departure_datetime + timedelta(seconds=total_time)
        timetable_entry['departure_datetime'] = departure_datetime
        timetable_entry['arrival_datetime'] = arrival_datetime

def calculate_departure_datetime_differences_between_travel_request_and_timetables(travel_request, timetables):
    """
    Calculate the datetime difference between a travel request and a list of timetables.

    :param travel_request: timetable_document
    :param timetables: [timetable_document]
    :return: departure_datetime_differences: [{
                 'timetable': timetable_document, 'departure_datetime_difference': float (in seconds)}]
    """
    departure_datetime_differences = []
    # starting_timetable_entry_index corresponds to the timetable_entry from where the passenger departs from.
    starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')

    for timetable in timetables:
        timetable_entries = timetable.get('timetable_entries')
        corresponding_timetable_entry = timetable_entries[starting_timetable_entry_index]

        departure_datetime_of_travel_request_in_seconds = datetime_to_seconds(
            provided_datetime=travel_request.get('departure_datetime')
        )
        departure_datetime_of_timetable_entry_in_seconds = datetime_to_seconds(
            provided_datetime=corresponding_timetable_entry.get('departure_datetime')
        )
        departure_datetime_difference = abs(departure_datetime_of_travel_request_in_seconds -
                                            departure_datetime_of_timetable_entry_in_seconds)

        departure_datetime_difference_entry = {
            'timetable': timetable,
            'departure_datetime_difference': departure_datetime_difference
        }
        departure_datetime_differences.append(departure_datetime_difference_entry)

    return departure_datetime_differences


def calculate_mean_departure_datetime(departure_datetimes):
    """
    Calculate the mean value of a list of departure_datetime values.

    :param departure_datetimes: [datetime]
    :return: mean_departure_datetime: datetime
    """
    total = 0
    number_of_departure_datetimes = len(departure_datetimes)

    for departure_datetime in departure_datetimes:
        total += (departure_datetime.hour * 3600) + (departure_datetime.minute * 60) + departure_datetime.second

    avg = total / number_of_departure_datetimes
    minutes, seconds = divmod(int(avg), 60)
    hours, minutes = divmod(minutes, 60)
    mean_departure_datetime = datetime.combine(departure_datetimes[0].date(), time(hours, minutes, seconds))

    return mean_departure_datetime


def calculate_number_of_passengers_of_timetable(timetable):
    """
    Calculate the number of onboarding, deboarding, and current passengers for each timetable entry,
    and update the corresponding values.

    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    clear_number_of_passengers_of_timetable(timetable=timetable)
    travel_requests = timetable.get('travel_requests')
    timetable_entries = timetable.get('timetable_entries')

    for travel_request in travel_requests:
        starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
        starting_timetable_entry = timetable_entries[starting_timetable_entry_index]
        starting_timetable_entry['number_of_onboarding_passengers'] += 1

        ending_timetable_entry_index = travel_request.get('ending_timetable_entry_index')
        ending_timetable_entry = timetable_entries[ending_timetable_entry_index]
        ending_timetable_entry['number_of_deboarding_passengers'] += 1

    previous_number_of_current_passengers = 0
    previous_number_of_deboarding_passengers = 0

    for timetable_entry in timetable_entries:
        number_of_current_passengers = (previous_number_of_current_passengers -
                                        previous_number_of_deboarding_passengers +
                                        timetable_entry.get('number_of_onboarding_passengers'))

        timetable_entry['number_of_current_passengers'] = number_of_current_passengers
        previous_number_of_current_passengers = number_of_current_passengers
        previous_number_of_deboarding_passengers = timetable_entry.get('number_of_deboarding_passengers')


def calculate_number_of_passengers_of_timetables(timetables):
    """
    Calculate the number of onboarding, deboarding, and current passengers for each timetable entry,
    and update the corresponding values in each one of timetables.

    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        calculate_number_of_passengers_of_timetable(timetable=timetable)

def ceil_datetime_minutes(starting_datetime):
    """
    Ceil the minutes of a datetime.

    :param starting_datetime: datetime
    :return: ending_datetime: datetime
    """
    ending_datetime = (starting_datetime - timedelta(microseconds=starting_datetime.microsecond) -
                       timedelta(seconds=starting_datetime.second) + timedelta(minutes=1))
    return ending_datetime

def clear_number_of_passengers_of_timetable(timetable):
    """
    Clear the number of passengers of a timetable.

    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')

    for timetable_entry in timetable_entries:
        timetable_entry['number_of_onboarding_passengers'] = 0
        timetable_entry['number_of_deboarding_passengers'] = 0
        timetable_entry['number_of_current_passengers'] = 0

def correspond_travel_requests_to_timetables(travel_requests, timetables):
    """
    Correspond each travel request to a timetable, so as to produce
    the minimum waiting time for each passenger.

    :param travel_requests: [travel_request_document]
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for travel_request in travel_requests:
        departure_datetime_differences = \
            calculate_departure_datetime_differences_between_travel_request_and_timetables(
                travel_request=travel_request,
                timetables=timetables
            )

        timetable_with_minimum_datetime_difference = get_timetable_with_minimum_departure_datetime_difference(
            departure_datetime_differences=departure_datetime_differences
        )

        add_travel_request_to_timetable_without_adjustments(
            travel_request=travel_request,
            timetable=timetable_with_minimum_datetime_difference
        )


def divide_timetable(timetable):
    """
    Create a copy of the initial timetable, split the requests of the initial timetable into the two timetables,
    adjust the departure_datetimes of both timetables, and return the new timetable.

    :param timetable: timetable_document
    :return: additional_timetable
    """
    additional_timetable = generate_additional_timetable(timetable=timetable)
    travel_requests = list(timetable.get('travel_requests'))
    timetable['travel_requests'] = []

    timetables = [timetable, additional_timetable]
    partition_travel_requests_in_timetables(travel_requests=travel_requests, timetables=timetables)
    adjust_departure_datetimes_of_timetables(timetables=timetables)
    calculate_number_of_passengers_of_timetables(timetables=timetables)

    # timetable['travel_requests'] = []
    # additional_timetable['travel_requests'] = []
    # correspond_travel_requests_to_timetables(travel_requests=travel_requests, timetables=timetables)
    # adjust_departure_datetimes_of_timetables(timetables=timetables)
    # calculate_number_of_passengers_of_timetables(timetables=timetables)

    return additional_timetable


def divide_timetable_based_on_average_waiting_time(timetable):
    """
    Check if a timetable should be divided, based on the number of travel requests and the average_waiting_time
    of the old and the two new timetables.

    :param timetable: timetable_document
    :return: additional_timetable if the timetable was divided, otherwise None.
    """
    initial_travel_requests = list(timetable.get('travel_requests'))

    if len(initial_travel_requests) < 2 * minimum_number_of_passengers_in_timetable:
        return None

    initial_timetable_entries = list(timetable.get('timetable_entries'))
    initial_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    additional_timetable = divide_timetable(timetable=timetable)
    new_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)
    additional_timetable_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(
        timetable=additional_timetable
    )

    # if (new_average_waiting_time + additional_timetable_average_waiting_time) / 2 > initial_average_waiting_time:
    #     timetable['timetable_entries'] = initial_timetable_entries
    #     timetable['travel_requests'] = initial_travel_requests
    #     return None

    if (new_average_waiting_time > initial_average_waiting_time or
                additional_timetable_average_waiting_time > initial_average_waiting_time):
        timetable['timetable_entries'] = initial_timetable_entries
        timetable['travel_requests'] = initial_travel_requests
        return None

    adjust_departure_datetimes_of_timetables(timetables=[timetable, additional_timetable])
    return additional_timetable


def estimate_ideal_departure_datetimes(ideal_departure_datetimes_of_travel_requests):
    """
    Process the ideal_departure_datetimes_of_travel_requests double list, which contains a list
    of ideal departure datetimes for each one of the timetable entries, calculate the mean value of each list,
    and return a list containing all of them.

    :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
    :return: ideal_departure_datetimes: [departure_datetime]
    """
    ideal_departure_datetimes = []

    for corresponding_departure_datetimes in ideal_departure_datetimes_of_travel_requests:

        ideal_departure_datetime = calculate_mean_departure_datetime(
            departure_datetimes=corresponding_departure_datetimes
        )
        ideal_departure_datetimes.append(ideal_departure_datetime)

    return ideal_departure_datetimes


def estimate_ideal_departure_datetimes_of_travel_request(travel_request, total_times):
    """
    Estimate the ideal departure datetime of a travel request, from all timetable entries.
    Initially, only the departure datetime from the corresponding starting timetable entry is known.
    Using the required traveling times from bus stop to bus stop (total_times), it is possible to
    estimate the ideal departure datetimes from all timetable entries.

    :param travel_request: travel_request_document
    :param total_times: [float] (in seconds)
    :return: ideal_departure_datetimes: [departure_datetime]
    """
    number_of_timetable_entries = len(total_times)
    ideal_departure_datetimes = [None for i in range(number_of_timetable_entries)]

    starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
    departure_datetime = travel_request.get('departure_datetime')

    ideal_departure_datetimes[starting_timetable_entry_index] = departure_datetime

    # Estimate ideal departure_datetimes before departure_datetime
    index = starting_timetable_entry_index - 1
    ideal_departure_datetime = departure_datetime

    while index > -1:
        corresponding_total_time = total_times[index]
        ideal_departure_datetime -= timedelta(seconds=corresponding_total_time)
        ideal_departure_datetimes[index] = ideal_departure_datetime
        index -= 1

    # Estimate ideal departure_datetimes after departure_datetime
    index = starting_timetable_entry_index
    ideal_departure_datetime = departure_datetime

    while index < number_of_timetable_entries:
        corresponding_total_time = total_times[index]
        ideal_departure_datetime += timedelta(seconds=corresponding_total_time)
        ideal_departure_datetimes[index] = ideal_departure_datetime
        index += 1

    for i in ideal_departure_datetimes:
        if i is None:
            print (ideal_departure_datetimes)

    return ideal_departure_datetimes


def generate_additional_timetable(timetable):
    """
    Generate an additional timetable, copying the timetable_entries of an existing one.

    :param timetable: timetable_document
    :return: additional_timetable
    """
    bus_line_id = timetable.get('bus_line_id')
    timetable_entries = timetable.get('timetable_entries')
    additional_timetable = {'bus_line_id': bus_line_id, 'timetable_entries': [], 'travel_requests': []}

    for timetable_entry in timetable_entries:
        additional_timetable_entry = {
            'starting_bus_stop': timetable_entry.get('starting_bus_stop'),
            'ending_bus_stop': timetable_entry.get('ending_bus_stop'),
            'departure_datetime': timetable_entry.get('departure_datetime'),
            'arrival_datetime': timetable_entry.get('arrival_datetime'),
            'route': timetable_entry.get('route'),
            'number_of_onboarding_passengers': 0,
            'number_of_deboarding_passengers': 0,
            'number_of_current_passengers': 0
        }
        additional_timetable['timetable_entries'].append(additional_timetable_entry)

    return additional_timetable


def generate_additional_timetables(timetables):
    """

    :param timetables: [timetable_document]
    :return: additional_timetables
    """
    additional_timetables = []

    for timetable in timetables:
        additional_timetable = generate_additional_timetable(timetable=timetable)
        additional_timetables.append(additional_timetable)

    return additional_timetables


def get_overcrowded_timetables(timetables):
    """
    Get the timetables with number of passengers which exceeds the bus vehicle capacity.

    :param timetables: [timetable_document]
    :return: overcrowded_timetables: [timetable_document]
    """
    overcrowded_timetables = []

    for timetable in timetables:
        if not check_number_of_passengers_of_timetable(timetable=timetable):
            overcrowded_timetables.append(timetable)

    return overcrowded_timetables


def get_starting_datetime_of_timetable(timetable):
    """
    Get the starting_datetime of a timetable, which corresponds to
    the departure_datetime of the first timetable entry.

    :param timetable: timetable_document
    :return: starting_datetime_of_timetable: datetime
    """
    timetable_entries = timetable.get('timetable_entries')
    starting_timetable_entry = timetable_entries[0]
    starting_datetime_of_timetable = starting_timetable_entry.get('departure_datetime')
    return starting_datetime_of_timetable

def get_timetable_with_minimum_departure_datetime_difference(departure_datetime_differences):
    """
    Get the timetable with the minimum departure_datetime difference.

    :param departure_datetime_differences: [{
                 'timetable': timetable_document, 'departure_datetime_difference': float (in seconds)}]

    :return: timetable_with_min_departure_datetime_difference: timetable_document
    """
    # minimum_datetime_difference is initialized with a big datetime value.
    min_departure_datetime_difference = 356 * 86400
    timetable_with_min_departure_datetime_difference = None

    for departure_datetime_difference_entry in departure_datetime_differences:
        timetable = departure_datetime_difference_entry.get('timetable')
        departure_datetime_difference = departure_datetime_difference_entry.get('departure_datetime_difference')

        if departure_datetime_difference < min_departure_datetime_difference:
            min_departure_datetime_difference = departure_datetime_difference
            timetable_with_min_departure_datetime_difference = timetable

    return timetable_with_min_departure_datetime_difference


def get_timetables_with_average_waiting_time_above_threshold(timetables):
    """
    Retrieve a list containing the timetables_with_average_waiting_time_above_threshold.

    :param timetables: [timetable_document]
    :return: timetables_with_average_waiting_time_above_threshold: timetable_document
    """
    timetables_with_average_waiting_time_above_threshold = []

    for timetable in timetables:
        if not check_average_waiting_time_of_timetable(timetable=timetable):
            timetables_with_average_waiting_time_above_threshold.append(timetable)

    return timetables_with_average_waiting_time_above_threshold





def handle_timetables_with_average_waiting_time_above_threshold(timetables):
    """

    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    control = True

    while control:
        control = False
        timetables_with_average_waiting_time_above_threshold = get_timetables_with_average_waiting_time_above_threshold(
            timetables=timetables
        )
        for timetable in timetables_with_average_waiting_time_above_threshold:
            additional_timetable = divide_timetable_based_on_average_waiting_time(timetable=timetable)

            if additional_timetable is not None:
                add_timetable_to_timetables_sorted_by_starting_datetime(
                    timetable=additional_timetable,
                    timetables=timetables
                )
                control = True


def handle_overcrowded_timetables(timetables):
    """
    There might be timetables with number_of_current_passengers higher than the input: maximum_bus_capacity,
    which indicates that each one of these timetables cannot be served by one bus vehicle.
    For this reason, each one of these timetables is divided into two timetables
    and the corresponding travel requests are partitioned.
    The whole procedure is repeated until there is no timetable where the number of passengers
    exceeds the maximum_bus_capacity.

    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)

    while len(overcrowded_timetables) > 0:

        for overcrowded_timetable in overcrowded_timetables:
            additional_timetable = divide_timetable(timetable=overcrowded_timetable)

            add_timetable_to_timetables_sorted_by_starting_datetime(
                timetable=additional_timetable,
                timetables=timetables
            )

        overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)


def partition_travel_requests_by_departure_datetime(travel_requests):
    """
    Split a list of travel_requests into two lists, based on their departure_datetime values,
    and return a double list containing both of them.

    :param travel_requests: [travel_request_document]

    :return: travel_requests_for_timetables: {
             'travel_requests_for_first_timetable': [travel_request_document],
             'travel_requests_for_second_timetable': [travel_request_document]}
    """
    travel_requests_for_first_timetable = []
    travel_requests_for_second_timetable = []

    starting_timetable_entry_dictionary = get_starting_timetable_entry_dictionary(
        travel_requests=travel_requests
    )

    for corresponding_travel_requests_list in starting_timetable_entry_dictionary.itervalues():
        # travel_requests_lists: {'first_list': travel_requests, 'second_list': travel_requests}
        #
        travel_requests_lists = partition_travel_requests_list(travel_requests=corresponding_travel_requests_list)
        first_list = travel_requests_lists.get('first_list')
        second_list = travel_requests_lists.get('second_list')
        travel_requests_for_first_timetable.extend(first_list)
        travel_requests_for_second_timetable.extend(second_list)

    travel_requests_for_timetables = {
        'travel_requests_for_first_timetable': travel_requests_for_first_timetable,
        'travel_requests_for_second_timetable': travel_requests_for_second_timetable
    }

    return travel_requests_for_timetables


def partition_travel_requests_in_timetables(travel_requests, timetables):
    """
    Partition a list of travel_requests in two timetables, and update their corresponding entries.

    :param travel_requests: [travel_request_document]
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    # travel_requests_for_timetables: {
    #     'travel_requests_for_first_timetable': [travel_request_document],
    #     'travel_requests_for_second_timetable': [travel_request_document]}
    #
    travel_requests_for_timetables = partition_travel_requests_by_departure_datetime(travel_requests=travel_requests)
    travel_requests_for_first_timetable = travel_requests_for_timetables.get('travel_requests_for_first_timetable')
    travel_requests_for_second_timetable = travel_requests_for_timetables.get('travel_requests_for_second_timetable')

    timetables[0]['travel_requests'] = travel_requests_for_first_timetable
    timetables[1]['travel_requests'] = travel_requests_for_second_timetable


def partition_travel_requests_list(travel_requests):
    """
    Partition a list of travel_requests into two lists, and return a dictionary containing both of them.

    :param travel_requests: [travel_request_document]
    :return: travel_requests_lists: {'first_list': [travel_request_document], 'second_list': [travel_request_document]}
    """
    number_of_travel_requests = len(travel_requests)
    # half_number_of_travel_requests = number_of_travel_requests / 2
    #
    # first_list_of_travel_requests = travel_requests[0:half_number_of_travel_requests]
    # second_list_of_travel_requests = travel_requests[half_number_of_travel_requests:number_of_travel_requests]

    first_list_of_travel_requests = []
    second_list_of_travel_requests = []

    if number_of_travel_requests == 0:
        pass
    elif number_of_travel_requests == 1:
        first_list_of_travel_requests.append(travel_requests[0])
    else:
        first_list_of_travel_requests.append(travel_requests[0])
        second_list_of_travel_requests.append(travel_requests[number_of_travel_requests - 1])

        departure_datetimes = [travel_request.get('departure_datetime') for travel_request in travel_requests]
        first_list_of_departure_datetimes = [departure_datetimes[0]]
        second_list_of_departure_datetimes = [departure_datetimes[number_of_travel_requests - 1]]

        for i in range(1, number_of_travel_requests - 1):
            travel_request = travel_requests[i]
            departure_datetime = departure_datetimes[i]

            mean_of_first_list_of_departure_datetimes = calculate_mean_departure_datetime(
                departure_datetimes=first_list_of_departure_datetimes
            )
            mean_of_second_list_of_departure_datetimes = calculate_mean_departure_datetime(
                departure_datetimes=second_list_of_departure_datetimes
            )
            difference_with_first_list_of_departure_datetimes = abs(
                departure_datetime - mean_of_first_list_of_departure_datetimes
            )
            difference_with_second_list_departure_datetimes = abs(
                departure_datetime - mean_of_second_list_of_departure_datetimes
            )

            if difference_with_first_list_of_departure_datetimes < difference_with_second_list_departure_datetimes:
                first_list_of_travel_requests.append(travel_request)
                first_list_of_departure_datetimes.append(departure_datetime)
            else:
                second_list_of_travel_requests.append(travel_request)
                second_list_of_departure_datetimes.append(departure_datetime)

    travel_requests_lists = {
        'first_list': first_list_of_travel_requests,
        'second_list': second_list_of_travel_requests
    }
    return travel_requests_lists


def handle_undercrowded_timetable(timetable, timetables):
    """

    :param timetable: timetable_document
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    travel_requests = timetable.get('travel_requests')

    for travel_request in travel_requests:
        departure_datetime_differences = \
            calculate_departure_datetime_differences_between_travel_request_and_timetables(
                travel_request=travel_request,
                timetables=timetables
            )

        timetable_with_minimum_departure_datetime_difference = \
            get_timetable_with_minimum_departure_datetime_difference(
                departure_datetime_differences=departure_datetime_differences
            )

        add_travel_request_to_timetable_without_adjustments(
            travel_request=travel_request,
            timetable=timetable_with_minimum_departure_datetime_difference
        )

        # travel_requests.remove(travel_request)

        remove_travel_request_from_timetable_without_adjustments(
            travel_request=travel_request,
            timetable=timetable
        )


def handle_undercrowded_timetables(timetables):
    """

    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    travel_requests_of_undercrowded_timetables = []
    undercrowded_timetables = get_undercrowded_timetables(timetables=timetables)

    for undercrowded_timetable in undercrowded_timetables:
        travel_requests_of_undercrowded_timetable = list(undercrowded_timetable.get('travel_requests'))
        travel_requests_of_undercrowded_timetables.extend(travel_requests_of_undercrowded_timetable)
        timetables.remove(undercrowded_timetable)
        del undercrowded_timetable

    return travel_requests_of_undercrowded_timetables


def get_undercrowded_timetables(timetables):
    """
    Retrieve a list containing the timetables where the number of travel_requests
    is less than the minimum_number_of_passengers_in_timetable.

    :param timetables: [timetable_document]
    :return: undercrowded_timetables: [timetable_document]
    """
    undercrowded_timetables = []

    for timetable in timetables:
        travel_requests = timetable.get('travel_requests')

        if len(travel_requests) < minimum_number_of_passengers_in_timetable:
            undercrowded_timetables.append(timetable)

    return undercrowded_timetables

def print_timetable(timetable, timetable_entries_control=False, travel_requests_control=False):
    """
    Print a timetable_document.

    :param timetable: timetable_document
    :param timetable_entries_control: bool
    :param travel_requests_control: bool
    :return: None
    """
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')
    starting_datetime = get_starting_datetime_of_timetable(timetable=timetable)
    ending_datetime = get_ending_datetime_of_timetable(timetable=timetable)
    average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    print ('\n-- Printing Timetable--')
    print( 'starting_datetime:', starting_datetime, \
        '- ending_datetime:', ending_datetime, \
        '- number_of_travel_requests:', len(travel_requests), \
        '- average_waiting_time:', average_waiting_time)

    if timetable_entries_control:
        print ('- Timetable Entries:')

        for timetable_entry in timetable_entries:
            print ('starting_bus_stop:', timetable_entry.get('starting_bus_stop').get('name'), \
                '- ending_bus_stop:', timetable_entry.get('ending_bus_stop').get('name'), \
                '- departure_datetime:', timetable_entry.get('departure_datetime'), \
                '- arrival_datetime:', timetable_entry.get('arrival_datetime'), \
                '- total_time:', timetable_entry.get('route').get('total_time'), \
                '- number_of_onboarding_passengers:', timetable_entry.get('number_of_onboarding_passengers'), \
                '- number_of_deboarding_passengers:', timetable_entry.get('number_of_deboarding_passengers'), \
                '- number_of_current_passengers:', timetable_entry.get('number_of_current_passengers'), \
                '- route:', timetable_entry.get('route'))

    if travel_requests_control:
        print ('- Travel Requests:')

        for travel_request in travel_requests:
            print ('starting_bus_stop:', travel_request.get('starting_bus_stop').get('name'), \
                '- ending_bus_stop:', travel_request.get('ending_bus_stop').get('name'), \
                '- departure_datetime:', travel_request.get('departure_datetime'))

            # print 'starting_bus_stop:', travel_request.get('starting_bus_stop').get('name'), \
            #     '- ending_bus_stop:', travel_request.get('ending_bus_stop').get('name'), \
            #     '- departure_datetime:', travel_request.get('departure_datetime'), \
            #     '- starting_timetable_entry_index:', travel_request.get('starting_timetable_entry_index'), \
            #     '- ending_timetable_entry_index:', travel_request.get('ending_timetable_entry_index')


def print_timetables(timetables, timetables_control=False, timetable_entries_control=False,
                     travel_requests_control=False, counter=None):
    """
    Print multiple timetable_documents.

    :param timetables: [timetable_document]
    :param timetables_control: bool
    :param timetable_entries_control: bool
    :param travel_requests_control: bool
    :param counter: int
    :return: None
    """
    sort_timetables_by_starting_datetime(timetables=timetables)

    number_of_timetables = len(timetables)
    number_of_bus_vehicles = estimate_number_of_bus_vehicles_for_timetables(
        timetables=timetables
    )
    total_number_of_passengers_in_timetables = calculate_total_number_of_travel_requests_in_timetables(
        timetables=timetables
    )
    average_number_of_passengers_in_timetables = calculate_average_number_of_travel_requests_in_timetables(
        timetables=timetables
    )
    average_waiting_time = calculate_average_waiting_time_of_timetables_in_seconds(
        timetables=timetables
    )

    print ('number_of_timetables:', number_of_timetables, \
        '- number_of_bus_vehicles:', number_of_bus_vehicles, \
        '- total_number_of_passengers_in_timetables:', total_number_of_passengers_in_timetables, \
        '- average_number_of_passengers_in_timetables:', average_number_of_passengers_in_timetables, \
        '- average_waiting_time:', average_waiting_time)

    if counter is not None and counter < number_of_timetables:
        timetables_to_be_printed = list(timetables[0:counter])
    else:
        timetables_to_be_printed = list(timetables)

    if timetables_control:
        for timetable in timetables_to_be_printed:
            print_timetable(
                timetable=timetable,
                timetable_entries_control=timetable_entries_control,
                travel_requests_control=travel_requests_control
            )

