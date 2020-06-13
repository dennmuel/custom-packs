#!/usr/bin/python3

from operator import itemgetter
import argparse
import json
import string
import sys

def get_deck(infile):
    # maybe do some validation here?
    with open(infile) as json_file:
        return json.load(json_file)

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
    print("Let's add some cards!")
    color = ""
    while color != "n":
        if color != "b" and color != "w":
            color = str(input("Add (b)lack, (w)hite or (n)o cards?: ")).strip()
            continue
        if color == "b":
            content = str(input("Type in the content of your black card (leave empty to change color or exit): "))
        else:
            content = str(input("Type in your white card (leave empty to change color or exit): "))
        if content == "":
            color = content
            continue
        content = sanitize_content(content, color)
        if skip_duplicate(content, color, deck):
            continue
        deck = add_card(content, color, deck);
        print("Added '" + content + "'")
    else:
        print("Added cards to " + deck["pack"]["name"] + "!")
        return(deck)

def add_card(content, color, deck):
    if color == "b":
        print(content)
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
        deck["black"].append(card)
    else:
        deck["white"].append(content)
    return(deck)

def import_cards(deck):
    print("Let's import some cards!")
    color = "?"
    while color != "n":
        if color != "b" and color != "w":
            color = str(input("Add (b)lack, (w)hite or (n)o cards?: ")).strip()
            continue
        path = str(input("Type in the path to the card file: "))
        with open(path) as p:
            while True:
                content = p.readline()
                if not content.strip():
                    break
                content = sanitize_content(content, color)
                if skip_duplicate(content, color, deck):
                    continue
                deck = add_card(content, color, deck);
        print("---")
        color = str(input("Done! Add further (b)lack, (w)hite or (n)o cards? ")).strip()
    else:
        print("Alright! Cards imported to " + deck["pack"]["name"] + "!")
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
    print("Sorting...")
    deck["black"] = sorted(deck["black"], key=itemgetter('content'))
    deck["white"].sort()
    print("Cards sorted!")
    return deck

def count_cards(deck):
    print("Counting...")
    black = len(deck["black"])
    white = len(deck["white"])
    total = black + white
    deck["quantity"]["black"] = black
    deck["quantity"]["white"] = white
    deck["quantity"]["total"] = total
    txt = "Deck has {} black cards, {} white cards and thus {} cards in total!"
    print(txt.format(black, white, total))
    return deck

def recommit_deck(deck):
    print("Recommitting...")
    for blackcard in deck["black"]:
        blackcard["content"] = sanitize_content(blackcard["content"], "b")
    for whitecard in deck["white"]:
        whitecard = sanitize_content(whitecard, "w")
    print("Recommited!")
    return deck

def deck_info(deck):
    print("Name: " + deck["pack"]["name"])
    print("ID: " + deck["pack"]["id"])
    print("Black cards: " + str(deck["quantity"]["black"]))
    print("White cards: " + str(deck["quantity"]["white"]))
    print("Total cards: " + str(deck["quantity"]["total"]))

def write_deck(deck):
    outfile = "./packs/" + deck["pack"]["id"] + ".json"
    f = open(outfile, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Wrote to " + outfile)

def main():
    main_parser = argparse.ArgumentParser(
            description="Handle allbadcards custom decks in JSON format.",
            )

    operations_parser = argparse.ArgumentParser(
            description="Operations for create and edit commands.",
            add_help=False
            )
    operations_parser.add_argument(
            '-a', '--add',
            action="store_true",
            help="add cards to deck(s) manually"
            )
    operations_parser.add_argument(
            '-i', '--fileimport',
            action="store_true",
            help="import cards from line separated text file(s)"
            )
    operations_parser.add_argument(
            '-r', '--recommit',
            action="store_true",
            help="recommit existing deck(s) (encoding, capital letters, etc.)",
            )
    operations_parser.add_argument(
            '-s', '--sort',
            action="store_true",
            help="sort cards alphabetically"
            )
    operations_parser.add_argument(
            '-c', '--count',
            action="store_true",
            help="update card count"
            )

    file_parser = argparse.ArgumentParser(
            description="Input files for edit command.",
            add_help=False
            )
    file_parser.add_argument(
            'infiles',
            type=str,
            nargs='+',
            help="path to existing JSON file(s)",
            default=sys.stdin
            )

    subparsers = main_parser.add_subparsers(
            dest="command",
            title='supported commands',
            description="Actions to perform on a deck.",
            help='see "deck.py [command] -h" for more details'
            )
    create_parser = subparsers.add_parser(
            'create',
            parents=[operations_parser],
            help="create a new deck",
            description="Creates a new deck and performs the actions specified by the optional arguments.",
            )
    edit_parser = subparsers.add_parser(
            'edit',
            parents=[operations_parser, file_parser],
            help="modify existing deck(s)",
            description="Modifies existing deck(s) according to the optional arguments.",
            )
    status_parser = subparsers.add_parser(
            'status',
            parents=[file_parser],
            help="show deck info",
            description="Shows information about existing decks.",
            )

    args = main_parser.parse_args()

    decks = []

    if args.command == "create":
        decks.append(create_deck())
    else:
        for infile in args.infiles:
            decks.append(get_deck(infile))

    for deck in decks:
        if args.command == "create" or args.command == "edit":
            print("Editing " + deck["pack"]["name"] + " ...")
            if args.add:
                deck = add_cards(deck)
            if args.fileimport:
                deck = import_cards(deck)
            if args.recommit:
                deck = recommit_deck(deck)
            if args.sort:
                deck = sort_cards(deck)
            if args.count:
                deck = count_cards(deck)
            write_deck(deck)
            print("Done!\n")
        elif args.command == "status":
            deck_info(deck)
        else:
            print("Invalid command!")

if __name__ == "__main__":
    main()
