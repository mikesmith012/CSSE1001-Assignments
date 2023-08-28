"""
CSSE1001 Assignment 3
Semester 2, 2020
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


__author__ = "Mike Smith"
__email__ = "dongming.shi@uqconnect.edu.au"
__date__ = "30/10/2020"


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

DIRECTIONS = {"w": (-1, 0), "s": (1, 0), "d": (0, 1), "a": (0, -1)}

INVESTIGATE = "I"
QUIT = "Q"
HELP = "H"

VALID_ACTIONS = [INVESTIGATE, QUIT, HELP, *DIRECTIONS.keys()]

HELP_MESSAGE = f"Here is a list of valid actions: {VALID_ACTIONS}"

INVALID = "That's invalid."

WIN_TEXT = "You have won the game with your strength and honour!"
LOSE_TEXT = "You have lost all your strength and honour."

TASK_ONE = "TASK_ONE"
TASK_TWO = "TASK_TWO"

TITLE = "Key Cave Adventure Game"

WIN = "You Won!"
LOSE = "You Lose!"

PLAY_AGAIN = "Would you like to play again?"
FINISH = "You have finished the level!"
FINISH_SCORE = "You have finished the level with a score of "

IMAGES_PATH = "./images"
IMAGES = {
    "clock": f"{IMAGES_PATH}/clock.png",
    "door": f"{IMAGES_PATH}/door.png",
    "empty": f"{IMAGES_PATH}/empty.png",
    "key": f"{IMAGES_PATH}/key.png",
    "lightning": f"{IMAGES_PATH}/lightning.png",
    "lives": f"{IMAGES_PATH}/lives.png",
    "move increase": f"{IMAGES_PATH}/move_increase.png",
    "player": f"{IMAGES_PATH}/player.png",
    "wall": f"{IMAGES_PATH}/wall.png",
}


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
        for line in file:
            line = line.strip()
            dungeon_layout.append(list(line))

    return dungeon_layout


class Entity:
    """
    Sets collidability for all entities in game

    """

    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with

        """
        self._collidable = True

    def get_id(self):
        """
        Get's the id for the Entity objects
        Parameters: None
        Returns: id for the Entity objects (string)

        """
        return self._id

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
        Returns: collidability for the Entity objects (boolean)

        """
        return self._collidable

    def __str__(self):
        """
        Returns Entity

        """
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        """
        Returns Entity

        """
        return str(self)


class Wall(Entity):
    """
    Defines the Wall class

    """

    _id = WALL

    def __init__(self):
        """
        Constructs the Wall class
        Sets the collidability to False

        """
        super().__init__()
        self.set_collide(False)


class Item(Entity):
    """
    Defines the Item class

    """

    def on_hit(self, game):
        """
        Method not implemented

        """
        raise NotImplementedError


class Key(Item):
    """
    Defines the Key class

    """

    _id = KEY

    def on_hit(self, game):
        """
        Adds key object to player's inventory and removes it from game info
        Parameters: 'game' as an instance of GameLogic
        Returns: None

        """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())


class MoveIncrease(Item):
    """
    Defines the MoveIncrease class

    """

    _id = MOVE_INCREASE

    def __init__(self, moves=5):
        """
        Contructs the MoveIncrease class.
        Sets:
            'moves' to the number of move added, being the integer '5',
                which is passed in as a parameter
            'collidability' to True
        Parameters: 'moves' as an integer

        """
        super().__init__()
        self._moves = moves

    def on_hit(self, game):
        """
        Adds move increase object to player's inventory, removes it from game info
        and increments the remaining number of moves
        Parameters: 'game' as an instance of GameLogic
        Returns: None

        """
        player = game.get_player()
        player.change_move_count(self._moves)
        game.get_game_information().pop(player.get_position())


class Door(Entity):
    """
    Defines the Door class

    """

    _id = DOOR

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
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game.set_win(True)
                return
        # print("You don't have the key!")


class Player(Entity):
    """
    Defines the Player class.
    Sets defaults for position, move count and inventory

    """

    _id = PLAYER

    def __init__(self, move_count):
        """
        Constructs the Player class.
        Sets:
            'move count' as an integer passed in as a parameter
            'inventory' to an empty list
            'collidable' to True
        Parameters: 'move count' in the form of an integer

        """
        super().__init__()
        self._move_count = move_count
        self._inventory = []
        self._position = None

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
        Returns: player's position (tuple)

        """
        return self._position

    def set_move_count(self, number):
        self._move_count = number

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
        Returns: number of moves remaining for the player (int)

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
        """Gets the player's inventory
        Parameters: None
        Returns: player's inventory

        """
        return self._inventory


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
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """
        Returns a list of tuples containing all positions of a given Entity type.
        Parameters:
            entity (str): the id of an entity.
        Returns:
            list<tuple<int, int>>): Returns a list of tuples representing the
            positions of a given entity id.

        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))
        return positions

    def init_game_information(self):
        """
        Creates dictionary containing the initial game information
        Parameters: None
        Returns: Dictionary containing the initial game information

        """
        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)

        self._player.set_position(player_pos)

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

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
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """
        Gets entity in a given direction
        Parameters: 'direction' in the form of an input command of type string:
            'W', 'A', 'S' or 'D'
        Returns: entity in the given direction

        """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self):
        """
        Gets the dictionary containing the game information
        Parameters: None
        Returns: Dictionary containing the game information

        """
        return self._game_information

    def get_dungeon_size(self):
        """
        Gets the dungeon size
        Parameters: None
        Returns: Dungeon size (int)

        """
        return self._dungeon_size

    def move_player(self, direction):
        """
        Moves the player in the given direction and updates the player's position
        Parameters: 'direction' in the form of an input command of type string:
            'w', 'a', 's' or 'd'
        Returns: None

        """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): a direction for the player to travel in.
        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.

        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True
        return not (
            0 <= new_pos[0] < self._dungeon_size
            and 0 <= new_pos[1] < self._dungeon_size
        )

    def new_position(self, direction):
        """
        Gets the new position of the player after it has moved in the given direction
        Parameters: 'direction' in the form of an input command of type string:
            'w', 'a', 's' or 'd'
        Returns: new position of the player after it has moved in the given direction

        """
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """
        Checks if the player has any moves remaining
        Parameters: None
        Returns:
            True if the player is out of moves
            False if the player still has moves remaining

        """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """
        Sets the win status
        Parameters: 'win' in the form of a boolean
        Returns:
            True if the player has won
            False if the player has not won

        """
        self._win = win

    def won(self):
        """
        Gets the win status
        Parameters: None
        Returns: win status (boolean)

        """
        return self._win


class GameApp:
    """
    Defines the GameApp class.
    Communicates between GameLogic and Display

    """

    def __init__(self, master, task, dungeon_name):
        """
        Initialises the GameApp class
        Parameters
            master: the root window
            task: the specified task (string)
            dungeon_name: the name of the dungeon (string)

        """
        self._master = master
        self._task = task
        self._dungeon_name = dungeon_name

        # Creates Title Label
        self._title = tk.Label(self._master, text=TITLE, bg="light green", font=20)
        self._title.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        # Creates Game Frame
        self._game_frame = tk.Frame(self._master, bg="white")
        self._game_frame.pack(side=tk.TOP)

        # Sets GameLogic instance & game information
        self._game = GameLogic(self._dungeon_name)
        self._size = self._game.get_dungeon_size()
        self._game_info = self._game.get_game_information()

        # Sets player instance & position
        self._player = self._game.get_player()
        self._player_pos = self._player.get_position()

        # Creates & draws keyPad
        self._keypad = KeyPad(self._game_frame, width=200, height=100, bg="white")
        self._keypad.pack(side=tk.RIGHT)
        self._keypad.bind("<Button-1>", self.button_press)
        self._keypad.draw_keypad()

        # Selects the corresponding task
        if self._task == TASK_ONE:
            self.task_1()
        elif self._task == TASK_TWO:
            self.task_2()

    def move_player(self, direction, task):
        """
        Moves the player in the direction specified
        Updates the moves remaining label for task 2
        Parameters
            direction: the direction in which the player moves (str)
            task: the specified task (str)
        Returns: None

        """
        # Decrements the player's move count
        self._player.change_move_count(-1)
        self._moves_remaining = self._player.moves_remaining()

        # Updates the status bar if task is set to task 2
        if task == TASK_TWO:
            self._status_bar.update_moves(self._moves_remaining)

        # Checks collidability, moves player & redraws the dungeon map
        if not self._game.collision_check(direction):
            self._game.move_player(direction)
            player_pos = self._player.get_position()
            self._dungeon_map.delete(tk.ALL)
            self._dungeon_map.draw_grid(self._game_info, player_pos)

            # Checks collision with Key, MoveIncrease or Door
            if player_pos in self._game_info:
                item = self._game_info[player_pos]
                if item.get_id() == "K" or item.get_id() == "M" or item.get_id() == "D":
                    item.on_hit(self._game)

                # Checks if game has been won
                if self._game.won():
                    self.win()

        # Checks if game has been lost
        if self._player.moves_remaining() == 0:
            self.lose()

    def button_press(self, event):
        """
        Moves the player in the corresponding direction of the keypad press
        Method is called when the keypad is pressed
        Returns: None

        """
        # Translates pixel position to corresponding direction
        position = (event.x, event.y)
        direction = self._keypad.pixel_to_direction(position)

        # Checks that a valid direction on keypad has been pressed
        if direction in DIRECTIONS:
            self.move_player(direction, self._task)

    def key_press(self, event):
        """
        Moves the player in the corresponding direction of the keyboard press
        Method is called when the keyboard is pressed
        Returns: None

        """
        # Checks that a valid direction on keyboard has been pressed
        direction = event.char
        if direction in DIRECTIONS:
            self.move_player(direction, self._task)

    def task_1(self):
        """
        Draws the dungeon map based on task one specifications
        Parameters: None
        Returns: None

        """
        # Creates and draws the dungeon map
        self._dungeon_map = DungeonMap(
            self._game_frame, (self._size, self._size), width=600, bg="light grey"
        )
        self._dungeon_map.pack(side=tk.LEFT)
        self._dungeon_map.draw_grid(self._game_info, self._player_pos)

    def task_2(self):
        """
        Draws the dungeon map based on task two specifications
        Parameters: None
        Returns: None

        """
        # Creates and draws the dungeon map
        self._dungeon_map = AdvancedDungeonMap(
            self._game_frame, (self._size, self._size), width=600, bg="light grey"
        )
        self._dungeon_map.pack(side=tk.LEFT)
        self._dungeon_map.draw_grid(self._game_info, self._player_pos)

        # Creates the status bar
        self._status_bar = StatusBar(self._master, self, self._player, bg="white")
        self._status_bar.pack(expand=1, fill=tk.X)

        # Creates the menubar
        self._menubar = tk.Menu(self._master)
        self._master.config(menu=self._menubar)

        # Creates the filemenu
        self._filemenu = tk.Menu(self._menubar)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

        # Creates the methods inside the filemenu
        self._filemenu.add_command(label="Save game", command=self.save_game)
        self._filemenu.add_command(label="Load game", command=self.load_game)
        self._filemenu.add_command(label="New game", command=self.new_game)
        self._filemenu.add_command(label="Quit", command=self.quit)

        # Sets the default filemane to None
        self._filename = None

    def win(self):
        """
        Shows the corresponding messagebox if the player has won
        Method is called if game has been won
        Returns: None

        """
        # Checks the task and shows the corresponding messagebox
        if self._task == TASK_TWO:
            ans = messagebox.askokcancel(WIN, FINISH)
            if ans:
                self._master.destroy()
        elif self._task == TASK_TWO:
            ans = messagebox.askyesno(
                WIN,
                FINISH_SCORE + str(self._status_bar.get_score()) + ".\n\n" + PLAY_AGAIN,
            )
            if not ans:
                self._master.destroy()
            else:
                self.new_game()
                self._status_bar.update_timer()

    def lose(self):
        """
        Shows the corresponding messagebox if the player has won
        Method is called if game has been won
        Returns: None

        """
        # Checks the task and shows the corresponding messagebox
        if self._task == TASK_ONE:
            ans = messagebox.askokcancel(LOSE, "Quit?")
            if ans:
                self._master.destroy()
        elif self._task == TASK_TWO:
            ans = messagebox.askyesno(LOSE, PLAY_AGAIN)
            if not ans:
                self._master.destroy()
            else:
                self.new_game()

    def quit(self):
        """
        Quits the game
        Parameters: None
        Returns: None

        """
        # Destroys the window if user decides to quit
        ans = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if ans:
            self._master.destroy()

    def new_game(self):
        """
        Creates a new game
        Parameters: None
        Returns: None

        """
        # Creates new instance of GameLogic
        self._game = GameLogic(self._dungeon_name)
        self._game_info = self._game.get_game_information()

        # Redraws the new game map
        self._dungeon_map.delete(tk.ALL)
        self._dungeon_map.draw_grid(self._game_info, self._player_pos)

        # Sets the new player
        self._player = self._game.get_player()
        self._moves_remaining = self._player.moves_remaining()

        # Resets the status bar information
        self._status_bar.update_moves(self._moves_remaining)
        self._status_bar.init_timer(0, -1)

    def get_win(self):
        """
        Returns the win status of the player
        Parameters: None
        Returns: win status (bool)

        """
        return self._win

    def save_game(self):
        """
        Saves the game to a .txt file
        Parameters: None
        Returns: None

        """
        # Gets the player information
        self._player = self._game.get_player()

        # Sets the filename
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if filename:
                self._filename = filename

        # writes the game information to the file
        if self._filename:
            self._master.title(self._filename)
            file = open(self._filename, "w")
            file.write(self._filename + "\n")  # line 1: filename
            file.write(
                str(self._status_bar.get_score()).strip("()") + "\n"
            )  # line 2: timer
            file.write(
                str(self._player.get_position()).strip("()") + "\n"
            )  # line 3: player position
            file.write(
                str(self._status_bar.moves_remaining()) + "\n"
            )  # line 4: moves remaining
            file.write(
                str(len(self._player.get_inventory())) + "\n"
            )  # line 5: player inventory
            dungeon = ""
            for i in range(self._size):
                rows = ""
                for j in range(self._size):
                    position = (i, j)
                    entity = self._game_info.get(position)
                    if entity is not None:
                        char = entity.get_id()
                    elif position == self._player.get_position():
                        char = PLAYER
                    else:
                        char = SPACE
                    rows += char
                if i < self._size - 1:
                    rows += "\n"
                dungeon += rows
            file.write(dungeon)
            file.close()

    def load_game(self):
        """
        Loads a previously saved game
        Parameters: None
        Returns: None

        """
        # Opens the file corresponding to the filename
        filename = filedialog.askopenfilename()

        # Reads the information from the file
        if filename:
            self._filename = filename
            self._master.title(self._filename)
            file = open(filename, "r")
            lines = file.readlines()
            line_num = 1
            for line in lines:
                if line_num == 1:
                    pass
                elif line_num == 2:
                    time = int(line)
                    self._status_bar.init_timer(time // 60, time % 60)
                elif line_num == 3:
                    pos = (line,)
                    self._player.set_position(pos)
                elif line_num == 4:
                    moves = int(line)
                    self._player.set_move_count(moves)
                elif line_num == 5:
                    if line == "1":
                        pass
                    else:
                        pass
                else:
                    pass
                line_num += 1
            file.close()


class StatusBar(tk.Frame):
    """
    Defines the statusbar class
    Inherits from tk.Frame

    """

    def __init__(self, master, app, player, bg):
        """
        Initialises the statusbar class
        Parameters
            master: the root window
            app: the instance of GameApp
            player: the instance of the player
            bg: background colour of the frame

        """
        super().__init__(master, bg=bg)
        self._master = master
        self._player = player
        self._app = app

        # Creates image variables for the statusbar
        clock_im = Image.open(IMAGES["clock"])
        clock_im = clock_im.resize((50, 50))
        clock_tk = ImageTk.PhotoImage(clock_im)
        lightning_im = Image.open(IMAGES["lightning"])
        lightning_im = lightning_im.resize((50, 50))
        lightning_tk = ImageTk.PhotoImage(lightning_im)

        # Creates the buttons frame with its buttons
        self._button_frame = tk.Frame(self, bg="white")
        self._button_frame.pack(side=tk.LEFT, expand=1)
        self._new_game_button = tk.Button(
            self._button_frame, text="New Game", bg="white", command=self._app.new_game
        )
        self._new_game_button.pack()
        self._quit_button = tk.Button(
            self._button_frame, text="Quit", bg="white", command=self._app.quit
        )
        self._quit_button.pack()

        # Creates the timer frame with its timer label
        self._time_frame = tk.Frame(self, bg="white")
        self._time_frame.pack(side=tk.LEFT, expand=1)
        self._clock_label = tk.Label(self._time_frame, image=clock_tk, bg="white")
        self._clock_label.photo = clock_tk
        self._clock_label.pack(side=tk.LEFT)
        self._time_elapsed = tk.Label(
            self._time_frame, text="Time elapsed", font=12, bg="white"
        )
        self._time_elapsed.pack()
        self._min = 0
        self._sec = -1
        self.init_timer(self._min, self._sec)
        self._timer = tk.Label(
            self._time_frame,
            text=str(self._min) + "m " + str(self._sec) + "s",
            bg="white",
        )
        self._timer.pack()
        self.update_timer()

        # Creates the moves frame with the moves remaining label
        self._moves_frame = tk.Frame(self, bg="white")
        self._moves_frame.pack(side=tk.LEFT, expand=1)
        self._lightning_label = tk.Label(
            self._moves_frame, image=lightning_tk, bg="white"
        )
        self._lightning_label.photo = lightning_tk
        self._lightning_label.pack(side=tk.LEFT)
        self._moves_left = tk.Label(
            self._moves_frame, text="Moves left", font=12, bg="white"
        )
        self._moves_left.pack()
        self._moves_label = tk.Label(
            self._moves_frame,
            text=str(self.moves_remaining()) + " moves remaining",
            bg="white",
        )
        self._moves_label.pack()

    def moves_remaining(self):
        """
        Returns the moves remaining
        Parameters: None
        Returns: Number of moves remaining (int)

        """
        return self._player.moves_remaining()

    def update_moves(self, position):
        """
        Updates the moves remaining
        Parameters: position
        Returns: None

        """
        self._moves_label.config(text=str(position) + " moves remaining", bg="white")

    def init_timer(self, minute, sec):
        """
        Initialises the timer
        Parameters
            minute: number of minutes passed (int)
            sec: number of seconds passed (int)
        Returns: None

        """
        self._min = minute
        self._sec = sec

    def update_timer(self):
        """
        Updates the timer label
        Parameters: None
        Returns: None

        """
        # Checks if game has been won. If so, the timer will be paused
        if self._app._game.won():
            self._timer.config(text=str(self._min) + "m " + str(self._sec) + "s")
        else:
            self._sec += 1
            if self._sec == 60:
                self._min += 1
                self._sec = 0
            self._timer.config(text=str(self._min) + "m " + str(self._sec) + "s")
            self._master.after(1000, self.update_timer)

    def get_score(self):
        """
        Gets the score for the player
        Parameters: None
        Returns: the player's score (int)

        """
        return 60 * self._min + self._sec


class AbstractGrid(tk.Canvas):
    """
    An abstract version of the dungeon map and keypad
    Inherits from tk.Canvas

    """

    def __init__(self, master, rows, cols, width, height, bg):
        """
        Initialises the abstract grid class
        Parameters
            master: the root window
            rows: the number of rows (int)
            cols: the number of columns (int)
            width: the width of the game map (int)
            height: the height of the game map (int)
            bg: the background colour of the canvas (str)

        """
        super().__init__(master, width=width, height=height, bg=bg)
        self._width = width
        self._height = height

        self._cols = cols
        self._rows = rows

        self._x = self._width // self._cols
        self._y = self._height // self._rows

    def get_bbox(self, position):
        """
        Returns the bounding box for the (row, col) position
        Parameters
            position: the position of interest (int, int)
        Returns: the bounding box of given position ((int, int), (int, int))

        """
        x = position[0]
        y = position[1]
        i = (x * self._x, y * self._y)
        j = ((x + 1) * self._x, (y + 1) * self._y)
        return (i, j)

    def pixel_to_position(self, pixel):
        """
        Converts the x, y pixel position (in graphics units) to a (row, col) position for x, y in pixel
        Parameters
            pixel: the position of the pixel (int, int)
        Returns: the position of the corresponding pixel (int, int)

        """
        pos_x = pixel[0] // self._x
        pos_y = pixel[1] // self._y
        return (pos_x, pos_y)

    def get_position_centre(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the given (row, col) position
        Parameters
            position: the position of interest (int, int)
        Returns: the central position (int, int)

        """
        x1, y1 = position[0]
        x2, y2 = position[1]
        i = (x1 + x2) / 2
        j = (y1 + y2) / 2
        return (i, j)

    def annotate_position(self, position, text):
        """
        Annotates the cell at the given (row, col) position with the provided text
        Parameters
            position: the position of interest (int, int)
            text: the text that is to be written (str)
        returns: the annotation at the given position with the corresponding text

        """
        centre_pos = self.get_position_centre(position)
        annotation = self.create_text(centre_pos[1], centre_pos[0], text=text)
        return annotation


