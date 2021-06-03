from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, Property
import cv2
from pyzbar import pyzbar

from diltlang import language

class Screen(Widget):
	camimage = ObjectProperty(None)
	detectedcode = ObjectProperty(None)
	mynotes = ObjectProperty(None)
	good = ObjectProperty(None)
	meh = ObjectProperty(None)
	bad = ObjectProperty(None)

	mydata = ObjectProperty(None)

	def content(self, element, **kwargs):
		if len(kwargs):
			for arg in kwargs:
				# conditional property check because dynamic assignment subscritaple type error
				if arg=='text':
					self.ids[element].text = kwargs[arg]
				elif arg=='texture':
					self.ids[element].texture = kwargs[arg]
		lang = "en"
		return language(element, lang)
	
	def savefn(self):
		################ read toggle buttons and translate choice into rating 0-2, note the different order 
		states = [self.ids.bad, self.ids.meh, self.ids.good]
		rating = False
		for el in states:        
			if el.state == "down":
				rating = states.index(el)
		################ create rating summary
		self.productrating = {
			"code" : self.ids.detectedcode.text,
			"description" : self.ids.mynotes.text,
			"rating" : rating
		}
		print (self.productrating)


class DiltApp(App): # <- Main Class
	def build(self):
		self.capture = cv2.VideoCapture(0)
		Clock.schedule_interval(self.camupdate, 1.0 / 60)
		self.Screen=Screen()
		return self.Screen

	def camupdate(self, dt):
		ret, frame = self.capture.read()
		if ret:
			frame = self.read_barcodes(frame)
			################ convert it to texture
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tostring()
			image_texture = Texture.create(
				size = (frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
			image_texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
			################ display image from the texture
			self.Screen.content('camimage', texture = image_texture)

	def read_barcodes(self, frame):
		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			x, y , w, h = barcode.rect
			barcode_info = barcode.data.decode('utf-8')
			cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
			############### pass result to label
			self.Screen.content('detectedcode', text = barcode.type + " | " + barcode_info)
		return frame

	def on_stop(self):
		#without this, app will not exit even if the window is closed
		self.capture.release()

if __name__ == "__main__":
	DiltApp().run()
