#!/usr/bin/python3

from operator import itemgetter
import argparse
import json
import random
import string
import sys

#load deck dictionary from json file
def get_deck(filepath):
    with open(filepath) as json_file:
        return json.load(json_file)

#create deck dictionary
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

# interactive workflow framing the addition of cards
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
        if is_duplicate(content, color, deck) and skip_duplicate(content, deck):
            continue
        deck = add_card(content, color, deck);
        print("Added '" + content + "'")
    else:
        print("Added cards to " + deck["pack"]["name"] + "!")
        return(deck)

# interactive workflow for adding a single card
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

# interactive workflow for importing cards from files
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
                if is_duplicate(content, color, deck) and skip_duplicate(content, deck):
                    continue
                deck = add_card(content, color, deck);
        print("---")
        color = str(input("Done! Add further (b)lack, (w)hite or (n)o cards? ")).strip()
    else:
        print("Alright! Cards imported to " + deck["pack"]["name"] + "!")
        return(deck)

# normalize card content
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

# check if card is a duplicate with a given deck
def is_duplicate(content, color, deck):
    is_dupe = False
    if color == "w":
        for card in deck["white"]:
            if content == card:
                is_dupe = True
                print("White card '" + content + "' is a duplicate!")
                break
    elif color == "b":
        for card in deck["black"]:
            if content == card["content"]:
                is_dupe = True
                print("Black card '" + content + "' is a duplicate!")
                break
    return is_dupe

# ask user whether to keep or skip duplicate card
def skip_duplicate(content, deck):
    skip_dupe = False
    skip = "?"
    while skip != "y" or skip != "n":
        skip = str(input("Skip card (y/n)? ")).strip()
        if skip == "n":
            skip_dupe = False
            break
        elif skip == "y":
            skip_dupe = True
            break
        else:
            continue
    return skip_dupe

# check given deck for duplicate cards with another deck
# interactive workflow for duplicate deletion
def deduplicate(deck, refdeck):
    print("Checking '" + deck["pack"]["name"] + "' for duplicates with '" + refdeck["pack"]["name"] + "' ...")
    for blackcard in deck["black"]:
        if is_duplicate(blackcard["content"], "b", refdeck):
            delete = "?"
            while delete != "y" or delete != "n":
                delete = str(input("Delete card (y/n)? ")).strip()
                if delete == "y":
                    deck = delete_card(blackcard["content"], "b", deck)
                    break
                elif delete == "n":
                    break
                else:
                    continue
    for whitecard in deck["white"]:
        if is_duplicate(whitecard, "w", refdeck):
            delete = "?"
            while delete != "y" or delete != "n":
                delete = str(input("Delete card (y/n)? ")).strip()
                if delete == "y":
                    deck = delete_card(whitecard, "w", deck)
                    break
                elif delete == "n":
                    break
                else:
                    continue
    print("Deduplication complete!")
    return deck

# deletion of a single card in a given deck
def delete_card(content, color, deck):
    print("Deleting...")
    if color == "b":
        deck["black"][:] = [c for c in deck["black"] if c['content'] != content]
    else:
        deck["white"].remove(content)
    return deck

# sort cards in deck alphabetically
def sort_cards(deck):
    print("Sorting...")
    deck["black"] = sorted(deck["black"], key=itemgetter('content'))
    deck["white"].sort()
    print("Cards sorted!")
    return deck

# update the card count of a deck
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

# re-sanitize all cards of a deck
def recommit_deck(deck):
    print("Recommitting...")
    for blackcard in deck["black"]:
        blackcard["content"] = sanitize_content(blackcard["content"], "b")
    for whitecard in deck["white"]:
        whitecard = sanitize_content(whitecard, "w")
    print("Recommited!")
    return deck

# print some deck information
def deck_info(deck):
    print("Name: " + deck["pack"]["name"])
    print("ID: " + deck["pack"]["id"])
    print("Black cards: " + str(deck["quantity"]["black"]))
    print("White cards: " + str(deck["quantity"]["white"]))
    print("Total cards: " + str(deck["quantity"]["total"]))

