"""
CSSE1001 Assignment 2
Semester 2, 2020
"""

__author__ = "Mike Smith"
__email__ = "dongming.shi@uqconnect.edu.au"
__date__ = "28/09/2020"


# dungeon layout: max moves allowed
GAME_LEVELS_PATH = "./game_levels"
GAME_LEVEL_1 = "game1.txt"
GAME_LEVEL_2 = "game2.txt"
GAME_LEVEL_3 = "game3.txt"
GAME_LEVELS = {
    GAME_LEVEL_1: 7,
    GAME_LEVEL_2: 12,
    GAME_LEVEL_3: 19,
}

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {"W": (-1, 0), "S": (1, 0), "D": (0, 1), "A": (0, -1)}

INVESTIGATE = "I"
QUIT = "Q"
HELP = "H"

VALID_ACTIONS = [INVESTIGATE, QUIT, HELP]
VALID_ACTIONS.extend(list(DIRECTIONS.keys()))

HELP_MESSAGE = f"Here is a list of valid actions: {VALID_ACTIONS}"

INVALID = "That's invalid."

WIN_TEXT = "You have won the game with your strength and honour!"

LOSE_TEXT = "You have lost all your strength and honour."


def load_game(filename):
    """
    Create a 2D array of string representing the dungeon to display.

    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the
            dungeon.
    """
    dungeon_layout = []

    with open(filename, "r") as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)

    return dungeon_layout


class Display:
    """
    Display of the dungeon

    """

    def __init__(self, game_information, dungeon_size):
        """
        Construct a view of the dungeon.

        Parameters:
            game_information (dict<tuple<int, int>: Entity): Dictionary
                containing the position and the corresponding Entity
            dungeon_size (int): the width of the dungeon.

        """
        self._game_information = game_information
        self._dungeon_size = dungeon_size

    def display_game(self, player_pos):
        """
        Displays the dungeon.

        Parameters:
            player_pos (tuple<int, int>): The position of the Player

        """
        dungeon = ""

        for i in range(self._dungeon_size):
            rows = ""
            for j in range(self._dungeon_size):
                position = (i, j)
                entity = self._game_information.get(position)

                if entity is not None:
                    char = entity.get_id()
                elif position == player_pos:
                    char = PLAYER
                else:
                    char = SPACE
                rows += char
            if i < self._dungeon_size - 1:
                rows += "\n"
            dungeon += rows
        print(dungeon)

    def display_moves(self, moves):
        """
        Displays the number of moves the Player has left.

        Parameters:
            moves (int): THe number of moves the Player can preform.

        """
        print(f"Moves left: {moves}\n")


