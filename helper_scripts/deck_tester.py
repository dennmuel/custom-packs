import random
import argparse

def random_draw(n):
        
    with open('blacks.txt') as f:    
        black_data = f.readlines()

    with open('whites.txt') as f:    
        white_data = f.readlines()
    
    black_data = [x.strip() for x in black_data]
    white_data = [x.strip() for x in white_data]

    no_blacks = len(black_data)
    no_whites = len(white_data)

    inp = ""
    while inp == "":
        print("Black card:")
        print(" B --- ",black_data[random.randint(0,no_blacks-1)])

        print("\nWhite cards:")
        already_known = []
        while len(already_known)<n:
            current_ind = random.randint(0,no_whites-1)
            if current_ind in already_known:
                pass
            else:
                already_known = already_known + [current_ind]
            
        for ind in already_known:
            print(" W --- ",white_data[ind])

        inp = input("\nNext round? Press Enter! Otherwise something else + Enter!\n")
        
        print("===================================================")


# main argument parser
main_parser = argparse.ArgumentParser(
        description="Draws 1 black and n white cards from the files blacks.txt and whites.txt.",
        )

main_parser.add_argument(
        '-n', 
        type=int,
        default=6,
        help="number of white cards to be played"
        )

args = main_parser.parse_args()

random_draw(args.n)
