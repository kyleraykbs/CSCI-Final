from colorama import Fore, Back, Style
import os, subprocess, json

class Object:
    def __init__(self, pixel, collideable=True):
        self.pixel = pixel
        self.collideable = collideable

screen = []

class Pixel:
    fg_color = 0
    bg_color = 0
    char = "."

    def get_bg_color(self):
        return intToColor(self.bg_color, False)

    def get_fg_color(self):
        return intToColor(self.fg_color, True)

    def __init__(self, bg_color=0, fg_color=1, char=" "):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.char = char

objects = {
    0: lambda: Object(Pixel(-2, 7, " ")),
    1: lambda: Object(Pixel(-1, 7, " ")),
    2: lambda: Object(Pixel(0, 7, " ")),
    3: lambda: Object(Pixel(7, 7, " ")),
    4: lambda: Object(Pixel(1, 7, " ")),
    5: lambda: Object(Pixel(2, 7, " ")),
    6: lambda: Object(Pixel(3, 7, " ")),
    7: lambda: Object(Pixel(4, 7, " ")),
    8: lambda: Object(Pixel(5, 7, " ")),
    9: lambda: Object(Pixel(6, 7, " ")),
    10: lambda: Object(Pixel(-2, 2, "✖")),
    11: lambda: Object(Pixel(-2, 2, "✚")),
    12: lambda: Object(Pixel(-2, 3, "☨")),
    13: lambda: Object(Pixel(-2, 2, "☨")),
    14: lambda: Object(Pixel(-2, 3, "✖")),
    15: lambda: Object(Pixel(-2, 3, "✚")),
    16: lambda: Object(Pixel(-2, 0, "⊑")),
    17: lambda: Object(Pixel(-2, 0, "⊒")),
    18: lambda: Object(Pixel(-2, 0, "╔")),
    19: lambda: Object(Pixel(-2, 0, "╗")),
    20: lambda: Object(Pixel(-2, 0, "╚")),
    21: lambda: Object(Pixel(-2, 0, "╝")),
    22: lambda: Object(Pixel(-2, 0, "║")),
    23: lambda: Object(Pixel(-2, 0, "═")),
}

def intToColor(clr, fg):
    clr = int(clr)
    if clr == -1 or clr == -2:
            return ""
    elif clr == 0:
        if fg:
            return Fore.BLACK
        else:
            return Back.BLACK
    elif clr == 1:
        if fg:
            return Fore.RED
        else:
            return Back.RED
    elif clr == 2:
        if fg:
            return Fore.GREEN
        else:
            return Back.GREEN
    elif clr == 3:
        if fg:
            return Fore.YELLOW
        else:
            return Back.YELLOW
    elif clr == 4:
        if fg:
            return Fore.BLUE
        else:
            return Back.BLUE
    elif clr == 5:
        if fg:
            return Fore.MAGENTA
        else:
            return Back.MAGENTA
    elif clr == 6:
        if fg:
            return Fore.CYAN
        else:
            return Back.CYAN
    elif clr == 7:
        if fg:
            return Fore.WHITE
        else:
            return Back.WHITE

def getPixel(x,y):
    return screen[x][y]

def gen2DArray(xsize, ysize, initial_value=0):
    mainarray = []
    for y in range(ysize):
        row = []
        for x in range(xsize):
            row.append(initial_value)
        mainarray.append(row)
    return mainarray


def fillScreen(xsize, ysize, clr1=0,clr2=1):
    global screen
    screen = []
    for x in range(xsize):
        screen.append([])
        for y in range(ysize):
            screen[x].append(Pixel(clr1,clr2," "))

def flipScreen(xsize, ysize):
    os.system("clear")
    cscreen = []
    for y in range(ysize): cscreen.append("")
    for x in range(xsize):
        for y in range(ysize):
            px = getPixel(x,y)
            cscreen[y] += px.get_fg_color() + px.get_bg_color() + px.char + Style.RESET_ALL

    for y in cscreen:
        print(y)

def layerScreen(array, yfirst=True, objects=objects):
    yint = -1
    xint = -1
    for y in array:
        yint+=1
        for x in y:
            xint+=1
            if objects[x]().pixel.bg_color != -2:
                screen[xint][yint] = objects[x]().pixel
            else:
                if objects[x]().pixel.char != " ":
                    screen[xint][yint].fg_color = objects[x]().pixel.fg_color
                    screen[xint][yint].char = objects[x]().pixel.char
        xint=0-1

def text(x,y,txt,clr=7):
    txtpos = -1
    for char in txt:
        txtpos += 1
        xpos = txtpos + x
        ypos = y
        screen[xpos][ypos].char = char
        screen[xpos][ypos].fg_color = clr

