# -*- coding: utf-8 -*-
from kivy import platform
from kivy.graphics.texture import Texture
from pathlib import Path
import os
import plyer

import numpy
from PIL import Image
import cv2
from pyzbar import pyzbar

class platform_handler():
	window_size = (450, 750)
	app_dir = os.path.dirname(__file__)
	device = plyer.uniqueid.id
	imgframe = None
	stringdestination = None
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
	
	def imageProcessing(self, *args):
		detectedCode = None
		texture = self.imgframe.texture
		size = texture.size
		pixels = texture.pixels
		pil_image = Image.frombytes(mode='RGBA', size=size, data=pixels)
		numpypicture = numpy.array(pil_image)
		if numpypicture.any():
			barcodes = pyzbar.decode(numpypicture)
			for barcode in barcodes:
				detectedCode = barcode.type + " | " + barcode.data.decode('utf-8')
			############### pass result to label
			if self.stringdestination and detectedCode:
				self.stringdestination.text = detectedCode
				self.prefill_inputs(detectedCode)