class DungeonMap(AbstractGrid):
    """
    Defines the DungeonMap class
    Inherits from AbstractGrid

    """

    def __init__(self, master, size, width, bg):
        """
        Initialises the DungeonMap class

        """
        super().__init__(master, size[0], size[1], width, width, bg)

    def draw_grid(self, dungeon, player_pos):
        """
        Draws the dungeon on the DungeonMap based on dungeon and draws the player
        at the specifed (row, col) position

        """
        for key in dungeon:
            value = dungeon[key]
            i, j = self.get_bbox(key)
            y1, x1 = i
            y2, x2 = j
            if value.get_id() == "#":
                self.create_rectangle(x1, y1, x2, y2, fill="dark grey")
            elif value.get_id() == "K":
                self.create_rectangle(x1, y1, x2, y2, fill="yellow")
                self.annotate_position((i, j), "Trash")
            elif value.get_id() == "M":
                self.create_rectangle(x1, y1, x2, y2, fill="orange")
                self.annotate_position((i, j), "Banana")
            elif value.get_id() == "D":
                self.create_rectangle(x1, y1, x2, y2, fill="dark red")
                self.annotate_position((i, j), "Nest")
        p1, p2 = self.get_bbox(player_pos)
        self.create_rectangle(p1[1], p1[0], p2[1], p2[0], fill="light green")
        self.annotate_position((p1, p2), "Ibis")


