#!/usr/bin/python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from operator import itemgetter
import json

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
    proceed = "y"
    blackcards = []
    whitecards = []
    print("Let's add some cards!")
    while proceed == "y":
        color = input("Black or white card? (b/w)\n")
        if color != "b" and color != "w":
            print("Invalid color " + color + "!")
            continue
        content = input("Type in your card:\n")
        content = content.strip()
        #content = content.replace("\"", "\\\")
        if color == "b":
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
        proceed = input("Add another card? (y/n)\n")
    else:
        deck["black"].extend(blackcards)
        deck["white"].extend(whitecards)
        print(str(len(blackcards)) + " black cards and " + str(len(whitecards)) + " white cards added!")
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

def write_deck(deck, filepath):
    f = open(filepath, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Done! Wrote to file " + filepath)

parser = ArgumentParser(description="Add and modify ABC/CAH custom decks in JSON format.", formatter_class=RawTextHelpFormatter)
parser.add_argument("operation", metavar="operation", type=str,
                    help="""operation on deck
- create: create a new deck based on template.json
- insert: insert cards into the deck
- sort: sort the cards alphabetically
- count: update the card count
                        """)
parser.add_argument("file", metavar="file",
                    help="path to the file to operate on")
args = parser.parse_args()

operation = args.operation
filepath = args.file

if operation == "create":
    deck = create_deck()
    if input("Sort cards? (y/n)\n") == "y":
        deck = sort_cards(deck)
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
