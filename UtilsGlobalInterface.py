import wx
import wx.adv

"""

'CreateFrameUtils': provides methods to place and format elements on the wxpython Frame.

verticalTextAlign: apply specified margin-top to data
return type: BoxSizer

makeTextInputCell: make horizontally box with 'left_data' at the left and 'right_data' expanded at the right
return type: BoxSizer

getAlignedText: Create static text with data as text and align it
return type: BoxSizer

makeCheckboxInput: Create a horizontal cell of checkboxes from names and labels passed trought parameters
return type: BoxSizer

"""

class CreateFrameUtils:
	def __init__(self,m_frame):
		self.m_frame=m_frame

	def verticalTextAlign(self,data,margin_top=(0,2)):
		v_box=wx.BoxSizer(wx.VERTICAL)
		padding_top=wx.StaticText(self.m_frame, -1, "",size=margin_top)
		v_box.Add(padding_top,0,wx.EXPAND,0)
		v_box.Add(data,0,wx.EXPAND,0)
		return v_box

	def makeTextInputCell(self,left_data,right_data):
		h_box=wx.BoxSizer(wx.HORIZONTAL)
		h_box.Add(left_data,0,wx.ALL,5)
		h_box.Add(right_data,proportion=1)
		return h_box

	def getAlignedText(self,data,margin=(0,2)):
		return self.verticalTextAlign(
			wx.StaticText(
				self.m_frame,
				-1,
				data
			),
			margin_top=margin
		)

	def makeCheckboxInput(self,label,name,padding=True):
		h_box=wx.BoxSizer(wx.HORIZONTAL)
		if padding:
			h_box.Add(wx.StaticText(self.m_frame, -1, '',),wx.RIGHT)
		[ h_box.Add(wx.CheckBox(self.m_frame,label=it_label,name=it_name),wx.RIGHT) for it_name,it_label in zip(name,label)]
		return h_box

	#Unused
	def makeLoadingAnimation(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		anim = wx.adv.Animation('./Ressources/loadinganimation.gif')
		ctrl = wx.adv.AnimationCtrl(self.m_frame, -1, anim)
		ctrl.Play()
		sizer.Add(ctrl)
		sizer.Hide(0)
		return sizer

"""

'mHandler': handle every frame events
every returns are functions catching the events.

wClose: run through data and execute each element as a function

wSubmit: data is a list to parse with parsingtool class. A function retrieved with parsing of data is executed

wChoice: Show and Hide panels depending on selection lists or checkboxes

wChangeFrame: Hide 'oldframe' and Show new frame

"""

class mHandler:
	def wClose(self,data):
		def OnClick(event):
			[ i() for i in data ]
		return OnClick

	def wSubmit(self,data,parsingtool):
		def OnClick(event):
			dataforplot,visufunc=parsingtool(data)
			if dataforplot==None or visufunc==None:
				return
			try:
				visufunc(**dataforplot)
			except:
				print('Error with parameters')
		return OnClick

	def wChoice(self,data,layout_data,p_sizer,thechoice,grp_data,whichbind=1):
		toretrieve={ 'GetSelection':lambda x: x.GetSelection(), 'GetValue':lambda x: x.GetValue() }
		def OnClick(event):
			toexec=[ i(data[thechoice]) for key,i in toretrieve.items() if key in dir(data[thechoice]) ]
			if toexec[0] != whichbind:
				for i in layout_data[grp_data]:
					for it,_ in enumerate(i.GetChildren()):
						i.Hide(it)
			else:
				for i in layout_data[grp_data]:
					for it,_ in enumerate(i.GetChildren()):
						i.Show(it)
			p_sizer.Fit(p_sizer.GetContainingWindow())
		return OnClick

	def wChangeFrame(self,oldframe,nstate):
		def OnClick(event):
			oldframe.Hide()
			oldframe.otherframe[oldframe.CState.stringtoenum[nstate]].Show()
		return OnClick