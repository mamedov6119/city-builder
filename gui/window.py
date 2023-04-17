from gameconfig import *;
from classes.Human import *;
from classes.Building import *;

import arcade, arcade.gui, math, random, datetime, json;

speed = 1 # as global

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

class Window(arcade.Window):
    selected = -1
    hover_sprite = Hover()
    sidebtns = [
        {"text": "Powerplant", "color": arcade.color.DARK_PUCE, "class": PowerPlant()},
        {"text": "Police Dep", "color": arcade.color.AZURE, "class": PoliceDepartment()},  
        {"text": "Fire Dep", "color": arcade.color.ALABAMA_CRIMSON, "class": FireDepartment()},   
        {"text": "Stadium", "color": arcade.color.BURNT_ORANGE, "class": Stadium()},
        {"text": "Remove", "color": arcade.color.RED, "class": None}
    ]

    """ Class which renders the field of the game. """
    def __init__(self, filename="save.json", width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        super().__init__(width, height, title, False)
        self.load(filename)
        arcade.set_background_color(arcade.color.AMAZON)
        self.menu_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidetop_manager = arcade.gui.UIManager(auto_enable=True)
        self.sidebtm_manager = arcade.gui.UIManager(auto_enable=True)

        # Top-menu
        self.draw_topbar()

        # Side-menu (top)
        self.draw_sidetop()
        
        # Side-menu (bottom)
        self.hb_box = arcade.gui.UIBoxLayout(vertical=True)
        self.hb_box.add(arcade.gui.UIFlatButton(text='disaster', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4, style={"font_color": arcade.color.RED, "border_color": arcade.color.RED, "bg_color": arcade.color.TEA_ROSE}).with_space_around(right=2,top=2,bottom=2,left=2))
        save_btn = arcade.gui.UIFlatButton(text='SAVE', width=(BLOCK_SIZE*3)-4, height=BLOCK_SIZE-4)
        save_btn.on_click = lambda e: self.save()
        self.hb_box.add(save_btn.with_space_around(right=2,top=2,bottom=2,left=2))
        self.sidebtm_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.hb_box, align_x=0, align_y=0))

        # Add hover-sprite
        humans_sprites.append(self.hover_sprite)

    def load(self, filename="save.json"):
        global speed
        self.boost = 1; self.items = []; self.time = 0; self.money = 1000
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.time = data["time"] if "time" in data else self.time
                self.boost = data["boost"] if "boost" in data else self.boost
                self.money = data["money"] if "money" in data else self.money
                self.items = data["items"] if "items" in data else self.items
        except: pass
        speed = self.boost
        for item in self.items:
            if item["type"] == "Powerplant": PowerPlant(item["x"],item["y"])
            elif item["type"] == "Police Dep": PoliceDepartment(item["x"],item["y"])
            elif item["type"] == "Fire Dep": FireDepartment(item["x"],item["y"])
            elif item["type"] == "Stadium": Stadium(item["x"],item["y"])

    def save(self, filename="save.json"):
        print("Saving...")
        with open(filename, "w") as f:
            json.dump({"time": self.time, "boost": self.boost, "money": self.money, "items": self.items}, f)

    def set_select(self, e):
        self.selected = e.source.text if self.selected != e.source.text else -1
        if self.selected != -1 and self.selected != "Remove":
            dim = self.sidebtns[[i["text"] for i in self.sidebtns].index(self.selected)]["class"].getDim()
            self.hover_sprite.set_size(dim)
        elif self.selected == "Remove": self.hover_sprite.set_size(2)
        else: self.hover_sprite.set_size(0)
        self.draw_sidetop()

    def set_boost(self, e):
        global speed
        self.boost = int(e.source.text[1])
        self.draw_topbar()
        speed = self.boost

    def draw_sidetop(self):
        self.ht_box = arcade.gui.UIBoxLayout(vertical=True)
        for i in self.sidebtns:
            btn = arcade.gui.UIFlatButton(text=i["text"], width=(BLOCK_SIZE*2)-2, height=BLOCK_SIZE-2, style={"font_size": 8, "bg_color": i["color"], "border_color": arcade.color.WHITE if self.selected == i["text"] else None})
            btn.on_click = lambda e: self.set_select(e)
            self.ht_box.add(btn.with_space_around(right=1,top=1,bottom=1,left=1))
        self.sidetop_manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.ht_box, align_x=BLOCK_SIZE//2, align_y=-BLOCK_SIZE))

    def draw_topbar(self):
        self.v_box = arcade.gui.UIBoxLayout(vertical=False)
        for i in ["x1", "x2", "x3", "||"]:
            stl = {"bg_color": arcade.color.LIMERICK if f"x{self.boost}" == i else arcade.color.DARK_PUCE} if i != "||" else {}
            btn = arcade.gui.UIFlatButton(text=i, width=BLOCK_SIZE-4, height=BLOCK_SIZE-4, style=stl)
            if i == "||": btn.on_click = lambda e: self.save()
            else: btn.on_click = lambda e: self.set_boost(e)
            self.v_box.add(btn.with_space_around(right=2,top=2,bottom=2,left=2))
        self.menu_manager.add(arcade.gui.UIAnchorWidget(anchor_x="right", anchor_y="top", child=self.v_box))

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

        # test boundaries rectangle
        # arcade.draw_rectangle_filled(SCREEN_WIDTH/2+1.5*BLOCK_SIZE, SCREEN_HEIGHT/2-BLOCK_SIZE, SCREEN_WIDTH-3*BLOCK_SIZE, SCREEN_HEIGHT-BLOCK_SIZE, arcade.color.BLACK)

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
        for i in range(10): Human()
        # for i in range(8): PowerPlant((i*3),1)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.show_menu()
        self.draw_grid()
        self.menu_manager.draw()
        self.sidetop_manager.draw()
        self.sidebtm_manager.draw()
        humans_sprites.draw()
        building_sprites.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        humans_sprites.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if (key == 65307): self.save()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        if self.selected != -1:
            i = (x//BLOCK_SIZE)-3; j = y//BLOCK_SIZE
            if (0 <= i and 0 <= j <= 14):
                self.hover_sprite.update_pos(i,j)
        
        # self.center_x = ((x+3)*BLOCK_SIZE + (self.dim)*BLOCK_SIZE/2)
        # self.center_y = ((y+1)*BLOCK_SIZE - (self.dim)*BLOCK_SIZE/2)
    def find_sprite(self, x, y):
        # Loop through all of your sprites and check their positions
        for sprite in building_sprites:
            if (x+3)*BLOCK_SIZE <= sprite.center_x <= ((x+3)*BLOCK_SIZE + (2)*BLOCK_SIZE) and (y+1)*BLOCK_SIZE <= sprite.center_y <= ((y+1)*BLOCK_SIZE - (2)*BLOCK_SIZE):
                # Return the sprite if its position matches
                print(sprite)
                return sprite
        
        # If no sprite was found, return None
        return None

    def getBuildingType(self, c):
        if c.__class__.__name__ == "PowerPlant": return "Powerplant"
        elif c.__class__.__name__ == "PoliceDepartment": return "Police Dep"
        elif c.__class__.__name__ == "FireDepartment": return "Fire Dep"
        elif c.__class__.__name__ == "Stadium": return "Stadium"
        


    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        i = (x//BLOCK_SIZE)-3; j = y//BLOCK_SIZE
        # print(f"!!x:{i}, y:{j}. BX:{x}, BY:{y}")
        if (0 <= i and 0 <= j <= 14 and self.selected != -1):
            a = None
            if self.selected == "Powerplant": a = PowerPlant(i,j)
            elif self.selected == "Police Dep": a = PoliceDepartment(i,j)
            elif self.selected == "Fire Dep": a = FireDepartment(i,j)
            elif self.selected == "Stadium": a = Stadium(i,j)
            elif self.selected == "Remove": 
                try:
                    a = arcade.get_sprites_at_point([(i+4)*BLOCK_SIZE, (j+1)*BLOCK_SIZE], building_sprites)[0]
                    a.cost *= -1
                    building_sprites.remove(a)
                except: pass
            self.money -= a.cost
            if self.selected != "Remove": self.items.append({"x": i, "y": j, "type": self.selected})
            else: self.items.remove({"x": i, "y": j, "type": self.getBuildingType(a)})
            # self.items.append({"x": i, "y": j, "type": self.selected})

                
            