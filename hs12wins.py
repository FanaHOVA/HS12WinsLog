import praw #Reddit API

user_agent = ("HS 12 Wins Stats 0.1 by /u/FanaHOVA "
			   "github.com/FanaHOVA/HS12WinsLog")

r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit('12winArenaLog').get_hot(limit=10)

'''PRAW/Reddit API works on lazy objects, splitting the functions to avoid useless data fetching'''

def getdeck():

	for each in submissions:
		deck = []
		op = each.selftext.lower() #Deck list, need formatting
		for line in op.split("\n"):
			deck.append(line)

def getclass():

	for each in submissions:
		title = each.title.lower()
		
		if "paladin" in title:
			return "Paladin"

		elif "mage" in title:
			return "Mage"

		elif "warlock" in title:
			if "zoo" in title:
				return "Zoolock"
			elif "hand" in title:
				return "Handlock"
			else:
				return "Warlock"
		
		elif "priest" in title:
			return "Priest"

		elif "hunter" in title:
			return "Hunter"

		elif "warrior" in title:
			return "Warrior"

		elif "rogue" in title:
			if "miracle" in title:
				return "Miracle Rogue"
			else:
				return "Rogue"

		elif "shaman" in title:
			return "Shaman"

		elif "druid" in title:
			return "Druid"