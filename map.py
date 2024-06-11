from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk
import random
from numpy import sort

scale = 10
width = 150 * scale
height = 150 * scale
padding = scale
road_width = 2 *scale
maps = Image.new("RGBA", (width , height), "gray")
mapDraw = ImageDraw.Draw(maps,"RGBA")
lastVertices = [(0,0)]
count = 0
roadx, roady = Image.open("assets/roads/roadss-x.png"), Image.open("assets/roads/roadss-y.png")
cornerR, cornerL= Image.open("assets/roads/cornersr2.png") , Image.open("assets/roads/cornersl2.png")
t= Image.open("assets/roads/t.png")
tl= Image.open("assets/roads/tl.png")
tr= Image.open("assets/roads/tr.png")
building = [ 
    [Image.open("assets/buildings/large-x.png"), Image.open("assets/buildings/large-y.png")],[Image.open("assets/buildings/large2-x.jpg"), Image.open("assets/buildings/large2-y.jpg")],
    [Image.open("assets/buildings/medium-x.jpg"), Image.open("assets/buildings/medium-y.jpg")],[Image.open("assets/buildings/medium2-x.jpg"), Image.open("assets/buildings/medium2-y.jpg")],
    [Image.open("assets/buildings/small-x.jpg"), Image.open("assets/buildings/small-y.jpg")],
    # [Image.open("assets/buildings/small2-x.jpg"), Image.open("assets/buildings/small2-y.jpg")],
    [Image.open("assets/buildings/house-x.png"), Image.open("assets/buildings/house-y.png")]
]

decoration = [ Image.open("assets/decor/tree1.png"),Image.open("assets/decor/plan1.png"),Image.open("assets/decor/plan2.png"),Image.open("assets/decor/plant3.png"),Image.open("assets/decor/plant4.png"),Image.open("assets/decor/stone.png"),Image.open("assets/decor/genangan.png")]

def drawArea(pos1, pos2,text):
    if abs(pos1[0] - pos2[0]) > road_width and abs(pos1[1] - pos2[1]) > road_width:
        ysort = sort((pos1[1], pos2[1])) + (padding if pos1[1] > road_width else -padding, -padding)
        xsort = sort((pos1[0], pos2[0])) + (padding if pos1[0] > road_width else -padding, -padding)
        mapDraw.rectangle(((xsort[0], ysort[0]),(xsort[1], ysort[1])), "green")
        posY = ysort[0]
        tertinggi = 10
        while posY < ysort[1] :
            posX = xsort[0] 
            posY = posY if posY <= ysort[1] else ysort[1]
            if posY < 0 :continue
            while posX < xsort[1] - padding:
                if (posY == ysort[0] ) or (posY == ysort[1] ) :
                    builds = [build for build in building if posX + build[0].size[0]< xsort[1]]
                    if len(builds):
                        img = random.choice(builds)
                        tertinggi = max(img[0].size[1] +5, tertinggi)
                        maps.paste(img[0], (posX, posY if posY != ysort[1] else ysort[1]-img[0].size[1]))
                        posX += img[0].size[0] + 5
                    else :break
                else: 
                    if posX >= xsort[1] - 50: posX = xsort[1] - 50
                    if posY + 50 >= ysort[1] -50 and ysort[1] - posY >= 50:
                        posY = ysort[1]
                        continue 
                    builds = [build[1] for build in building if posX + build[1].size[0]< xsort[1] and posY+build[1].size[1] < ysort[1] - 50]
                    decor = [decor for decor in decoration if decor.size[0] + posX <= xsort[1] and decor.size[1] + posY <= ysort[1] - 50]
                    if len(builds):
                        img = random.choice(builds if (posX == xsort[0]  or posX >= xsort[1]-55) else decor)
                        tertinggi = max(img.size[1] +5, tertinggi ) 
                        maps.paste(img, (posX if posX < xsort[1]-50 else xsort[1] - img.size[0], posY + random.randint(0,(tertinggi )-(img.size[1]))))
                        posX += img.size[0] + 5 if posX < xsort[1]-55 else xsort[1] + 5
                    else :break
            posY += tertinggi
 
