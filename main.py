import arcade, arcade.gui, datetime;

BLOCK_SIZE = 30
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 480
SCREEN_TITLE = "City-Builder"

class Game(arcade.Window):
    """
    Class which renders the field of the game.
    """
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        self.time = 0 + 8*32
        self.boost = 1
        self.items = []
        self.money = 1000

        super().__init__(width, height, title, False)
        arcade.set_background_color(arcade.color.AMAZON)
        self.menu_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidetop_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidebtm_manager = arcade.gui.UIManager(auto_enable=True)

        # Top-menu
        self.v_box = arcade.gui.UIBoxLayout(vertical=False)
        for i in ["x1", "x2", "x3", "||"]:
            stl = {"bg_color": arcade.color.LIMERICK if f"x{self.boost}" == i else arcade.color.DARK_PUCE} if i != "||" else {}
            self.v_box.add(arcade.gui.UIFlatButton(text=i, width=BLOCK_SIZE-4, height=BLOCK_SIZE-4, style=stl).with_space_around(right=2,top=2,bottom=2,left=2))
        self.menu_manager.add(arcade.gui.UIAnchorWidget(anchor_x="right", anchor_y="top", child=self.v_box))

        # Side-menu (top)
        self.ht_box = arcade.gui.UIBoxLayout(vertical=True)
        for i in ["a", "b", "c"]*3:
            self.ht_box.add(arcade.gui.UIFlatButton(text=i, width=(BLOCK_SIZE*2)-2, height=BLOCK_SIZE-2).with_space_around(right=1,top=1,bottom=1,left=1))
        self.sidetop_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.ht_box, align_x=BLOCK_SIZE//2, align_y=-BLOCK_SIZE))
        
        # Side-menu (bottom)
        self.hb_box = arcade.gui.UIBoxLayout(vertical=True)
        self.hb_box.add(arcade.gui.UIFlatButton(text='disaster', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4, style={"font_color": arcade.color.RED, "border_color": arcade.color.RED, "bg_color": arcade.color.TEA_ROSE}).with_space_around(right=2,top=2,bottom=2,left=2))
        self.hb_box.add(arcade.gui.UIFlatButton(text='SAVE', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4).with_space_around(right=2,top=2,bottom=2,left=2))
        self.sidebtm_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.hb_box, align_x=0, align_y=0))

    def show_date(self):
        """ Show the date """
        startdate = datetime.date(2000, 1, 1)
        result = startdate + datetime.timedelta(days=self.time)
        return result.strftime("%d %B %Y")
        

    def show_menu(self):
        """ Show the menu """
        # Side-menu & Top-menu
        arcade.draw_rectangle_filled((3*BLOCK_SIZE)/2, SCREEN_HEIGHT/2, 3*BLOCK_SIZE, SCREEN_HEIGHT, arcade.color.DARK_GRAY)
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT - (BLOCK_SIZE/2), SCREEN_WIDTH, BLOCK_SIZE, arcade.color.GRAY)

        # Money 
        arcade.draw_text(f"Funds: ${self.money:,}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14, font_name="Courier")

        # Time (right-aligned)
        # arcade.draw_text(self.show_date(), (SCREEN_WIDTH - 10) - BLOCK_SIZE*4, SCREEN_HEIGHT - 20, arcade.color.APRICOT, 14, font_name="Courier", anchor_x="right")
        
        # Time (center-aligned)
        arcade.draw_text(self.show_date(), SCREEN_WIDTH/2, SCREEN_HEIGHT - 20, arcade.color.APRICOT, 14, font_name="Courier", anchor_x="center")

    def draw_grid(self):
        """ Draw the grid """
        for x in range(BLOCK_SIZE*3, SCREEN_WIDTH, BLOCK_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT-BLOCK_SIZE, arcade.color.GRAY, 1)
        for y in range(BLOCK_SIZE, SCREEN_HEIGHT, BLOCK_SIZE):
            arcade.draw_line(BLOCK_SIZE*3, y, SCREEN_WIDTH, y, arcade.color.GRAY, 1)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        pass

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.show_menu()
        self.draw_grid()
        self.menu_manager.draw()
        self.sidetop_manager.draw()
        self.sidebtm_manager.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        pass # hover, if building is selected

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        print(x//BLOCK_SIZE,y//BLOCK_SIZE)

def main():
    """ Main function """
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()