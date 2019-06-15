# Flight Space

ADS-B Flight Visualizer Using the Panda3D Game Engine

## ADS-B Interfaces

At the moment the only way to receive ADS-B messages is by using the OpenSky API

https://github.com/openskynetwork/opensky-api

### Open Sky API

To install clone the repo in local directory

    git clone https://github.com/openskynetwork/opensky-api.git
    pip3 install -e ./opensky-api/python

To use OpenSky within the app pass in 'opensky' as the name to the ADBSFactory open function

    adsb = ADBSFactory().open("opensky")

## Thank You

[Somsubhra FlySim: Great Reference](https://github.com/Somsubhra/FlySim)

