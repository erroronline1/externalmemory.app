# -*- coding: utf-8 -*-
__version__ = "1.0"

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.animation import Animation

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.uix.camera import Camera

import os
import re
import webbrowser
from datetime import datetime

from language import Language
from platformhandler import platform_handler
import database

os.environ["KIVY_ORIENTATION"] = "Portrait"

class IconListItem(OneLineIconListItem):
	icon = StringProperty()

class CamImage(Camera):
	pass

class ContentNavigationDrawer(MDBoxLayout):
	screen_manager = ObjectProperty()
	nav_drawer = ObjectProperty()
	camImage = ObjectProperty()
	toolbar = ObjectProperty()

class ExternalMemoryApp(MDApp): # <- main class
	dialog = None
	currentRating = 2
	dbname = "ExternalMemory.app.db"
	selected = None
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.platform = platform_handler()
		self.database = database.DataBase(os.path.join( self.platform.app_dir, self.dbname))
		lang = self.database.read(["VALUE"], "SETTING", {"KEY": "lang"})
		self.text = Language(lang[0][0] if lang else None)
		
		self.screen = Builder.load_file("layout.kv")
		if self.platform.window_size:
			Window.size = self.platform.window_size

	def on_pause(self):
		self.screen.ids["camImage"].play = False
		return True
	def on_resume(self):
		self.screen.ids["camImage"].play = True
		return True

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.icon = r'assets/app_icon.png'
		dropdown_options = self.dropdown_options()
		self.settingLanguageDropdown = self.dropdown_generator(dropdown_options["languageSetting"])

		self.platform.imgframe = self.screen.ids["camImage"]
		self.platform.stringdestination = self.screen.ids["productCode"]
		self.platform.prefill_inputs = self.prefill_inputs
		self.platform.adjustCamera()

		Clock.schedule_interval(self.platform.imageProcessing, 1.0 / 10)
		return self.screen

	def dropdown_options(self):
		return {
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
				text = msg
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
		self.dialog = None
		if btnObj[0].text ==  self.text.get("settingConfirmClearLocal"):
			self.database.clear(["DATA"])
			self.screen.ids["libraryLocal"].text = ""
		if btnObj[0].text ==  self.text.get("settingConfirmExportLocal"):
			success = self.platform.file.copy_to_shared(
				os.path.join(self.platform.app_dir, self.dbname),
				collection = None,
				filepath = self.platform.export_path(self.dbname))
			self.notif(f"{success}")
		if btnObj[0].text ==  self.text.get("settingConfirmImportLocal"):
			self.platform.chooser.choose_content('*/*')

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
		rating = ["productRatingBad", "productRatingMeh", "productRatingGood"]
		self.screen.ids["libraryLocal"].clear_widgets()
		if library:
			for item in library:
				self.screen.ids["libraryLocal"].add_widget(
					MDLabel(
						text = f"{item[0]}: {item[1]} - {self.text.elements[rating[item[3]]][self.text.selectedLanguage]}\n{item[2]}",
						size_hint = (.9, None ),
						adaptive_height = True,
					)
				)

	def set_selection_mode(self, instance_selection_list, mode):
		if mode:
			md_bg_color = self.theme_cls.primary_light
			left_action_items = [
				[
					"close",
					lambda x: self.root.ids.libraryLocal.unselected_all(),
				]
			]
			right_action_items = [["search-web", lambda x: self.lookup_library_items()], ["trash-can-outline", lambda x: self.delete_and_update_library()]]
		else:
			md_bg_color = self.theme_cls.primary_color
			left_action_items = []
			right_action_items = [["search-web", lambda x: self.lookup_library_items()], ['dots-vertical', lambda x: self.root.ids.nav_drawer.set_state("open")]]
			self.root.ids.toolbar.title = self.text.get("menuLibrary")
			self.selected = None

		Animation(md_bg_color=md_bg_color, d=0.2).start(self.root.ids.toolbar)
		self.root.ids.toolbar.left_action_items = left_action_items
		self.root.ids.toolbar.right_action_items = right_action_items

	def on_selected(self, instance_selection_list, instance_selection_item):
		self.root.ids.toolbar.title = str(len(instance_selection_list.get_selected_list_items()))
		self.selected=[re.findall(r"^([^\n\r]+?)(?:: \d{4}\-\d{2}\-\d{2} \- .+?)$", item.instance_item.text, re.MULTILINE)[0] for item in instance_selection_list.get_selected_list_items()]

	def on_unselected(self, instance_selection_list, instance_selection_item):
		if instance_selection_list.get_selected_list_items():
			self.root.ids.toolbar.title = str(len(instance_selection_list.get_selected_list_items()))
			self.selected=[re.findall(r"^([^\n\r]+?)(?:: \d{4}\-\d{2}\-\d{2} \- .+?)$", item.instance_item.text, re.MULTILINE)[0] for item in instance_selection_list.get_selected_list_items()]
		
	def delete_and_update_library(self):
		if self.selected:
			for entry in self.selected:
				self.database.delete("DATA", {"id": entry})
			self.display_library()

	def lookup_library_items(self):
		search = ""
		if self.selected:
			for entry in self.selected:
				search += re.findall(r"^.+?\| ([^\n\r]+?)$", entry, re.MULTILINE)[0] + " "
		elif self.platform.found_barcode:
			search = self.platform.found_barcode
		if search:
			self.weblink(f"https://ecosia.org/search?q={search}")

	def weblink(self, url):
		webbrowser.open(url)

if __name__ == "__main__":
	ExternalMemoryApp().run()
