# user interface and default values
def language(chunk, lang):
	element={
		"diltTitle":{
			"en": "Do I Like That?",
			"de": "Mag ich das?"
		},
		"diltDetectedcode":{
			"en": "detected code...",
			"de": "erkannter Code..."
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
			"en": "Your data is stored on your device only by default. You can push and restore it to and from the cloud manually.",
			"de": "Deine Daten werden standardmäßig nur auf deinem Gerät gespeichert. Du kannst sie manuell in die Cloud hochladen oder von dort wiederherstellen." 
		},
		"mydataClear":{
			"en": "clear all data from device",
			"de": "alle Daten auf dem Gerät löschen"
		},
		"mydataPush":{
			"en": "push",
			"de": "hochladen"
		},
		"mydataRestore":{
			"en": "restore",
			"de": "wiederherstellen"
		},

		"aboutTitle":{
			"en": "About",
			"de": "Über die App"
		},
		"aboutText":{
			"en": "this app is awesome!",
			"de": "ganz tolle App!"
		}
	}
	if chunk not in element:
		return "This content snippet has not been declared yet"
	return element[chunk][lang] if lang in element[chunk] else element[chunk]["en"]