class player:
	id=0					#to identify player
	name=''					#name of the player
	total_money=0			#total money in the bag
	card_set=[]				#cards in a perticular game
	is_blind=True			#false if the player has seen the cards
	game_money=0			#money take out for the game
	is_playing=True			#false if the player has folded
	score=0					#score of the cards in a game
	#current_game
	def __int__(self,plid,plname,money):
		self.id=plid
		self.name=plname
		self.total_money=money
	