import PVGeo

"""

Plot3DPvGeo: Generate 3D Plot using PVGeo.


"""

class Plot3DPvGeo:
	def readModel(self,mesh,model):
		reader = PVGeo.ubc.TensorMeshReader()
		reader.set_mesh_filename(mesh)
		reader.add_model_file_name(model)
		self.mesh = reader.apply()
		self.c_mesh = self.mesh.threshold()

	def slice_ortho(self,s_min,s_max,colormap='jet'):
		self.mesh.slice_orthogonal().plot(cmap=colormap,clim=[s_min, s_max],show_edges=True)

	def run(self,s_min,s_max,colormap='jet'):
		self.c_mesh.plot(cmap=colormap,clim=[s_min, s_max],show_edges=True)


"""

VisuFullDomain: is called by GUI when the user chooses this type of visualization.

"""

def getargs(**kwargs):
	return { key:kwargs.get(key,i) for key,i in { 'cmap':'jet','s_min':4,'s_max':7,'pmap':None,'mmap':None }.items() }

def VisuFullDomain(**kwargs):
	p_args=getargs(**kwargs)
	if p_args['pmap']==None or p_args['mmap']==None:
		print('VisuFullDomain error: mesh or model not found')
		raise FileNotFoundError
	mplot=Plot3DPvGeo()
	mplot.readModel(p_args['pmap'],p_args['mmap'])
	mplot.run(float(p_args['s_min']),float(p_args['s_max']),p_args['cmap'])

# def main():
# 	mesh_file = './inputs/map.out'
# 	model_file = './inputs/mesh.out'

# 	p3 = Plot3DPvGeo()
# 	p3.readModel(mesh_file,model_file)
# 	p3.run(-1,1)

# if __name__ == '__main__':
# 	main()