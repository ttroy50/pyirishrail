"""
Irish Rail RTPI API

Some code taken from
https://github.com/scottcunningham/irish_rail.py/blob/master/irish_rail.py
"""

from xml.dom import minidom
import logging
import requests


STATION_TYPE_TO_CODE_DICT = {
    'mainline': 'M',
    'suburban': 'S',
    'dart': 'D'
}

_LOGGER = logging.getLogger(__name__)


def _get_minidom_tag_value(station, tag_name):
    """get a value from a tag (if it exists)"""
    tag = station.getElementsByTagName(tag_name)[0].firstChild
    if tag:
        return tag.nodeValue

    return None


def _parse(data, obj_name, attr_map):
    """parse xml data into a python map"""
    parsed_xml = minidom.parseString(data)
    parsed_objects = []
    for obj in parsed_xml.getElementsByTagName(obj_name):
        parsed_obj = {}
        for (py_name, xml_name) in attr_map.items():
            parsed_obj[py_name] = _get_minidom_tag_value(obj, xml_name)
        parsed_objects.append(parsed_obj)
    return parsed_objects


class IrishRailRTPI(object):
    """Interacts with the Irish Rail RTPI API.
    """

    # pylint: disable=R0201

    def _parse_station_list(self, data):
        """parse the station list"""
        attr_map = {
            'name': 'StationDesc',
            'alias': 'StationAlias',
            'lat': 'StationLatitude',
            'long': 'StationLongitude',
            'code': 'StationCode',
            'id': 'StationId',
        }
        return _parse(data, 'objStation', attr_map)

    def _parse_station_data(self, data):
        """parse the station data"""
        attr_map = {
            'code': 'Traincode',
            'origin': 'Origin',
            'destination': 'Destination',
            'origin_time': 'Origintime',
            'destination_time': 'Destinationtime',
            'due_in_mins': 'Duein',
            'late_mins': 'Late',
            'expected_arrival_time': 'Exparrival',
            'expected_departure_time': 'Expdepart',
            'scheduled_arrival_time': 'Scharrival',
            'scheduled_departure_time': 'Schdepart',
            'type': 'Traintype',
            'direction': 'Direction',
            'location_type': 'Locationtype',
        }
        return _parse(data, 'objStationData', attr_map)

    def _parse_all_train_data(self, url):
        """parse train data"""
        attr_map = {
            'status': 'TrainStatus',
            'latitude': 'TrainLatitude',
            'longitude': 'TrainLongitude',
            'code': 'TrainCode',
            'date': 'TrainDate',
            'message': 'PublicMessage',
            'direction': 'Direction'
        }
        return _parse(url, 'objTrainPositions', attr_map)

    def get_all_stations(self, station_type=None):
        """Returns information of all stations.
        @param<optional> station_type: ['mainline', 'suburban', 'dart']
        """
        params = None
        if station_type and station_type in STATION_TYPE_TO_CODE_DICT:
            url = self.api_base_url + 'getAllStationsXML_WithStationType?'
            params = {
                'stationType': STATION_TYPE_TO_CODE_DICT[station_type]
            }
        else:
            url = self.api_base_url + 'getAllStationsXML'

        response = requests.get(
            url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        return self._parse_station_list(response.content)

    def get_all_current_trains(self, train_type=None, direction=None):
        """Returns all trains that are due to start in the next 10 minutes
        @param train_type: ['mainline', 'suburban', 'dart']
        """
        params = None
        if train_type:
            url = self.api_base_url + 'getCurrentTrainsXML_WithTrainType'
            params = {
                'TrainType': STATION_TYPE_TO_CODE_DICT[train_type]
            }
        else:
            url = self.api_base_url + 'getCurrentTrainsXML'

        response = requests.get(
            url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        trains = self._parse_all_train_data(response.content)

        if direction is not None:
            return self._prune_trains(trains, direction=direction)

        return trains

    def get_station_by_name(self,
                            station_name,
                            num_minutes=None,
                            direction=None,
                            destination=None):
        """Returns all trains due to serve station `station_name`.
        """
        url = self.api_base_url + 'getStationDataByNameXML?'
        params = {
            'StationDesc': station_name
        }
        if num_minutes:
            params['NumMins'] = num_minutes

        response = requests.get(
            url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        trains = self._parse_station_data(response.content)
        if direction is not None or destination is not None:
            return self._prune_trains(trains,
                                      direction=direction,
                                      destination=destination)

        return trains

    def get_station_by_code(self,
                            station_code,
                            num_minutes=None,
                            direction=None,
                            destination=None):
        """Returns all trains due to serve station with code `station code`.
        """
        url = self.api_base_url + 'getStationDataByCodeXML?'
        params = {
            'StationCode': station_code
        }
        if params:
            params['NumMins'] = num_minutes

        response = requests.get(
            url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        trains = self._parse_station_data(response.content)
        if direction is not None or destination is not None:
            return self._prune_trains(trains,
                                      direction=direction,
                                      destination=destination)

        return trains

    def _prune_trains(self, trains, direction=None, destination=None):
        """Only return the data matching direction and / or destination"""
        pruned_data = []
        for train in trains:
            append = True
            if direction is not None and train["direction"] != direction:
                append = False

            if destination is not None and train["destination"] != destination:
                append = False

            if append:
                pruned_data.append(train)

        return pruned_data

    # Ctor
    def __init__(self):
        """Setup Class."""
        self.api_base_url = 'http://api.irishrail.ie/realtime/realtime.asmx/'
