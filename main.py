from colorama import Fore, Back, Style
import os, subprocess, json, copy, sys
import sys, tty, termios
def getinp():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == "":
        ch = " "
    return ch

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
    24: lambda: Object(Pixel(-2, 4, "⊑")),
    25: lambda: Object(Pixel(-2, 4, "⊒")),
    26: lambda: Object(Pixel(-2, 3, "⊐")),
    27: lambda: Object(Pixel(-2, 0, "⊂")),
    28: lambda: Object(Pixel(-2, 0, "⊃")),
    29: lambda: Object(Pixel(-2, 4, "▒")),
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

def update_player_data(name, x, y, mapname, inventory=""):
    db_file = "players.db"

    update_command = f"sqlite3 {db_file} 'UPDATE players SET x={x}, y={y}, inventory=\"{inventory}\", mapname=\"{mapname}\" WHERE name=\"{name}\";'"

    os.system(update_command)

Cursor = [0,0,True]
MainPlayerPos = [0,0]

def load_map(xsize,ysize,mappath):
    currentMap = None
    if not os.path.exists(mappath):
        currentMap = {
            "paint": [gen2DArray(xsize,ysize,1)],
            "collision": gen2DArray(xsize,ysize,0),
            "doors_vis": gen2DArray(xsize,ysize,0),
            "doors": gen2DArray(xsize,ysize,0)
        }
    else:
        with open(mappath, 'r') as file:
            data = json.load(file)
            currentMap = data
        if "collision" not in currentMap: currentMap["collision"] = gen2DArray(xsize,ysize,0)
        if "doors_vis" not in currentMap: currentMap["doors_vis"] = gen2DArray(xsize,ysize,0)
        if "doors" not in currentMap: currentMap["doors"] = gen2DArray(xsize,ysize,0)
    return currentMap

def game(xsize, ysize, mappath, startpos=[9,5],name="user"):
    MainPlayerPos = startpos
    currentMap = load_map(xsize,ysize,mappath)

    def render(xsize, ysize):
        fillScreen(xsize,ysize + 3,-1)

        # Build out the map.
        for layer in currentMap["paint"]:
            layerScreen(layer)

        # Overlays
        if Cursor[2] == True:
            screen[MainPlayerPos[0]][MainPlayerPos[1]].fg_color = 5
            screen[MainPlayerPos[0]][MainPlayerPos[1]].char = "◉"

        # Custom Area
        for x in range(xsize): screen[x - 1][ysize].bg_color = 6
        for x in range(xsize): screen[x - 1][ysize + 1].bg_color = 6
        for x in range(xsize): screen[x - 1][ysize + 2].bg_color = 6
        text(0,ysize,f"🎮:[wasd, k]")
        text(0,ysize + 1,f"K to exit")
        text(0,ysize + 2,f"Player: {name}")
        screen[xsize - 1][ysize].bg_color = -1

        flipScreen(xsize,ysize + 3)

    running = True
    while running:
        render(xsize,ysize)
        kp = getinp()
        if kp.strip().lower() == "k":
            running = False
            exit()
        if len(kp) < 1: kp = " "

        oldpos = copy.deepcopy(MainPlayerPos)

        if kp == "a":
            if MainPlayerPos[0] > 0:
                MainPlayerPos[0] -= 1
        elif kp == "d":
            if MainPlayerPos[0] < xsize - 1:
                MainPlayerPos[0] += 1
        elif kp == "s":
            if MainPlayerPos[1] < ysize - 1:
                MainPlayerPos[1] += 1
        elif kp == "w":
            if MainPlayerPos[1] > 0:
                MainPlayerPos[1] -= 1

        if currentMap["collision"][MainPlayerPos[1]][MainPlayerPos[0]] == 1:
            MainPlayerPos = oldpos
        elif currentMap["doors"][MainPlayerPos[1]][MainPlayerPos[0]] != 0:
            if currentMap["doors"][MainPlayerPos[1]][MainPlayerPos[0]][2]:
                door = currentMap["doors"][MainPlayerPos[1]][MainPlayerPos[0]]
                currentMap = load_map(xsize,ysize,door[3])
                mappath = door[3]
                MainPlayerPos[0] = door[0]
                MainPlayerPos[1] = door[1]

        update_player_data(name, MainPlayerPos[0], MainPlayerPos[1], mappath, "")

