from gameconfig import *;
from classes.Zone import *;
from classes.Human import *;
from classes.Building import *;

from logic.variables import v;
import arcade, arcade.gui, datetime, json;

class Hover(arcade.Sprite):
    def __init__(self, size=0, color=arcade.color.RED):
        super().__init__()
        self.color = color
        self.set_size(size)
    
    def set_size(self, size):
        self.size = size
        self.width = size * BLOCK_SIZE
        self.height = size * BLOCK_SIZE
        self.texture = arcade.make_soft_square_texture(size*BLOCK_SIZE, self.color)

    def update_pos(self, i, j):
        self.center_x = ((i+3)*BLOCK_SIZE + (self.size)*BLOCK_SIZE/2)
        self.center_y = ((j+1)*BLOCK_SIZE - (self.size)*BLOCK_SIZE/2)

class RotateMode(arcade.Sprite):
    def __init__(self, size=20, color=arcade.color.RED):
        self.e = arcade.Texture.create_empty(name="empty", size=(0,0))
        self.t = arcade.Texture(name="text", image=arcade.create_text_image("Rotate mode ON", color, size))
        super().__init__(texture=self.e)
        self.center_x = SCREEN_WIDTH - 100
        self.center_y = SCREEN_HEIGHT - 50
        self.on = False 

    def toggle(self):
        self.on = not self.on
        self.texture = self.t if self.on else self.e

