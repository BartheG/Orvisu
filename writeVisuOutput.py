import numpy

class WriteVisuOutput:
	def __init__(self):
		self.choice_read = {
			'ubc':self.writeUBC,
		}

	#Transforms numpy array to model files following 'ubc' format
	def writeUBC(self):
		if len(self.data.shape) != 3:
			return False
		n_data = numpy.flip(self.data.ravel())
		with open(self.filename, mode='wt', encoding='utf-8') as myfile:
			if self.bedrock:
				myfile.write('\n'.join(str(line).replace('-100.0','nan') for line in n_data))
			else:
				myfile.write('\n'.join(str(line).replace('-100.0','nan').replace('100.0','nan') for line in n_data))
		return True

	#Calls 'outFormat' method to write model file
	#toWrite: numpy array, array to transform
	#outFormat: 'ubc'
	#filename: str, prefix of the model and map output files
	def run(self,toWrite,outFormat,filename,bedrock=False):
		if outFormat in self.choice_read.keys() and len(toWrite.shape)==3:
			self.data = toWrite
			self.filename = filename+'_model.out'
			self.bedrock = bedrock
			self.draw_magage(
				filename+'_mesh.out',
				self.data.shape[0],
				self.data.shape[1],
				self.data.shape[2]
			)
			print('Write complete...') if self.choice_read[outFormat]() else print('Error on data')
		else:
			print('Write format not recognized...')

	#Draw map file following 'ubc' format
	#filename: name of output file
	#x,y,z: dimension of array
	def draw_magage(self,filename,x,y,z):
		file = open(filename,'w')
		file.write(str(x)+' '+str(y)+' '+str(z)+'\n')
		file.write('1 1 1\n')
		xlist = ' '.join('{}'.format('1') for k in range(x))
		ylist = ' '.join('{}'.format('1') for k in range(y))
		zlist = ' '.join('{}'.format('1') for k in range(z))
		file.write(xlist+'\n'+ylist+'\n'+zlist)
		file.close()
		print('Write of mapage...')

#Main to test
def main():
	data = numpy.linspace(1,80,60*60*60)
	data = data.reshape((
		60,60,60
	))

	w = WriteVisuOutput()
	w.run(data,'ubc','./test')

if __name__ == '__main__':
	main()