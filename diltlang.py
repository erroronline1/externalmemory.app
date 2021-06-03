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
		"mydataPush":{
			"en": "push",
			"de": "hochladen"
		},
		"mydataRestore":{
			"en": "restore",
			"de": "wiederherstellen"
		},

		"aboutTitle":{
			"en": "about",
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