from player import player
import random

allcards=['s:a', 'c:a', 'd:a', 'h:a', 's:2', 'c:2', 'd:2', 'h:2', 's:3', 'c:3', 'd:3', 'h:3', 's:4', 'c:4', 'd:4', 'h:4', 's:5', 'c:5', 'd:5', 'h:5', 's:6', 'c:6', 'd:6', 'h:6', 's:7', 'c:7', 'd:7', 'h:7', 's:8', 'c:8', 'd:8', 'h:8', 's:9', 'c:9', 'd:9', 'h:9', 's:10', 'c:10', 'd:10', 'h:10', 's:j', 'c:j', 'd:j', 'h:j', 's:q', 'c:q', 'd:q', 'h:q', 's:k', 'c:k', 'd:k', 'h:k']
char_to_number={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'j':11,'q':12,'k':13,'a':14}
number_to_char={2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'j', 12: 'q', 13: 'k', 14: 'a'}

class game:
	gid=0
	is_running=False 					#True if the game is running 
	fairdeal_single_card=''				#the single card on the 3rd game on fairdeal
	total_board_money=0					#the money on the table in each game
	board_amount=0						#set the board money amount
	waiting_players=[]					#list of object of players waiting for the game to join in
	active_players=[]					#list of object of the players currently playing the game
	players=[]							#all players in the room
	blind_amount=0						#blind amount set by the player while creating the game 
	bet_amount=0						#set same as blind amount unless a blind is played, then it is doubled
	dealing_player=0					#object of the player dealing the cards
	is_fairdeal=True					#True when a fairdeal is dealed
	fairdeal_counter=0					#counter to check the games after fairdeal
	current_player=0					#the player playing the current bet
	is_round_blind=True					#True if any player played a blind
	is_currently_blind=True				#True if someone is still blind
	def __init__(self,board_amount,blind_amount):
		self.dealing_player=player(100,plname,100)			#take input money from web page
		self.players.append(self.dealing_player)
		self.active_players.append(self.dealing_player)
		#create game link
		#game id assignment
		self.bet_amount=blind_amount
		self.blind_amount=blind_amount
	def shuffle_and_distribute(self,all_players):
		random.shuffle(allcards)
		x=0													#x decides the number of cards each player gets
		if self.fairdeal_counter==4:
			x=4
		elif self.fairdeal_counter==3:
			x=2
		elif self.fairdeal_counter==2:
			x=1
			self.fairdeal_single_card=allcards[-1]
		else:
			x=3
		for j,i in all_players:
			i.card_set=allcards[j*x:(j*x)+x]
	def cardrank(self,card):
		''' This function takes the cards, decides the hand and puts the according value in the "handrank" variable. "hand" stores numaric of the cards. '''
		self.hand=[]
		self.handrank=0
		self.hand.append(char_to_number[card[0].split(':')[1]])
		self.hand.append(char_to_number[card[1].split(':')[1]])
		self.hand.append(char_to_number[card[2].split(':')[1]])
		self.hand=(sorted(self.hand))
		if self.hand[0]==self.hand[1] and self.hand[1]==self.hand[2]:							#TRAIL	6
			self.handrank=6
		elif ((self.hand[2]-self.hand[1]==1 and self.hand[1]-self.hand[0]==1) or (self.hand[0]==2 and self.hand[1]==3 and self.hand[2]==14)) and card[0].split(':')[0]==card[1].split(':')[0] and card[1].split(':')[0]==card[2].split(':')[0]:		#PURE SEQUENCE 5
			self.handrank=5
		elif ((self.hand[2]-self.hand[1]==1 and self.hand[1]-self.hand[0]==1) or (self.hand[0]==2 and self.hand[1]==3 and self.hand[2]==14)):						#SEQUENCE	4
			self.handrank=4
		elif card[2].split(':')[0]==card[1].split(':')[0] and card[1].split(':')[0]==card[2].split(':')[0]:		#COLOR	3
			self.handrank=3
		elif self.hand[0]==self.hand[1] or self.hand[1]==self.hand[2] or self.hand[0]==self.hand[2]:		#PAIR	2
			self.handrank=2
		else:																							#HIGH CARDS 1
			self.handrank=1
		return self.handrank*1000000+self.hand[2]*10000+self.hand[1]*100+self.hand[0]
	def calculate_score(self,all_players):
		temp_card_set=[]
		for i in all_players:	
			if self.fairdeal_counter==4:											#4cards
				i.score=max(cardrank([i.card_set[0],i.card_set[1],i.card_set[2]]),cardrank([i.card_set[0],i.card_set[1],i.card_set[3]]),cardrank([i.card_set[0],i.card_set[2],i.card_set[3]]),cardrank([i.card_set[1],i.card_set[2],i.card_set[3]]))
			elif self.fairdeal_counter==3:											#2 cards
				colorcards=False
				sequencecards=False
				bigger_card_index=0
				if i.card_set[0].split(':')[0]==i.card_set[1].split(':')[0]:
					colorcards=True
				if (int(i.card_set[0].split(':')[1])-int(i.card_set[1].split(':')[1]))==1:
					sequencecards=True
				if (int(i.card_set[1].split(':')[1])-int(i.card_set[0].split(':')[1]))==1:
					sequencecards=True
					bigger_card_index=1
				if (int(i.card_set[0].split(':')[1])-int(i.card_set[1].split(':')[1]))==0:			#trail
					temp_card_set=i.card_set
					temp_card_set.append(temp_card_set[0])
					i.score=cardrank(temp_card_set)
				elif colorcards==True and sequencecards==True:										#pure sequence
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])+1])		
					i.score=cardrank(temp_card_set)
				elif sequencecards==True:															#sequence
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])+1])
					i.score=cardrank(temp_card_set)	
				elif colorcards==True:																#color
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':a')
					i.score=cardrank(temp_card_set)
				else:																				#pair
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])])
					i.score=cardrank(temp_card_set)
			elif self.fairdeal_counter==2:											#1 cards
				colorcards=False
				sequencecards=False
				bigger_card_index=0
				temp_card_set.append(fairdeal_single_card)
				if i.card_set[0].split(':')[0]==i.card_set[1].split(':')[0]:
					colorcards=True
				if (int(i.card_set[0].split(':')[1])-int(i.card_set[1].split(':')[1]))==1:
					sequencecards=True
				if (int(i.card_set[1].split(':')[1])-int(i.card_set[0].split(':')[1]))==1:
					sequencecards=True
					bigger_card_index=1
				if (int(i.card_set[0].split(':')[1])-int(i.card_set[1].split(':')[1]))==0:			#trail
					temp_card_set=i.card_set
					temp_card_set.append(temp_card_set[0])
					i.score=cardrank(temp_card_set)
				elif colorcards==True and sequencecards==True:										#pure sequence
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])+1])		
					i.score=cardrank(temp_card_set)
				elif sequencecards==True:															#sequence
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])+1])
					i.score=cardrank(temp_card_set)	
				elif colorcards==True:																#color
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':a')
					i.score=cardrank(temp_card_set)
				else:																				#pair
					temp_card_set=i.card_set
					temp_card_set.append(i.card_set[0].split(':')[0]+':'+number_to_char[int(i.card_set[bigger_card_index].split(':')[1])])
					i.score=cardrank(temp_card_set)
			elif self.fairdeal_counter==1:						#muflis
				i.score=100000000-cardrank(i.card_set)
			else:
				i.score=cardrank(i.card_set)
	def add_player(self,player):		# see own cards
		waiting_players.append(player)
	def remove_player(self.player):
		for i in range(len(self.active_players)):
			if self.active_players[i]==player:
				active_players.pop(i)
		for i in range(len(self.players)):
			if self.players[i]==player:
				players.pop(i)

