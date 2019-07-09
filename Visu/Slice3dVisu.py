import pyvista
import numpy as np
import PVGeo
from PVGeo.filters import ManySlicesAlongPoints

"""

SlicedPlotPvGeo: Generate 3D Sliced plot using PVGeo.

readModel: Reads UBC files map and model to load the plot.

createSliceMap,sliceOnAllDomain,getSliceMap: Generates slices positions depending on the domain width/height and the number of slices.

viewSliceMap: Debug function

manualSlice: Generates slices from coordinates in data parameter provided by user

generateSlices: Draw slices on plot

"""

class SlicedPlotPvGeo:
	def readModel(self,mesh,model):
		reader = PVGeo.ubc.TensorMeshReader()
		reader.set_mesh_filename(mesh)
		reader.add_model_file_name(model)
		mesh = reader.apply()
		self.modelRun(mesh.threshold())

	def createSliceMap(self,sliced):
		self.sliced = sliced
		self.sliceOnAllDomain(self.sliced)
		return (pyvista.PolyData(self.xslicemap),\
			pyvista.PolyData(self.yslicemap),\
			pyvista.PolyData(self.zslicemap)
		)

	def modelRun(self,data):
		self.model = data

	def sliceOnAllDomain(self,sliced):
		x1,x2 = self.model.bounds[0],self.model.bounds[1]
		x=abs((x2-x1)/sliced)

		y1,y2 = self.model.bounds[2],self.model.bounds[3]
		y=abs((y2-y1)/sliced)

		z1,z2=self.model.bounds[4],self.model.bounds[5]
		z=abs(abs(z2)-abs(z1))/sliced

		datax = np.arange(x1+x, x2+x, x)
		datay,dataz = np.zeros(datax.shape), np.zeros(datax.shape)

		ysdatay = np.arange(y1+y, y2+y, y)
		ysdatax,ysdataz = np.zeros(ysdatay.shape), np.zeros(ysdatay.shape)

		zsdataz=np.arange(z1+z,z2+z,z)
		zsdatax,zsdatay=np.zeros(zsdataz.shape),np.zeros(zsdataz.shape)

		self.xslicemap = np.column_stack((datax,datay,dataz))
		self.yslicemap = np.column_stack((ysdatax,ysdatay,ysdataz))
		self.zslicemap = np.column_stack((zsdatax,zsdatay,zsdataz))

	def viewSliceMap(self,psize=5.0,color='k'):
		p = pyvista.Plotter()
		p.add_mesh(self.model.outline(), color=color)
		p.add_mesh(self.xsmap, point_size=psize)
		p.show()

	def getSliceMap(self,slicenum):
		self.xsmap,self.ysmap,self.zsmap = self.createSliceMap(slicenum)
		xslices = ManySlicesAlongPoints(n_slices=slicenum).apply(
			self.xsmap,
			self.model
		)
		yslices = ManySlicesAlongPoints(n_slices=slicenum).apply(
			self.ysmap,
			self.model
		)
		zslices = ManySlicesAlongPoints(n_slices=slicenum).apply(
			self.zsmap,
			self.model
		)
		return (xslices,yslices,zslices)

	def manualSlice(self,data,slicenum,s_min,s_max,cmap):
		if slicenum > data.shape[0]:
			slicenum = data.shape[0]
		self.smap = pyvista.PolyData(data)
		slices = ManySlicesAlongPoints(n_slices=slicenum).apply(
			self.smap,
			self.model
		)
		self.p.add_mesh(slices,lighting=False,clim=[s_min,s_max],cmap=cmap)

	def generateSlices(self,slicenum,s_min,s_max,cmap,axis,withLine):
		xslices,yslices,zslices = self.getSliceMap(slicenum)

		dataslice=[
			('x',xslices,self.xsmap),
			('y',yslices,self.ysmap),
			('z',zslices,self.zsmap)
		]

		for ax,sdata,smap in dataslice:
			if ax not in axis:
				continue
			if withLine:
				line=PVGeo.filters.AddCellConnToPoints().apply(smap)
				self.p.add_mesh(line,line_width=10)
			self.p.add_mesh(sdata,lighting=False,clim=[s_min,s_max],cmap=cmap)

	def run(self,slicenum,s_min,s_max,cmap,axis,isData=np.array(None),withLine=False):
		slicenum+=1 #Pour avoir le bon nombre de slices
		if slicenum<=0:
			return
		self.p = pyvista.Plotter()

		#Si on slice manuellement
		if isData.all() != None:
			self.manualSlice(isData,slicenum,s_min,s_max,cmap)
		else:
			self.generateSlices(slicenum,s_min,s_max,cmap,axis,withLine)

		self.p.add_mesh(self.model.outline())
		self.p.show_grid()
		self.p.show()

"""

VisuSlicesOnDomain: is called by GUI when the user chooses this type of visualization.

"""

def VisuSlicesOnDomain(**kwargs):
	cmap=kwargs.get('cmap','jet')
	s_min=float(kwargs.get('s_min',4))
	s_max=float(kwargs.get('s_max',7))
	mesh=kwargs.get('pmap')
	model=kwargs.get('mmap')
	slices_num=kwargs.get('nbslices',3)
	axis_l=[ i.split('_')[1] for i in ['axists_x','axists_y','axists_z'] if kwargs.get(i)]
	axis=''.join(axis_l)
	if len(axis)==0:
		print('VisuSlicesOnDomain error: choose one axis to slice')
		raise ValueError
	if mesh==None or model==None:
		print('VisuSlicesOnDomain error: mesh or model not found')
		raise FileNotFoundError
	mplot=SlicedPlotPvGeo()
	mplot.readModel(mesh,model)
	mplot.run(slices_num,s_min,s_max,cmap,axis)

# def main():
# 	mesh_file = './inputs/mapfram_188.out'
# 	model_file = './inputs/viewfram_188.out'

# 	s = SlicedPlotPvGeo()
# 	s.readModel(mesh_file,model_file)

# 	# testslicearray = np.array([
# 	# 	[2,2,-2],
# 	# 	[9,2,-2],
# 	# 	[10,2,-2],
# 	# 	[20,2,-2],
# 	# 	[30,2,-2]
# 	# ])

# 	s.run(3,0.49,0.51,'jet','z')

# if __name__ == '__main__':
# 	main()