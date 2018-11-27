#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from bson import ObjectId
from pymongo import MongoClient

class MongodbDatabaseConnection(object):
    

    def __init__(self, host, port):
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client.dynamic_bus_scheduling
        self.bus_line_documents_collection = self.db.BusLineDocuments
        self.bus_stop_documents_collection = self.db.BusStopDocuments
        self.timetable_documents_collection = self.db.TimetableDocuments
        self.travel_request_documents_collection = self.db.TravelRequestDocuments

    def clear_bus_line_documents_collection(self):
        """
        Delete all the documents of the BusLineDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_line_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_documents_collection(self):
        """
        Delete all the documents of the BusStopDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_documents_collection.delete_many({})
        return result.deleted_count

   
    def clear_timetable_documents_collection(self):
        """
        Delete all the documents of the TimetableDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.timetable_documents_collection.delete_many({})
        return result.deleted_count

    def clear_travel_request_documents_collection(self):
        """
        Delete all the documents of the TravelRequestDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.travel_request_documents_collection.delete_many({})
        return result.deleted_count

    def delete_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Delete a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: True if the bus_line_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_line_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif bus_line_id is not None:
            result = self.bus_line_documents_collection.delete_one({
                'bus_line_id': bus_line_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_line_documents(self, object_ids=None, bus_line_ids=None):
        """
        Delete multiple bus_line_document.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_line_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_line_ids is not None:
            result = self.bus_line_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_bus_stop_document(self, object_id=None, osm_id=None):
        """
        Delete a bus_stop_document.

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the bus_stop_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_stop_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            result = self.bus_stop_documents_collection.delete_one({
                'osm_id': osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_stop_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple bus_stop_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_stop_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            result = self.bus_stop_documents_collection.delete_many({
                'osm_id': {'$in': osm_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_timetable_document(self, object_id=None, timetable_id=None):
        """
        Delete a timetable_document.

        :param object_id: ObjectId
        :param timetable_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.timetable_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif timetable_id is not None:
            result = self.timetable_documents_collection.delete_one({
                'timetable_id': timetable_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_id=None):
        """
        Delete multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_id: int
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.timetable_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif timetable_ids is not None:
            result = self.timetable_documents_collection.delete_many({
                'timetable_id': {'$in': timetable_ids}
            })
        elif bus_line_id is not None:
            result = self.timetable_documents_collection.delete_many({
                'bus_line_id': bus_line_id
            })
        else:
            return 0

        return result.deleted_count

    def delete_travel_request_document(self, object_id):
        """
        Delete a travel_request_document.

        :param object_id: ObjectId
        :return: True if the travel_request_document was successfully deleted, otherwise False.
        """
        result = self.travel_request_documents_collection.delete_one({
            '_id': ObjectId(object_id)
        })
        return result.deleted_count == 1

    def delete_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                        min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.travel_request_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif client_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'client_id': {'$in': client_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif bus_line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            result = self.travel_request_documents_collection.delete_many({
                'client_id': {'$in': client_ids}
            })
        elif bus_line_ids is not None:
            result = self.travel_request_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids}
            })
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        else:
            return 0

        return result.deleted_count

    def find_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Retrieve a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: bus_line_document
        """
        if object_id is not None:
            bus_line_document = self.bus_line_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif bus_line_id is not None:
            bus_line_document = self.bus_line_documents_collection.find_one({
                'bus_line_id': bus_line_id
            })
        else:
            return None

        return bus_line_document

    def find_bus_line_documents(self, object_ids=None, bus_line_ids=None, in_dictionary=False):
        """
        Retrieve multiple bus_line_documents.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :param in_dictionary: bool
        :return: bus_line_documents: [bus_line_document] or {bus_line_id -> bus_line_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_line_documents_cursor = self.bus_line_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_line_ids is not None:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({})

        if in_dictionary:
            bus_line_documents = {}

            for bus_line_document in bus_line_documents_cursor:
                bus_line_id = bus_line_document.get('bus_line_id')
                bus_line_documents[bus_line_id] = bus_line_document
        else:
            bus_line_documents = list(bus_line_documents_cursor)

        return bus_line_documents

    def find_bus_stop_document(self, object_id=None, osm_id=None, name=None, longitude=None, latitude=None):
        """
        Retrieve a bus_stop_document.

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: bus_stop_document
        """
        if object_id is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'osm_id': osm_id
            })
        elif name is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'name': name
            })
        elif longitude is not None and latitude is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'point': {
                    'longitude': longitude,
                    'latitude': latitude
                }
            })
        else:
            return None

        return bus_stop_document

    def find_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, in_dictionary=False):
        """
        Retrieve multiple bus_stop_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :param in_dictionary: bool
        :return: bus_stop_documents: [bus_stop_document] or {name -> bus_stop_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                'osm_id': {'$in': osm_ids}
            })
        elif names is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                'name': {'$in': names}
            })
        else:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({})

        if in_dictionary:
            bus_stop_documents = {}

            for bus_stop_document in bus_stop_documents_cursor:
                name = bus_stop_document.get('name')
                bus_stop_documents[name] = bus_stop_document
        else:
            bus_stop_documents = list(bus_stop_documents_cursor)

        return bus_stop_documents

    def find_timetable_document(self, object_id=None, timetable_id=None):
        """
        Retrieve a timetable_document.

        :param object_id: ObjectId
        :param timetable_id: int
        :return: timetable_document
        """
        if object_id is not None:
            timetable_document = self.timetable_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif timetable_id is not None:
            timetable_document = self.timetable_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        else:
            return None

        return timetable_document

    def find_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_ids=None, in_dictionary=False):
        """
        Retrieve multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_ids: [int]
        :param in_dictionary: bool
        :return: timetable_documents: [timetable_document] or {timetable_id -> timetable_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            timetable_documents_cursor = self.timetable_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif timetable_ids is not None:
            timetable_documents_cursor = self.timetable_documents_collection.find({
                'timetable_id': {'$in': timetable_ids}
            })
        elif bus_line_ids is not None:
            timetable_documents_cursor = self.timetable_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            timetable_documents_cursor = self.timetable_documents_collection.find({})

        if in_dictionary:
            timetable_documents = {}

            for timetable_document in timetable_documents_cursor:
                timetable_id = timetable_document.get('timetable_id')
                timetable_documents[timetable_id] = timetable_document
        else:
            timetable_documents = list(timetable_documents_cursor)

        return timetable_documents
		
    def find_travel_request_document(self, object_id):
        """
        Retrieve a travel_request_document.

        :param object_id: ObjectId
        :return: travel_request_document
        """
        travel_request_document = self.travel_request_documents_collection.find_one({'_id': ObjectId(object_id)})
        return travel_request_document

    def find_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                      min_departure_datetime=None, max_departure_datetime=None, in_dictionary=False):
        """
        Retrieve multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :param in_dictionary: bool
        :return: travel_request_documents: [travel_request_document] or {client_id: [travel_request_document]}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            travel_requests_cursor = self.travel_request_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif client_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'client_id': {'$in': client_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif bus_line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'client_id': {'$in': client_ids}
            })
        elif bus_line_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        else:
            travel_requests_cursor = self.travel_request_documents_collection.find({})

        if in_dictionary:
            travel_requests = {}

            for travel_request in travel_requests_cursor:
                client_id = travel_request.get('client_id')

                if client_id in travel_requests:
                    travel_requests[client_id].append(travel_request)
                else:
                    travel_requests[client_id] = list(travel_request)
        else:
            travel_requests = list(travel_requests_cursor)

        return travel_requests

    def insert_bus_line_document(self, bus_line_document=None, bus_line_id=None, bus_stops=None):
        """
        Insert a new bus_line_document or update, if it already exists in the database.

        :param bus_line_document
        :param bus_line_id: int
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: new_object_id: ObjectId
        """
        if bus_line_document is None and (bus_line_id is None or bus_stops is None):
            return None

        elif bus_line_document is not None:
            object_id = bus_line_document.get('_id')

            if object_id is not None:
                key = {
                    '_id': ObjectId(object_id)
                }
                data = {
                    '$set': {
                        'bus_line_id': bus_line_document.get('bus_line_id'),
                        'bus_stops': bus_line_document.get('bus_stops')
                    }
                }
            else:
                key = {
                    'bus_line_id': bus_line_document.get('bus_line_id')
                }
                data = {
                    '$set': {
                        'bus_stops': bus_line_document.get('bus_stops')
                    }
                }
        else:
            key = {
                'bus_line_id': bus_line_id
            }
            data = {
                '$set': {
                    'bus_stops': bus_stops
                }
            }

        result = self.bus_line_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_bus_line_documents(self, bus_line_documents):
        """
        Insert a list of bus_line_documents or update, if it already exists in the database.

        :param bus_line_documents: [bus_line_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        for bus_line_document in bus_line_documents:
            new_object_id = self.insert_bus_line_document(bus_line_document=bus_line_document)
            new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_bus_stop_document(self, bus_stop_document=None, osm_id=None, name=None, point=None):
        """
        Insert a bus_stop_document.

        :param bus_stop_document
        :param osm_id: int
        :param name: string
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if bus_stop_document is None:
            bus_stop_document = {
                'osm_id': osm_id,
                'name': name,
                'point': {
                    'longitude': point.longitude,
                    'latitude': point.latitude
                }
            }

        result = self.bus_stop_documents_collection.insert_one(bus_stop_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_bus_stop_documents(self, bus_stop_documents):
        """
        Insert multiple bus_stop documents.

        :param bus_stop_documents: [bus_stop_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if bus_stop_documents:
            result = self.bus_stop_documents_collection.insert_many(bus_stop_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_timetable_document(self, timetable):
        """
        Insert a new timetable_document or update, if it already exists in the database.

        :param timetable: timetable_document
        :return: new_object_id: ObjectId
        """
        key = {
            '_id': ObjectId(timetable.get('_id'))
        }
        data = {
            '$set': {
                'bus_line_id': timetable.get('bus_line_id'),
                'timetable_entries': timetable.get('timetable_entries'),
                'travel_requests': timetable.get('travel_requests')
            }
        }
        result = self.timetable_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_timetable_documents(self, timetable_documents):
        """
        Insert multiple new timetable_documents or update, if they already exist in the database.

        :param timetable_documents: [timetable_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        for timetable in timetable_documents:
            new_object_id = self.insert_timetable_document(timetable=timetable)
            new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_travel_request_document(self, travel_request_document=None, client_id=None, bus_line_id=None,
                                       starting_bus_stop=None, ending_bus_stop=None,
                                       departure_datetime=None, arrival_datetime=None,
                                       starting_timetable_entry_index=None, ending_timetable_entry_index=None):
        """
        Insert a travel_request_document.

        :param travel_request_document
        :param client_id: int
        :param bus_line_id: int
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param departure_datetime: datetime
        :param arrival_datetime: datetime
        :param starting_timetable_entry_index: int
        :param ending_timetable_entry_index: int
        :return: new_object_id: ObjectId
        """
        if travel_request_document is None:
            travel_request_document = {
                'client_id': client_id,
                'bus_line_id': bus_line_id,
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'departure_datetime': departure_datetime,
                'arrival_datetime': arrival_datetime,
                'starting_timetable_entry_index': starting_timetable_entry_index,
                'ending_timetable_entry_index': ending_timetable_entry_index
            }

        result = self.travel_request_documents_collection.insert_one(travel_request_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_travel_request_documents(self, travel_request_documents):
        """
        Insert multiple travel_request_documents.

        :param travel_request_documents: [travel_request_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if travel_request_documents:
            result = self.travel_request_documents_collection.insert_many(travel_request_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def print_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Print a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: bus_line_document
        """
        bus_line_document = self.find_bus_line_document(
            object_id=object_id,
            bus_line_id=bus_line_id
        )
        print (bus_line_document)

    def print_bus_line_documents(self, object_ids=None, bus_line_ids=None, counter=None):
        """
        Print multiple bus_line_documents.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :param counter: int
        :return: None
        """
        bus_line_documents_list = self.find_bus_line_documents(
            object_ids=object_ids,
            bus_line_ids=bus_line_ids
        )
        number_of_bus_line_documents = len(bus_line_documents_list)

        if counter is not None:
            if number_of_bus_line_documents < counter:
                counter = number_of_bus_line_documents

            for i in range(0, counter):
                bus_line_document = bus_line_documents_list[i]
                print (bus_line_document)

        else:
            for bus_line_document in bus_line_documents_list:
                print (bus_line_document)

        print ('number_of_bus_line_documents:', number_of_bus_line_documents)

    def print_bus_stop_document(self, object_id=None, osm_id=None, name=None, longitude=None, latitude=None):
        """
        Retrieve a bus_stop_document.

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: None
        """
        bus_stop_document = self.find_bus_stop_document(
            object_id=object_id,
            osm_id=osm_id, name=name,
            longitude=longitude,
            latitude=latitude
        )
        print (bus_stop_document)

    def print_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, counter=None):
        """
        Print multiple bus_stop_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :param counter: int
        :return: None
        """
        bus_stop_documents_list = self.find_bus_stop_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            names=names
        )
        number_of_bus_stop_documents = len(bus_stop_documents_list)

        if counter is not None:
            if number_of_bus_stop_documents < counter:
                counter = number_of_bus_stop_documents

            for i in range(0, counter):
                bus_stop_document = bus_stop_documents_list[i]
                print (bus_stop_document)

        else:
            for bus_stop_document in bus_stop_documents_list:
                print (bus_stop_document)

        print ('number_of_bus_stop_documents:', number_of_bus_stop_documents)

    def print_travel_request_document(self, object_id):
        """
        Print a travel_request_document.

        :param object_id: ObjectId
        :return: None
        """
        travel_request_document = self.find_travel_request_document(
            object_id=object_id
        )
        print (travel_request_document)

    def print_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                       min_departure_datetime=None, max_departure_datetime=None,
                                       counter=None):
        """
        Print multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :param counter: int
        :return: None
        """
        travel_request_documents_list = self.find_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            bus_line_ids=bus_line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        number_of_travel_request_documents = len(travel_request_documents_list)

        if counter is not None:
            if number_of_travel_request_documents < counter:
                counter = number_of_travel_request_documents

            for i in range(0, counter):
                travel_request_document = travel_request_documents_list[i]
                print (travel_request_document)

        else:
            for travel_request_document in travel_request_documents_list:
                print (travel_request_document)

        print ('number_of_travel_request_documents:', number_of_travel_request_documents)

    def print_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_ids=None, timetables_control=True,
                                  timetable_entries_control=False, travel_requests_control=False,
                                  counter=None):
        """
        Print multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_ids: [int]
        :param timetables_control: bool
        :param timetable_entries_control: bool
        :param travel_requests_control: bool
        :param counter: int
        :return: None
        """
        timetable_documents = self.find_timetable_documents(
            object_ids=object_ids,
            timetable_ids=timetable_ids,
            bus_line_ids=bus_line_ids
        )
        

    def print_traffic_event_document(self, traffic_event_document=None, object_id=None, event_id=None):
        """
        Print a traffic_event_document.

        :param traffic_event_document: traffic_event_document
        :param object_id: ObjectId
        :param event_id: string
        :return: traffic_event_document
        """
        if traffic_event_document is None:
            traffic_event_document = self.find_traffic_event_document(
                object_id=object_id,
                event_id=event_id
            )

        print (traffic_event_document)

    def print_traffic_event_documents(self, traffic_event_documents=None, object_ids=None,
                                      event_ids=None, counter=None):
        """
        Print multiple traffic_event_documents.

        :param traffic_event_documents: [traffic_event_documents]
        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :param counter: int
        :return: traffic_event_documents: [traffic_event_document]
        """
        if traffic_event_documents is None:
            traffic_event_documents = self.find_traffic_event_documents(
                object_ids=object_ids,
                event_ids=event_ids
            )

        number_of_traffic_event_documents = len(traffic_event_documents)

        if counter is not None:
            if number_of_traffic_event_documents < counter:
                counter = number_of_traffic_event_documents

            for i in range(0, counter):
                traffic_event_document = traffic_event_documents[i]
                print (traffic_event_document)

        else:
            for traffic_event_document in traffic_event_documents:
                print (traffic_event_document)

        print ('number_of_traffic_event_documents:', number_of_traffic_event_documents)