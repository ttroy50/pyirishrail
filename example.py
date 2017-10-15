from pyirishrail.pyirishrail import IrishRailRTPI
import sys
import json

def main():
    
    ir = IrishRailRTPI()
    print(json.dumps(ir.get_all_stations(), indent=4, sort_keys=True))
    print ("All Current Trains")
    print(json.dumps(ir.get_all_current_trains(), indent=4, sort_keys=True))
    print ("Tara Street")
    print(json.dumps(ir.get_station_by_name("Tara Street"), indent=4, sort_keys=True))
    print ("Tara Street southbound to Pearse Street")
    print(json.dumps(ir.get_station_by_name("Tara Street", direction="Southbound"),
                     indent=4,
                     sort_keys=True))
    print("All stops for P671")
    print(json.dumps(ir.get_train_stops("P671"), indent=4, sort_keys=True))
    print("Tara Street southbound stops at Dun Laoghaire in 30 minutes")
    print(json.dumps(ir.get_station_by_name("Tara Street",
                                            direction="Southbound",
                                            stops_at="Dun Laoghaire",
                                            num_minutes=30), indent=4, sort_keys=True))

    return 0

if __name__ == '__main__':
    sys.exit(main())


