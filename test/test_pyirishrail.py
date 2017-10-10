from pyirishrail.pyirishrail import IrishRailRTPI

trains =    [{
        "code": "E136 ",
        "destination": "Bray",
        "destination_time": "23:32",
        "direction": "Northbound",
        "due_in_mins": "52",
        "expected_arrival_time": "22:42",
        "expected_departure_time": "22:43",
        "late_mins": "0",
        "location_type": "S",
        "origin": "Greystones",
        "origin_time": "22:15",
        "scheduled_arrival_time": "22:42",
        "scheduled_departure_time": "22:43",
        "type": "DART"
    },
    {
        "code": "P672 ",
        "destination": "Greystones",
        "destination_time": "22:49",
        "direction": "Southbound",
        "due_in_mins": "56",
        "expected_arrival_time": "22:46",
        "expected_departure_time": "22:47",
        "late_mins": "0",
        "location_type": "S",
        "origin": "Maynooth",
        "origin_time": "22:05",
        "scheduled_arrival_time": "22:46",
        "scheduled_departure_time": "22:47",
        "type": "Train"
    },
    {
        "code": "E133 ",
        "destination": "Greystones",
        "destination_time": "23:53",
        "direction": "Southbound",
        "due_in_mins": "67",
        "expected_arrival_time": "22:57",
        "expected_departure_time": "22:58",
        "late_mins": "0",
        "location_type": "S",
        "origin": "Malahide",
        "origin_time": "22:30",
        "scheduled_arrival_time": "22:57",
        "scheduled_departure_time": "22:58",
        "type": "DART"
    }]

def test_prune_direction():
    ir = IrishRailRTPI()
    only_southbound = ir._prune_trains(trains, direction="Southbound")
    assert len(only_southbound) == 2
    for train in only_southbound:
        assert train["direction"] == "Southbound"

    only_northbound = ir._prune_trains(trains, direction="Northbound")
    assert len(only_northbound) == 1
    for train in only_northbound:
        assert train["direction"] == "Northbound"


def test_prune_destination():
    ir = IrishRailRTPI()
    only_bray = ir._prune_trains(trains, destination="Bray")
    assert len(only_bray) == 1
    for train in only_bray:
        assert train["destination"] == "Bray"

    only_greystones = ir._prune_trains(trains, destination="Greystones")
    assert len(only_greystones) == 2
    for train in only_greystones:
        assert train["destination"] == "Greystones"

def test_prune_both():
    ir = IrishRailRTPI()
    only_bray = ir._prune_trains(trains, direction="Northbound", destination="Bray")
    assert len(only_bray) == 1
    for train in only_bray:
        assert train['direction'] == "Northbound"
        assert train["destination"] == "Bray"

    only_greystones = ir._prune_trains(trains, direction="Southbound", destination="Greystones")
    assert len(only_greystones) == 2
    for train in only_greystones:
        assert train['direction'] == "Southbound"
        assert train["destination"] == "Greystones"

    no_trains = ir._prune_trains(trains, direction="Northbound", destination="Greystones")
    assert len(no_trains) == 0
