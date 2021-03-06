import random

'''
Random Generation
-- More details here
'''
def random_int():
    random_number = random.randint(1,6)
    return random_number

def random_hand():
    deck = []
    for x in range(5):
        deck.append(random_int())
    return deck

def hands():
    hand = {'player':[],'dealer':[]}
    for user in hand:
        hand[user] = random_hand()
    return hand

'''
Occurences Count
-- More details here
'''
def occurences(hand):
    occurences_list = []
    for x in range(1,7):
        count = hand.count(x)
        occurences_list.append(count)
    return occurences_list

def count_hands(hand):
    counted = {'player':[], 'dealer':[]}
    for user in hand:
        print # solely to elimate pylint warning
        counted[user] = occurences(hand[user])
    return counted

'''
Possible Hands
'''
def evaluate_5_of_a_kind(occurences_list):
    if 5 in occurences_list:
        return True
    else:
        return False

def evaluate_full_house(occurences_list):
    if 3 in occurences_list and 2 in occurences_list:
        return True
    else:
        return False

def evaluate_4_of_a_kind(occurences_list):
    if 4 in occurences_list:
        return True
    else:
        return False

def evaluate_straight(occurences_list):
    is_a_straight = False 
    if occurences_list == [1,1,1,1,1,0]:
        is_a_straight = True
    if occurences_list == [0,1,1,1,1,1]:
        is_a_straight = True
    if is_a_straight:
        return True
    else:
        return False

def evaluate_3_of_a_kind(occurences_list):
    if 3 in occurences_list:
        return True
    else:
        return False

def evaluate_2_pair(occurences_list):
    pair_count = 0
    for occurence in occurences_list:
        if occurence == 2:
            pair_count += 1
    if pair_count == 2:
        return True
    else:
        return False

def evaluate_pair(occurences_list):
    if 2 in occurences_list:
        return True
    else:
        return False

'''
Number Indexing
'''
def index_value(occurences_list, numbers):
    indexes = []
    x = 1
    for occurence in occurences_list:
        if occurence in numbers:
            indexes.append(x)
        x+=1
    return indexes

def straight_power(occurences_list):
    if occurences_list == [1,1,1,1,1,0]:
        return [1] # purposely a list to remain consistent with index_value
    if occurences_list == [0,1,1,1,1,1]:
        return [2]
    else:
        return False

# Determine whole number power, append prefixed
# to suffix value as a float to help
# compare dealer hand to players
# 
# refactor for legibility
# fix run on float error

def create_float(whole_number_value, suffix_list):
    try:
        suffix = (suffix_list[0]*0.1)+(suffix_list[1]*0.01)
    except:
        suffix = suffix_list[0]*0.1
    float_value = round(whole_number_value + suffix,2) # round to remove trailing 0s, refactor needed
     
    return float_value

'''
Hand Strength
-- Depricate and refacter asap
'''
def evaluation(occurences_list):
    # consider a case switch
    # refinement needed
    if evaluate_5_of_a_kind(occurences_list):
        return create_float(7,
        index_value(occurences_list, [5]))

    elif evaluate_full_house(occurences_list):
        return create_float(6, 
        index_value(occurences_list, [3,2]))

    elif evaluate_4_of_a_kind(occurences_list):
        return create_float(5, 
        index_value(occurences_list, [4]))

    elif evaluate_straight(occurences_list):
                                  
        return create_float(4, 
        straight_power(occurences_list))

    elif evaluate_3_of_a_kind(occurences_list):
        return create_float(3, 
        index_value(occurences_list, [3]))
    # debugging needed
    elif evaluate_2_pair(occurences_list):
        return create_float(2, 
        index_value(occurences_list, [2,2]))

    elif evaluate_pair(occurences_list):
        return create_float(1, 
        index_value(occurences_list, [2]))

    else:
        return 0.0

'''
Hand Scoring
'''
def score_hand(hand_counted):
    score = evaluation(hand_counted)
    return score

def score_hands(counted):
    score = {"player":score_hand(counted['player']),
    "dealer":score_hand(counted['dealer'])}
    return score

'''
Hand Score to Text
'''
def score_as_text(float):
    hands = [
        "Nothing",
        "Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight", # add high straight / low straight
        "Four of a Kind",
        "Full House",
        "Five of a Kind"
    ]
    string = str(float)
    string = string.split(".")
    whole_number = int(string[0])
    if whole_number == 0:
        payload = "No Hand"
    elif whole_number == 2:
        payload = "Pair of " + string[1][0] + "s and " + string[1][1] + "s"
    elif whole_number == 4:
        if string[1] == 1:
            prefix = "Low"
        else:
            prefix = "High"
        payload = prefix + " Straight"
    else:
        payload = hands[whole_number] + " of " + string[1] + "s"
    return payload
'''
Game
'''

def Hand(hands,counted,score):
    # consider single schema population
    # to allow for objects variable
    # player and dealer
    # rather than slicing

    # consider getting counted and score values
    # from object, rather than 
    # inserting as attr
    both_hands = {
    "player":
        {
            "hand": [],
            "counted": [],
            "score": 0.0,
            "text": ""
        },
    "dealer":
        {
            "hand": [],
            "counted": [],
            "score": 0.0,
            "text": ""
        }
    }
    users = ["player", "dealer"]
    for user in users:
        both_hands[user]['hand'] = hands[user]
        both_hands[user]['counted'] = counted[user]
        both_hands[user]['score'] = score[user]
        both_hands[user]['text'] = score_as_text(score[user])
    return both_hands

def dealer_wins(hand):
    if hand['dealer']['score'] >= hand['player']['score']:
        return True
    else: 
        return False
