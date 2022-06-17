from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
#https://docs.python.org/3/howto/curses.html
import curses
#stdscr = curses.initscr()
#https://rhodesmill.org/skyfield/earth-satellites.html
#http://celestrak.com/NORAD/elements/
#https://isstracker.pl/en?utm_source=partner&utm_medium=widget&utm_term=issfanclubeu
ts = load.timescale()
stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
#print('Loaded', len(satellites), 'satellites')

by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
#print(satellite)
#grondstation = wgs84.latlon(+51.5, -3.55)
#Unit 1B, Kingsway Bldg, Bridgend Industrial Estate, Bridgend CF31 3YH
#random numbers?
#position set from terminal 
station_lat= float(input("Enter station_lat: "))
print("The type of ",station_lat," is", type(station_lat))
station_lon = float(input("Enter station_lat: "))
print("The type of ",station_lon," is", type(station_lon))
grondstation = wgs84.latlon(station_lat,station_lon)
# list passes for time period 
#t0 = ts.utc(2022, 6, 14)
#t1 = ts.utc(2022, 6, 18)
#t, events = satellite.find_events(grondstation, t0, t1, altitude_degrees=30.0)
#for ti, event in zip(t, events):
#    name = ('rise above 30°', 'culminate', 'set below 30°')[event]
#    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
# You can instead use ts.now() for the current time
#t = ts.utc(2022, 6, 14, 13, 30, 0)
elevation_m = 20.0
stdscr = curses.initscr()
try:
    while True:
      t = ts.now()
      geocentric = satellite.at(t)
      #print(geocentric.position.km)
      stdscr.addstr(0, 0, 'Satellite: {}'.format(satellite))
      lat, lon = wgs84.latlon_of(geocentric)
      stdscr.addstr(1, 0, 'Latitude: {} Longitude {}   '.format(lat, lon))
      #stdscr.refresh()
      #print('Latitude:', lat, 'Longitude:', lon)      
      subpoint = wgs84.latlon(lat.degrees, lon.degrees, elevation_m)      
      difference = satellite - grondstation
      topocentric = difference.at(t)
      #print(topocentric.position.km)     
      alt, az, distance = topocentric.altaz()
      stdscr.addstr(2, 0, 'Altitude: {} Azimuth: {} Distance:  {:.1f}'.format(alt, az, distance.km ))
            
      if alt.degrees > 0:
        #print('The ISS is above the horizon')
        stdscr.addstr(3, 0, 'The ISS is above the horizon', curses.A_REVERSE)
        stdscr.refresh()
      else:
        stdscr.addstr(3, 0, 'The ISS is below the horizon', curses.A_REVERSE)
        stdscr.refresh()         
      #print('Altitude:', alt, 'Azimuth:', az, 'Distance: {:.1f} km'.format(distance.km))
      stdscr.refresh()        
except KeyboardInterrupt:
    pass