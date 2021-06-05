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
			"en": "My Data",
			"de": "Meine Daten"
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
			"en": "Settings",
			"de": "Einstellungen"
		},
		"aboutLanguage":{
			"en": "Language",
			"de": "Sprache"
		},
		"aboutCam":{
			"en": "Camera",
			"de": "Kamera"
		},
		"aboutTitle":{
			"en": "About",
			"de": "Über die App"
		},
		"aboutText":{
			"en": "this app is awesome!",
			"de": "ganz tolle App!"
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