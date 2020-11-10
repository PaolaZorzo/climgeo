'''

This script aims to interpolate precipitation data and export the result in a netCDF4 arquive

_____________________________________________________________________________________________

Pay attention to the spatial resolution and location of interpolation:
    - Paraná state of Brasil in a grid of 0.1°x0.1° ~ 10km
    
_____________________________________________________________________________________________

In griddata(), linear method is the indicated for precipitation data, any other can produce 
negative results

_____________________________________________________________________________________________

For any error/coment/contibuction please contact me at:

paolajzorzo@gmail.com
paola.zorzo@simepar.br

https://linktr.ee/paolazorzo

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd
from netCDF4 import Dataset
import os
import datetime as dt
from netCDF4 import date2num,num2date

#opening file with the loop file names

'''
For each hour of data we have an archive,
these comand will open a list with the 
names of these archives organized in lines
'''

os.chdir("/your/directory/path/")
dates=open('ARCHIVE', "r")
lines=dates.readlines()


'''
Here I present to you two option of how 
can be created the grid space for the interpolation
'''

'''
1ST grid
#delta is the spatial resolution
delta=0.1
X = np.arange(-55,-48,delta)
Y = np.arange(-27,-22,delta)
'''

#2ST grid
X=np.linspace(-55,-48,71)
Y= np.linspace(-27,-22,51)

(x,y)=np.meshgrid(X,Y)

#making a netCDF4 file

'''
Here I demonstrate how to create a simple netCDF file with only three dimensions
arrange in P(time, latitude, longitude)

'''
dataset = Dataset('prec.nc', 'w', format='NETCDF4')
dataset.createDimension('X', 71)
dataset.createDimension('Y', 51)
dataset.createDimension('t', 8761)
lonvar = dataset.createVariable('X','float32',('X'));lonvar[:] = X);
lonvar.units = 'degrees_east'
lonvar.long_name = 'longitude'
latvar = dataset.createVariable('Y','float32',('Y'));latvar[:] = Y);
latvar.units = 'degrees_north'
latvar.long_name = 'latitude'
timevar = dataset.createVariable('t','float64',('t'))
timevar.units = 'hours since 1800-01-01'
timevar.long_name = 'time'
timevar.calendar = 'gregorian'
timevar.time_step = 'hourly'
date = pd.date_range(dt.datetime(2019,1,1,0),dt.datetime(2020,1,1,0),freq='60min')
times = date2num(date.to_pydatetime(), timevar.units)
timevar[:]=times
crsvar = dataset.createVariable('crs', np.int8, ())
crsvar.standard_name = 'crs'
crsvar.grid_mapping_name = 'latitude_longitude'
crsvar = dataset.createVariable('WGS84', 'c')crsvar.spatial_ref = """GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]"""
vble = dataset.createVariable("vble", np.float32, ("latvar", "lonvar"))
vble.grid_mapping = 'WGS84' # the crs variable name
vble.grid_mapping_name = 'latitude_longitude'
vble[:] = array_variable
P.units='mm'
P.standard_name='Precipitation'
P.short_name='p'

print(P)

#hour interpolation loop

'''
The archives with precipitation data are save in .csv,
where wich line corespond to a meteorological station data
localized in (day.longitude,day.latitude)
'''

for i in range(0,8761):
    print(i)
    aux=lines[i]
    day= pd.read_csv(aux[0:19])
    lat=day.latitude
    lon=day.longitude
    #column with the precipitaion dataset
    p=day.valor
    #performing the interpolation
    grid_datos = griddata((lon,lat),p,(x, y),method='linear')
    P[i] = grid_datos
    
#closing netCDF4    
dataset.close()

#plot

'''
This is a simple plot to see if the interpolation is
done correctly
'''

plt.clf()
plt.contourf(X,Y,grid_datos,8,cmap='Blues')
plt.colorbar()
plt.scatter(lon,lat)
plt.xlim(np.min(lon),np.max(lon))
plt.ylim(np.min(lat),np.max(lat))
plt.show()
