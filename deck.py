#!/usr/bin/python3

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
    name = str(input("Enter the name for the deck below:\n")).strip()
    deck = {
            "packName": name.title(),
            "blackCards": [],
            "whiteCards": []
            }
    return deck

# interactive workflow to manually add cards
def add_cards(deck):
    color = True
    newBlack = []
    newWhite = []
    while color:
        if color != "b" and color != "w":
            color = str(input("Add (b)lack or (w)hite cards? (Leave empty to exit.): ")).strip()
            continue
        print("Type in your card below or leave empty to change color.")
        card = type_card(color)
        if not card:
            color = True
            print("\n")
            continue
        if color == "b":
            cardtype = "blackCards"
            newlist = newBlack
        else:
            cardtype = "whiteCards"
            newlist = newWhite
        if (card in newlist or is_duplicate(card, color, deck)) and not add_duplicate(card):
                continue
        newlist.append(card)
        print("'" + card + "' will be added.\n")
    else:
        deck["blackCards"].extend(newBlack)
        deck["whiteCards"].extend(newWhite)
        print(str("\n" + str(len(newBlack)) + " new black and " + str(len(newWhite)) + " new white cards added!\n"))
        return(deck)

# prompt to type in a card
def type_card(color):
    card = False
    while not card:
        card = str(input("Card content: ")).strip()
        if not card:
            return False
        card = sanitize_content(card, color)
        if not card:
            continue
    return card

# import cards from files
def import_cards(deck, color, path):
    if color == "b":
        cardtype = "blackCards"
    else:
        cardtype = "whiteCards"
    with open(path) as p:
        while True:
            card = p.readline()
            if not card.strip():
                break
            card = sanitize_content(card, color)
            if not card:
                prompt = True
                while prompt != "s" or prompt != "r":
                    prompt = str(input("Should it be (r)ewritten or (s)kipped? ")).strip()
                    if prompt == "s":
                        print("Card skipped!\n")
                        break
                    elif prompt == "r":
                        print("Type in your rewritten card below.")
                        while not card:
                            card = type_card(color)
                        deck[cardtype].append(card)
                        print("Imported '" + card + "'\n")
                        break
            else:
                if is_duplicate(card, color, deck) and not add_duplicate(card):
                    continue
                deck[cardtype].append(card)
        print("Cards imported!\n")
        return(deck)

# normalize card content
def sanitize_content(content, color):
    content = content.strip()
    if not content:
        print("Card is empty.")
        return False
    if content[0].islower():
        content = content[0].upper() + content[1:]
    if color == "w":
        endswithchar = False
        for i in string.punctuation:
            if content.endswith(i):
                endswithchar = True
                break
        if endswithchar:
            print(content)
            print("This white card ends with punctuation. White cards usually don't.")
            keep = ""
            while keep != "y" and keep != "n":
                keep = str(input("Keep punctuation (y/n)? ")).strip()
                continue
            if keep == "n":
                content = content[:-1]
            print("\n")
    elif color == "b":
        if not "_" in content:
            print(content)
            print("This black card does not contain a '_' character.\nBlack cards must include as many blanks as it takes white cards to answer them.\n")
            content = False
    return content

# check if card is a duplicate with a given deck
def is_duplicate(content, color, deck):
    if color == "b":
        cardType = "blackCards"
    else:
        cardType = "whiteCards"
    for card in deck[cardType]:
        if content == card:
            return True
    return False

# ask user whether to keep or skip duplicate card
def add_duplicate(card):
    print("'" + card + "' is a duplicate.")
    while True:
        add = str(input("Add/keep it anyway (y/n)? ")).strip()
        if add == "y":
            print("Card added/kept!\n")
            return True
        elif add == "n":
            print("Card deleted/skipped!\n")
            return False

