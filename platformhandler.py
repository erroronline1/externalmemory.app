# -*- coding: utf-8 -*-
from kivy import platform
from kivy.graphics.texture import Texture
from pathlib import Path
import os
import plyer

import cv2
from pyzbar import pyzbar

class platform_handler():
	window_size = (450, 800)
	app_dir = os.path.dirname(__file__)
	device = plyer.uniqueid.id
	imgdestination = None
	stringdestination = None
	selectedCamera = 1
	videocapture = None
	def __init__(self):
		if platform=="android":
			from android.permissions import Permission, request_permissions, check_permission
			from android.storage import app_storage_path
			perms = [Permission.CAMERA, Permission.INTERNET]
			def check_permissions(perms):
				for perm in perms:
					if check_permission(perm) != True:
						return False
				return True
			if check_permissions(perms)!= True:
				request_permissions(perms)	# get android permissions     
				#exit()						# app has to be restarted; permissions will work on 2nd start		
			
			self.window_size = None
			self.app_dir = app_storage_path()

	def init_capture(self):
		self.videocapture = cv2.VideoCapture(self.selectedCamera - 1)

	def process_camera_image(self, *args):
		if not self.videocapture:
			self.init_capture()
		ret, frame = self.videocapture.read()
		detectedCode = None
		if ret:
			barcodes = pyzbar.decode(frame)
			for barcode in barcodes:
				x, y , w, h = barcode.rect
				barcode_info = barcode.data.decode('utf-8')
				cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
				############### pass result to label
				detectedCode = barcode.type + " | " + barcode_info
			################ convert img to texture
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tobytes()
			image_texture = Texture.create(
				size = (frame.shape[1], frame.shape[0]), colorfmt='bgr')
			image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
			################ display image from the texture
			if self.imgdestination and image_texture:
				self.imgdestination.texture = image_texture
			if self.stringdestination and detectedCode:
				self.stringdestination.text = detectedCode
				self.prefill_inputs(detectedCode)
