# -*- coding: utf-8 -*-
from kivy import platform
from kivy.metrics import dp
from pathlib import Path
import os
import shutil

import numpy
from PIL import Image
from pyzbar import pyzbar

class WinShared():
	#mimics androidstorage4kivy SharedStorage to just have one super handling method for files
	def copy_to_shared(self, private_file, collection = None, filepath = None):
		#returns shared_file or None
		shutil.copyfile(private_file, filepath)
		return filepath

	def copy_from_shared(self, shared_file):
		#returns private_file or None
		filename = os.path.split(shared_file)[1]
		destination = os.path.join(os.path.dirname(__file__), filename)
		shutil.copyfile(shared_file, destination)
		return destination

	def delete_shared(self, shared_file):
		#returns True if deleted, else False
		pass 

class WinChooser():
	#mimics androidstorage4kivy Chooser to just have one super handling method for files
	def __init__(self, callback):
		from tkinter import Tk, filedialog
		self.tkinter = Tk
		self.filedialog = filedialog
		self.callback = callback

	def choose_content(self, filetypes):
		picker = self.tkinter()
		picker.attributes("-topmost", True)
		path = self.filedialog.askopenfilename()
		picker.destroy()
		self.callback([path])

class platform_handler():
	imgframe = None
	stringdestination = None
	def __init__(self):
		if platform=="android":
			from android.permissions import Permission, request_permissions, check_permission
			from android.storage import app_storage_path, primary_external_storage_path
			from androidstorage4kivy import SharedStorage, Chooser
			perms = [Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
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
			self.shared_dir = primary_external_storage_path()
			self.file = SharedStorage()
			self.chooser = Chooser(self.chooser_callback)
		else:
			self.window_size = (450, 750)
			self.app_dir = os.path.dirname(__file__)
			self.shared_dir = os.path.join(str(Path.home()), "Documents")
			self.file = WinShared()
			self.chooser = WinChooser(self.chooser_callback)
	
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

	def adjustCamera(self):
		if platform != "android":
			return
		self.imgframe.angle = -90
		self.imgframe.parent.padding = dp(20)

	def chooser_callback(self, shared_file_list):
		for shared_file in shared_file_list:
			imported = self.file.copy_from_shared(shared_file)
			try:
				shutil.copy(imported, self.app_dir)
			except:
				pass

	def export_path(self, file):
		if platform=="android":
			return file
		return os.path.join(self.platform.shared_dir, self.dbname) if self.platform.shared_dir else self.dbname