# check given deck for duplicate cards with another deck
# interactive workflow for duplicate deletion
def deduplicate(deck, refdeck):
    print("Checking for duplicates with '" + refdeck["packName"] + "' ...")
    for cardType in ["blackCards", "whiteCards"]:
        for card in deck[cardType]:
            if card in refdeck[cardType] and not add_duplicate(card):
                deck[cardType].remove(card)
                print("Card deleted from " + deck["packName"] + "!")
    print("Deduplication complete!\n")
    return deck

# sort cards in deck alphabetically
def sort_cards(deck):
    deck["blackCards"].sort()
    deck["whiteCards"].sort()
    return deck

# re-sanitize all cards of a deck
def revalidate_deck(deck):
    newdeck = deck
    for i in [{"color": "b", "cardtype": "blackCards", "array": []},
            {"color": "w", "cardtype": "whiteCards", "array": []}]:
        for card in deck[i["cardtype"]]:
            newdeck[i["cardtype"]] = i["array"]
            card = sanitize_content(card, i["color"])
            if not card:
                prompt = True
                while prompt != "d" or prompt != "r":
                    prompt = str(input("Should it be (r)ewritten or (d)eleted? ")).strip()
                    if prompt == "d":
                        print("Card deleted!\n")
                        break
                    elif prompt == "r":
                        print("Type in your rewritten card below.")
                        while not card:
                            card = type_card(i["color"])
                        print("Card changed to '" + card + "'\n")
                        break
            if is_duplicate(card, i["color"], newdeck) and not add_duplicate(card):
                continue
            i["array"].append(card)
        newdeck[i["cardtype"]] = i["array"]
    return newdeck

# print some deck information
def print_info(deck):
    print_separator()
    print(deck["packName"] + "\n")
    black = len(deck["blackCards"])
    white = len(deck["whiteCards"])
    total = black + white
    print("Black cards: " + str(black))
    print("White cards: " + str(white))
    print("Cards total: " + str(total))
    print("Card ratio: 1:" + str(round(white / black, 2)))
    print_separator()

# write deck dictionary to json file
def write_json(deck, filepath):
    f = open(filepath, "w")
    f.write(json.dumps(deck, indent=2))
    f.close
    print("Wrote to " + filepath)

# print random cards from given decks
def play_round(decks, hands):
    blackcards = []
    whitecards = []
    for deck in decks:
        blackcards.extend(deck["blackCards"])
        whitecards.extend(deck["whiteCards"])
    inp = ""
    while inp == "":
        blackcard = random.choice(blackcards)
        pick = blackcard.count("_")
        if pick * hands > len(whitecards):
            print("Not enough white cards available to play " + str(hands) + " hands for\n'" + blackcard + "'")
        else:
            print_separator()
            print("Black card:\n" + blackcard + "\n")
            already_drawn = []
            for i in range(hands):
                response = "Hand " + str(i+1) + ":\n"
                for n in range(pick):
                    whitecard = random.choice(whitecards)
                    while whitecard in already_drawn:
                        whitecard = random.choice(whitecards)
                    already_drawn.append(whitecard)
                    response += whitecard + "\n"
                print(response)
        print_separator()
        inp = str(input("Press Enter for another round. Otherwise type something else + Enter!\n"))

def print_separator():
    print("\n" + 50 * "=" + "\n")

