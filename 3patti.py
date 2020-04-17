import random
#from pynput import keyboard 
allcards=['s:a', 'c:a', 'd:a', 'h:a', 's:2', 'c:2', 'd:2', 'h:2', 's:3', 'c:3', 'd:3', 'h:3', 's:4', 'c:4', 'd:4', 'h:4', 's:5', 'c:5', 'd:5', 'h:5', 's:6', 'c:6', 'd:6', 'h:6', 's:7', 'c:7', 'd:7', 'h:7', 's:8', 'c:8', 'd:8', 'h:8', 's:9', 'c:9', 'd:9', 'h:9', 's:10', 'c:10', 'd:10', 'h:10', 's:j', 'c:j', 'd:j', 'h:j', 's:q', 'c:q', 'd:q', 'h:q', 's:k', 'c:k', 'd:k', 'h:k']
char_to_number={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'j':11,'q':12,'k':13,'a':14}
number_of_players=1
class players:
	hand=[]
	plid=100
	handrank=0
	score=0
	name=""
	money=50
	def __init__(self,x):
		self.plid=self.plid+x+1
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
		self.score=self.handrank*1000000+self.hand[2]*10000+self.hand[1]*100+self.hand[0]
		#print(handrank,hand,cards)
	def display(self):
		print(self.plid,self.score,self.hand,self.handrank)#L,self.money)
def gameplay(player):
	random.shuffle(allcards)
	while True:
		i=0
		for i in range(len(player)):
			player[i].cardrank(allcards[i*3:i*3+3])
		folded_players=[]
		while True:					#One game
			if player[i].id in folded_players:
				i+=1
				continue
			choice=input()
			if choice=='f':
				folded_players.append(player[i].plid)

			i+=1
nop=5 # input("Enter the numbers of players:")
random.shuffle(allcards)
player=[]
for j in range(nop):
	for i in range(nop):
		player.append(players(i))
		player[i].cardrank(allcards[i*3:(i*3)+3])
		if i==j:
			player[i].money-=5
		#player[i].display()
	#print("==============================================")
temp={}
for i in char_to_number:
	temp[char_to_number[i]]=i
print(temp)