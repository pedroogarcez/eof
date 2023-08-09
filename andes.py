import cartopy.crs as ccrs
from netCDF4 import Dataset
import cartopy
import matplotlib.pyplot as plt
import numpy as np
from eofs.standard import Eof
from eofs.examples import example_data_path
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np

# Referências: https://ajdawson.github.io/eofs/latest/examples/nao_standard.html

def variaveis(arquivo):
	ncin = Dataset(arquivo, 'r')
	z_djf = ncin.variables['geopotential_height'][:,11,:,:]
	lons = ncin.variables['longitude'][:]
	lats = ncin.variables['latitude'][:]
	time = ncin.variables['time'][:]
	return z_djf, lons, lats, time
	
def media(z):
	return np.ma.mean(z,axis=0)

def anomalia(z):
	z_djf_mean = z.mean(axis=0)
	z_djf = z - z_djf_mean
	return z_djf

# Create an EOF solver to do the EOF analysis. Square-root of cosine of
# latitude weights are applied before the computation of EOFs.
def eof_solver(z_anom,lats):
	coslat = np.cos(np.deg2rad(lats)).clip(0., 1.)
	wgts = np.sqrt(coslat)[..., np.newaxis]
	solver = Eof(z_anom, weights=wgts)
	eof1 = solver.eofsAsCorrelation(neofs=1)
	return eof1

def plot_eof(eof,lons,lats,titulo,inf=-80,sup=80,step=11):
# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
	plt.figure(figsize=(12,8))
	#clevs = np.linspace(inf, sup, step)
	clevs = np.arange(inf, sup, step)
	ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=190))
	ax.coastlines()
	ax.gridlines(draw_labels=True)
	fill = ax.contourf(lons, lats, eof.squeeze(), levels=clevs,
	            cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
	cb = plt.colorbar(fill, orientation='horizontal')            
	plt.title(f'EOF {titulo}', fontsize=16)
	fig_name = titulo.replace(" ", "")
	plt.savefig(f'EOF{fig_name}')
	plt.show()
	return

#def plot(media_geopotencial,lats,lons,titulo,inf=4900,sup=5880,step=11):
def plot(media_geopotencial,lats,lons,titulo,lmin,lmax):
	fig = plt.figure(figsize=(12, 8))
	m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
	#m = Basemap(projection='cyl', llcrnrlat=-55, urcrnrlat=15, llcrnrlon=270, urcrnrlon=330, resolution='c')
	lon, lat = np.meshgrid(lons, lats)
	x, y = m(lon, lat)

#	levels = np.linspace(np.min(media_geopotencial), np.max(media_geopotencial)+1, 20)
	levels = np.arange(lmin, lmax+.1, .1)
#	levels = np.linspace(5650, 5885, 11)
	cs = m.contourf(x, y, media_geopotencial, levels, cmap=plt.cm.RdBu_r)
#	cs = m.contour(x, y, media_geopotencial)
#	plt.clabel(cs, inline=1, fontsize=10)	
	cbar = m.colorbar(cs, location='right', pad='5%')
	cbar.set_label('Geopotential (m)')
	
	m.drawcoastlines()
	m.drawmapboundary()
	m.drawparallels(np.arange(-60.,60.,30.),labels=[1,0,0,0]) # draw parallels
	m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
	
	plt.title(titulo,fontsize=16)
	fig_name = titulo.replace(" ", "")
	plt.savefig(fig_name)
	plt.show()
	return
	
# Analisando para os meses de DJF
z1_DJF, lons1_DJF, lats1_DJF,time1_DJF = variaveis('zg1_DJF.nc')
z2_DJF, lons2_DJF, lats2_DJF,time2_DJF = variaveis('zg2_DJF.nc')

z1_anom_DJF = anomalia(z1_DJF)
z2_anom_DJF = anomalia(z2_DJF)

eof1_DJF = eof_solver(z1_anom_DJF,lats1_DJF)
eof2_DJF = eof_solver(z2_anom_DJF,lats2_DJF)
cordilheira_DJF = eof1_DJF-eof2_DJF

# Analisando a variável sem calcular o EOF
media_z1 = media(z1_DJF)
media_z2 = media(z2_DJF)
cordilheira = media_z1-media_z2
media_hs = media(z1_hs)
media2_hs = media(z2_hs)
cordilheira_hs = media_hs-media2_hs

cordilheira1 = cordilheira/np.max(cordilheira)
cordilheira1_hs = (cordilheira_hs/np.max(cordilheira_hs))

#plot(media_z1,lats2_DJF,lons2_DJF,'Central zg1',-50,50)
#plot(cordilheira1_hs,lats_hs,lons_hs,'Central zg1',-1,1.1)
#plot(media_z2,lats2_DJF,lons2_DJF,'Central zg2')
plot(cordilheira1,lats1_DJF,lons1_DJF,'Geopotential zg1-zg2 (Verão(Dez,Jan,Fev))',-1,1)

plot_eof(eof1_DJF, lons1_DJF,lats1_DJF,titulo,inf=-80,sup=80,step=11)
plot_eof(eof2_DJF, lons2_DJF,lats2_DJF,titulo,inf=-80,sup=80,step=11)
plot_eof(cordilheira_DJF,lons1_DJF,lats1_DJF,titulo,inf=-80,sup=80,step=11)