def main():
    # establish command line arguments

    # main argument parser
    main_parser = argparse.ArgumentParser(
            description="Handle allbadcards custom decks in JSON format.",
            )

    # parent parser for flags used in create and edit operations
    operations_parser = argparse.ArgumentParser(
            add_help=False
            )
    operations_parser.add_argument(
            '-a', '--add',
            action="store_true",
            help="add cards to decks manually"
            )
    operations_parser.add_argument(
            '-b', '--blackcards',
            type=str,
            help="import black cards from given line separated file",
            default=sys.stdin
            )
    operations_parser.add_argument(
            '-w', '--whitecards',
            type=str,
            help="import white cards from given line separated file",
            default=sys.stdin
            )
    operations_parser.add_argument(
            '-r', '--revalidate',
            action="store_true",
            help="revalidate existing cards in decks (punctuation, capital letters, check for blanks, duplicates)",
            )
    operations_parser.add_argument(
            '-s', '--sort',
            action="store_true",
            help="sort cards alphabetically"
            )

    # parent parser for commands that accept multiple input files
    infiles_parser = argparse.ArgumentParser(
            add_help=False
            )
    infiles_parser.add_argument(
            'infiles',
            type=str,
            nargs='+',
            help="path to JSON file(s)",
            default=sys.stdin
            )

    # parent parser for a single input file (or path to save to)
    infile_parser = argparse.ArgumentParser(
            add_help=False
            )
    infile_parser.add_argument(
            'infile',
            type=str,
            help="path to a single JSON file",
            default=sys.stdin
            )

    # subparser for supported commands
    subparsers = main_parser.add_subparsers(
            dest="command",
            title='supported commands',
            help='see "deck.py [command] -h" for more details'
            )
    info_parser = subparsers.add_parser(
            'info',
            parents=[infiles_parser],
            help="show deck info",
            description="Shows information about decks.",
            )
    play_parser = subparsers.add_parser(
            'play',
            parents=[infiles_parser],
            help="play random cards",
            description="Plays one black card and a number of responses from the specified deck(s).",
            )
    play_parser.add_argument(
            '-n', '--number',
            type=int,
            default=3,
            help="number of responses to be played"
            )
    create_parser = subparsers.add_parser(
            'create',
            parents=[infile_parser, operations_parser],
            help="create a new deck",
            description="Creates a new deck and performs the actions specified by the optional arguments.",
            )
    edit_parser = subparsers.add_parser(
            'edit',
            parents=[operations_parser, infiles_parser],
            help="modify existing decks",
            description="Modifies existing decks according to the optional arguments.",
            )
    dupe_parser = subparsers.add_parser(
            'deduplicate',
            parents=[infile_parser],
            help="remove duplicates with other decks",
            description="Checks given deck for duplicates with other decks and allows deletion from said deck.",
            )
    dupe_parser.add_argument(
            'reffiles',
            type=str,
            nargs='+',
            help="path to JSON files to check against",
            default=sys.stdin
            )

    args = main_parser.parse_args()

    # get all filepaths to decks for commands that need to write files
    infiles = []
    if args.command == "create":
        # create empty deck and save it
        deck = create_deck()
        write_json(deck, args.infile)
        infiles.append(args.infile)
    elif args.command == "deduplicate":
        # only one deck is sensible here
        infiles.append(args.infile)
    else:
        # multiple decks for all the other commands
        infiles.extend(args.infiles)

    # get all the decks for non-writing commands
    decks = []
    for infile in infiles:
        decks.append(get_deck(infile))

    if args.command == "play":
        # put all deckstogether and draw random cards
        play_round(decks, args.number)
    elif args.command == "info":
        for deck in decks:
            print_info(deck)
    else:
        # commands that write to json file
        # loop through files, get deck, operate and save them
        for infile in infiles:
            print_separator()
            deck = get_deck(infile)
            print("Editing " + deck["packName"] + " ...\n")
            if args.command == "create" or args.command == "edit":
                if args.add:
                    print("Let's add some cards!\n")
                    deck = add_cards(deck)
                if type(args.blackcards) is str:
                    print("Importing black cards...\n")
                    deck = import_cards(deck, "b", args.blackcards)
                if type(args.whitecards) is str:
                    print("Importing white cards...\n")
                    deck = import_cards(deck, "w", args.whitecards)
                if args.revalidate:
                    print("Validating...\n")
                    deck = revalidate_deck(deck)
                if args.sort:
                    print("Sorting cards...\n")
                    deck = sort_cards(deck)
            elif args.command == "deduplicate":
                # loop through reference files for dupe check
                for reffile in args.reffiles:
                    if infile == reffile:
                        print("Not checking '" + deck["packName"] + "' with itself!\nUse 'deck.py edit -r " + infile + "' to do that.\n")
                    else:
                        deck = deduplicate(deck, get_deck(reffile))
            write_json(deck, infile)
            print_separator()

if __name__ == "__main__":
    main()