class AdvancedDungeonMap(DungeonMap):
    """
    Defines the AdvancedDungeonMap class
    Inherits from the DungeonMap class

    """

    def __init__(self, master, size, width, bg):
        """
        Initialises the AdvancedDungeonMap class

        """
        super().__init__(master, size, width, bg)

        # Creates the variable for the images
        wall_im = Image.open(IMAGES["wall"])
        wall_im = wall_im.resize((self._x, self._y))
        self._wall_tk = ImageTk.PhotoImage(wall_im)

        key_im = Image.open(IMAGES["key"])
        key_im = key_im.resize((self._x, self._y))
        self._key_tk = ImageTk.PhotoImage(key_im)

        move_increase_im = Image.open(IMAGES["move increase"])
        move_increase_im = move_increase_im.resize((self._x, self._y))
        self._move_increase_tk = ImageTk.PhotoImage(move_increase_im)

        door_im = Image.open(IMAGES["door"])
        door_im = door_im.resize((self._x, self._y))
        self._door_tk = ImageTk.PhotoImage(door_im)

        empty_im = Image.open(IMAGES["empty"])
        empty_im = empty_im.resize((self._x, self._y))
        self._empty_tk = ImageTk.PhotoImage(empty_im)

        player_im = Image.open(IMAGES["player"])
        player_im = player_im.resize((self._x, self._y))
        self._player_tk = ImageTk.PhotoImage(player_im)

    def draw_grid(self, dungeon, player_pos):
        """
        Draws the dungeon on the DungeonMap based on dungeon and draws the player
        at the specifed (row, col) position

        """
        # Draws background
        a1 = 0
        while a1 < self._rows:
            a2 = 0
            while a2 < self._cols:
                b1, b2 = self.get_bbox((a1, a2))
                ax, ay = self.get_position_centre((b1, b2))
                self.create_image(ay, ax, image=self._empty_tk)
                a2 += 1
            a1 += 1

        # Draws entities
        for key in dungeon:
            value = dungeon[key]
            i, j = self.get_bbox(key)
            x, y = self.get_position_centre((i, j))
            if value.get_id() == "#":
                self.create_image(y, x, image=self._wall_tk)
            elif value.get_id() == "K":
                self.create_image(y, x, image=self._key_tk)
            elif value.get_id() == "M":
                self.create_image(y, x, image=self._move_increase_tk)
            elif value.get_id() == "D":
                self.create_image(y, x, image=self._door_tk)

        # Draws player
        p1, p2 = self.get_bbox(player_pos)
        px, py = self.get_position_centre((p1, p2))
        self.create_image(py, px, image=self._player_tk)