def drawRoad(start,end,dir):
    for ver in range(start[0] if dir=="x" else start[1], end[0] if dir=="x" else end[1], road_width): maps.paste(roadx if dir == "x" else roady , (ver if dir=="x" else start[0],start[1] if dir=="x" else ver))

def drawCorner(pos, dir):maps.paste(cornerL if dir=="l" else cornerR, pos)

def mapping(ver1,ver2,ver3,ver4,adver,add,text):
    if (ver1[1] == ver2[1] and ver1[0] == ver4[0]) and (ver2[0] == ver3[0] and ver4[1] == ver3[1]) and len(add) < 5 : 
        drawArea((ver1[0]+road_width,ver1[1]+road_width), (ver3[0], ver3[1]), text)
    elif (ver1[1] == ver2[1] and ver1[0] == ver4[0]) and (ver2[0] == ver3[0] and ver4[1] == ver3[1]) and len(add) >= 5  :
        max_atas = max([data[1] for data in add])
        drawArea((ver1[0]+road_width,max_atas+road_width), (ver3[0], ver3[1]), text)
    #Bentuk L Terbalik
    elif ver1[1] >  ver2[1]  and text == "normal" :
        max_atas = max([data[1] for data in add])
        minx = min([ver[0] for ver in add if ver[0] > ver4[0] and ver[1] < max_atas])
        mapping((ver4[0], ver1[1] if len(add) <= 3 else max_atas), (ver2[0], ver1[1] if len(add) <= 3 else max_atas), ver3, ver4, [],[], "bawah")
        mapping((minx,adver[-1:][0][1]), ( ver2[0], adver[-1:][0][1]), (ver2[0], ver1[1] + ((road_width+padding) if ver1[1] < ver3[1] else 0)), (adver[-2:-1][0][0] if len(adver) > 1 else adver[-1:][0][0], ver1[1] + ((road_width+padding) if ver1[1] < ver3[1] else 0)), [], [],"atas")
    #bentuk  L
    elif ver1[1] < ver2[1] and text == "normal":
        max_atas = max([data[1] for data in add])
        mapping((ver1[0], ver2[1]), (ver2[0], ver2[1]), ver3, ver4, adver, [], "bawah")
        mapping(ver1,add[-2:-1][0] if len(add) > 2 else add[-1:][0], (add[-2:-1][0][0] if len(add) >2 else add[-1:][0][0],ver2[1] + ((road_width+padding) if ver2[1] < ver3[1] else 0)),(ver1[0], ver2[1]+ ((road_width+padding) if ver2[1] < ver3[1] else 0)),[],[],"atas")

def limitX(x): return x if x < width else width
def limitY(y): return y if y < height else height

#Algo Jalan dan mapping area
def divideArea(pos, save_point):
    nextJump = (limitX(pos[0]+ random.randint(2,4) * 10*scale),  limitY(random.randint(2,4) * 10*scale))
    limit_atas, limit_atass = pos[1], pos[1]
    midver = []
    max_atas = 0
    overlap = False
    add = [(pos)]
    prev = lastVertices[0]
    for ver in lastVertices:
        if pos[0] > prev[0] and pos[0] < ver[0]: 
            limit_atas = ver[1] 
            if prev != ver : prev = ver
        if ver[0] < nextJump[0]:
            if ver[0]>=pos[0] : 
                if not len(midver): midver = [ver]
                else :midver.append(ver)
            limit_atass = ver[1]
            max_atas = ver[1] if ver[1] > max_atas else max_atas
        if ver[0] < nextJump[0] and ver[0] > pos[0]: add.append(ver)
    maks = max(pos[1],max_atas,limit_atass+nextJump[1])
    nextJump = (nextJump[0], maks if maks<= height else height )
    for ver in save_point: 
        if ver[0] == pos[0] and ver[1] > nextJump[1]: overlap = True
    corcount = sum( [ver == (nextJump[0], limit_atass) for ver in lastVertices])
    drawCorner((pos[0], nextJump[1]-road_width), "l") if (pos[0], nextJump[1]) not in save_point and not overlap and pos[0]> 0 else drawRoad((pos[0], nextJump[1]),(pos[0]+road_width, nextJump[1]),"x")
    if(nextJump[0]+road_width<=width and nextJump[1]  < height):drawCorner((nextJump[0]-road_width, nextJump[1]-road_width), "r")
    if(pos[0]>0): drawRoad((pos[0] , limit_atas+ (road_width if limit_atas>0 else 0) ),(pos[0], nextJump[1]), "y")
    drawRoad((pos[0]+road_width, nextJump[1]),(nextJump), "x")
    drawRoad((nextJump[0], limit_atass+(road_width if not corcount else 0)),(nextJump), "y")
    save_point.extend(((pos[0], nextJump[1]) , nextJump))
    mapping((pos[0],limit_atas), (nextJump[0], limit_atass), nextJump, (pos[0], nextJump[1]), midver,add, "normal")
    if(pos[0] >= 0 and pos[0] < width): 
        divideArea((nextJump[0], limit_atass), save_point)
    else:       
        if(pos[1] >= 0 and pos[1]+200 < height):
            lastVertices.clear()  
            lastVertices.extend((save_point))
            divideArea((0, lastVertices[0][1]), [])
    