def run_bash_script(script_path):
    try:
        subprocess.run(['bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Bash script: {e}")
        exit()

if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # Verify filestructure, we do this using bash cause of the arbitrary command amount we have to hit for each language. Trust me, I would much rather do this in python.
    run_bash_script("verify.bash")

    Cursor = [0,0,True]
    def editor(xsize, ysize, mappath):
        editorMap = None
        if not os.path.exists(mappath):
            editorMap = {
                "paint": [gen2DArray(xsize,ysize,1)],
                "collision": gen2DArray(xsize,ysize,0),
                "doors_vis": gen2DArray(xsize,ysize,0),
                "doors": gen2DArray(xsize,ysize,{"isdoor":False, "mapname":"", "x":"", "y":""})
            }
        else:
            with open(mappath, 'r') as file:
                data = json.load(file)
                editorMap = data
            if "collision" not in editorMap: editorMap["collision"] = gen2DArray(xsize,ysize,0)
            if "doors_vis" not in editorMap: editorMap["doors_vis"] = gen2DArray(xsize,ysize,0)
            if "doors" not in editorMap: editorMap["doors"] = gen2DArray(xsize,ysize,{"isdoor":False, "mapname":"", "x":"", "y":""})

        editingCollisions = False
        collision_objects = {
            0: lambda: Object(Pixel(-2, 1, " ")),
            1: lambda: Object(Pixel(-2, 1, "╳")),
        }

        editingDoors = False
        door_objects = {
            0: lambda: Object(Pixel(-2, 1, " ")),
            1: lambda: Object(Pixel(-2, 5, "╳")),
        }

        layernum = 0

        def render(xsize, ysize):
            fillScreen(xsize,ysize + 3,-1)

            # Build out the map.
            for layer in editorMap["paint"]:
                layerScreen(layer)

            if editingCollisions:
                layerScreen(editorMap["collision"],objects=collision_objects)

            if editingDoors:
                layerScreen(editorMap["doors_vis"],objects=door_objects)

            # Overlays
            if Cursor[2] == True:
                if Cursor[0] < xsize - 1:
                    screen[Cursor[0] + 1][Cursor[1]].fg_color = 1
                    screen[Cursor[0] + 1][Cursor[1]].char = "⇠"
                if Cursor[0] != 0:
                    screen[Cursor[0] - 1][Cursor[1]].fg_color = 1
                    screen[Cursor[0] - 1][Cursor[1]].char = "⇢"
                if Cursor[1] != 0:
                    screen[Cursor[0]][Cursor[1] - 1].fg_color = 1
                    screen[Cursor[0]][Cursor[1] - 1].char = "⇣"
                if Cursor[1] < ysize - 1:
                    screen[Cursor[0]][Cursor[1] + 1].fg_color = 1
                    screen[Cursor[0]][Cursor[1] + 1].char = "⇡"

            # Custom Area
            for x in range(xsize): screen[x - 1][ysize].bg_color = 6
            for x in range(xsize): screen[x - 1][ysize + 1].bg_color = 6
            for x in range(xsize): screen[x - 1][ysize + 2].bg_color = 6
            text(0,ysize,f"🎮:[wasd, qe, +-, cr] layer: {layernum}")
            text(0,ysize + 1,f"(c)olEdit: {editingCollisions} | X: {Cursor[0]} Y: {Cursor[1]}")
            text(0,ysize + 2,f"doo(r)Edit: {editingDoors}")
            screen[xsize - 1][ysize].bg_color = -1

            flipScreen(xsize,ysize + 3)

        running = True
        while running:
            render(xsize,ysize)
            kp = subprocess.check_output("read -n 1 keypress; echo $keypress", shell=True).decode("utf-8").strip() # 2 bash commands
            if len(kp) < 1: kp = " "

            if len(editorMap["paint"]) - 1 < layernum: editorMap["paint"].append(gen2DArray(xsize,ysize,0))
            cursorTile = editorMap["paint"][layernum][Cursor[1]][Cursor[0]]

            if kp == "a":
                if Cursor[0] > 0:
                    Cursor[0] -= 1
            elif kp == "d":
                if Cursor[0] < xsize - 1:
                    Cursor[0] += 1
            elif kp == "s":
                if Cursor[1] < ysize - 1:
                    Cursor[1] += 1
            elif kp == "w":
                if Cursor[1] > 0:
                    Cursor[1] -= 1
            elif kp == " ":
                if cursorTile < len(objects) - 1:
                    editorMap["collision"][layernum][Cursor[1]][Cursor[0]] += 1
            elif kp == "q":
                if editingCollisions:
                    editorMap["collision"][Cursor[1]][Cursor[0]] = 0
                elif editingDoors:
                    editorMap["doors_vis"][Cursor[1]][Cursor[0]] = 0
                    editorMap["doors"][Cursor[1]][Cursor[0]]["isdoor"] = False
                else:
                    if cursorTile > 0:
                        editorMap["paint"][layernum][Cursor[1]][Cursor[0]] -= 1
                    else:
                        editorMap["paint"][layernum][Cursor[1]][Cursor[0]] = len(objects) - 1
            elif kp == "e":
                if editingCollisions:
                    editorMap["collision"][Cursor[1]][Cursor[0]] = 1
                elif editingDoors:
                    print()
                    print()
                    editorMap["doors"][Cursor[1]][Cursor[0]]["mapname"] = input("Door leads to the map named: ")
                    editorMap["doors"][Cursor[1]][Cursor[0]]["x"] = int(input("Next map X pos: "))
                    editorMap["doors"][Cursor[1]][Cursor[0]]["y"] = int(input("Next map Y pos: "))
                    editorMap["doors"][Cursor[1]][Cursor[0]]["isdoor"] = True
                    editorMap["doors_vis"][Cursor[1]][Cursor[0]] = 1
                else:
                    if cursorTile < len(objects) - 1:
                        editorMap["paint"][layernum][Cursor[1]][Cursor[0]] += 1
                    else:
                        editorMap["paint"][layernum][Cursor[1]][Cursor[0]] = 0
            elif kp == "=": layernum += 1
            elif kp == "-": layernum -= 1
            elif kp == "p":
                os.system("clear")
                with open(mappath, 'w') as file:
                    json.dump(editorMap, file)
                print(f"Dumped map data to file {mappath}")
                input("Press ENTER to continue.")
            elif kp == "c": 
                editingCollisions = not editingCollisions
                editingDoors = False
            elif kp == "r": 
                editingDoors = not editingDoors
                editingCollisions = False

    editor(32,9,"maps/quad.json")
