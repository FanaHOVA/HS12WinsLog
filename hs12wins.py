import praw #Reddit API
import json

user_agent = ("HS 12 Wins Stats 0.3 by /u/FanaHOVA "
			   "github.com/FanaHOVA/HS12WinsLog")

r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit('12winArenaLog').get_hot(limit=250) #Replace with get_top(limit=3000) to run full script and not just test it

f = open("database.json","r+")
db = json.load(f)

cardsx = ["alexstrasza", "explosion", "execute", "explosive", "axe", "hex", "jaraxxus", "maexxna", "onyxia", "naxxramas"] #Only instances in which a x is in the card name; if not, must be a 2x/3x

for each in submissions:

	title = each.title.lower() #Title of the post, usually is: [W-L] Class [DD-MM-YYYY]

	if "meta" in title:
		pass #Disregard meta posts 

	deck = [] #Empty list to fill
	
	op = each.selftext.lower() #Whole post from subreddit

	for line in op.split("\n"): #Split each line to analyze if it's a card or not
		if line.isspace(): #Skip empty lines
			pass
		elif len(line) > 30: #No card name is that long, must be a note
			pass
		elif len(line) < 5 and "hex" not in line: #No other card name is that short
			pass
		elif "!" in line or "?" in line or "http" in line: #Skips imgur screens and "12 wins baby!" etc
			pass 
		elif "prizes" in line or "rewards" in line or "notes" in line or "results" in line: #Prizes are listed at the end of the post after the deck, you can break from here
			break
		else: #Must be a "Boulderfist Ogre 2x" or something like that. 
			bits = line.split(" ")

			count = 1
			for bit in bits:
				if "x" in bit and bit not in cardsx:

					if "2" in bit:
						count = 2
					elif "3" in bit:
						count = 3
					elif "4" in bit:
						count = 4
					bits.remove(bit)
				elif "*" in bit:
					bits.remove(bit)

			card = " ".join(bits).title().rstrip(" ")

			for i in range(count):
				if card == "" or card == "Deck:" or card == "Decklist:" or card == "Draft":
					pass
				else:
					deck.append(card)

	race = "" #Used to create deck ID

	if "paladin" in title:
		db["classes"]["count"]["Paladin"] += 1
		race = "Paladin"

	elif "mage" in title:
		db["classes"]["count"]["Mage"] += 1
		race = "Mage"

	elif "warlock" in title:
		if "zoo" in title:
			db["classes"]["count"]["Zoolock"] += 1
			db["classes"]["count"]["Warlock"] += 1
			race = "Warlock"
					
		elif "hand" in title:
			db["classes"]["count"]["Handlock"] += 1
			db["classes"]["count"]["Warlock"] += 1
			race = "Warlock"

		else:
			db["classes"]["count"]["Warlock"] += 1
			race = "Warlock"

	elif "priest" in title:
		db["classes"]["count"]["Priest"] += 1
		race = "Priest"

	elif "hunter" in title:
		db["classes"]["count"]["Hunter"] += 1
		race = "Hunter"

	elif "warrior" in title:
		db["classes"]["count"]["Warrior"] += 1
		race = "Warrior"

	elif "rogue" in title:
		if "miracle" in title:
			db["classes"]["count"]["Miracle"] += 1
			db["classes"]["count"]["Rogue"] += 1
			race = "Rogue"

		else:
			db["classes"]["count"]["Rogue"] += 1
			race = "Rogue"

	elif "shaman" in title:
			db["classes"]["count"]["Shaman"] += 1
			race = "Shaman"

	elif "druid" in title:
			db["classes"]["count"]["Druid"] += 1
			race = "Druid"

	score = title[0:6]
	deckid = score + race + "(%s)" % (each.name) #ID of Reddit post

	db["decks"][deckid] = deck

f.seek(0) #Reset file position to the beginning.
json.dump(db, f, indent=4)