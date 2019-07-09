import wx

import Frames.FrameDomainSlice
import Frames.MenuInterface
import Frames.FrameVisuAnimation
#import Frames.FrameLoading

"""

Cstate: equivalent to C/C++ enum. Defines the actual showed frame.

"""

class CState:
	MENU=1
	VISU=2
	ANIM=3
	OTHER=4

	stringtoenum={
		'menu':MENU,
		'anim':ANIM,
		'visu':VISU,
	}


"""

CoreInterface: initialize all the frames needed for the GUI interface.
Each frame contains the other frames.
Each frame is centred on the screen.

"""

class CoreInterface:
	def __init__(self,):
		self.app=wx.App()

		self.frame_func={
			CState.MENU:Frames.MenuInterface.VisuFrame(),
			CState.VISU:Frames.FrameDomainSlice.VisuFrame(),
			CState.ANIM:Frames.FrameVisuAnimation.VisuFrame(),
			#'loading':Frames.FrameLoading.VisuFrame(),
		}

	def run(self):
		width, height = wx.GetDisplaySize()
		for key,i in self.frame_func.items():
			other_f_tab={ key:oframe for key,oframe in self.frame_func.items() if type(i) != type(oframe) }
			i.run(other_f_tab,CState,)
			i.SetPosition(
				(
					(width/2) - (i.GetSize()[0]/2),
					(height/2) - (i.GetSize()[1]/2)
				)
			)
			if key==CState.MENU:
				i.Show()
		self.app.MainLoop()

def main():
	CoreInterface().run()

if __name__ == "__main__":
	main()