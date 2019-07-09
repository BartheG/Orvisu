import wx
import os

from Frames.__impvisugui__ import *

"""

VisuFrame: Frame providing fields to setup and run Animations of 3D plot.

"""

class VisuFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title='Orvisu - 3D Animated Plot')
		self.m_sizer = wx.BoxSizer(wx.VERTICAL)

	def addToLayout(self,data):
		[self.m_sizer.Add(toadd,0,wx.ALL|wx.EXPAND,5,userData=key) for key,i in data.items() for toadd in i]

	def bindFiels(self):
		self.globalHandler=mHandler()
		self.l_child={ i.GetName():i for i in self.GetChildren() }
		self.Bind(wx.EVT_CLOSE, self.globalHandler.wClose([ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy ] ))

		childToBind={
			'close':(
				wx.EVT_BUTTON,
				self.globalHandler.wClose(
					[ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy ]
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
			'autocam':(
				wx.EVT_CHECKBOX,
				self.globalHandler.wChoice(
					self.l_child,
					self.l_data,
					self.m_sizer,
					'autocam',
					'grp_optautocam'
				)
			)
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
		if not os.path.exists(self.parsed_data['dirmap']):
			return False
		if not os.path.exists(self.parsed_data['dirmodel']):
			return False
		if not '.mp4' in self.parsed_data['moviename']:
			self.parsed_data['moviename']+='.mp4'
		return True

	def run(self,data):
		parsed_data={ key: get(i) for key,i in data.items() for check,get in self.toretrieve.items() if check in dir(i) }
		self.parsed_data=parsed_data
		if self.check()==False:
			return None,None
		return self.parsed_data,VisuAnimation

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
				self.f_utils.getAlignedText('Directory containing map files\t'),
				wx.DirPickerCtrl(self.m_frame,name='dirmap',path='./Examples/Animation/')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Directory containing model files\t'),
				wx.DirPickerCtrl(self.m_frame,name='dirmodel',path='./Examples/Animation/')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Pattern of map files'),
				wx.TextCtrl(self.m_frame,name='patternmap',value='map_*.out')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Pattern of model files'),
				wx.TextCtrl(self.m_frame,name='patternmodel',value='model_*.out')
			),

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
				self.f_utils.getAlignedText('Number of frames\t'),
				wx.Slider(self.m_frame,value=10,minValue=1,maxValue=60,name='frame',style=wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL)
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Name of exported movie\t'),
				wx.TextCtrl(self.m_frame,value='nmovie.mp4',name='moviename')
			),
			self.f_utils.makeTextInputCell(
				self.f_utils.getAlignedText('Auto move cam\t'),
				wx.CheckBox(self.m_frame,name='autocam')
			)
		],'grp_addiparams')

	def genOptAutocam(self,):
		startangle=self.f_utils.makeTextInputCell(
			self.f_utils.getAlignedText('Start angle\t'),
			wx.Slider(self.m_frame,value=0,minValue=0,maxValue=360,name='startangle',style=wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL)
		)
		[ startangle.Hide(i) for i,_ in enumerate(startangle.GetChildren()) ]
		radius=self.f_utils.makeTextInputCell(
			self.f_utils.getAlignedText('Radius\t'),
			wx.TextCtrl(self.m_frame,value='150',name='radius')
		)
		[ radius.Hide(i) for i,_ in enumerate(radius.GetChildren()) ]
		self.addToLayout([startangle,radius],'grp_optautocam')

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
		self.genOptAutocam()
		self.genBtn()
		return self.layout