def editor(xsize, ysize, mappath, selectmode=False):
    global Cursor
    editorMap = None
    if not os.path.exists(mappath):
        editorMap = {
            "paint": [gen2DArray(xsize,ysize,1)],
            "collision": gen2DArray(xsize,ysize,0),
            "doors_vis": gen2DArray(xsize,ysize,0),
            "doors": gen2DArray(xsize,ysize,0)
        }
    else:
        with open(mappath, 'r') as file:
            data = json.load(file)
            editorMap = data
        if "collision" not in editorMap: editorMap["collision"] = gen2DArray(xsize,ysize,0)
        if "doors_vis" not in editorMap: editorMap["doors_vis"] = gen2DArray(xsize,ysize,0)
        if "doors" not in editorMap: editorMap["doors"] = gen2DArray(xsize,ysize,0)

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
        if not selectmode:
            text(0,ysize,f"🎮:[wasd,qe,+-,cr,p,k] layer: {layernum}")
            text(0,ysize + 1,f"(c)olEdit: {editingCollisions}  | X: {Cursor[0]} Y: {Cursor[1]}")
            text(0,ysize + 2,f"doo(r)Edit: {editingDoors}|p=save k=exit")
            screen[xsize - 1][ysize].bg_color = -1
        else:
            for x in range(xsize): screen[x - 1][ysize].bg_color = 5
            for x in range(xsize): screen[x - 1][ysize + 1].bg_color = 5
            for x in range(xsize): screen[x - 1][ysize + 2].bg_color = 5
            text(0,ysize,f"🎮:[wasd, SPACE] layer: {layernum}")
            text(0,ysize + 1,f"SELECT MODE!")
            screen[xsize - 1][ysize].bg_color = -1

        flipScreen(xsize,ysize + 3)

    running = True
    while running:
        render(xsize,ysize)
        kp = getinp()
        if kp.strip().lower() == "k":
            running = False
            exit()
        if len(kp) < 1: kp = " "

        if len(editorMap["paint"]) - 1 < layernum: editorMap["paint"].append(gen2DArray(xsize,ysize,0))
        cursorTile = editorMap["paint"][layernum][Cursor[1]][Cursor[0]]
 
        if selectmode:
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
                return Cursor
        else:
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
            elif kp == "q":
                if editingCollisions:
                    editorMap["collision"][Cursor[1]][Cursor[0]] = 0
                elif editingDoors:
                    editorMap["doors_vis"][Cursor[1]][Cursor[0]] = 0
                    editorMap["doors"][Cursor[1]][Cursor[0]] = 0
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
                    nmapname = None
                    while nmapname == None:
                        nmapname = "maps/" + input("Door leads to the map named: ") + ".json"
                        if not os.path.isfile(nmapname):
                            nmapname = None
                            print("Map not found! Did you save?")
                    editorMapBackup = copy.deepcopy(editorMap)
                    cursorBackup = copy.deepcopy(Cursor)
                    out = editor(xsize, ysize, nmapname, True)
                    x = int(out[0])
                    y = int(out[1])
                    Cursor = cursorBackup
                    editorMap = editorMapBackup
                    isdoor = True
                    editorMap["doors"][Cursor[1]][Cursor[0]] = [x,y,isdoor,nmapname]
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



if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    if sys.argv[1] == "editor":
        emapname = None
        while emapname == None:
            if sys.argv[2] == "new":
                emapname = input("Map Name ('e' to exit): ")
            else:
                emapname = sys.argv[2]
            if emapname == "e":
                exit()
            editor(32,9,"maps/" + emapname + ".json")
            exit()
    elif sys.argv[1] == "game":
        game(32,9,sys.argv[5], [int(sys.argv[3]), int(sys.argv[4])], sys.argv[2])
