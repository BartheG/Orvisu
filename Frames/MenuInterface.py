import wx
import wx.adv
from Frames.__impvisugui__ import *

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

	def genBtn(self,):
		self.addToLayout([
			wx.Button(self.m_frame,-1,'3D Animated Plot',name='btn_animation'),
			wx.Button(self.m_frame,-1,'3D Plot/Sliced Plot',name='btn_visusd'),
			wx.Button(self.m_frame,-1,'Close',name='close')
		],'grp_btn')

	def run(self):
		self.genBtn()
		return self.layout

"""

VisuFrame: Frame providing fields to setup and run Menu.

"""

class VisuFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title='Orvisu - Menu',)
		self.m_sizer = wx.BoxSizer(wx.VERTICAL)

	def addToLayout(self,data):
		[self.m_sizer.Add(toadd,0,wx.ALL|wx.EXPAND,5,userData=key) for key,i in data.items() for toadd in i]

	def bindFiels(self):
		self.globalHandler=mHandler()
		self.l_child={ i.GetName():i for i in self.GetChildren() }
		self.Bind(wx.EVT_CLOSE, self.globalHandler.wClose([ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy] ))

		childToBind = {
			'close':(
				wx.EVT_BUTTON,
				self.globalHandler.wClose(
					[ i.Destroy for i in self.otherframe.values() ]+[ self.Destroy]
				)
			),
			'btn_visusd':(
				wx.EVT_BUTTON,
				self.globalHandler.wChangeFrame(
					self,
					'visu'
				)
			),
			'btn_animation':(
				wx.EVT_BUTTON,
				self.globalHandler.wChangeFrame(
					self,
					'anim'
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
		self.SetSize(300,-1)