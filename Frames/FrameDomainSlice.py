import wx

from Frames.__impvisugui__ import *

"""

VisuFrame: Frame providing fields to setup and run 3D plot or 3D sliced plot.

"""

class VisuFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title='Orvisu - 3D Plot/Sliced Plot')
		self.m_sizer = wx.BoxSizer(wx.VERTICAL)

	def addToLayout(self,data):
		[self.m_sizer.Add(toadd,0,wx.ALL|wx.EXPAND,5,userData=key) for key,i in data.items() for toadd in i]

	def bindFiels(self):
		self.globalHandler=mHandler()
		self.l_child={ i.GetName():i for i in self.GetChildren() }
		self.Bind(wx.EVT_CLOSE, self.globalHandler.wClose([ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy] ))

		childToBind={
			'close':(
				wx.EVT_BUTTON,
				self.globalHandler.wClose(
					[ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy]
				)
			),
			'submit':(
				wx.EVT_BUTTON,
				self.globalHandler.wSubmit(
					self.l_child,
					FieldSubmitParsing().run,
				)
			),
			'menu':(
				wx.EVT_BUTTON,
				self.globalHandler.wChangeFrame(
					self,
					'menu'
				)
			),
			'visu_type':(
				wx.EVT_CHOICE,
				self.globalHandler.wChoice(
					self.l_child,
					self.l_data,
					self.m_sizer,
					'visu_type',
					'grp_slicesparams'
				)
			),
		}

		for key,i in self.l_child.items():
			if key not in childToBind.keys():
				continue
			i.Bind(childToBind[key][0],childToBind[key][1])

	def run(self,otherframe,CState):
		self.otherframe=otherframe
		self.CState=CState
		self.l_data=GenOneFileVisuFrame(self).run()
		self.addToLayout(self.l_data)
		self.bindFiels()
		self.SetSizerAndFit(self.m_sizer)

"""

FieldSubmitParsing: Used to parse the data retrieved in the frame when the submit button is activated.

"""

class FieldSubmitParsing:
	def __init__(self):
		self.toretrieve={ 'GetValue':lambda x: x.GetValue(), 'GetPath':lambda x: x.GetPath() }
		self.visufunc={ 0:VisuFullDomain,1:VisuSlicesOnDomain }

	def isNum(self,data):
		try:
			float(data)
			return True
		except:
			return False

	def check(self):
		if 's_min' not in self.parsed_data or self.isNum(self.parsed_data['s_min'])==False:
			return False
		if 's_max' not in self.parsed_data or self.isNum(self.parsed_data['s_min'])==False:
			return False
		if self.type_visu not in self.visufunc.keys():
			return False
		return True

	def run(self,data):
		parsed_data={ key: get(i) for key,i in data.items() for check,get in self.toretrieve.items() if check in dir(i) }
		self.parsed_data=parsed_data
		self.type_visu=data['visu_type'].GetSelection()
		if self.check()==False:
			return None,None
		return self.parsed_data,self.visufunc[self.type_visu]

"""

GenOneFileVisuFrame: Generates all the elements of the frame.

"""

class GenOneFileVisuFrame:
	def __init__(self,m_frame):
		self.m_frame=m_frame
		self.f_utils=CreateFrameUtils(self.m_frame)
		self.layout={}

	def addToLayout(self,data,key_grp):
		for i in data:
			if key_grp not in self.layout.keys():
				self.layout[key_grp]=[]
			self.layout[key_grp].append(i)

	def genFilePicker(self):
		self.addToLayout([
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Path of map file\t'),
				wx.FilePickerCtrl(self.m_frame,name='pmap',path='./Examples/Plot/map.out')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Path of model file\t'),
				wx.FilePickerCtrl(self.m_frame,name='mmap',path='./Examples/Plot/model.out')
			)
		],'grp_filepicker')

	def genScale(self,):
		self.addToLayout([
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Scale min\t',(0,1)),
				wx.TextCtrl(self.m_frame,value='4',name='s_min')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Scale max\t',(0,1)),
				wx.TextCtrl(self.m_frame,value='7',name='s_max')
			)
		],'grp_scale')

	def genAddiParams(self,):
		self.addToLayout([
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Colormap\t'),
				wx.TextCtrl(self.m_frame,value='jet',name='c_map')
			)
		],'grp_addiparams')

	def genSlicesParams(self,):
		axists=self.f_utils.makeTextInputCell(
			self.f_utils.getAlignedText('Axis to slice\t'),
			self.f_utils.makeCheckboxInput(['x','y','z'],['axists_x','axists_y','axists_z'])
		)
		[ axists.Hide(i) for i,_ in enumerate(axists.GetChildren()) ]
		nbs=self.f_utils.makeTextInputCell(
			self.f_utils.getAlignedText('Number of slices (1 - 8)\t'),
			wx.Slider(self.m_frame,value=3,minValue=1,maxValue=8,name='nbslices',style=wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL)
		)
		[ nbs.Hide(i) for i,_ in enumerate(nbs.GetChildren()) ]
		self.addToLayout([
			axists,nbs
		],'grp_slicesparams')

	def genChoiceVisu(self,):
		self.addToLayout([
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Type of visualization\t'),
				wx.Choice(self.m_frame,choices=['Full domain','3D Slices',],name='visu_type')
			),
		],'grp_choicevisu')

	def genBtn(self,):
		self.addToLayout([
			wx.Button(self.m_frame,-1,'Submit',name='submit'),
			wx.Button(self.m_frame,-1,'Close',name='close'),
		],'grp_btn')

	def genMenuBtn(self,):
		self.addToLayout([ wx.Button(self.m_frame,-1,'Menu',name='menu') ],'grp_menu')

	def run(self,):
		self.genMenuBtn()
		self.genFilePicker()
		self.genScale()
		self.genAddiParams()
		self.genChoiceVisu()
		self.genSlicesParams()
		self.genBtn()
		return self.layout
