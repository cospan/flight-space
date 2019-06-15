
'''
    Using OpenSky's State Vector for all outputs, other sources need to
    populate this state vector object
'''

class StateVector(object):
    """ Represents the state of a vehicle at a particular time. It has the following fields:

      |  **icao24** - ICAO24 address of the transmitter in hex string representation.
      |  **callsign** - callsign of the vehicle. Can be None if no callsign has been received.
      |  **origin_country** - inferred through the ICAO24 address
      |  **time_position** - seconds since epoch of last position report. Can be None if there was no position report received by OpenSky within 15s before.
      |  **last_contact** - seconds since epoch of last received message from this transponder
      |  **longitude** - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
      |  **latitude** - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
      |  **geo_altitude** - geometric altitude in meters. Can be None
      |  **on_ground** - true if aircraft is on ground (sends ADS-B surface position reports).
      |  **velocity** - over ground in m/s. Can be None if information not present
      |  **heading** - in decimal degrees (0 is north). Can be None if information not present.
      |  **vertical_rate** - in m/s, incline is positive, decline negative. Can be None if information not present.
      |  **sensors** - serial numbers of sensors which received messages from the vehicle within the validity period of this state vector. Can be None if no filtering for sensor has been requested.
      |  **baro_altitude** - barometric altitude in meters. Can be None
      |  **squawk** - transponder code aka Squawk. Can be None
      |  **spi** - special purpose indicator
      |  **position_source** - origin of this state's position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM
    """
    keys = ["icao24", "callsign", "origin_country", "time_position",
            "last_contact", "longitude", "latitude", "baro_altitude", "on_ground",
            "velocity", "heading", "vertical_rate", "sensors",
            "geo_altitude", "squawk", "spi", "position_source"]

    # We are not using namedtuple here as state vectors from the server might be extended; zip() will ignore additional
    #  entries in this case
    def __init__(self, arr):
        """ arr is the array representation of a state vector as received by the API """
        self.__dict__ = dict(zip(StateVector.keys, arr))

    def __repr__(self):
        return "StateVector(%s)" % repr(self.__dict__.values())

    def __str__(self):
        return pprint.pformat(self.__dict__, indent=4)



class ADBSSource:
    def __init__(self):
        pass
        self.bounding_box = [[0.0, 0.0], [0.0, 0.0]]
        self.bounding_box_enabled = False

    def open(self):
        pass

    def close(self):
        pass

    def enable_bounding_box(self, enable):
        self.bounding_box_enabled = enable

    def set_bounding_box(self, min_long, max_long, min_lat, max_lat):
        """
        Bounding Box Values, all values are in WGS84 format:

        Example:

        min lat = 45.8389
        max lat = 47.8229

        min lon = 5.9962
        max lon = 10.5226
        """

        self.bounding_box[0][0] = min_lat
        self.bounding_box[0][1] = max_lat
        self.bounding_box[1][0] = min_long
        self.bounding_box[1][1] = max_long

    def get_states(self):
        pass

class OpenSkyADBS(ADBSSource):
    def __init__(self):
        ADBSSource.__init__(self)

    def open(self):
        from opensky_api import OpenSkyApi
        self.api = OpenSkyApi()

    def get_states(self):
        if self.bounding_box_enabled:
            return self.api.get_states(bbox=(self.bounding_box[0][0], self.bounding_box[0][1],
                                             self.bounding_box[1][0], self.bounding_box[1][1]))
        else:
            return self.api.get_states()



class ADBSFactory:
    def __init__(self):
        pass

    def open(self, name = "opensky"):
        if name == "opensky":
            adsb = OpenSkyADBS()
            adsb.open()
            return adsb
        else:
            print ("No Other API is supported at this time")


if __name__ == "__main__":
    print ("Testing... Getting all planes for Massachusetts")
    adsb = ADBSFactory().open("opensky")
    adsb.set_bounding_box(42.067599, 42.68852, -73.504556, -70.629270)
    #adsb.enable_bounding_box(True);
    s = adsb.get_states()
    print("States")
    print(s)
