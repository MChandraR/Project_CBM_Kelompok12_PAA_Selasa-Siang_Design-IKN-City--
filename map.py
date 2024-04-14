from PIL import Image, ImageDraw
import random
import math

# Ukuran gambar dan jumlah langkah
scale = 10
width = 150 * scale
height = 150 * scale
max_count = 20
roadWidth = 15

streetv = Image.open("image/streetv.png")
streeth = Image.open("image/streeth.png")
building = Image.open("image/buildings.png")
school = Image.open("image/school.png")
house = Image.open("image/house.png")
buildings = [building,house,school]
tree = Image.open("image/tree.png")
pinus = Image.open("image/pinuss.png")
image = Image.new("RGBA", (width, height), color="green")
images = Image.new("RGBA", (width, height), color="green")
draw = ImageDraw.Draw(image)
draws = ImageDraw.Draw(images)
trees = [tree,pinus]
#vertexList = [(0,0),(width-(2*scale),height-(2*scale)),(0,height-(2*scale)),(width-(2*scale),0)]
vertexList = []

def generateVertex(width, height, previousVertex, vertexList):
    min_distance = min(width, height) / 15  #Jarak minimum antar vertex
    while True:
        edge = random.choice(['x', 'y'])

        if edge == 'x':
            x = previousVertex[0]
            y = random.randint(0, height)
        else:
            x = random.randint(0, width)
            y = previousVertex[1]

        if all(math.sqrt((x - v[0])**2 + (y - v[1])**2) >= min_distance for v in vertexList):
            valid_point = True
            for i in range(len(vertexList) - 1):
                x1, y1, _ = vertexList[i]
                x2, y2, _ = vertexList[i + 1]
                distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
                if distance < min_distance:
                    valid_point = False
                    break

            if valid_point:
                return x, y, edge

def firstVertex(width, height):
    edge = random.choice(['atas', 'bawah', 'kiri', 'kanan'])
    
    if edge == 'atas':
        x = random.randint(0, width)
        y = 0
    elif edge == 'bawah':
        x = random.randint(0, width)
        y = height
    elif edge == 'kiri':
        x = 0
        y = random.randint(0, height)
    else:
        x = width
        y = random.randint(0, height)
        
    return x, y

def lastVertex(width, height, previousVertex):
    edge = previousVertex[2]
    if(edge == 'x'):
        edge = 'y'
    else:
        edge = 'x'

    if edge == 'x':
        x = previousVertex[0]
        if(previousVertex[1] > height/2):
            y = height
        else:
            y = 0
    else:
        if(previousVertex[0] > width/2):
            x = width
        else:
            x = 0
        y = previousVertex[1]

    return x, y, edge

def drawArea(x,y,x1,y1,side):
    padding  = 2*scale
    x += padding ; y+= padding
    if x >= x1-scale or y >= y1-scale:
        return
    curX,curY = x ,y
    
    gedung = random.choice(buildings)
    if  gedung.size[0] < (x1-x-scale) and  gedung.size[1] < (y1-y-scale):
        image.paste(gedung,(x,y))
    elif (x1-x) > tree.size[0] and (y1-y) > tree.size[1] :
        gedung = random.choice(trees)
        image.paste(gedung,(x,y))
    while (curX + gedung.size[0] + padding) < x1 and side:
        size = gedung.size[0] + scale
        if y+building.size[0]-padding < y1:
            drawArea(curX+size,y-padding,x1,y+building.size[0]-padding,False)
        curX += size + scale
    while (curY + gedung.size[1] + padding) < y1 and side:
        size = gedung.size[1] + scale
        if x+building.size[1]-padding < x1:
            drawArea(x-padding,curY+size,x+building.size[1]-padding,y1,False)
        curY += size + scale
    
    if (x+gedung.size[0]-padding+scale)<x1 and (y+gedung.size[1]-padding+scale) < y1 and not side:
        drawArea(x+gedung.size[0],y+gedung.size[1],x1,y1,True)

def search():
    for idx, ver in enumerate(vertexList):
        minX  = 0
        nearX = width
        nearY = height
        minY = 0
        maxX = 0
        maxY = 0
        for i in range(0,len(vertexList)):
            if i == idx :
               continue
            if vertexList[i][0] > ver[0] and vertexList[i][0]  < nearX:
                nearX = vertexList[i][0]
            if vertexList[i][1] > ver[1] and vertexList[i][1]  < nearY:
                nearY = vertexList[i][1]
            if vertexList[i][0] >= minX and vertexList[i][0] < ver[0]:
               minX = vertexList[i][0]
               maxY = vertexList[i][1]
            if vertexList[i][1] >= minY and vertexList[i][1] < ver[1]:
               minY = vertexList[i][1]
               maxX = vertexList[i][0]
        if minX > 0 and minY > 0:
            print("jumpa")
            if (minX,minY) not in vertexList:
                vertexList.append((minX,minY)) 
            if (maxX,maxY) not in vertexList:
                vertexList.append((maxX,maxY))
            print(ver, minX,minY)
            drawArea(minX+scale,minY+scale,ver[0],ver[1],True)
        if (nearX,nearY) not in vertexList:
            vertexList.append((nearX,nearY))
        if minX == 0 or minY == 0:
            drawArea(minX,minY,ver[0],ver[1],True)
       
#generate firstVertex
previousVertex = firstVertex(width, height)
vertexList.append(previousVertex + ('',))

#generate random Vertex
for _ in range(max_count - 2):
    nextVertex = generateVertex(width, height, previousVertex, vertexList)
    draw.line((previousVertex[0], previousVertex[1], nextVertex[0], nextVertex[1]), fill='black', width=roadWidth)
    #draw.ellipse((nextVertex[0] - 2, nextVertex[1] - 2, nextVertex[0] + 2, nextVertex[1] + 2), fill='red')
    previousVertex = nextVertex
    vertexList.append(nextVertex)

#generate lastVertex
endVertex = lastVertex(width, height, previousVertex)
vertexList.append(endVertex)
draw.line((previousVertex[0], previousVertex[1], endVertex[0], endVertex[1]), fill='black', width=roadWidth)

search()
print(vertexList)
print(len(vertexList))
for ver in vertexList:
   draws.rectangle(xy = (ver[0],ver[1],ver[0]+(2*scale),ver[1]+(2*scale)),fill=(0,0,0))
# Menyimpan gambar sebagai file
image.show()
#image.save("map2.png")
#images.save("vertices.png")