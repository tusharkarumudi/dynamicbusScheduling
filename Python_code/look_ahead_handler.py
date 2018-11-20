from parameters import mongodb_host, mongodb_port
from mongodb_database_connection import MongodbDatabaseConnection
from timetable_generator import *
from timetable_updater import *


class LookAheadHandler(object):
 def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
		
def update_timetables_of_bus_lines(self):
        """
        Update the timetables of all bus_lines, taking into consideration the current levels of traffic_density.

        :return: None
        """
        bus_lines = self.mongodb_database_connection.find_bus_line_documents()

        for bus_line in bus_lines:
            self.update_timetables_of_bus_line(bus_line=bus_line)

def update_timetables_of_bus_line(self, bus_line=None, bus_line_id=None):
        """
        Update the timetables of a bus_line, taking into consideration the current levels of traffic_density.

        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: None
        """
        if bus_line is None and bus_line_id is None:
            return None
        elif bus_line is None:
            bus_line = self.mongodb_database_connection.find_bus_line_document(bus_line_id=bus_line_id)
        else:
            bus_line_id = bus_line.get('bus_line_id')

        bus_stops = bus_line.get('bus_stops')
        timetables = self.mongodb_database_connection.find_timetable_documents(bus_line_ids=[bus_line_id])
        travel_requests = get_travel_requests_of_timetables(timetables=timetables)

        timetable_updater = TimetableUpdater(
            bus_stops=bus_stops,
            timetables=timetables,
            travel_requests=travel_requests
        )
        update_entries_of_timetables(
            timetables=timetable_updater.timetables,
        )
        current_average_waiting_time_of_timetables = calculate_average_waiting_time_of_timetables_in_seconds(
            timetables=timetable_updater.timetables
        )
        print_timetables(timetables=timetable_updater.timetables)

        while True:
            new_timetables = generate_new_timetables_based_on_travel_requests(
                current_timetables=timetable_updater.timetables,
                travel_requests=timetable_updater.travel_requests
            )
            new_average_waiting_time_of_timetables = calculate_average_waiting_time_of_timetables_in_seconds(
                timetables=new_timetables
            )
            if new_average_waiting_time_of_timetables < current_average_waiting_time_of_timetables:
                timetable_updater.timetables = new_timetables
                current_average_waiting_time_of_timetables = new_average_waiting_time_of_timetables
                print_timetables(timetables=timetable_updater.timetables)
            else:
                break

        print_timetables(timetables=timetable_updater.timetables)

        self.mongodb_database_connection.delete_timetable_documents(
            bus_line_id=bus_line.get('bus_line_id')
        )
        self.mongodb_database_connection.insert_timetable_documents(
            timetable_documents=timetable_updater.timetables
        )
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='update_timetable_documents (mongodb_database): ok')			
		
		
def generate_new_timetables_based_on_travel_requests(current_timetables, travel_requests):
    
    # The timetables_entries of new_timetables are initialized, based on the corresponding timetable_entries
    # of current_timetables, and their travel_requests entry is empty.
    new_timetables = generate_additional_timetables(timetables=current_timetables)

    # 1: (Initial Clustering) Each one of the retrieved travel_requests is corresponded to the timetable
    #    which produces the minimum_individual_waiting_time for the passenger. The waiting time is calculated
    #    as the difference between the departure_datetime of the travel_request and the departure_datetime of
    #    the timetable_entry from where the passenger departs from (identified by the
    #    'starting_timetable_entry_index' value).
    #
    correspond_travel_requests_to_timetables(
        travel_requests=travel_requests,
        timetables=new_timetables
    )

    # 2: (Handling of Undercrowded Timetables) After the initial clustering step, there might be timetables
    #    where the number of travel_requests is lower than the input: minimum_number_of_passengers_in_timetable.
    #    This is usual during night hours, where transportation demand is not so high. These timetables are
    #    removed from the list of generated timetables and each one of their travel_requests is corresponded
    #    to one of the remaining timetables, based on the individual_waiting_time of the passenger.
    #
    travel_requests_of_undercrowded_timetables = handle_undercrowded_timetables(timetables=new_timetables)
    correspond_travel_requests_to_timetables(
        travel_requests=travel_requests_of_undercrowded_timetables,
        timetables=new_timetables
    )

    # 3: (Handling of Overcrowded Timetables) In addition, there might be timetables where the
    #    number_of_current_passengers is higher than the input: maximum_bus_capacity, which indicates that
    #    each one of these timetables cannot be served by one bus vehicle. For this reason, each one of these
    #    timetables should be divided into two timetables, and the corresponding travel_requests are partitioned.
    #    The whole procedure is repeated until there is no timetable where the number_of_current_passengers
    #    exceeds the maximum_bus_capacity.
    #
    #    The first step is to calculate the number_of_current_passengers in each one of the timetable_entries.
    #
    calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    handle_overcrowded_timetables(timetables=new_timetables)

    # 4: (Adjust Departure Datetimes) At this point of processing, the number of travel_requests in each timetable
    #    is higher than the minimum_number_of_passengers_in_timetable and lower than the maximum_bus_capacity.
    #    So, the departure_datetime and arrival_datetime values of each timetable_entry are re-estimated,
    #    taking into consideration the departure_datetime values of the corresponding travel_requests.
    #    In each timetable and for each travel_request, the ideal departure_datetimes from all bus_stops
    #    (not only the bus stop from where the passenger desires to depart) are estimated. 
	#    Then, the ideal departure_datetimes of the timetable, for each bus stop, correspond to the mean values of the ideal
    #    departure_datetimes of the corresponding travel_requests. 
	#    Finally, starting from the initial bus_stop and combining the ideal departure_datetimes of each bus_stop and 
	#    the required traveling time between
    #    bus_stops, included in the response of the Route Generator, the departure_datetimes of the
    #    timetable_entries are finalized.
    adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    # 5: (Individual Waiting Time) For each timetable, the individual_waiting_time of each passenger is calculated.
    #     For each one of the travel_requests where individual_waiting_time is higher than the
    #     input: individual_waiting_time_threshold, alternative existing timetables are investigated, based on the
    #     new individual_waiting_time, the average_waiting_time and the number_of_current_passengers of each
    #     timetable. For the travel_requests which cannot be served by the other existing timetables, if their
    #     number is greater or equal than the mini_number_of_passengers_in_timetable, then a new timetable is
    #     generated with departure_datetimes based on the ideal departure_datetimes of the
    #     aforementioned passengers.
    #
    # handle_travel_requests_of_timetables_with_waiting_time_above_threshold(
    #     timetables=new_timetables
    # )
    # calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    # adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    # 6: (Average Waiting Time) For each timetable, the average_waiting_time of passengers is calculated.
    #     If the average waiting time is higher than the input: average-waiting-time-threshold, then the
    #     possibility of dividing the timetable is investigated. If the two new timetables have lower
    #     average_waiting_time than the initial one and both have more travel_requests than the
    #     minimum_number_of_passengers_in_timetable, then the initial timetable is divided, its travel_requests
    #     are partitioned, and the departure_datetime and arrival_datetime values of the timetable_entries of
    #     the new timetables, are estimated based on the departure_datetime values of the partitioned requests.
    #
    handle_timetables_with_average_waiting_time_above_threshold(timetables=new_timetables)
    calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    return new_timetables


def get_travel_requests_of_timetables(timetables):
    """
    Retrieve a list containing all the travel_request_documents,
    which are included in a list of timetable_documents.

    :param timetables: [timetable_documents]
    :return: travel_requests: [travel_request_documents]
    """
    travel_requests = []

    for timetable in timetables:
        travel_requests_of_timetable = timetable.get('travel_requests')
        travel_requests.extend(travel_requests_of_timetable)

    return travel_requests