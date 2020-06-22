# Custom card packs for allbad.cards

## The Script
`deck.py` is a helper script that allows you to create, edit and test custom decks. It produces a JSON file you can upload to the custom pack editor at https://allbad.cards/packs/mine.

Features include:

- import cards from line separated textfiles
- add cards manually in an interactive workflow
- check look and sanity of added or already existing cards (e.g. if black cards have blanks)
- check if added cards are duplicates
- check a single deck for duplicates with several other decks
- sorting cards alphabetically
- test your deck with random drawn cards
- show info about decks

For instructions on all supported commands and flags run `deck.py --help` and `deck.py [command] --help` respectively.

### Quickstart

To create a new deck and import your black and white cards run

`deck.py create my-deck.json -b my-black-cards.txt -w my-white-cards.txt`

To add cards to all your existing decks run

`deck.py edit -a my-deck.json [my-other-deck.json my-foobar-deck.json]`.

Test your packs by playing e.g. 5 random hands via `deck.py play -n 5 .my-*.json`

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

### Nerds With Turds
IT-themed expansion pack fueled by frustration.

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
