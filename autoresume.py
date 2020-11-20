import xbmc
import time, os

class Main:
	def __init__(self):
		self.xmlfile = os.getcwd().replace(";","")+"\\data.xml"
		self.maximum_pls_size = 200
		self.player = xbmc.Player()
		
		if os.path.exists(self.xmlfile):
			self.resume_playback()
		elif not os.path.exists(self.xmlfile):
			if self.player.isPlayingAudio():
				self.save_playlist()
			elif not self.player.isPlayingAudio():
				self.play_random()
	def fade_in_music(self):
		volume = 50
		while volume < 100:
			volume += 2.5
			xbmc.executebuiltin("XBMC.SetVolume("+str(volume)+")")
			time.sleep(.085)
	def fade_out_music(self):
		volume = 100
		while volume > 50:
			volume -= 2.5
			xbmc.executebuiltin("XBMC.SetVolume("+str(volume)+")")
			time.sleep(.085)#seconds
	def activate_visualizations(self):
		vis_window_id = 12006
		xbmc.executebuiltin("xbmc.activatewindow("+str(vis_window_id)+")")
	def play_random(self):
		time.sleep(3)#Allow the startup sound to finsh playing.
		xbmc.executebuiltin("XBMC.SetVolume(50)")
		
		pls = xbmc.PlayList(0)
		pls.load("Q:\\UserData\\playlists\\music\\All.m3u")
		pls.shuffle()
		self.player.play(pls)
		
		self.fade_in_music()
		self.activate_visualizations()
	def save_playlist(self):
		self.time = self.player.getTime()
		self.plist = xbmc.PlayList(0)
		self.plsize = self.plist.size()
		if self.plsize > self.maximum_pls_size:#XBMC chokes on large playlists, this limits the # of entries to be safe
			self.plsize = self.maximum_pls_size
		self.place = self.plist.getposition()
		self.playing = self.player.getPlayingFile()
		
		f = open(self.xmlfile, "wb")
		f.write("<data>\n")
		f.write("\t<time>"+str(self.time)+"</time>\n")
		f.write("\t<plspos>"+str(self.place)+"</plspos>\n")
		if self.plsize != "-":
			for i in range (0 , self.plsize): 
				f.write("\t<plistfile>"+str(xbmc.PlayListItem.getfilename(self.plist[i]))+"</plistfile>\n")
		f.write("\t<playing>"+str(self.playing)+"</playing>\n")
		f.write("</data>\n")
		f.close()
		
		self.fade_out_music()
		self.player.stop()
		xbmc.executebuiltin("XBMC.SetVolume(100)")
		xbmc.shutdown()
	def resume_playback(self):
		time.sleep(3.5)#Allow the startup sound to finsh playing.
		xbmc.executebuiltin("XBMC.SetVolume(50)")
		
		self.plist = xbmc.PlayList(0)
		self.plist.clear()
		
		fh = open(self.xmlfile)
		for line in fh.readlines():
			theLine = line.strip()
			if theLine.count("<time>") > 0:
				self.time = theLine[6:-7]
				if self.time == "-":
					self.time = False
				else:
					self.time = float(self.time)
			if theLine.count("<plspos>") > 0:
				self.place = theLine[8:-9]
				if self.place == "-":
					self.place = False
				else:
					self.place = int(self.place)
			if theLine.count("<playing>") > 0:
				self.playing = theLine[9:-10]
				if self.playing == "-":
					self.playing = False
			if theLine.startswith("<plistfile"):
				self.plist.add(theLine.split(">")[1].split("<")[0])
		
		fh.close()
		
		
		self.player.play(self.plist)
		self.player.playselected(self.place)
		self.player.seekTime(self.time)
		
		self.fade_in_music()
		self.activate_visualizations()
		os.remove(self.xmlfile)
	
if __name__ == '__main__':
    Main()