class GameLogic:
    """
    Creates the instances for all entities

    """

    def __init__(self, dungeon_name=GAME_LEVEL_1):
        """
        Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.

        """
        self._dungeon = load_game(f"{GAME_LEVELS_PATH}/{dungeon_name}")
        self._dungeon_size = len(self._dungeon)
        self._dungeon_name = dungeon_name

        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """
        Returns a list of tuples containing all positions of a given Entity type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            (list<tuple<int, int>>): Returns a list of tuples representing the
            positions of a given entity id.

        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def get_dungeon_size(self):
        """
        Gets the dungeon size
        Parameters: None
        Returns: Dungeon size

        """
        return self._dungeon_size

    def init_game_information(self):
        """
        Creates dictionary containing the initial game information
        Parameters: None
        Returns: Dictionary containing the initial game information

        """
        dictionary = {}
        x = 0
        for row in self._dungeon:
            y = 0
            for element in row:
                position = (x, y)
                if element == WALL:
                    dictionary[position] = Wall()
                elif element == KEY:
                    dictionary[position] = Key()
                elif element == DOOR:
                    dictionary[position] = Door()
                elif element == MOVE_INCREASE:
                    dictionary[position] = MoveIncrease()
                elif element == PLAYER:
                    self._player.set_position(position)
                y += 1
            x += 1
        return dictionary

    def get_game_information(self):
        """
        Gets the dictionary containing the game information
        Parameters: None
        Returns: Dictionary containing the game information

        """
        return self._game_information

    def get_player(self):
        """
        Gets the Player instance
        Parameters: None
        Returns: Player instance

        """
        return self._player

    def get_entity(self, position):
        """
        Gets entity at a given position
        Parameters: 'position' in the form of a tuple: (x,y)
        Returns: entity in the given position

        """
        dictionary = self._game_information
        try:
            return dictionary[position]
        except:
            return

    def get_entity_in_direction(self, direction):
        """
        Gets entity in a given direction
        Parameters: 'direction' in the form of an input command of type string:
            'W', 'A', 'S' or 'D'
        Returns: entity in the given direction

        """
        dictionary = self._game_information
        player_pos = self._player.get_position()
        y, x = player_pos
        if direction == "W":
            y = y - 1
        elif direction == "A":
            x = x - 1
        elif direction == "S":
            y = y + 1
        elif direction == DOOR:
            x = x + 1
        direction_pos = (y, x)
        try:
            return dictionary[direction_pos]
        except:
            return

    def collision_check(self, direction):
        """
        Checks if entity in direction can be collided with
        Parameters: 'direction' in the form of an input command of type string:
            'W', 'A', 'S' or 'D'
        Returns:
            True if the player is going to collide with an object in the given direction
            False if the player can travel in the given direction and will not collide

        """
        entity = self.get_entity_in_direction(direction)
        try:
            if not entity.can_collide():
                return True
            else:
                return False
        except:
            return False

    def new_position(self, direction):
        """
        Gets the new position of the player after it has moved in the given direction
        Parameters: 'direction' in the form of an input command of type string:
            'W', 'A', 'S' or 'D'
        Returns: new position of the player after it has moved in the given direction

        """
        player_pos = self._player.get_position()
        y, x = player_pos
        if direction == "W":
            y = y - 1
        elif direction == "A":
            x = x - 1
        elif direction == "S":
            y = y + 1
        elif direction == DOOR:
            x = x + 1
        return (y, x)

    def move_player(self, direction):
        """
        Moves the player in the given direction and updates the player's position
        Parameters: 'direction' in the form of an input command of type string:
            'W', 'A', 'S' or 'D'
        Returns: None

        """
        new_position = self.new_position(direction)
        self._player.set_position(new_position)

    def check_game_over(self):
        """
        Checks if the player has any moves remaining
        Parameters: None
        Returns:
            True if the player is out of moves
            False if the player still has moves remaining

        """
        moves_remaining = self._player.moves_remaining()
        if moves_remaining == 0:
            return True
        else:
            return False

    def set_win(self, win):
        """
        Sets the win status
        Parameters: 'win' in the form of a boolean
        Returns:
            True if the player has won
            False if the player has not won

        """
        if win == False:
            self._win = False
        else:
            self._win = True

    def won(self):
        """
        Gets the win status
        Parameters: None
        Returns: win status

        """
        return self._win


class Entity:
    """
    Sets collidability for all entities in game

    """

    def __init__(self):
        """
        Constructs the Entity class
        Sets the default collidability to True

        """
        self._collidable = True

    def get_id(self):
        """
        Get's the id for the Entity objects
        Parameters: None
        Returns: id for the Entity objects

        """
        return "Entity"

    def set_collide(self, collidable):
        """
        Updates the collidability for the Entity objects
        Parameters: 'collidable' in the form of a boolean
        Returns: None

        """
        self._collidable = collidable

    def can_collide(self):
        """
        Gets the collidability for the Entity objects
        Parameters: None
        Returns: collidability for the Entity objects

        """
        return self._collidable

    def __str__(self):
        """
        Returns Entity

        """
        return "Entity('Entity')"

    def __repr__(self):
        """
        Returns Entity

        """
        return str(self)


class Wall(Entity):
    """
    Defines the Wall class

    """

    def __init__(self):
        """
        Constructs the Wall class
        Sets the collidability to False

        """
        self._collidable = False

    def get_id(self):
        """
        Get's the id for the Wall objects
        Parameters: None
        Returns: id for the Wall objects

        """
        return WALL

    def __str__(self):
        """
        Returns Wall

        """
        return "Wall('#')"


class Item(Entity):
    """
    Defines the Item class

    """

    def on_hit(self, game):
        """
        Method not implemented

        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns Item

        """
        return "Item('Entity')"


class Key(Item):
    """
    Defines the Key class

    """

    def get_id(self):
        """
        Get's the id for the Key objects
        Parameters: None
        Returns: id for the Key objects

        """
        return KEY

    def on_hit(self, game):
        """
        Adds key object to player's inventory and removes it from game info
        Parameters: 'game' as an instance of GameLogic
        Returns: None

        """
        player = game.get_player()
        position = player.get_position()
        key = game.get_game_information().pop(position)
        player.add_item(key)

    def __str__(self):
        """
        Returns Key

        """
        return "Key('K')"


class MoveIncrease(Item):
    """
    Defines the MoveIncrease class

    """

    def __init__(self, moves=5):
        """
        Contructs the MoveIncrease class.
        Sets:
            'moves' to the number of move added, being the integer '5',
                which is passed in as a parameter
            'collidability' to True
        Parameters: 'moves' as an integer

        """
        self._moves = moves
        self._collidable = True

    def get_id(self):
        """
        Get's the id for the MoveIncrease objects
        Parameters: None
        Returns: id for the MoveIncrease objects

        """
        return MOVE_INCREASE

    def on_hit(self, game):
        """
        Adds move increase object to player's inventory, removes it from game info
        and increments the remaining number of moves
        Parameters: 'game' as an instance of GameLogic
        Returns: None

        """
        player = game.get_player()
        position = player.get_position()
        move_increase = game.get_game_information().pop(position)
        player.add_item(move_increase)
        player.change_move_count(self._moves)

    def __str__(self):
        """
        Returns MoveIncrease

        """
        return "MoveIncrease('M')"


class Door(Entity):
    """
    Defines the Door class

    """

    def get_id(self):
        """
        Get's the id for the Door objects
        Parameters: None
        Returns: id for the Door objects

        """
        return DOOR

    def on_hit(self, game):
        """
        Checks whether key object is in the player's inventory.
        If the key object is in the player's inventory, the game is won.
        else if the key object is not in the player's inventory,
        the player is informed of this and the game continues.
        Parameters: 'game' as an instance of GameLogic
        Returns: None

        """
        player = game.get_player()
        inventory = player.get_inventory()
        if inventory != []:
            for item in inventory:
                if item.get_id() == KEY:
                    game.set_win(True)
        else:
            game.set_win(False)
            print("You don't have the key!")

    def __str__(self):
        """
        Returns Door

        """
        return "Door('D')"


class Player(Entity):
    """
    Defines the Player class.
    Sets defaults for position, move count and inventory

    """

    def __init__(self, move_count):
        """
        Constructs the Player class.
        Sets:
            'move count' as an integer passed in as a parameter
            'inventory' to an empty list
            'collidable' to True
        Parameters: 'move count' in the form of an integer

        """
        self._move_count = move_count
        self._inventory = []
        self._collidable = True

    def get_id(self):
        """
        Get's the id for the Player objects
        Parameters: None
        Returns: id for the Player objects

        """
        return PLAYER

    def set_position(self, position):
        """
        Sets and updates the player's position
        Parameters: 'position' in the form of a tuple (x,y)
        Returns: None

        """
        self._position = position

    def get_position(self):
        """
        Gets the player's position
        Parameters: None
        Returns: player's position

        """
        try:
            return self._position
        except:
            return

    def change_move_count(self, number):
        """
        Updates the number of moves remaining for the player
        Parameters: 'number' in the form of an integer
        Returns: None

        """
        self._move_count += number

    def moves_remaining(self):
        """
        Gets the number of moves remaining for the player
        Parameters: None
        Returns: number of moves remaining for the player

        """
        return self._move_count

    def add_item(self, item):
        """
        Adds an item to the player's inventory
        Parameters: 'item' in the form of an object of an item
        Returns: None

        """
        self._inventory.append(item)

    def get_inventory(self):
        """
        Gets the player's inventory
        Parameters: None
        Returns: player's inventory

        """
        return self._inventory

    def __str__(self):
        """
        Returns Player

        """
        return "Player('O')"


class GameApp:
    """
    Defines the GameApp class.
    Communicates between GameLogic and Display

    """

    def __init__(self):
        """
        Constructs the GameApp class
        Sets:
            'game' as an instance of GameLogic
            'display' as an instance of Display
            'player' as an instance of Player called from GameLogic

        """
        self._game = GameLogic()
        self._display = Display(
            self._game.get_game_information(), self._game.get_dungeon_size()
        )
        self._player = self._game.get_player()

    def play(self):
        """
        Handles inputs from the user
        Parameters: None

        """
        self.draw()  # Initializes the display
        while True:
            input_action = input("Please input an action: ")  # Gets the input from user
            if (
                input_action == "W"
                or input_action == "A"
                or input_action == "S"
                or input_action == "D"
            ):
                try:  # Checks if there is a wall in the way
                    if (
                        self._game.get_entity_in_direction(input_action).get_id()
                        == WALL
                    ):
                        print(INVALID)
                    else:
                        self._game.move_player(input_action)
                except:
                    self._game.move_player(input_action)
                self._player.change_move_count(-1)
            elif input_action == HELP:
                print(HELP_MESSAGE)  # Displays help message
            elif input_action == QUIT:
                while True:
                    input_quit = input("Are you sure you want to quit? (y/n): ")
                    if input_quit == "y":
                        return  # Quits Game
                    elif input_quit == "n":
                        break
                    else:
                        pass
            elif (
                input_action == "I W"
                or input_action == "I A"
                or input_action == "I S"
                or input_action == "I D"
            ):
                substrings = str.split(input_action, SPACE)
                try:  # Gets the direction that user wants to investigate
                    entity = self._game.get_entity_in_direction(substrings[1])
                    if (
                        entity.get_id() == KEY
                        or entity.get_id() == DOOR
                        or entity.get_id() == MOVE_INCREASE
                        or entity.get_id() == WALL
                    ):
                        print(f"{entity} is on the {substrings[1]} side.")
                except:
                    print(f"None is on the {substrings[1]} side.")
                self._player.change_move_count(-1)
            else:
                print("That's invalid.")

            pos = self._player.get_position()
            game_info = self._game.get_game_information()
            try:  # checks if the player has collided with another entity
                if (
                    game_info[pos].get_id() == KEY
                    or game_info[pos].get_id() == DOOR
                    or game_info[pos].get_id() == MOVE_INCREASE
                ):
                    game_info[pos].on_hit(self._game)
                    if self._game.won():
                        print(WIN_TEXT)
                        break  # Player has won
                    else:
                        pass
            except:
                pass

            if (
                self._player.moves_remaining() == 0
            ):  # Checks if the player has moves remaining
                print(LOSE_TEXT)
                break  # Player has lost
            else:
                self.draw()  # Reprints the display

    def draw(self):
        """
        Creates the display information for the Display object
        Parameters: None
        Returns: None

        """
        self._display.display_game(self._player.get_position())
        self._display.display_moves(self._player.moves_remaining())


def main():
    game_app = GameApp()
    game_app.play()


if __name__ == "__main__":
    main()
