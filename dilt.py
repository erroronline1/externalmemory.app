from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from pyzbar import pyzbar

class DiltApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.camupdate, 1.0 / 60)
        ################ basic layout properties
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (.8, 1)
        self.window.pos_hint = {"center_x" : .5, "center_y" : .5}
        
        self.screen = Accordion( orientation ="vertical")

        '''##############'''
        ''' about screen '''
        '''##############'''
        self.infoscreen=AccordionItem(title="About", orientation="vertical")




        self.screen.add_widget(self.infoscreen)

        '''##############'''
        ''' data screen '''
        '''##############'''
        self.datascreen=AccordionItem(title="data", orientation="vertical")



        self.screen.add_widget(self.datascreen)

        '''##############'''
        ''' start screen '''
        '''##############'''
        self.astartscreen=AccordionItem( title="Do I Like That?", orientation="vertical")
        self.startscreen=GridLayout(cols=1)

        ################ cam image dummy
        self.camimg=Image(
            allow_stretch= True,
			keep_ratio= True,
            size_hint = (5,5)
        )
        self.startscreen.add_widget(self.camimg)
        self.detected=Label(
            text="detected code...",
            size_hint = (1,0.5)
        )
        self.startscreen.add_widget(self.detected)

        ################ user inputs on product
        self.startscreen.add_widget(
            Label(
                text = "your notes:",
                size_hint = (1,1)
            )
        )
        self.product = TextInput()
        self.startscreen.add_widget(self.product)

        self.good=ToggleButton(text = "good", group = "opinion")
        self.startscreen.add_widget(self.good)
        self.meh=ToggleButton(text = "meh", group = "opinion")
        self.startscreen.add_widget(self.meh)
        self.bad=ToggleButton(text = "bad", group = "opinion")
        self.startscreen.add_widget(self.bad)

        ################ save input 
        self.save=Button(text = "save")
        self.save.bind(on_press = self.savefn)
        self.startscreen.add_widget(self.save)

        self.astartscreen.add_widget(self.startscreen)
        self.screen.add_widget(self.astartscreen)


        self.window.add_widget(self.screen)
        return self.window

    def savefn(self, event):
        ################ read toggle buttons and translate choice into rating 0-2, note the different order 
        states = [self.bad, self.meh, self.good]
        rating = False
        for el in states:        
            if el.state == "down":
                rating = states.index(el)
        ################ create rating summary
        self.productrating = {
            "code" : self.detected.text,
            "description" : self.product.text,
            "rating" : rating
        }
        print (self.productrating)

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
            self.camimg.texture = image_texture

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            ############### pass result to label
            self.detected.text = barcode.type + " | " + barcode_info
        return frame

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()

if __name__ == '__main__':
    DiltApp().run()