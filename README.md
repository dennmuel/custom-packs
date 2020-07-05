# Custom card packs for allbad.cards

## The Packs
See `CONTRIBUTING.md` for writing tips.

### Schakal Edition
A handmade allround deck carefully crafted by yours truly, Der Schakal.
This deck was designed to both work standalone as well as integrate well with other packs.

ABC pack code: VRRCeJAWJ

### A Handmaid's Fail
KeGro's potpourri of allround madness - because women can be inhuman, too!

ABC pack code: HWpLb4zCn

### Bearded Pack
Beard-themed expansion pack made by some friends and lovers of facial hair.

ABC pack code: 1nMOZB6wn

### Code Against Humanity
IT-themed expansion pack.

ABC pack code: ZjnhXwI-w

### Chords Against Humanity
Music-themed expansion pack.

ABC pack code: OyeZBfx4j

### Farts With Frank Brutality
Random collection deck for ideas from friends.

ABC pack code: Yk1skE31V

### Rejection Selection
Rejected cards from Schakal Edition.

ABC pack code: 56hm4kKGU


## The Script
`deck.py` is a helper script that allows you to handle your custom packs. It produces a JSON file you can upload to the custom pack editor at https://allbad.cards/packs/mine.

### Features

- create new packs or edit existing ones
- import cards from textfiles or add them manually
- check cards for duplicates and sanity
- check pack for duplicates with other packs
- play random cards
- show card count and ratio

### Quickstart

Create a new deck and import your black and white cards:

    deck.py create packs/my-deck.json -b my-black-cards.txt -w my-white-cards.txt

Add cards to a deck and sort them alphabetically:

    deck.py edit -as packs/my-deck.json

The `create` and `edit` commands share the same flags, so you can also import cards to an existing deck or add them manually to a new deck.

Test your pack by playing 5 random hands:

    deck.py play -n 5 packs/my-deck.json

For instructions on all supported commands and flags run `deck.py --help` and `deck.py [command] --help` respectively.
