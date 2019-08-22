
# coding: utf-8

# In[2]:


import random
from IPython.display import clear_output

class BlackJack_Game(object):
        
    _card_ranks = {'Ace':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':10,'Queen':10,'King':10}
    _card_suits = ('Spades','Hearts','Clubs','Diamonds')
        
    class _Player(object):        
        def __init__(self, player_name, bankroll = 1000):
            self.player_name = player_name
            self.bankroll = bankroll
        
        #def GetPlayerHandSum(self):
        #    hand_sum = 0
        #    for card in _deck:
        #        if _deck[card] == self:
        #            hand_sum += _card_ranks[card[0]]
        #    return hand_sum
        
    def __init__(self):
        self._deck = {(rank,suit):None for rank in BlackJack_Game._card_ranks for suit in BlackJack_Game._card_suits}
        self._players = set()
        
        print 'Starting a new BlackJack game!'
        self.AddPlayer('Dealer')
        self.AddPlayer()
        #SetPlayers() #--> Gives the option to add, remove and view players in the game
        print '\nPlayers have been defined!'
        self.ViewPlayers()
        raw_input('Press Enter to start the game.')
        self.StartGame()
        print '\nGame over!\nThanks for playing!'            

    def ViewPlayers(self):
        if len(self._players) <= 0:
            print 'There are no players in the game!'
        else:
            print 'The following players are in the game:'
            sorted_player_list = sorted(self._players, key = lambda player: player.player_name)
            for player in sorted_player_list:
                print '\nPlayer: ' + player.player_name + '\nBankroll: ' + str(player.bankroll)
        
    def AddPlayer(self, player_name = 'Player', bankroll = 1000):
        if player_name == 'Player':         
            player_name = self.GetNewDefaultPlayerName()
        if player_name not in [player.player_name for player in self._players]:
            new_player = self._Player(player_name, bankroll)
            self._players.add(new_player)
            print 'Added "' + player_name + '" to the game!'
        else:
            print '"' + player_name + '" already exists in the game!'
        
    def GetNewDefaultPlayerName(self):
        player_name = 'Player'
        player_index = 1
        new_player_name = player_name + str(player_index)

        while new_player_name in [player.player_name for player in self._players]:
            player_index += 1
            new_player_name = player_name + str(player_index)
        return new_player_name
        
    def RemovePlayer(self, player_name):
        if player_name == 'Dealer':
            print "The Dealer can't be removed from the game!"
        else:
            players_to_remove = [player for player in self._players if player.player_name == player_name]
            if len(players_to_remove) > 0:
                for player in players_to_remove:
                    self._players.remove(player)
                print 'Removed "' + player_name + '" from the game!'
            else:
                print '"' + player_name + '" is not in this game!'     
        
    def ResetDeck(self):
        for card, owner in self._deck.iteritems():
            owner = None if owner <> None else owner
        print 'Deck has been reseted!'
        
    def StartGame(self):
        _game_is_over = False
        _round_is_over = False
        clear_output()
        
        while _game_is_over == False:
            winners = list()
            self.ResetDeck()
            self.DealFirstCards()
            winners = self.GetPlayersWithBlackJack()
            raw_input('Press Enter to continue the game.')
            
            while len(winners) <= 0 and _round_is_over == False:
                for player in self._players:
                    clear_output()
                    stand = False
                    option = ''
                    while self.GetPlayerPointSum(player) < 21 and stand == False:
                        self.ViewCardsFromAllPlayers()
                        print "It's " + player.player_name + "'s turn!"
                        option = self.GetPlayerAction()
                        if option == 'S':
                            print 'Stand!'
                            stand = True
                        else:
                            print 'Hit!'
                            self.DealOneCard(player)
                    if self.GetPlayerPointSum(player) > 21:
                        print '"' + player.player_name +'" busted!'
                _round_is_over = True
            print '\nRound over!'
            
            _game_is_over = True
    
    def GetPlayerAction(self):
        option = ''
        while option.upper() not in ['H', 'S']:
            option = raw_input('Choose an option:' + '\n' + 'Enter "H" to Hit.' + '\n' + 'Enter "S" to Stand\n')
        return option.upper()
    
    def DealFirstCards(self):
        print 'Dealing cards...\n'
        for player in self._players:
            for card in random.sample([card for card, owner in self._deck.iteritems() if owner == None], 2):
                self._deck[card] = player
            self.ViewCardsFromOnePlayer(player)
    
    def DealOneCard(self, player):
        for card in random.sample([card for card, owner in self._deck.iteritems() if owner == None], 1):
            self._deck[card] = player
        self.ViewCardsFromOnePlayer(player)
    
    def ViewCardsFromAllPlayers(self):
        for player in self._players:
            self.ViewCardsFromOnePlayer(player)

    def ViewCardsFromOnePlayer(self, player):
        print player.player_name + ' has the following cards:'
        for card, owner in self._deck.iteritems():
            if owner == player:
                print card[0] + ' of ' + card[1]
        print player.player_name + ' has ' + str(self.GetPlayerPointSum(player)) + ' points.' + '\n'
        
    def ViewWinners(self, winners):
        if len(winners) == 1:
            print 'The winner is :' + winners[0].player_name + '!'
        elif len(winners) > 1:
            print "It's a tie !"
            #print "It's a tie between these players: " + (lambda winner: winners

    def GetPlayersWithBlackJack(self):
        players_with_blackjack = list()
        for player in self._players:
            if self.GetPlayerPointSum(player) == 21:
                players_with_blackjack.append(player)
        
        return players_with_blackjack
    
    def GetWinners(self):
        winners = list()
        max_points = 0
        player_sum = {player : self.GetPlayerPointSum(player) for player in self._players}
        player_sum_not_busted = {player : points for player, points in player_sum.iteritems() if points <= 21}
        if len(winners) > 1:
            max_points = max(player_sum_not_busted.values())
            winners = [player for player, points in player_sum_not_busted.iteritems() if points == max_points]
        return winners
    
    def GetPlayerPointSum(self, player):
        hand_sum = 0
        for card, owner in self._deck.iteritems():
            if owner == player:
                hand_sum += BlackJack_Game._card_ranks[card[0]]
        return hand_sum
    


# In[3]:


game = BlackJack_Game()


# In[3]:


game.ViewPlayers()
game._card_ranks


# In[311]:


game.AddPlayer('Leo')
game.ViewPlayers()


# In[312]:


game.RemovePlayer('Leo')


# In[31]:


k={'King':10}


# In[32]:


k.keys


# In[53]:


_card_ranks = {'Ace':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':10,'Queen':10,'King':10}
_card_suits = ('Spades','Hearts','Clubs','Diamonds')
_deck = {(rank,suit):'none' for rank in _card_ranks for suit in _card_suits}


# In[57]:


_deck


# In[72]:


for card in random.sample(_deck, 1):
    print card, _card_ranks[card[0]]


# In[40]:


x = 'asd'


# In[41]:


x.upper()


# In[11]:


aaa = 'x'
bbb = 'teste' if aaa == None else 'd'
bbb


# In[58]:


d = {'a':1000, 'b':2000, 'c':5000, 'd':5000}


# In[52]:


max(d)


# In[49]:


max(d, key=lambda x: d[x])


# In[60]:


a = [(x,y) for x,y in d.iteritems() if y == max(d.values())]


# In[62]:


a = 'dd'


# In[ ]:


a.join

