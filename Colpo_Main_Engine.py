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
    
    print(f"Bluff check for card: {card}")
    print(f"Player's hand: {player.show_hand()}")

    actual_hand = player.show_hand()

    # Extract the first value from each tuple in the player's hand
    card_names_in_hand = [c[0] for c in actual_hand]

    if card not in card_names_in_hand:
        print("BLUFF!")
        return False

    # If player has the card
    print("No bluff detected.")
    return True

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
        for card_name, description in list(card_descriptions.items())[:-1]: #stop at Default since that ios always an option, not a Lie/bluff check eligible
            if card_name in hand_card_names:
                print(f"{card_name}: {description}")
            else:
                print(f"{card_name}: {description} (Lie)")
        print("Default : Draw 2 credits")

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
                
                if choice_index < 7 :
                    selected_card_name = list(card_descriptions.keys())[choice_index]
                    print(f"You selected: {selected_card_name} - {card_descriptions[selected_card_name]}")
                    return selected_card_name
                
                else:
                    print("Invalid choice, please choose an option you can use.")
            except (ValueError, IndexError):
                print("Invalid input, please enter a valid number.")

# Testing the Player class
def execute_action(card, player, other_players):
    if card == "Ambassador":
        player.add_card()
        print(f"{player} has drawn a new card.")
    elif card == "Assassin":
        if player.credits >= 3:
            target_player = select_target_player(other_players)
            target_card = target_player.show_hand()[0]  # Assumes you choose the first card to kill
            target_player.remove_card(target_card)
            player.update_credits(-3)
            print(f"{player} has assassinated one of {target_player}'s cards.")
        else:
            print(f"{player} doesn't have enough credits to use the Assassin.")
    elif card == "Contessa":
        print(f"{player} attempts to block the assassination. (Requires bluff check)")
        # Assuming there's a bluff check to handle this
    elif card == "Duke":
        player.update_credits(3)
        print(f"{player} has drawn 3 credits.")
    elif card == "Captain":
        if len(other_players) > 0:
            target_player = select_target_player(other_players)
            player.update_credits(2)
            target_player.update_credits(-2)
            print(f"{player} has stolen 2 credits from {target_player}.")
        else:
            print("No other players to steal from.")
    elif card == "Default":
        player.update_credits(2)
        print(f"{player} has drawn 2 credits.")
    else:
        print("Unknown action.")


def select_target_player(other_players):
    # This function selects a target player. For simplicity, we'll just return the first one.
    # You could extend this with input or a more complex selection mechanism.
    return other_players[0] if other_players else None


#Debug/Test Cases
"""
player1 = Player()

#create a second player for gampleay testing
player2 = Player()
other_players = [player2]
print("Here are player 1's cards:")
print(player1.show_hand())

# Updating credits
player1.update_credits(6)
print("Player 1's credits after adding 6:")
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

if selected_option != "Default":

    call_bluff = input("Do you want to bluff check? Enter 1 for yes, any other key for no: ")
    if call_bluff == "1":
        bluff_check(selected_option, player1)

execute_action(selected_option, player1, other_players)
"""

def main():
    # Create two players
    player1 = Player()
    player2 = Player()
    players = [player1, player2]

    print("Game Start!")
    print("Player 1's initial hand:", player1.show_hand())
    print("Player 2's initial hand:", player2.show_hand())

    # Game loop
    while True:
        for i, player in enumerate(players):
            other_players = [p for p in players if p != player]

            print(f"\nPlayer {i + 1}'s turn:")
            print(f"Player {i + 1}'s credits: {player.credits}")
            print(f"Player {i + 1}'s hand: {player.show_hand()}")
            #player.options()

            selected_option = player.select_option()
            print(f"Player {i + 1} selected: {selected_option}")

            if selected_option != "Default":
                call_bluff = input("Do you want to bluff check? Enter 1 for yes, any other key for no: ")
                if call_bluff == "1":
                    if not bluff_check(selected_option, player):
                        player.remove_card(player.show_hand()[0])
                        print(f"Player {i + 1} lost a card due to bluffing!")
                        if len(player.show_hand()) == 0:
                            print(f"Player {i + 1} is out of cards and loses the game!")
                            return

            execute_action(selected_option, player, other_players)

            # Check if any player is out of cards
            for j, p in enumerate(players):
                if len(p.show_hand()) == 0:
                    print(f"Player {j + 1} is out of cards and loses the game!")
                    return

if __name__ == "__main__":
    main()
