# user interface and default values
def languageSupport():
	return [
			{
				"name": "english",
				"abbrev": "en"
			},
			{
				"name": "deutsch",
				"abbrev": "de"
			},
		]

def language(chunk, lang):
	element={
		"diltDetectedcode":{
			"en": "scan code...",
			"de": "scanne Code..."
		},
		"diltMynotes":{
			"en": "my notes:",
			"de": "meine Notizen:"
		},
		"diltGood":{
			"en": "good",
			"de": "gut"
		},
		"diltMeh":{
			"en": "meh",
			"de": "solala"
		},
		"diltBad":{
			"en": "bad",
			"de": "mies"
		},
		"diltSave":{
			"en": "save",
			"de": "speichern"
		},

		"mydataTitle":{
			"en": "[size=24]My Data[/size]",
			"de": "[size=24]Meine Daten[/size]"
		},
		"mydataDefault":{
			"en": "You have no data stored yet. Your data is stored on your device only by default. You can push and restore it to and from the server manually.",
			"de": "Du hast noch keine Daten gespeichert. Deine Daten werden standardmäßig nur auf deinem Gerät gespeichert. Du kannst sie manuell auf den Server hochladen oder von dort wiederherstellen." 
		},
		"mydataClear":{
			"en": "clear all data from device",
			"de": "alle Daten auf dem Gerät löschen"
		},
		"mydataClearConfirm":{
			"en": "really clear all data from device?",
			"de": "Wirklich alle Daten auf dem Gerät löschen?"
		},
		"mydataPush":{
			"en": "push to server",
			"de": "auf den Server hochladen"
		},
		"mydataRestore":{
			"en": "restore from server",
			"de": "vom Server wiederherstellen"
		},

		"aboutSettings":{
			"en": "[size=24]Settings[/size]",
			"de": "[size=24]Einstellungen[/size]"
		},
		"aboutLanguage":{
			"en": "Language",
			"de": "Sprache"
		},
		"aboutCam":{
			"en": "Camera",
			"de": "Kamera"
		},
		"aboutSettingsApply":{
			"en": "[size=10]please restart app for changes to take effect[/size]",
			"de": "[size=10]App bitte neustarten damit die Änderungen wirksam werden[/size]"
		},		
		"aboutTitle":{
			"en": "[size=24]About[/size]",
			"de": "[size=24]Über die App[/size]"
		},
		"aboutText":{
			"en": """
When having a hard time to remember brands, this app helps by storing your personal rating for the product. 
Scan the barcode and rate the product. If a product crosses your way and you are unsure if you liked it, just scan the barcode.
You can add your notes and always change your mind!

[size=24]Your Data[/size]
Your data is stored on your device only by default. You can delete it, or store and restore it to and from the webserver manually.

[size=24]Data Usage[/size]
Eventually I try to monetize the data on the webserver. Ratings are anonymous per se unless you provide personal information within the memo intentionally.

© 2021 by error on line 1 (erroronline.one)
made with <3, python, kivy and hardly knowing what i am doing
colours from nordtheme
""",
			"de": """
Bei Schwierigkeiten sich Marken zu merken hilft diese App durch Speichern deiner persönlichen Bewertungen für das Produkt.
Scanne den Barcode und bewerte das Produkt. Wenn dir ein Produkt über den Weg läuft und du nicht mehr weißt, ob du es mochtest, scanne einefach den Barcode.
Du kannst deine eigenen Notizen hinzufügen und deine Meinung jederzeit ändern!

[size=24]Deine Daten[/size]
Deine Daten werden standardmäßig nur auf deinem Gerät gespeichert. Du kannst sie löschen oder auf dem Webserver speichern oder von dort wieder herstellen.

[size=24]Datennutzung[/size]
Irgendwann werde ich vielleicht versuchen die Daten auf dem Webserver zu Geld zu machen. Die Bewertungen für sich sind immer anonym, es sei denn du gibst in deinen Notizen absichtlich persönliche Daten an. 

© 2021 by error on line 1 (erroronline.one)
made with <3, python, kivy and hardly knowing what i am doing
colours from nordtheme
"""
		},

		"generalOK":{
			"en": "ok",
			"de": "OK"
		},
		"generalCancel":{
			"en": "cancel",
			"de": "Abbrechen"
		},
	}
	if chunk not in element:
		return "This content snippet has not been declared yet"
	return element[chunk][lang] if lang in element[chunk] else element[chunk]["en"]