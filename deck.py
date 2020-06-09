#!/usr/bin/python3

from operator import itemgetter
import argparse
import json
import string
import sys

def get_deck(infile):
    # maybe do some validation here?
    with open(infile) as json_file:
        deck = json.load(json_file)
        return deck

def create_deck():
    name = str(input("Enter the name for the deck:\n")).strip()
    deck = {
            "pack": {
                "name": name.title(),
                "id": name.lower().replace(" ","-")
                },
            "black": [],
            "white": [],
            "quantity": {
                "black": 0,
                "white": 0,
                "total": 0
                }
            }
    return deck

def add_cards(deck):
    print("Let's add some cards to " + deck["pack"]["name"] + "!")
    newblackcards = []
    newwhitecards = []
    newcard = "?"
    while newcard != "n":
        if newcard != "b" and newcard != "w":
            newcard = str(input("Add (b)lack, (w)hite or (n)o card?: ")).strip()
            continue
        content = str(input("Type in your card: "))
        content = sanitize_content(content, newcard)
        if skip_duplicate(content, newcard, deck):
            newcard = "?"
            continue
        if newcard == "b":
            pick = 0
            while pick < 1 or pick > 3:
                pick = int(input("How many white cards does it take to answer the card (min: 1, max: 3)? "))
                continue
            draw = 9
            while draw < 0 or draw > 2:
                draw = int(input("How many white cards should be drawn after playing the card (min: 0, max: 2)? "))
            card = {
                    "content": content,
                    "pick": pick,
                    "draw": draw
                    }
            newblackcards.append(card)
        else:
            newwhitecards.append(content)
        newcard = str(input("OMG, so funny! Add another (b)lack, (w)hite or (n)o card? ")).strip()
    else:
        deck["black"].extend(newblackcards)
        deck["white"].extend(newwhitecards)
        txt = "Alright! {} black cards and {} white cards added to " + deck["pack"]["name"] + "!"
        print(txt.format(len(newblackcards), len(newwhitecards)))
        return(deck)

def sanitize_content(content, color):
    content = content.strip()
    if content[0].islower():
        content = content[0].upper() + content[1:]
    if color == "w":
        endswithchar = False
        for i in string.punctuation:
            if content.endswith(i):
                endswithchar = True
                break
        if endswithchar:
            print("'" + content + "' ends with punctuation (white cards usually don't).")
            force = "?"
            while force != "y" and force != "n":
                force = str(input("Keep punctuation (y/n)? ")).strip()
                continue
            if force == "n":
                content = content[:-1]
    return content

def skip_duplicate(content, color, deck):
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
    if is_dupe:
        print("'" + content + "' already exists in " + deck["pack"]["name"] + "...\n")
        skip = "?"
        while skip != "y" or skip != "n":
            skip = str(input("Skip card (y/n)? ")).strip()
            print(skip)
            if skip == "n":
                is_dupe = False
                break
            elif skip == "y":
                is_dupe = True
                break
            else:
                continue
    return is_dupe

def sort_cards(deck):
    deck["black"] = sorted(deck["black"], key=itemgetter('content'))
    deck["white"].sort()
    print("Cards sorted!")
    return deck

def count_cards(deck):
    black = len(deck["black"])
    white = len(deck["white"])
    total = black + white
    deck["quantity"]["black"] = black
    deck["quantity"]["white"] = white
    deck["quantity"]["total"] = total
    txt = deck["pack"]["name"] + " has {} black cards, {} white cards and thus {} cards in total!"
    print(txt.format(black, white, total))
    return deck

def write_deck(deck):
    outfile = "./packs/" + deck["pack"]["id"] + ".json"
    f = open(outfile, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Done! Wrote to " + outfile)

def main():
    main_parser = argparse.ArgumentParser(
            description="Add and modify ABC/CAH custom decks in JSON format."
            )

    #main_parser.addArgument(
            #'command',
            #choice=['create', 'add-cards', 'edit', 'sort', 'count']
            #)
    # optionales infile, outfile, sort, count
    # consolidate/recommit?

    subparsers = main_parser.add_subparsers(
            dest="command",
            description="Actions to perform on a deck."
            )

    create_parser = subparsers.add_parser(
            'create',
            help="Create a new deck.",
            description="Creates a new deck in an interactive workflow."
            )
    #create_parser.set_defaults(func=create_deck)

    edit_parser = subparsers.add_parser(
            'edit',
            help="Modify an existing deck.",
            description="Modifies an existing deck in the way specified by the optional arguments."
            )
    edit_parser.add_argument(
            'infile',
            type=str,
            help="Path to an existing JSON file to edit.",
            default=sys.stdin
            )
    edit_parser.add_argument(
            '-a', '--add',
            action="store_true",
            help="Add cards to the deck."
            )
    edit_parser.add_argument(
            '-s', '--sort',
            action="store_true",
            help="Sort cards alphabetically by their contents."
            )
    edit_parser.add_argument(
            '-c', '--count',
            action="store_true",
            help="Update the card count."
            )
    #edit_parser.set_defaults(func=get_deck)

    args = main_parser.parse_args()

    if args.command == "create":
        deck = create_deck()
    else:
        deck = get_deck(args.infile)

    if args.command == "create" or args.add:
        deck = add_cards(deck)
    if args.command == "create" or args.sort:
        deck = sort_cards(deck)
    if args.command == "create" or args.count:
        deck = count_cards(deck)

    write_deck(deck)

if __name__ == "__main__":
    main()
