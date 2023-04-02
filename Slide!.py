"""The sliding game. The user has to arrange the tiles in ascending order where 1 is at the top left.
---------------------------------------------------------------------------------------------------------------"""
# Import necessary modules
import random
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk


class Tile(object):
    """The class that represents each tile.

        Attributes:
            new_empty (tuple): The position of the empty square with the first column being row and
                               the second being column.
            current_position (tuple): The current position of the tile with the first column being row and
                                      the second being column.
        Methods:
            move: Move the tile to the empty space if tile is adjacent.
            draw: Draw the tile on its `current_position`.
        """
    
    def __init__(self, _image: ImageTk.PhotoImage, position: tuple[int, int], screen: tkinter.Tk,
                 number_of_columns: int) -> None:
        """Initialize the tile and define necessary variables.

        :param _image: The image of the tile.
        :param position: The correct position of the image.
        :param screen: The screen on which the tile has to be drawn
        :param number_of_columns: The number of columns"""
        # self.move_ = True
        # Define the necessary variables.
        self.new_empty = (number_of_columns - 1, number_of_columns - 1)
        self._screen = screen
        self.button = tkinter.Button(self._screen, image=_image, compound=tkinter.CENTER, relief='sunken',
                                     borderwidth=1, command=self.move)
        label = tkinter.Label(self._screen, image=_image)
        label.image = _image

        # Set the current and correct position
        self._correct_position = self.current_position = position

    def move(self) -> None:
        """Move the tile to the empty space if possible. Change the row and column
        of the empty space"""
        # If either the column or the row is equal, and the other is adjacent, then move the tile when clicked.
        # if self.move_:
        difference_row = self.new_empty[0] - self.current_position[0]
        difference_column = self.new_empty[1] - self.current_position[1]
        if difference_column == 0 and \
           (difference_row == 1 or difference_row == -1):
            self.current_position, self.new_empty = self.new_empty, self.current_position
        elif difference_row == 0 and \
                (difference_column == 1 or difference_column == -1):
            self.current_position, self.new_empty = self.new_empty, self.current_position

    def draw(self) -> tuple:
        """Draw the tile and return the position of the empty place

        :return: The tuple containing the row and the column of the empty place respectively."""
        self.button.grid(row=self.current_position[0], column=self.current_position[1], sticky='nsew')
        return self.new_empty, self.current_position == self._correct_position


class AllTiles(object):
    """The class that manages all the tiles and their methods.

        Methods:
            draw: Draw all the tiles.
            shuffle: Shuffle the tiles.
    """

    def __init__(self, image: str, screen: tkinter.Tk, number_of_columns: int) -> None:
        """Define necessary variables and create necessary objects.

        :param image: The path of the image given by the user.
        :param screen: The screen on which the tiles have to be drawn.
        :param number_of_columns: The number of columns."""
        # Declare the necessary variables.
        self._screen = screen
        self._all_tiles = []
        self._main_image = Image.open(image)
        self.PIXELS = 580
        self._main_image = self._main_image.resize((self.PIXELS, self.PIXELS))
        self._images = []
        self._number_of_columns = number_of_columns
        positions = []

        # Make the images and the objects.
        
        n = number_of_columns
        for number in range(1, n ** 2):
            if number % number_of_columns == 0:
                column = number_of_columns
                number -= 1
            else:
                column = number % number_of_columns
            positions.append((int(number / number_of_columns), column - 1))
        for value in range(int(self.PIXELS/number_of_columns), self.PIXELS + 1, int(self.PIXELS/number_of_columns)):
            for value2 in range(int(self.PIXELS/number_of_columns), self.PIXELS + 1,
                                int(self.PIXELS/number_of_columns)):
                image_cropped = self._main_image.crop((value2 - int(self.PIXELS/number_of_columns),
                                                       value - int(self.PIXELS/number_of_columns), value2, value))
                self._images.append(image_cropped)

        for index in range(len(self._images) - 1):
            image_photo = ImageTk.PhotoImage(self._images[index])
            self._all_tiles.append(Tile(image_photo, positions[index],
                                        self._screen, number_of_columns))
        self._empty = (number_of_columns - 1, number_of_columns - 1)

    def draw(self) -> bool:
        """Draw the tiles."""
        is_correct = []
        for tile in self._all_tiles:
            # Run a for loop through each tile and draw it.
            empty, boolean = tile.draw()
            is_correct.append(boolean)
            if empty != self._empty:
                # If a tile has been moved, update empty tile position for each tile.
                self._empty = empty
                for each_tile in self._all_tiles:
                    each_tile.new_empty = self._empty
        return len(is_correct) == is_correct.count(True)

    def shuffle(self) -> None:
        """Shuffle the tiles."""
        # We move a random tile random number of times so that it shuffles.
        for i in range(random.randint(50, 500)):
            choice = random.randint(1, 2)
            if choice == 1:
                dimensions = (self._empty[0], self._empty[1] - (random.choice((-1, 1))))
            else:
                dimensions = (self._empty[0] - (random.choice((-1, 1))), self._empty[1])
            for tile in self._all_tiles:
                if tile.current_position == dimensions:
                    tile.move()
                    self.draw()

    def win(self) -> None:
        """Show the last tile (which was empty so that the user can slide the puzzle) and stop the tiles
        from moving when clicked."""
        # Add the new object to the list.
        self._all_tiles.append(Tile(ImageTk.PhotoImage(self._images[-1]), (self._number_of_columns - 1,
                                                                           self._number_of_columns - 1),
                                    self._screen, self._number_of_columns))
        # Do not allow the movement of each tile.
        for tile in self._all_tiles:
            tile.move_ = False
            tile.draw()
        # Update the screen so the changes can be seen.
        self._screen.update()


