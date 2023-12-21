clues = [
    "There is a faded painting on the wall, depicting a great battle of the past.",
    "There is a worn-out diary, its pages filled with tales of epic voyages and harrowing adventures.",
    "There is a mysterious symbol etched into the floor, its origin lost to time.",
    "There is a subtle draft coming from the wall, hinting at hidden passages.",
    "There is a haunting melody echoing through the room, a remnant of a forgotten song.",
    "There is a cryptic inscription on the ceiling, its meaning shrouded in mystery.",
    "There is a shattered mirror, reflecting a past filled with turmoil and strife.",
    "There is a weathered statue, its features eroded by time, standing as a silent witness to history.",
    "There is a strange aura in the room, a lingering energy from a bygone era.",
    "There is a dusty tome on the shelf, its pages filled with cryptic runes and ancient lore."
]


sense_exp = [
    "You see shadows dancing on the walls, cast by the flickering torchlight.",
    "You hear the distant echo of footsteps, yet see no one.",
    "You smell the musty scent of old stone mixed with something unidentifiable.",
    "You feel a chill wind that seems to seep from the very walls themselves.",
    "You sense an unseen presence, watching from the shadows.",
    "You see a faint glow coming from a crack in the stone floor.",
    "You hear a soft whispering, but when you turn, there is nothing there.",
    "You smell a sudden, sharp scent of roses, though there are no flowers in sight.",
    "You feel a sudden warmth, like a brief touch on your arm.",
    "You sense a shift in the air, as if something just moved past you.",
    "You see a shadow pass over the window, but when you look, there's nothing flying in the sky.",
    "You hear the distant sound of a bell tolling, though there is no church nearby."
]


import random

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
    

from enum import Enum

class EncounterOutcome(Enum):
    CONTINUE = 1
    END = 2


from abc import ABC, abstractmethod

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
        result = self.encounter.run_encounter()
        if result == EncounterOutcome.END:
            return result
        elif result == EncounterOutcome.CONTINUE:
            # Add your logic here for what should happen when the encounter outcome is CONTINUE
            pass


rooms = [
    Room("Throne Room", DefaultEncounter(clues, sense_exp)),
    Room("Armory", DefaultEncounter(clues, sense_exp)),
    Room("Library", DefaultEncounter(clues, sense_exp)),
    Room("Dungeon", DefaultEncounter(clues, sense_exp)),
    Room("Observatory", DefaultEncounter(clues, sense_exp)),
    Room("Royal Chamber", DefaultEncounter(clues, sense_exp))
]


class Castle:
    def __init__(self, rooms):
        self.room_selector = RandomItemSelector(rooms)

    def select_door(self):
        num_doors = random.randint(2, 4)
        print(f"There are {num_doors} doors.")
        while True:
            door = input("Select a door (enter a number): ")
            if not door.isdigit() or not 1 <= int(door) <= num_doors:
                print("Invalid input. Please enter a valid door number.")
            else:
                return int(door)

    def next_room(self):
        self.select_door()
        room = self.room_selector.pull_random_item()
        print(f"You have entered the {room.name}.")
        return room.visit_room()

    def reset(self):
        self.room_selector.reset()


class Game:
    def __init__(self, rooms):
        self.castle = Castle(rooms)

    def play_game(self):
        print("Welcome to the Castle Adventure Game!")
        print("Your goal is to navigate the castle and find the treasure to win.")
        while True:
            result = self.castle.next_room()
            if result == EncounterOutcome.END:
                self.castle.reset()
                print("Game Over. You did not find the treasure.")
                play_again = input("Would you like to explore a different castle? (yes/no): ")
                if play_again.lower() != "yes":
                    break 