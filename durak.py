import random
import string

class Colour:
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[32m"
    END = "\033[0m"

suits = (
    Colour.RED + 'Diamonds' + Colour.END,
    Colour.BLACK + 'Clubs' + Colour.END,
    Colour.BLACK + 'Spades' + Colour.END,
    Colour.RED + 'Hearts' + Colour.END
)
card_index = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
card_values = {'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13}

class Card:
    number : string
    suit : string
    def __init__(self, n, s):
        self.number = n
        self.suit = s

def get_card():
    new_card = random.choice(deck)
    deck.remove(new_card)
    return new_card

def fill_deck():
    for suit in suits:
        for index in card_index:
            deck.append(Card(index, suit))

class Player:
    def __init__(self, cards, name):
        self.hand = []
        self.name = name
        for i in range(cards):
            self.hand.append(get_card())

def next_player(player):
    index = players.index(player) + 1
    if index is players.count:
        index = 0
    return players[index]

deck = []
players = []
trump : Card
cur_attacker : Player = []
table = []
allattacks = []
table_counter = 0

def clear_table():
    global table
    global allattacks
    global table_counter
    table = []
    allattacks = []
    table_counter = 0

def can_add_attack():
    return table_counter < 6 and len(next_player(cur_attacker).hand) > 0

def addAttack(card):
    global allattacks
    global table
    global table_counter
    allattacks.append(card)
    table.append(card)
    table_counter += 1

def set_up(playercount, names):
    fill_deck()

    for i in range(playercount):
        players.append(Player(6, names[i]))

    global cur_attacker
    global trump
    cur_attacker = players[0]
    trump = get_card()
    deck.append(trump)

def print_cards(hand):
    for card in hand:
        print(str(hand.index(card) + 1) + '. ' + card_as_str(card))

def card_as_str(card):
    return card.number + ' of ' + card.suit

def can_beat(attack_c, defense_c) -> bool:
    if attack_c.suit == defense_c.suit:
        return card_values[defense_c.number] > card_values[attack_c.number]

    if attack_c.suit == trump.suit:
        return False

    if defense_c.suit == trump.suit:
        return True

    return False

def usable_cards(hand):
    usables = []
    for card in hand:
        for attack_card in allattacks:
            if can_beat(attack_card, card):
                usables.append(card)
                break
    return usables

def try_parse_int(s):
    try:
        return int(s)
    except:
        return -1

def begin_attack():
    print('\n Trump card is ' + card_as_str(trump))
    print(cur_attacker.name + ' is attacking ' + next_player(cur_attacker).name)
    print('Cards on the table: ' + str(table_counter) + '/6')
    print(cur_attacker.name + 's cards:')
    print_cards(cur_attacker.hand)

def attack():
    print('\n Enter card index (1-6)')

    i = try_parse_int(input()) - 1
    if (i < 0 or i >= len(cur_attacker.hand)):
        print('Invalid answer, try again \n')
        attack()
        return

    addAttack(cur_attacker.hand[i])
    print('\n Attacked ' + str(next_player(cur_attacker).name) +' with '+ card_as_str(cur_attacker.hand[i]))
    del cur_attacker.hand[i]

def defend():
    player = next_player(cur_attacker)
    usables = usable_cards(player.hand)

    print(player.name + ' must defend')

    print('\n Attacks:')
    print_cards(allattacks)

    if len(usables) == 0:
        for card in table:
            player.hand.append(card)
        clear_table()
        print('Unable to beat, forced take')
        return

    print('\n Your usable cards:')
    print_cards(usables)
    print('Type 100 to take the cards')

    if len(allattacks) == 1 and len(usables) > 0:
        print('\n Your usable cards:')
        print_cards(usables)
        beat(0)
        return

    if len(allattacks) > len(usables):
        for card in table:
            player.hand.append(card)
        clear_table()
        print('More attacks then usable cards, forced take')
        return

    print('Enter card (1-6) to defend AGAINST')

    i = try_parse_int(input()) - 1
    if i == 99:
        print(player.name + ' took these cards:')
        print_cards(table)
        for card in table:
            player.hand.append(card)
        clear_table()      
        return

    if (i < 0 or i >= len(allattacks)):
        print('Invalid answer, try again')
        defend()
        return

    beat(i)

def beat(i):
    global cur_attacker
    player = next_player(cur_attacker)

    print('\n Enter card (1-6) to beat ' + card_as_str(allattacks[i]))
    print('Type 400 to cancel selection')
    j = try_parse_int(input()) - 1

    if j == 99:
        print(player.name + ' took these cards:')
        print_cards(table)
        for card in table:
            player.hand.append(card)
        clear_table()
        return

    if j == 399:
        print('Cancelled selection, restarting last turn...')
        defend()
        return

    if (j < 0 or j >= len(usable_cards(player.hand))):
        print('Invalid answer, try again')
        beat(i)
        return

    if player.hand[j].number == allattacks[i].number and table_counter == len(allattacks):
        cur_attacker = player
        print('All attacks passed onto ' + cur_attacker.name)
        addAttack(player.hand[j])
        del player.hand[j]
        return

    if not can_beat(allattacks[i], player.hand[j]):
        print('Card is incapable of beating attack, try again')
        beat(i)
        return

    print('Card successfully beaten, there are now ' + str(table_counter) + '/6')
    table.append(player.hand[j])
    del allattacks[i]
    del player.hand[j]

def addable_cards(hand):
    cards = []
    for add_card in hand:
        for card in table:
            if add_card.number == card.number:
                cards.append(add_card)
                break
    return cards

def add_cards():
    for player in players:
        if player == next_player(cur_attacker):
            continue
        adding = True
        while adding and can_add_attack:
            cards = addable_cards(player.hand)
            if len(cards) == 0:
                adding = False
                continue

            print('\n There are ' + str(table_counter) + ' cards')
            print('\n' + player.name + ' can add these cards:')
            print_cards(cards)
            print('Enter single card to add \n Type 200 to skip \n Type 300 to add all')

            i = try_parse_int(input()) - 1
            if i == 199:
                adding = False
                print('Skipped')
                continue

            if i == 299:
                for card in cards:
                    if not can_add_attack:
                        print('Cannot add all cards')
                        return
                    print('Added ' + card_as_str(card))
                    addAttack(card)
                    player.hand.remove(card)
                    adding = False
                continue

            if i < 0 or i >= len(cards):
                print('Invalid answer, try again')
                continue

            print('Added ' + card_as_str(cards[i]))
            addAttack(cards[i])
            player.hand.remove(cards[i])

def restock_cards():
    for player in players:
        while len(deck) > 0 and len(player.hand) < 6:
            player.hand.append(get_card())
    print('\n Restocked cards')
    print(str(len(deck)) + ' remaining in the deck')

def check_winner():
    if len(deck) == 0:
        for player in players:
            if len(player.hand) == 0:
                print(player.name + ' won the game!!')

def cycle():
    begin_attack()
    attack()
    add_cards()

    while len(allattacks) > 0:
        defend()
        add_cards()

    global cur_attacker
    cur_attacker = next_player(cur_attacker)
    restock_cards()
    check_winner()
    cycle()

def begin():
    print('How many players? (2-8)')
    x = try_parse_int(input())
    if x < 2 or x > 8:
        print('Invalid input, try again')
        begin()
        return
    names = []
    for i in range(x):
        print('Name player #' + str(i + 1))
        names.append(input())
    set_up(x, names)
    cycle()

begin()
