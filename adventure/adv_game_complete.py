import random
from enum import Enum
from abc import ABC, abstractmethod


clues = [
    "There is a faded painting on the wall, depicting a great battle of the past.",
    "There is a worn-out diary, its pages filled with tales of epic voyages and harrowing adventures.",
    "There is a subtle draft coming from the wall, hinting at a hidden passage.",
    "There is a mysterious symbol etched into the floor, its meaning lost to time.",
    "There is a shattered mirror, reflecting a room that doesn't seem to exist.",
    "There is an ancient map, its destinations long forgotten.",
    "There is a cryptic inscription on the wall, its message obscured by the ravages of time.",
    "There is a haunting melody echoing through the room, its source unknown.",
    "There is a single feather, a remnant of a creature from a bygone era.",
    "There is a ghostly light flickering in the corner, its origin a mystery."
]


sense_exp = [
    "You see a flickering light in the distance, casting long shadows on the stone walls.",
    "You hear the distant echo of footsteps, but you can't tell where they're coming from.",
    "You smell the dampness of the stone and the faint scent of old parchment.",
    "You feel a cold draft, as if coming from a hidden passage.",
    "You sense an ancient presence, as if the castle itself is watching you.",
    "You see dust particles dancing in a beam of light from a tiny window.",
    "You hear the soft rustling of a tapestry, disturbed by an unseen force.",
    "You smell a sudden, sharp scent of rusted iron - the smell of old blood.",
    "You feel the rough texture of the stone walls, worn by time.",
    "You sense a sudden shift in the air, a change that you can't quite identify.",
    "You see a shadow move quickly across the room, but find no source for it.",
    "You hear a whispering echo, a wordless murmur that sends chills down your spine."
]


class RandomItemSelector:
    def __init__(self, items):
        self.items = items
        self.used_items = []

    def add_item(self, item):
        self.items.append(item)

    def pull_random_item(self):
        if not self.items:
            raise Exception("No items to select.")
        if not set(self.items) - set(self.used_items):
            self.reset()
        item = random.choice(list(set(self.items) - set(self.used_items)))
        self.used_items.append(item)
        return item

    def reset(self):
        self.used_items = []


class SenseClueGenerator:
    _instance = None

    def __new__(cls, clues, sense_exp):
        if cls._instance is None:
            cls._instance = super(SenseClueGenerator, cls).__new__(cls)
            cls._instance.clue_selector = RandomItemSelector(clues)
            cls._instance.sense_selector = RandomItemSelector(sense_exp)
        return cls._instance

    def get_senseclue(self):
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()
        return f"{clue} {sense}"
   

class EncounterOutcome(Enum):
    CONTINUE = 1
    END = 2


class Encounter(ABC):
    @abstractmethod
    def run_encounter(self):
        pass


class DefaultEncounter(Encounter):
    def __init__(self, clues, sense_exp):
        self.sense_clue_generator = SenseClueGenerator(clues, sense_exp)

    def run_encounter(self):
        sense_clue = self.sense_clue_generator.get_senseclue()
        print(sense_clue)
        return EncounterOutcome.CONTINUE


class Room:
    def __init__(self, name, encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self):
        outcome = self.encounter.run_encounter()
        if outcome == EncounterOutcome.END:
            return outcome
        else:
            return EncounterOutcome.CONTINUE
       

rooms = [
    Room("Throne Room", DefaultEncounter(clues, sense_exp)),
    Room("Library", DefaultEncounter(clues, sense_exp)),
    Room("Dungeon", DefaultEncounter(clues, sense_exp)),
    Room("Armory", DefaultEncounter(clues, sense_exp)),
    Room("Observatory", DefaultEncounter(clues, sense_exp)),
    Room("Royal Chamber", DefaultEncounter(clues, sense_exp))
]


class TreasureEncounter(Encounter):
    def run_encounter(self):
        print("You found the treasure! You have won the game.")
        return EncounterOutcome.END


class BlueWizardEncounter(Encounter):
    def run_encounter(self):
        choices = ['fireball', 'lightning bolt', 'ice shard']
        outcome = None

        while outcome is None:
            user_choice = input("Choose your spell: fireball, lightning bolt, or ice shard: ")
            wizard_choice = random.choice(choices)

            print(f"You cast {user_choice}, Blue Wizard casts {wizard_choice}.")

            if user_choice == wizard_choice:
                print("The spells collide, it's a draw! Cast again!")
            elif (user_choice == 'fireball' and wizard_choice == 'ice shard') or \
                 (user_choice == 'lightning bolt' and wizard_choice == 'fireball') or \
                 (user_choice == 'ice shard' and wizard_choice == 'lightning bolt'):
                print("Your spell overpowers the Blue Wizard's! You have defeated the wizard!")
                outcome = EncounterOutcome.CONTINUE
            else:
                print("The Blue Wizard's spell overwhelms you! You have been defeated!")
                outcome = EncounterOutcome.END

        return outcome
    

class RedWizardEncounter(Encounter):
    def run_encounter(self):
        choices = ['fireball', 'lightning bolt', 'ice shard', 'earthquake', 'summon familiar']
        win_conditions = {
            'fireball': ['ice shard', 'earthquake'],
            'lightning bolt': ['fireball', 'summon familiar'],
            'ice shard': ['lightning bolt', 'earthquake'],
            'earthquake': ['summon familiar', 'fireball'],
            'summon familiar': ['ice shard', 'lightning bolt']
        }

        while True:
            user_choice = input("Choose your spell: fireball, lightning bolt, ice shard, earthquake, summon familiar: ")
            wizard_choice = random.choice(choices)
            print(f"You cast {user_choice}, Red Wizard casts {wizard_choice}.")

            if user_choice == wizard_choice:
                print("It's a draw, play again!")
            elif user_choice in win_conditions[wizard_choice]:
                print("The Red Wizard's spell overpowers you! You have been defeated!")
                return EncounterOutcome.END
            else:
                print("Your spell overpowers the Red Wizard's! You have defeated the wizard!")
                return EncounterOutcome.CONTINUE


# add the treasure room to the list of rooms
rooms.append(Room("Treasure Room", TreasureEncounter()))

# add the blue wizard room to the list of rooms
rooms.append(Room("Blue Wizard Room", BlueWizardEncounter()))

# add the red wizard room to the list of rooms
rooms.append(Room("Red Wizard Room", RedWizardEncounter()))


class Castle:
    def __init__(self, rooms):
        self.room_selector = RandomItemSelector(rooms)

    def select_door(self):
        doors = random.randint(2, 4)
        print(f"\nThere are {doors} doors. Choose one.")

        while True:
            choice = input("Your choice: ")
            if choice.isdigit() and 1 <= int(choice) <= doors:
                break
            else:
                print("Invalid choice. Try again.")

    def next_room(self):
        self.select_door()
        room = self.room_selector.pull_random_item()
        print(f"\nYou have entered the {room.name}.")
        return room.visit_room()

    def reset(self):
        self.room_selector.reset()


class Game:
    def __init__(self, castle):
        self.castle = castle

    def play_game(self):
        print("Welcome to the Castle Maze Game!")
        print("Navigate through the castle and find the treasure to win the game.")

        while True:
            outcome = self.castle.next_room()
            if outcome == EncounterOutcome.END:
                print("Game Over!")
                self.castle.reset()
                play_again = input("Would you like to explore another castle? (yes/no): ")
                if play_again.lower() != "yes":
                    break


if __name__ == "__main__":
    game = Game(Castle(rooms))
    game.play_game()