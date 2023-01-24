# -*- coding: utf-8 -*-
import random

class Language():
	# text chunks. extend elements at your convenience
	elements={
		"productCode": {
			"english": "detected code",
			"deutsch": "erkannter Code",
		},
		"productRateDate": {
			"english": "last rated on",
			"deutsch": "zuletzt bewertet am",
		},
		"productNotes": {
			"english": "my notes",
			"deutsch": "meine Notizen",
		},
		"productRatingGood": {
			"english": "good",
			"deutsch": "gut",
		},
		"productRatingMeh": {
			"english": "meh",
			"deutsch": "solala",
		},
		"productRatingBad": {
			"english": "bad",
			"deutsch": "mies",
		},
		"productSave": {
			"english": "save product",
			"deutsch": "Produkt speichern",
		},

		"libraryClear": {
			"english": "clear local library",
			"deutsch": "lokale Bibliothek löschen",
		},
		"libraryUpload": {
			"english": "save to cloud",
			"deutsch": "in die Cloud speichern",
		},
		"libraryDownload": {
			"english": "retrieve from cloud",
			"deutsch": "aus der Cloud laden",
		},
		"libraryDeleteCloud": {
			"english": "delete from cloud",
			"deutsch": "aus der Cloud löschen",
		},

		"libraryClearLocal": {
			"english": "clear local library",
			"deutsch": "lokale Bibliothek löschen",
		},
		"libraryClearLocalConfirm": {
			"english": "Are you sure to delete your local library?",
			"deutsch": "Sicher, dass du die lokale Bibliothek löschen willst?",
		},
		"librarySynchronizeCloud": {
			"english": "synchronize cloud",
			"deutsch": "Cloud synchronisieren",
		},

		"settingCameraLabel": {
			"english": "camera",
			"deutsch": "Kamera",
		},
		"settingLanguageLabel": {
			"english": "language",
			"deutsch": "Sprache",
		},
		"settingSaveAndApply": {
			"english": "save and apply",
			"deutsch": "speichern und anwenden",
		},
		"settingDevice": {
			"english": "device id",
			"deutsch": "Geräte-ID",
		},
		"settingDeleteCloud": {
			"english": "delete my data from cloud",
			"deutsch": "meine Daten aus der Cloud löschen",
		},
		"settingDeleteCloudConfirm": {
			"english": "Are you sure to delete your data from cloud?",
			"deutsch": "Sicher, dass du deine Daten aus der Cloud löschen willst?",
		},
		"settingConfirmClearLocal":{
			"english": "yes, clear library",
			"deutsch": "ja, Bibliothek löschen",
		},
		"settingConfirmDeleteCloud":{
			"english": "yes, delete from cloud",
			"deutsch": "ja, aus der Cloud löschen",
		},
		"settingDecline":{
			"english": "no",
			"deutsch": "nein",
		},
		"settingInfo":{
			"english": """
When having a hard time to remember brands, this app helps by storing your personal rating for the product. 
Scan the barcode and rate the product. If a product crosses your way and you are unsure if you liked it, just scan the barcode.
You can add your notes and always change your mind!

Your Data
Your data is stored on your device only by default. You can delete it, or store and restore it to and from the webserver manually.

Data Usage
Eventually I try to monetize the data on the webserver by selling it to companies that are honestly interested in opinions on their product. Ratings are anonymous per se unless you provide personal information within the memo intentionally.

© 2023 by error on line 1 (erroronline.one)
made with <3, python, kivy and hardly knowing what i am doing
""",
			"deutsch": """
Bei Schwierigkeiten sich Marken zu merken hilft diese App durch das Speichern deiner persönlichen Bewertungen für das jeweilige Produkt.
Scanne den Barcode und bewerte das Produkt. Wenn dir ein Produkt über den Weg läuft und du nicht mehr weißt, ob du es mochtest, scanne einefach den Barcode.
Du kannst deine eigenen Notizen hinzufügen und deine Meinung jederzeit ändern!

Deine Daten
Deine Daten werden standardmäßig nur auf deinem Gerät gespeichert. Du kannst sie löschen oder auf dem Webserver speichern oder von dort wieder herstellen.

Datennutzung
Irgendwann werde ich vielleicht versuchen die Daten auf dem Webserver zu Geld zu machen indem ich sie an Firmen verkaufe die ehrlich an Meinungen zu ihren Produkten interessiert sind. Die Bewertungen für sich sind immer anonym, es sei denn du gibst in deinen Notizen absichtlich persönliche Daten an. 

© 2023 by error on line 1 (erroronline.one)
made with <3, python, kivy and hardly knowing what i am doing
"""
		},

	}
	def __init__(self, selectedLanguage = None):
		# define selected langauge, defaults to first available language
		self.selectedLanguage = selectedLanguage if selectedLanguage in self.available() else self.available()[0]
	def available(self):
		# tuple of all defined languages for what
		return tuple(key for key in self.elements[random.choice(list(self.elements.keys()))])
	def get(self, chunk):
		# returns requested element for admin
		result = self.elements.get(chunk)
		return result[self.selectedLanguage] if result else "This content snippet has not been declared yet"
