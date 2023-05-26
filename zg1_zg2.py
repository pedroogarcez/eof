import cartopy.crs as ccrs
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from eofs.standard import Eof
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np

# Referências: https://ajdawson.github.io/eofs/latest/examples/nao_standard.html

#Criando uma função responsável por ler as variáveis presentes no arquivo.
# Através do comando "ncdump -h nome_do_arquivo.nc" no terminal é possível descobrir como cada variável está nomeada.

def variaveis(arquivo):
	ncin = Dataset(arquivo, 'r')
	# Como a altura geopotencial depende de time,level,lats,lons, vamos específicar somente o nível 11 (level=200 hPa).
	z_djf = ncin.variables['geopotential_height'][:,11,:,:]
	# Selecionando todas as longitudes do arquivo
	lons = ncin.variables['longitude'][:]
	# Selecionando todas as latitudes do arquivo
	lats = ncin.variables['latitude'][:]
	# Selecionando todas as datas do arquivo
	time = ncin.variables['time'][:]
	return z_djf, lons, lats, time

# Calculando a média do vetor Geopotencial
def media(z):
	return np.ma.mean(z,axis=0)

#Calculando a anomalia
def anomalia(z):
	z_djf_mean = z.mean(axis=0)
	z_djf = z - z_djf_mean
	return z_djf

# Calculando o eof
def eof_solver(z_anom,lats):
	coslat = np.cos(np.deg2rad(lats)).clip(0., 1.)
	wgts = np.sqrt(coslat)[..., np.newaxis]
	solver = Eof(z_anom, weights=wgts)
	eof1 = solver.eofsAsCorrelation(neofs=1)
	return eof1

# Criando uma figura para plot do Eof calculado
def plot_eof(eof,lons,lats,titulo,inf=-80,sup=80,step=11):
# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
	plt.figure(figsize=(12,8))
	#clevs = np.linspace(inf, sup, step)
	clevs = np.arange(inf, sup, step)
	ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=190))
	ax.coastlines()
	ax.gridlines(draw_labels=True)
	fill = ax.contour(lons, lats, eof.squeeze(), levels=clevs,
	            cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
	cb = plt.colorbar(fill, orientation='horizontal')            
	plt.title(f'EOF {titulo}', fontsize=16)
	fig_name = titulo.replace(" ", "")
	plt.savefig(f'EOF{fig_name}')
	plt.show()
	return


#def plot(media_geopotencial,lats,lons,titulo,inf=4900,sup=5880,step=11):
def plot(media_geopotencial,lats,lons,titulo):
	fig = plt.figure(figsize=(12, 8))
	m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
	#m = Basemap(projection='cyl', llcrnrlat=-55, urcrnrlat=15, llcrnrlon=270, urcrnrlon=330, resolution='c')
	lon, lat = np.meshgrid(lons, lats)
	x, y = m(lon, lat)

	levels = np.linspace(np.min(media_geopotencial), np.max(media_geopotencial)+1, 20)
#	levels = np.linspace(5650, 5885, 11)
	cs = m.contour(x, y, media_geopotencial, levels, cmap=plt.cm.RdBu_r)
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

#z1_anom_DJF = anomalia(z1_DJF*-1)
z1_anom_DJF = anomalia(z1_DJF)
z2_anom_DJF = anomalia(z2_DJF)

eof1_DJF = eof_solver(z1_anom_DJF,lats1_DJF)
eof2_DJF = eof_solver(z2_anom_DJF,lats2_DJF)
cordilheira_DJF = eof1_DJF-eof2_DJF

# Analisando a variável após o cálculo do EOF
#plot_eof(eof1_DJF,lons1_DJF,lats1_DJF,'DJF 1978-2014 zg_test1',np.min(eof1_DJF),np.max(eof1_DJF))
#plot_eof(eof2_DJF,lons2_DJF,lats2_DJF,'DJF 1978-2014 zg_test2',np.min(eof2_DJF),np.max(eof2_DJF))
#plot_eof(cordilheira_DJF*-1,lons1_DJF,lats1_DJF,'zg1 - zg2',np.min(cordilheira_DJF),np.max(cordilheira_DJF))
#plot_eof(cordilheira_DJF*-1,lons1_DJF,lats1_DJF,'zg1 - zg2',-1,1.1,0.1)#,0.3,1,0.1)

# Analisando a variável sem calcular o EOF
media_z1 = media(z1_DJF)
media_z2 = media(z2_DJF)
cordilheira = media_z1-media_z2

#plot(media_z1,lats2_DJF,lons2_DJF,'Central zg1')
plot(media_z2,lats2_DJF,lons2_DJF,'Central zg2')
#plot(cordilheira,lats1_DJF,lons1_DJF,'Geopotential zg1-zg2 (Verão(Dez,Jan,Fev))')
