import pyvista
import PVGeo

import AdditionnalModules.UsefullFunc.utilsfunc as usef

"""

HandleAnimationFiles: Reads and creates mesh from model and map files passed through the constructor.

"""

class HandleAnimationFiles:
	def __init__(self,m_map,m_model):
		self.map_pattern,self.map_dir=m_map
		self.model_pattern,self.model_dir=m_model

	def getFilenames(self,m_pattern,m_dir):
		return usef.findMatch(m_pattern,m_dir)

	def mSort(self,tosort):
		if len(tosort)==0:
			return False
		return usef.sortByName(tosort)

	def getRectGrid(self,mapdata,modeldata):
		def compute(compute_map,compute_model):
			reader.clear_mesh()
			reader.clear_models()
			reader.set_mesh_filename(compute_map)
			reader.add_model_file_name(compute_model)
			return reader.apply().threshold()
		reader=PVGeo.ubc.TensorMeshReader()
		return [ compute(m_map,m_model) for m_map,m_model in zip(mapdata,modeldata) ]

	def wrapFileOp(self):
		m_map=self.mSort(self.getFilenames(self.map_pattern,self.map_dir))
		m_model=self.mSort(self.getFilenames(self.model_pattern,self.model_dir))
		if m_map==False or m_model==False:
			self.m_mesh=False
		self.m_mesh=self.getRectGrid(m_map,m_model)

	def run(self):
		self.wrapFileOp()
		return self.m_mesh

"""

CameraRotation: Useful calculations needed to move the camera.

"""

class CameraRotation:
	def getCircleCoo(self,angle,radius,base):
		import math as m
		return ((m.cos(m.radians(angle))*radius)+base[0]) , ((m.sin(m.radians(angle))*radius)+base[1])


"""

MakeAnimationVideo: Creates list of meshes with 'HandleAnimationFiles' and runs into this list to display each meshes and creates an animation.

__init__: Retrieves all parameters and get the list of meshes

initVideo: Open the file to write the animation and display the first mesh of the animation

rewrite: Clear the screen and draw the next mesh of the animation

updateCamCoo: If the camera moves during the simulation, this retrieves the new camera position

update: Main loop, writes new displayed frame to the file predecily opened

"""

class MakeAnimationVideo:
	def __init__(self,filename,m_map,m_model,**kwargs):
		self.m_mesh=HandleAnimationFiles(m_map,m_model).run()
		if not self.m_mesh:
			return
		self.filename=filename

		self.framepersecond=kwargs.get('frames',1)
		if self.framepersecond<=0:
			return
		self.smin=kwargs.get('smin',5)
		self.smax=kwargs.get('smax',7)

		self.radius=kwargs.get('radius',50)

		self.movecam=kwargs.get('movecam',False)
		self.angle=kwargs.get('startangle',0)

	def initVideo(self):
		self.plotter = pyvista.Plotter()
		self.plotter.open_movie(self.filename,framerate=60)

		self.plotter.add_mesh(
			self.m_mesh[0],
			cmap='jet',
			clim=[self.smin,self.smax]
		)
		self.initializeCam(self.m_mesh[0])
		if self.movecam==True:
			self.updateCamCoo()
		self.plotter.show(auto_close=False)
		self.plotter.write_frame()

	def rewrite(self,it_mesh):
		self.plotter.clear()
		self.plotter.add_mesh(
			it_mesh,
			cmap='jet',
			clim=[self.smin,self.smax]
		)

	def updateCamCoo(self):
		x,y=CameraRotation().getCircleCoo(
			self.angle,
			self.radius,
			(
				self.x_center,
				self.y_center
			)
		)
		self.plotter.camera_position=[ (x,y,0), (self.x_center,self.y_center,self.z_size), (0,0,1) ]
		self.angle=((self.angle+2)%360)

	def initializeCam(self,mesh):
		x_size=abs(mesh.bounds[1]-mesh.bounds[0])
		y_size=abs(mesh.bounds[3]-mesh.bounds[2])
		z_size=mesh.bounds[5]-mesh.bounds[4]

		self.x_center=int(x_size/2)
		self.y_center=int(y_size/2)
		self.z_center=int(z_size)
		self.z_size=mesh.bounds[4]

	def update(self):
		for it_mesh in self.m_mesh:
			self.rewrite(it_mesh)
			if self.movecam==True:
				self.updateCamCoo()
			[self.plotter.write_frame() for _ in range(self.framepersecond)]

	def run(self):
		self.initVideo()
		print('Starting video...')
		self.update()
		print('Close...')
		self.plotter.close()


"""

VisuAnimation: is called by GUI when the user chooses this type of visualization.

"""

def getargs(**kwargs):
	return {
		key:kwargs.get(key,i) for key,i in {
			'patternmap':None,
			'patternmodel':None,
			'moviename':'nmovie.mp4',
			'frame':1,
			's_min':4,
			's_max':7,
			'dirmap':None,
			'dirmodel':None,
			'autocam':False,
			'startangle':0,
			'radius':150,
		}.items()
	}

def VisuAnimation(**kwargs):
	p_args=getargs(**kwargs)

	if p_args['dirmap']==None\
		or p_args['dirmodel']==None\
		or p_args['patternmap']==None\
		or p_args['patternmodel']==None:
		print('VisuAnimation error: mesh or model not found')
		raise FileNotFoundError

	MakeAnimationVideo(
		p_args['moviename'], (
			p_args['patternmap'],
			p_args['dirmap']
		), (
			p_args['patternmodel'],
			p_args['dirmodel']
		),
		frames=p_args['frame'],
		smin=float(p_args['s_min']),
		smax=float(p_args['s_max']),
		movecam=p_args['autocam'],
		startangle=float(p_args['startangle']),
		radius=float(p_args['radius'])
	).run()

def main():
	VisuAnimation(dirmap='../Examples/Animation/',dirmodel='../Examples/Animation/',patternmap='map_*.out',patternmodel='model_*.out',autocam=True,radius=40)

if __name__ == "__main__":
	main()
