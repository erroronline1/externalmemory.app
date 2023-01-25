# -*- coding: utf-8 -*-
__version__ = "1.0"

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.camera import Camera

import os
from datetime import datetime

from language import Language
from platformhandler import platform_handler
import database

class IconListItem(OneLineIconListItem):
	icon = StringProperty()

class CamImage(Camera):
	pass

class ExternalMemoryApp(MDApp): # <- main class
	dialog = None
	currentRating = 2

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.platform = platform_handler()
		self.database = database.DataBase(os.path.join( self.platform.app_dir, "ExternalMemory.app.db"))
		lang = self.database.read(["VALUE"], "SETTING", {"KEY": "lang"})
		self.text = Language(lang[0][0] if lang else None)
		
		self.screen = Builder.load_file("layout.kv")
		if self.platform.window_size:
			Window.size = self.platform.window_size

	def build(self):
		#self.icon = r'assets/app_icon.png'
		dropdown_options = self.dropdown_options()
		self.settingCameraDropdown = self.dropdown_generator(dropdown_options["cameraSetting"])
		self.settingLanguageDropdown = self.dropdown_generator(dropdown_options["languageSetting"])

		cam = self.database.read(["VALUE"], "SETTING", {"KEY": "cam"})
		self.screen.ids.camImage.index = int(cam[0][0] if cam else 1) - 1
		self.platform.imgframe = self.screen.ids["camImage"]
		self.platform.stringdestination = self.screen.ids["productCode"]
		self.platform.prefill_inputs = self.prefill_inputs
		self.platform.adjustCamera()

		Clock.schedule_interval(self.platform.imageProcessing, 1.0 / 10)
		return self.screen

	def dropdown_options(self):
		return {
			"cameraSetting":{
				"options": [{"icon": "camera-outline", "option": str(cam + 1)} for cam in range(2)],
				"fields": ["settingCameraSelection"],
				"context": "settingCameraDropdown"
			},
			"languageSetting":{
				"options": [{"icon": "translate", "option": lang} for lang in self.text.available()],
				"fields": ["settingLanguageSelection"],
				"context": "settingLanguageDropdown"
			},
		}

	def dropdown_generator(self, parameter):
		items = [
			{
				"text": self.text.get(i["content"]) if "content" in i else i["option"],
				"content": i.get("content"),
				"height": dp(64),
				"viewclass": "IconListItem" if "icon" in i else None,
				"icon": i.get("icon")
			} for i in parameter["options"]
		]
		return {
			field: MDDropdownMenu(
					caller = self.screen.ids[field],
					items = [dict(i,
						**{"on_release": lambda x = (field, i["text"], parameter["context"]): self.select_dropdown_item(x[0], x[1], x[2])}
						) for i in items],
					position = "center",
					width_mult = 4
			) for field in parameter["fields"]
		}

	def select_dropdown_item(self, field, text, context):
		self.screen.ids[field].text = text
		con_text = getattr(self, context)
		con_text[field].dismiss()

	def notif(self, msg, display_delayed = 0):
		def sb(this):
			Snackbar(
				text = msg,
				snackbar_x = self.layout["left"],
				snackbar_y = self.layout["bottom"],
				size_hint_x = (Window.width - self.layout["left"] - self.layout["right"]) / Window.width,
			).open()
		Clock.schedule_once(sb, display_delayed)

	def cancel_confirm_dialog(self, decision, cancel, confirm):
		if not self.dialog:
			self.dialog = MDDialog(
				text = decision,
				buttons = [
					MDFlatButton(
						text = cancel,
						on_release = self.cancel_confirm_dialog_handler
					),
					MDFlatButton(
						text = confirm,
						on_release = self.cancel_confirm_dialog_handler
					),
				],
			)
		self.dialog.open()

	def cancel_confirm_dialog_handler(self, *btnObj):
		self.dialog.dismiss()
		if btnObj[0].text ==  self.text.get("settingConfirmClearLocal"):
			self.database.clear(["DATA"])
			self.screen.ids["libraryLocal"].text = ""
		if btnObj[0].text ==  self.text.get("settingConfirmDeleteCloud"):
			pass
			#self.screen.ids["libraryLocal"].text = ""
			#self.notif(self.text.admin("resetMessage"))

	def translate(self, lang):
		self.text.selectedLanguage = lang
		for element in self.text.elements:
			try:
				# not all language chunks have their respective id'd counterparts like
				# * dropdown-objects
				obj = self.screen.ids[element]
				if hasattr(obj, "hint_text") and obj.hint_text:
					obj.hint_text = self.text.elements[element][lang]
					continue
				elif hasattr(obj, "text") and obj.text:
					obj.text = self.text.elements[element][lang]
			except:
				continue

	def save_setting(self, key, value):
		sanitize={
			"default": lambda x: int(x),
			"lang": lambda x: x.strip(),
		}
		try:
			if key in sanitize:
				value=sanitize[key](value)
			else:
				value=sanitize["default"](value)
		except Exception as e:
			value=""
		if value in ("", "NULL"):
			self.database.delete("SETTING", {"KEY": key})
		else:
			self.database.write("SETTING", {"KEY": key, "VALUE": value}, {"KEY": key})
		return str(value)

	def set_current_rating(self, *args) -> None:
		rating = None
		selected = args[1].text
		for i, option in enumerate(["productRatingBad", "productRatingMeh", "productRatingGood"]):
			if selected == self.text.elements[option][self.text.selectedLanguage]:
				rating = i
				break
		self.currentRating = (rating)

	def save_inputs(self):
		productCode = self.screen.ids["productCode"].text
		if "|" in productCode and len(productCode[productCode.index("|")+1:]):
			key_value = {
				"ID": productCode,
				"DATE": datetime.now().strftime("%Y-%m-%d"),
				"MEMO": self.screen.ids["productNotes"].text if self.screen.ids["productNotes"].text else "NULL",
				"RATING": self.currentRating
				}
			self.session = self.database.write("DATA", key_value, {"ID": productCode})
		else:
			self.notif(self.text.get("missingRateNotif"))

	def prefill_inputs(self, productCode):
		# this is to be passed to the platformhandler and executed if something like a code is recognized
		known = self.database.read(["*"], "DATA", {"ID": productCode})
		if not known:
			self.screen.ids["productNotes"].text = ""
			self.screen.ids["productRateDate"].text = ""
			return
		self.screen.ids["productNotes"].text = known[0][2] if known[0][2] else ""
		self.screen.ids["productRateDate"].text = known[0][1] if known[0][1] else ""

		rating = self.screen.ids["productRating"]
		segment = rating.ids.segment_panel.children[known[0][3] * 2]
		if rating.current_active_segment != segment:
			rating.animation_segment_switch(segment)
			rating.current_active_segment = segment
			rating.dispatch("on_active", segment)

	def display_library(self):
			library = self.database.read(["*"], "DATA")
			output = "\n"
			rating = ["productRatingBad", "productRatingMeh", "productRatingGood"]
			if library:
				for item in library:
					output += f"{item[0]}: {item[1]} - {self.text.elements[rating[item[3]]][self.text.selectedLanguage]}\n{item[2]}\n\n"
			return output
		

if __name__ == "__main__":
	ExternalMemoryApp().run()
