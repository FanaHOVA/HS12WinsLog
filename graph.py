import json, pprint, matplotlib

f = open("database.json", "r+")
data = json.load(f)

classes = ["Mage", "Hunter", "Warrior", "Paladin", "Priest", "Shaman", "Druid", "Rogue", "Miracle", "Zoolock", "Handlock"]

db = {}

for each in classes:
	db[each] = data["classes"]["count"][each]

decks = data["decks"].keys()
print decks