# write deck dictionary to json file
def write_deck(deck):
    outfile = "./packs/" + deck["pack"]["id"] + ".json"
    f = open(outfile, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Wrote to " + outfile)

# print random cards from given decks
def play_round(decks, hands):
    blackcards = []
    whitecards = []
    for deck in decks:
        blackcards.extend(deck["black"])
        whitecards.extend(deck["white"])
    blackcard = random.choice(blackcards)
    if blackcard["pick"] * hands > len(whitecards):
        print("Not enough white cards available to play " + str(hands) + " hands for\n'" + blackcard["content"] + "'")
    else:
        print("Prompt:\n" + blackcard["content"] + "\n---")
        for i in range(hands):
            response = "Response " + str(i+1) + ":\n"
            for n in range(blackcard["pick"]):
                response += str(random.choice(whitecards)) + "\n"
            response += "---\n"
            print(response)

def main():
    # main argument parser
    main_parser = argparse.ArgumentParser(
            description="Handle allbadcards custom decks in JSON format.",
            )

    # parser for operation flags used in creation and editing
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

    # parent parser for multiple input files, used in several commands
    # (e.g. edit, status, play, deduplicate)
    infiles_parser = argparse.ArgumentParser(
            description="Input files for edit command.",
            add_help=False
            )
    infiles_parser.add_argument(
            'infiles',
            type=str,
            nargs='+',
            help="path to JSON file(s)",
            default=sys.stdin
            )

    # subparser for supported commands
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
            parents=[operations_parser, infiles_parser],
            help="modify existing deck(s)",
            description="Modifies existing deck(s) according to the optional arguments.",
            )
    dupe_parser = subparsers.add_parser(
            'deduplicate',
            help="remove duplicates with other deck(s)",
            description="Removes duplicates with other deck(s).",
            )
    # single input file (not to be confused with the one for multiple infiles!)
    # should be made a parent parser as soon as there are other commands that require
    # (exactly) one input file
    dupe_parser.add_argument(
            'infile',
            type=str,
            help="path to JSON file to check for duplicates",
            default=sys.stdin
            )
    # multiple reference files. should be made a parent parser as soon as there are other
    # commands requiring multiple reference files
    dupe_parser.add_argument(
            'reffiles',
            type=str,
            nargs='+',
            help="path to JSON file(s) to check against",
            default=sys.stdin
            )
    status_parser = subparsers.add_parser(
            'status',
            parents=[infiles_parser],
            help="show deck info",
            description="Shows information about existing decks.",
            )
    play_parser = subparsers.add_parser(
            'play',
            parents=[infiles_parser],
            help="plays random cards",
            description="Plays one black card and a number of responses from the specified deck(s)",
            )
    play_parser.add_argument(
            '-n', '--number',
            type=int,
            default=1,
            help="number of hands to be played"
            )

    args = main_parser.parse_args()

    # create or get deck(s) to operate on
    decks = []
    if args.command == "create":
        # create deck
        decks.append(create_deck())
    elif args.command == "deduplicate":
        # only one deck is sensible here
        decks.append(get_deck(args.infile))
    else:
        # multiple decks for all the other commands
        for infile in args.infiles:
            decks.append(get_deck(infile))

    if args.command == "play":
        # put all cards in big lists and play them
        play_round(decks, args.number)
    else:
        # loop through decks (even if there's just one in it)
        for deck in decks:
            if args.command == "create" or args.command == "edit":
                # operations only available for creation and editing
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
            elif args.command == "deduplicate":
                # loop through reference files for dupe check
                for filepath in args.reffiles:
                    deck = deduplicate(deck, get_deck(filepath))
                write_deck(deck)
                print("Done!\n")
            elif args.command == "status":
                deck_info(deck)

if __name__ == "__main__":
    main()
