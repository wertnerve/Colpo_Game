#Ambassador - get a new card
#Assasin - kill card for 3
#Contessa - block assasination
#Duke, draw 3 credits
#Captain - steal 2 coins


#Two cards in each persons hand
#Goal: get cards down to 0

#Actions
#Activate card
#Grab 2 money
#Coup for 7 money

import random

cards = {
    "Ambassador": 1,
    "Assassin": 2,
    "Contessa": 3,
    "Duke": 4,
    "Captain": 5
}

card_descriptions = {
    "Ambassador": "Get a new card",
    "Assassin": "Kill card for 3 credits",
    "Contessa": "Block assassination",
    "Duke": "Draw 3 credits",
    "Captain": "Steal 2 credits",
    "Default" : "Draw 2 credits"
}
#call bluff function
#each card needs an id

def bluff_check(card, player):
    
    print(card)
    print(player.show_hand())

    if card not in player.show_hand():
        print("BLUFF!")
        return False
    #if player has card
    return True 
    #if player does not have card
    return False

class Player:
    # Holds the current cards
    def __init__(self):
        self.cards = [self.generate_card(),self.generate_card()]
        self.credits = 0  # Initialize credits

    def show_hand(self):
        return self.cards

    def remove_card(self, card):
        for c in self.cards:
            if c == card:
                self.cards.remove(c)
                return
        print("Card not in hand")

    def generate_card(self):
        return random.choice(list(cards.items()))

    def add_card(self):
        new_card = self.generate_card()
        self.cards.append(new_card)

    def update_credits(self, amount):
        self.credits += amount

    def options(self):
        hand_card_names = [card[0] for card in self.cards]
        for card_name, description in card_descriptions.items():
            if card_name in hand_card_names:
                print(f"{card_name}: {description}")
            else:
                print(f"{card_name}: {description} (Lie)")

    def select_option(self):
        hand_card_names = [card[0] for card in self.cards]
        while True:
            print("\nSelect an option:")
            for index, (card_name, description) in enumerate(card_descriptions.items(), start=1):
                if card_name in hand_card_names or card_name == "Default":
                    print(f"{index}. {card_name}: {description}")
                else:
                    print(f"{index}. {card_name}: {description} (Lie)")
            choice = input("Enter the number of your choice: ")
            try:
                choice_index = int(choice) - 1
                selected_card_name = list(card_descriptions.keys())[choice_index]
                if selected_card_name in hand_card_names or selected_card_name == "Default":
                    print(f"You selected: {selected_card_name} - {card_descriptions[selected_card_name]}")
                    return selected_card_name
                else:
                    print("Invalid choice, please choose an option you can use.")
            except (ValueError, IndexError):
                print("Invalid input, please enter a valid number.")

# Testing the Player class


player1 = Player()
print("Here are player 1's cards:")
print(player1.show_hand())

# Updating credits
player1.update_credits(5)
print("Player 1's credits after adding 5:")
print(player1.credits)

player1.update_credits(-3)
print("Player 1's credits after subtracting 3:")
print(player1.credits)

# Showing options
print("Player 1's options:")
player1.options()
#
# Selecting an option
selected_option = player1.select_option()
print(f"Player 1 selected: {selected_option}")


call_bluff = input("Do you want to bluff check? 1 for yes, any other key for no")

if call_bluff == "1":
    bluff_check(selected_option, player1)