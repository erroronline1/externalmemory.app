# -*- coding: utf-8 -*-
import random

class Language():
	# text chunks. extend elements at your convenience
	elements={
		"menuMain": {
			"english": "Scan",
			"deutsch": "Scannen",
		},
		"menuLibrary": {
			"english": "Library",
			"deutsch": "Bibliothek",
		},
		"menuSettings": {
			"english": "Settings",
			"deutsch": "Einstellungen",
		},

		"productCode": {
			"english": "detected code",
			"deutsch": "erkannter Code",
		},
		"productLookup": {
			"english": "lookup with ecosia",
			"deutsch": "mit Ecosia suchen",
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

		"settingLanguageLabel": {
			"english": "language",
			"deutsch": "Sprache",
		},
		"settingClearLocal": {
			"english": "clear local library",
			"deutsch": "lokale Bibliothek löschen",
		},
		"settingClearLocalConfirm": {
			"english": "Are you sure to delete your local library?",
			"deutsch": "Sicher, dass du die lokale Bibliothek löschen willst?",
		},
		"settingConfirmClearLocal":{
			"english": "yes, clear library",
			"deutsch": "ja, Bibliothek löschen",
		},
		"settingExportLocal": {
			"english": "export database",
			"deutsch": "Datenbank exportieren",
		},
		"settingExportLocalConfirm": {
			"english": "Overwrite possible former export?",
			"deutsch": "Möglicherweise bestehenden früheren Export überschreiben?",
		},
		"settingConfirmExportLocal":{
			"english": "yes, export database",
			"deutsch": "ja, Datenbank exportieren",
		},
		"settingImportLocal": {
			"english": "import database",
			"deutsch": "Datenbank importieren",
		},
		"settingImportLocalConfirm": {
			"english": "Overwrite current database?",
			"deutsch": "Aktuelle Datenbank überschreiben?",
		},
		"settingConfirmImportLocal":{
			"english": "yes, import database",
			"deutsch": "ja, Datenbank importieren",
		},
		"settingImportLocalSelectDirectory":{
			"english": "Select directory with database backup",
			"deutsch": "Verzeichnis mit Datenbank-Sicherung wählen",
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

Your data is stored on your device only by default. You can delete, export and restore it to and from the local shared storage.
""",
			"deutsch": """
Bei Schwierigkeiten sich Marken zu merken hilft diese App durch das Speichern deiner persönlichen Bewertungen für das jeweilige Produkt.
Scanne den Barcode und bewerte das Produkt. Wenn dir ein Produkt über den Weg läuft und du nicht mehr weißt, ob du es mochtest, scanne einefach den Barcode.
Du kannst deine eigenen Notizen hinzufügen und deine Meinung jederzeit ändern!

Deine Daten werden standardmäßig nur auf deinem Gerät gespeichert. Du kannst sie löschen, auf den geteilten Speicher des Geräts exportieren oder von dort wieder herstellen.
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
