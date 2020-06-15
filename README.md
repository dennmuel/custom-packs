# Custom card packs for allbad.cards

## The Script
`deck.py` is a helper script that allows you to create, edit and test custom decks. It produces a JSON file you can upload to the custom pack editor at https://allbad.cards/packs/mine.

For instructions on supported commands and flags run `deck.py --help` and `deck.py [command] --help` respectively.

### Quickstart

Run `deck.py create -isc` to create a new deck, import cards from textfiles, sort them alphabetically and update the card count in an interactive workflow.

Add (and sort and count) cards to existing decks with `deck.py edit -asc ./packs/my-pack.json [./packs/my-other-pack.json ./packs/my-next-pack.json]`.

Files are saved to the `packs/` directory by default.

Test your packs by playing e.g. 5 random hands using `deck.py play -n 5 ./packs/my-*.json`

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

### Farts With Frank Brutality
Random collection deck for ideas from friends.

ABC pack code: Yk1skE31V

### Rejection Selection
Rejected cards from Schakal Edition.

ABC pack code: 56hm4kKGU
