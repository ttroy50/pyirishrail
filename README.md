PyIrishRail
========================================

Python Interface for the Irish Rail RTPI XML interface.

[![Build Status](https://travis-ci.org/ttroy50/pyirishrail.svg?branch=master)](https://travis-ci.org/ttroy50/pyirishrail)



Example basic usage
-------------------

    >>> from pyirishrail.pyirishrail import IrishRailRTPI
    >>> e = IrishRailRTPI()
    >>> e.get_station_by_name("Tara Street", direction="Southbound")