vportx , vporty = 0,0
zoom_factor = 1.0
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
viewport_x = 0
viewport_y = 0
viewport_width = 400
viewport_height = 400

def generateMap():
    global maps,mapDraw, lastVertices, count, out, viewport_x, viewport_y
    maps = Image.new("RGBA", (width , height), "gray")
    mapDraw = ImageDraw.Draw(maps,"RGBA")
    lastVertices = [(0,0)]
    count = 0
    divideArea((0,0), [])
    maps.save("map1.png")
    new = Image.new("RGBA", (width , height), "green")
    out = Image.alpha_composite( new,maps)
    out.save("map2.png")
    cropped_map = out.crop((vportx, vporty, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    viewport_x = ((out.width / zoom_factor) - viewport_width) // 2
    viewport_y = ((out.height / zoom_factor) - viewport_height) // 2
    update()

def update():
    global out
    cropped_map = out.crop((viewport_x * zoom_factor, viewport_y * zoom_factor, viewport_x* zoom_factor + viewport_width* zoom_factor, viewport_y* zoom_factor + viewport_height* zoom_factor))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk

def on_key_press(event):
    global viewport_x, viewport_y
    if event.keysym == "Up" and viewport_y > 0:
        viewport_y -= 20
    elif event.keysym == "Down" and viewport_y < (out.height / zoom_factor) - viewport_height:
        viewport_y += 20
    elif event.keysym == "Left" and viewport_x > 0:
        viewport_x -= 20
    elif event.keysym == "Right" and viewport_x < (out.width / zoom_factor) - viewport_width:
        viewport_x += 20
    update()

def scroll(event):
    global zoom_factor, viewport_x, viewport_y
    if event.delta > 0 and zoom_factor < 3.9:
        zoom_factor += 0.1
        viewport_x = ((out.width / zoom_factor) - viewport_width) // 2
        viewport_y = ((out.height / zoom_factor) - viewport_height) // 2
    elif zoom_factor > 1.0:
        zoom_factor -= 0.1
        viewport_x = ((out.width / zoom_factor) - viewport_width) // 2
        viewport_y = ((out.height / zoom_factor) - viewport_height) // 2
    update()

root = tk.Tk()
root.title("Map Generator")
root.state("zoom")
root.configure(bg="#D3D3D3")
root.bind("<MouseWheel>", scroll)
root.bind("<KeyPress>", on_key_press)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = ttk.Style()
style.configure("TFrame", background="#D3D3D3")

frame = ttk.Frame(root, padding=1)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

map_label = ttk.Label(frame)
map_label.grid(row=0, column=0)

frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)

generate_button = ttk.Button(root, text="GENERATE MAP", command=generateMap, width=40)
generate_button.grid(row=1, column=0, pady=90)

generateMap()

root.mainloop()