class Game(object):
    """The class that represents the main game.

        Methods:
            play: Play the game!
    """

    def __init__(self) -> None:
        """Define the necessary variables and ask for the image."""

        def get_path() -> str:
            """Make a GUI for making the user select the path of the image and then return the path.

            :return: The path of the image selected by the user."""

            def set_path() -> None:
                """Open the screen for browsing the image file and set `path` to the path and then destroy
                the screen."""
                nonlocal path
                path = tkinter.filedialog.askopenfilename(title='Select File', initialdir='\\', filetypes=(('Image '
                                                                                                            'Files',
                                                                                                            '*.png '
                                                                                                            '*.jpg '
                                                                                                            '*.tiff '
                                                                                                            '*.bmp'),
                                                                                                           ('All Files',
                                                                                                            '*.*')))
                screen.destroy()

            # Make the screen.
            path = ''
            screen = tkinter.Tk()
            screen.title('Select')
            screen.resizable(False, False)
            screen.geometry('300x100-500-500')
            # Configure columns
            for i in range(2):
                screen.rowconfigure(i, weight=1)
            screen.columnconfigure(0, weight=1)

            # Define and grid the widgets.
            label = tkinter.Label(screen, text='Select Image:')
            go = tkinter.Button(screen, text='Select file', command=set_path)
            label.grid(row=0, column=0, sticky='nsew')
            go.grid(row=1, column=0)
            screen.mainloop()
            if path == '':
                # If the user did not select a file then exit the program.
                exit()
            return path

        self._image_path = get_path()

        # Set the screen
        self._set_screen()
        try:
            # Open the image and resize according to the screen
            image = Image.open(self._image_path)
            image_resized = image.resize((250, 230))
            image_resized_photo_image = ImageTk.PhotoImage(image_resized)
            image_label = tkinter.Label(self._screen, image=image_resized_photo_image)
            image_label.image = image_resized_photo_image
            image_label.grid(row=0, column=5, rowspan=4, padx=30)
        except FileNotFoundError:
            exit()

        # Create the `AllTiles` object.
        self._all_tiles = AllTiles(self._image_path, self._screen, self._column_or_row)

        # Create the shuffle button.
        self._button = tkinter.Button(self._screen, text='Shuffle', bg='red', activebackground='red',
                                      command=self._all_tiles.shuffle, relief='raised')
        self._button.grid(row=2, column=5, rowspan=2, sticky='s', pady=40)

    def _set_screen(self, won: bool = False):
        """Set the screen"""
        screen = tkinter.Tk()
        screen.config(bg='black')
        if not won:
            screen.geometry('900x560-250-100')
        else:
            screen.geometry('350x300-500-200')
        screen.title('Slide!')
        screen.resizable(False, False)

        # Configure column and rows.
        self._column_or_row = 4
        for i in range(self._column_or_row):
            screen.columnconfigure(i, weight=1)
            screen.rowconfigure(i, weight=1)
        screen.columnconfigure(self._column_or_row, weight=1)
        if won:
            self._won_screen = screen
        else:
            self._screen = screen

    def _won(self) -> None:
        """Show the win screen and the empty tile."""
        self._all_tiles.win()

        def play() -> None:
            """Replay the game."""
            self._screen.destroy()
            self._won_screen.destroy()
            self.__init__()
            self.play()

        self._set_screen(won=True)
        # Declare and grid the necessary widgets.
        win_label = tkinter.Label(self._won_screen, text='You Won!', bg='black', fg='orange', font=('Game Over', 60))
        exit_ = tkinter.Button(self._won_screen, text='Exit', bg='orange', activebackground='orange',
                               command=exit)
        play_again = tkinter.Button(self._won_screen, text='Play again', bg='orange', activebackground='orange',
                                    command=play)

        win_label.grid(column=2, row=1, columnspan=3, rowspan=2, sticky='nsew', padx=10, pady=5)
        exit_.grid(column=0, row=2, sticky='new', padx=10)
        play_again.grid(column=5, row=2, sticky='new', padx=10)
        self._won_screen.mainloop()

    def _main(self) -> None:
        """The function to be included in the _screen.mainloop. Draw the tiles."""
        solved = self._all_tiles.draw()
        if solved:
            self._won()
        self._screen.after(20, self._main)

    def play(self) -> None:
        """Play the game!"""
        # Shuffle it once and then the main loop.
        self._all_tiles.shuffle()
        self._screen.after(20, self._main)
        self._screen.mainloop()


if __name__ == '__main__':
    game = Game()
    game.play()
