#!/usr/bin/python3

import argparse
import json
from operator import itemgetter

def get_deck(filepath):
    # maybe do some validation here?
    with open(filepath) as json_file:
        json_data = json.load(json_file)
        return json_data

def create_deck():
    deck = json.loads('{"pack":{"name":"","id":""},"black":[],"white":[],"quantity":{"black":0,"white":0,"total": 0}}')
    name = input("Enter the name for the deck:\n")
    # maybe do some validation here?
    deck["pack"]["name"] = name
    deck["pack"]["id"] = name.lower().replace(" ","-")
    deck = insert_cards(deck)
    return deck

def insert_cards(deck):
    blackcards = []
    whitecards = []
    newcard = input("Do you want to add a black, a white or no more cards? (b/w/n)\n")
    while newcard != "n":
        if newcard != "b" and newcard != "w":
            newcard = input("Invalid input " + newcard + "! Type b, w or n!\n")
            continue
        content = input("Type in your card:\n")
        content = content.strip()
        if is_duplicate(content, newcard, deck):
            newcard = input("Card already exists! Add another card? (b/w/n)\n")
            continue
        if newcard == "b":
            pick = 0
            while pick < 1 or pick > 3:
                pick = int(input("How many white cards does it take to answer the card? (min: 1, max: 3)\n"))
                continue
            draw = 9
            while draw < 0 or draw > 2:
                draw = int(input("How many white cards should be drawn after playing the card? (min: 0, max: 2)\n"))
            card = {
                    "content": content,
                    "pick": pick,
                    "draw": draw
                    }
            blackcards.append(card)
        else:
            whitecards.append(content)
        newcard = input("Do you want to add another black or white card or none? (b/w/n)\n")
    else:
        deck["black"].extend(blackcards)
        deck["white"].extend(whitecards)
        print(str(len(blackcards)) + " black cards and " + str(len(whitecards)) + " white cards added!")
        if input("Sort cards? (y/n)\n") == "y":
            deck = sort_cards(deck)
        return update_count(deck)

def update_count(deck):
    black = len(deck["black"])
    white = len(deck["white"])
    total = black + white
    deck["quantity"]["black"] = black
    deck["quantity"]["white"] = white
    deck["quantity"]["total"] = total
    print(deck["pack"]["name"] + " has " + str(black) + " black cards, " + str(white) + " white cards and thus " + str(total) + " cards in total!")
    return deck

def sort_cards(deck):
    deck["black"] = sorted(deck["black"], key=itemgetter('content'))
    deck["white"].sort()
    print("Cards sorted!")
    return deck

def is_duplicate(content, color, deck):
    is_dupe = False
    if color == "w":
        for card in deck["white"]:
            if content == card:
                is_dupe = True
                break
    elif color == "b":
        for card in deck["black"]:
            if content == card["content"]:
                is_dupe = True
                break
    return is_dupe

def write_deck(deck, filepath):
    f = open(filepath, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Done! Wrote to file " + filepath)

parser = argparse.ArgumentParser(description="Add and modify ABC/CAH custom decks in JSON format.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("operation", type=str, choices=['create', 'insert', 'count', 'sort'],
                    help="""operation on deck
- create: create a new deck based on template.json
- insert: insert cards into the deck
- count: update the card count
- sort: sort the cards alphabetically
                        """)
parser.add_argument("filepath", type=str, help="path to the file to operate on")
#parser.add_argument('--infile', type=argparse.FileType('r'), default=sys.stdin)
#parser.add_argument('--outfile', type=argparse.FileType('w'), default=sys.stdout)

args = parser.parse_args()

operation = args.operation
filepath = args.filepath

if operation == "create":
    deck = create_deck()
elif operation == "insert":
    deck = get_deck(filepath)
    deck = insert_cards(deck)
elif operation == "count":
    deck = get_deck(filepath)
    deck = update_count(deck)
elif operation == "sort":
    deck = get_deck(filepath)
    deck = sort_cards(deck)
else:
    print("Invalid operation " + operation + "!")
    exit()

write_deck(deck, filepath)