class Window(arcade.Window):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE, filename="save.json"):
        super().__init__(width, height, title, False)
        self.menu_view = MenuView()
        self.game_view = GameView(filename)
        self.show_view(self.menu_view)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_manager = arcade.gui.UIManager(auto_enable=True)
        self.setup()

    def setup(self):
        self.box = arcade.gui.UIBoxLayout(vertical=True)

        play_btn = arcade.gui.UIFlatButton(text="Play", width=200, height=50, center_x=SCREEN_WIDTH//2, center_y=SCREEN_HEIGHT//2, style={"bg_color": arcade.color.APPLE_GREEN, "font_color": arcade.color.WHITE})
        play_btn.on_click = lambda _: self.window.show_view(self.window.game_view)
        self.box.add(play_btn.with_space_around(top=10))

        load_btn = arcade.gui.UIFlatButton(text="Load", width=200, height=50, center_x=SCREEN_WIDTH//2, center_y=SCREEN_HEIGHT//2)
        load_btn.on_click = lambda _: self.window.show_view(self.window.game_view)
        self.box.add(load_btn.with_space_around(top=10))

        exit_btn = arcade.gui.UIFlatButton(text="Exit", width=200, height=50, center_x=SCREEN_WIDTH//2, center_y=SCREEN_HEIGHT//2, style={"bg_color": arcade.color.ALABAMA_CRIMSON, "font_color": arcade.color.WHITE})
        exit_btn.on_click = lambda _: self.window.close()
        self.box.add(exit_btn.with_space_around(top=10))

        self.menu_manager.add(arcade.gui.UIAnchorWidget(anchor_x="center", anchor_y="center", child=self.box, align_x=0, align_y=0))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu", SCREEN_WIDTH//2, SCREEN_HEIGHT - 2*BLOCK_SIZE, arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="top")
        self.menu_manager.draw()

class GameView(arcade.View):
    selected = -1
    hover_sprite = Hover()
    rotate_sprite = RotateMode()

    sidebtns = [
        {"text": "Powerplant", "color": arcade.color.DARK_PUCE, "class": PowerPlant()},
        {"text": "Police Dep", "color": arcade.color.AZURE, "class": PoliceDepartment()},  
        {"text": "Fire Dep", "color": arcade.color.ALABAMA_CRIMSON, "class": FireDepartment()},   
        {"text": "Stadium", "color": arcade.color.BURNT_ORANGE, "class": Stadium()},
        {"text": "Road", "color": arcade.color.BLACK, "class": Road()},
        {"text": "Remove", "color": arcade.color.RED, "class": None}
    ]

    sidezonebtns = [
        {"text": "Residential", "class": Residential()},
        {"text": "Service", "class": Service()},
        {"text": "Industrial", "class": Industrial()}
    ]

    """ Class which renders the field of the game. """
    def __init__(self, filename):
        super().__init__()
        self.load(filename)
        arcade.set_background_color(arcade.color.AMAZON)
        self.menu_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidetop_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidebtm_manager = arcade.gui.UIManager(auto_enable=True)
        self.setup()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def load(self, filename="save.json"):
        v.load(filename)
        for item in v.items:
            b = None
            if item["type"] == "Road":
                b = eval(item["type"])(item["x"],item["y"],item["index"],item["rotation"])
            else:
                b = eval(item["type"])(item["x"],item["y"])
            b.place()

    def save(self, filename="save.json"):
        v.save(filename)

    def set_select(self, e):
        self.selected = e.source.text if self.selected != e.source.text else -1
        if self.selected != -1 and self.selected != "Remove":
            dim = self.sidebtns[[i["text"] for i in self.sidebtns].index(self.selected)]["class"].getDim()
            self.hover_sprite.set_size(dim)
        else: self.hover_sprite.set_size(0)
        self.draw_sidetop()

    def set_speed(self, e):
        v.change_speed(int(e.source.text[1]))
        self.draw_topbar()

    def draw_sidetop(self):
        self.ht_box = arcade.gui.UIBoxLayout(vertical=True)
        for i in self.sidebtns:
            btn = arcade.gui.UIFlatButton(text=i["text"], width=(BLOCK_SIZE*2)-2, height=BLOCK_SIZE-2, style={"font_size": 8, "bg_color": i["color"], "border_color": arcade.color.WHITE if self.selected == i["text"] else None})
            btn.on_click = lambda e: self.set_select(e)
            self.ht_box.add(btn.with_space_around(right=1,top=1,bottom=1,left=1))
        self.sidetop_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.ht_box, align_x=BLOCK_SIZE//2, align_y=-BLOCK_SIZE))

        self.ht2_box = arcade.gui.UIBoxLayout(vertical=True)
        for i in self.sidezonebtns:
            btn = arcade.gui.UIFlatButton(text=i["text"], width=(BLOCK_SIZE*2)-2, height=BLOCK_SIZE-2, style={"font_size": 8, "bg_color": arcade.color.DARK_PUCE, "border_color": arcade.color.WHITE if self.selected == i["text"] else None})
            btn.on_click = lambda e: self.set_select(e)
            self.ht2_box.add(btn.with_space_around(right=1,top=1,bottom=1,left=1))
        self.sidetop_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.ht2_box, align_x=BLOCK_SIZE//2, align_y=-BLOCK_SIZE*(len(self.sidebtns)+3)))

    def draw_topbar(self):
        self.v_box = arcade.gui.UIBoxLayout(vertical=False)
        for i in ["x1", "x2", "x3", "||"]:
            stl = {"bg_color": arcade.color.LIMERICK if f"x{v.speed}" == i else arcade.color.DARK_PUCE} if i != "||" else {}
            btn = arcade.gui.UIFlatButton(text=i, width=BLOCK_SIZE-4, height=BLOCK_SIZE-4, style=stl)
            if i == "||": btn.on_click = lambda _: self.back_to_menu()
            else: btn.on_click = lambda e: self.set_speed(e)
            self.v_box.add(btn.with_space_around(right=2,top=2,bottom=2,left=2))
        self.menu_manager.add(arcade.gui.UIAnchorWidget(anchor_x="right", anchor_y="top", child=self.v_box))

    def back_to_menu(self):
        self.save()
        self.window.show_view(self.window.menu_view)

    def show_date(self):
        """ Show the date """
        startdate = datetime.date(2000, 1, 1)
        result = startdate + datetime.timedelta(days=v.time)
        return result.strftime("%d %B %Y")

    def show_menu(self):
        """ Show the menu """
        # Side-menu & Top-menu
        arcade.draw_rectangle_filled((3*BLOCK_SIZE)/2, SCREEN_HEIGHT/2, 3*BLOCK_SIZE, SCREEN_HEIGHT, arcade.color.DARK_GRAY)
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT - (BLOCK_SIZE/2), SCREEN_WIDTH, BLOCK_SIZE, arcade.color.GRAY)

        # Money 
        arcade.draw_text(f"Funds: ${v.money:,}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14, font_name="Courier")

        # Time (center-aligned)
        arcade.draw_text(self.show_date(), SCREEN_WIDTH/2, SCREEN_HEIGHT - 20, arcade.color.APRICOT, 14, font_name="Courier", anchor_x="center")

        # Satisfaction 
        arcade.draw_text(f"{round(v.satisfaction,2)}%", SCREEN_WIDTH - (BLOCK_SIZE*5), SCREEN_HEIGHT - 20, arcade.color.WHITE, 14, font_name="Courier", anchor_x="right")

    def draw_grid(self):
        """ Draw the grid """
        for x in range(BLOCK_SIZE*3, SCREEN_WIDTH, BLOCK_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT-BLOCK_SIZE, arcade.color.GRAY, 1)
        for y in range(BLOCK_SIZE, SCREEN_HEIGHT, BLOCK_SIZE):
            arcade.draw_line(BLOCK_SIZE*3, y, SCREEN_WIDTH, y, arcade.color.GRAY, 1)

    def setup(self):
        # Top-menu
        self.draw_topbar()

        # Side-menu (top)
        self.draw_sidetop()

        # Side-menu (bottom)
        self.hb_box = arcade.gui.UIBoxLayout(vertical=True)
        dis_btn = arcade.gui.UIFlatButton(text='disaster', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4, style={"font_color": arcade.color.RED, "border_color": arcade.color.RED, "bg_color": arcade.color.TEA_ROSE})
        dis_btn.on_click = lambda e: v.summon_disaster()
        self.hb_box.add(dis_btn.with_space_around(right=2,top=2,bottom=2,left=2))
        save_btn = arcade.gui.UIFlatButton(text='SAVE', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4)
        save_btn.on_click = lambda e: self.save()
        self.hb_box.add(save_btn.with_space_around(right=2,top=2,bottom=2,left=2))
        self.sidebtm_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.hb_box, align_x=0, align_y=0))

        # Add hover-sprite
        humans_sprites.append(self.hover_sprite)
        humans_sprites.append(self.rotate_sprite)
        
        # Place humans
        for _ in range(10): Human()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.show_menu()
        self.draw_grid()
        self.menu_manager.draw()
        self.sidetop_manager.draw()
        self.sidebtm_manager.draw()
        building_sprites.draw()
        humans_sprites.draw()
        zone_sprites.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        humans_sprites.update()
        v.time += (delta_time/20) * v.speed
        v.maintenance_charge()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if (key == 65307): self.save()
        if (key == 114): self.rotate_sprite.toggle()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        if self.selected != -1:
            i = (x//BLOCK_SIZE)-3; j = y//BLOCK_SIZE
            if (0 <= i and 0 <= j <= 14):
                self.hover_sprite.update_pos(i,j)
        
    def find_sprite(self, x, y):
        # Loop through all of your sprites and check their positions
        for sprite in building_sprites:
            if (x+3)*BLOCK_SIZE <= sprite.center_x <= ((x+3)*BLOCK_SIZE + (2)*BLOCK_SIZE) and (y+1)*BLOCK_SIZE <= sprite.center_y <= ((y+1)*BLOCK_SIZE - (2)*BLOCK_SIZE):
                return sprite
        return None

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        i = (x//BLOCK_SIZE)-3; j = y//BLOCK_SIZE
        print(f"!!x:{i}, y:{j}. BX:{x}, BY:{y}")
        try:
            if (self.rotate_sprite.on and 0 <= i and 0 <= j <= 14):
                c = arcade.get_sprites_at_point([(i+4)*BLOCK_SIZE, (j+1)*BLOCK_SIZE], building_sprites)[0]
                if c.__class__.__name__ == "Road": v.rotate_road(c)

            if (0 <= i and 0 <= j <= 14 and self.selected != -1):
                if self.selected != 'Remove':
                    target = None
                    for item in self.sidebtns:
                        if item['text'] == self.selected:
                            target = item['class'].__class__
                    v.place_building(building=target, x=i, y=j)
                else: v.remove_building(i, j)
        except Exception as e:
            print(e)
    