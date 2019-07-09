import wx

from Frames.__impvisugui__ import *

class VisuFrame(wx.Frame):
	def __init__(self):
		super().__init__(None,title='Orvisu - Loading...')
		self.m_sizer=wx.BoxSizer(wx.VERTICAL)

	def addToLayout(self,data):
		[self.m_sizer.Add(toadd,0,wx.ALL|wx.EXPAND,5,userData=key) for key,i in data.items() for toadd in i]

	def run(self,otherframe,CState):
		self.otherframe=otherframe
		self.CState=CState
		self.l_data=GenOneFileVisuFrame(self).run()
		self.addToLayout(self.l_data)
		self.SetSizerAndFit(self.m_sizer)


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

	def genAnim(self,):
		self.addToLayout([
			self.f_utils.makeLoadingAnimation()
		],'grp_anim')

	def run(self):
		self.genAnim()
		return self.layout