class KeyPad(AbstractGrid):
    """
    Defines the KeyPad class
    Inherits from AbstractGrid

    """

    def __init__(self, master, width, height, bg):
        """
        Initialises the KeyPad class

        """
        super().__init__(master, rows=2, cols=3, width=width, height=height, bg=bg)
        self._width = width // 3
        self._height = height // 2

    def pixel_to_direction(self, pixel):
        """
        Converts the x, y pixel position to the direction of the arrow depicted at that position
        Parameters
            pixel: the position of the pixel (int, int)
        Returns: the direction corresponding to the pixel direction

        """
        pos_x = pixel[0] // self._width
        pos_y = pixel[1] // self._height
        if (pos_x, pos_y) == (1, 0):
            return "w"
        elif (pos_x, pos_y) == (0, 1):
            return "a"
        elif (pos_x, pos_y) == (1, 1):
            return "s"
        elif (pos_x, pos_y) == (2, 1):
            return "d"

    def draw_keypad(self):
        """
        Draws the keypad

        """
        # Sets the position of the keys for the keypad
        pos_n = ((0, self._width), (self._height, 2 * self._width))
        pos_w = ((self._height, 0), (2 * self._height, self._width))
        pos_s = ((self._height, self._width), (2 * self._height, 2 * self._width))
        pos_e = ((self._height, 2 * self._width), (2 * self._height, 3 * self._width))

        # Creates the keys for the keypad
        self.create_rectangle(
            pos_n[0][1], pos_n[0][0], pos_n[1][1], pos_n[1][0], fill="dark grey"
        )
        self.create_rectangle(
            pos_w[0][1], pos_w[0][0], pos_w[1][1], pos_w[1][0], fill="dark grey"
        )
        self.create_rectangle(
            pos_s[0][1], pos_s[0][0], pos_s[1][1], pos_s[1][0], fill="dark grey"
        )
        self.create_rectangle(
            pos_e[0][1], pos_e[0][0], pos_e[1][1], pos_e[1][0], fill="dark grey"
        )

        # Labels the keys for the keypad
        self.annotate_position(pos_n, "N")
        self.annotate_position(pos_w, "W")
        self.annotate_position(pos_s, "S")
        self.annotate_position(pos_e, "E")


def main():
    root = tk.Tk()
    root.title(TITLE)
    app = GameApp(root, TASK_TWO, GAME_LEVEL_2)
    root.bind("<Key>", app.key_press)
    root.mainloop()


if __name__ == "__main__":
    main()
