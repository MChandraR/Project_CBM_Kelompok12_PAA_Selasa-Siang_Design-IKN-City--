from PIL import Image, ImageDraw
import random
import math

imageWidth = 1500
imageHeight = 1500

#properti jalan
padding = 100
jumlahPotongan = 8
lebarJalan = 20


image = Image.new("RGB", (imageWidth, imageHeight), "green")
draw = ImageDraw.Draw(image)

vertexJalan = []

def firstVertex():
    edge = random.choice(['atas', 'bawah', 'kiri', 'kanan'])
    
    if edge == 'atas':
        x = random.randint(padding, imageWidth - padding)
        y = 0
        edge = 'y'
    elif edge == 'bawah':
        x = random.randint(padding, imageWidth - padding)
        y = imageHeight
        edge = 'y'
    elif edge == 'kiri':
        x = 0
        y = random.randint(padding, imageHeight - padding)
        edge = 'x'
    else:
        x = imageWidth
        y = random.randint(padding, imageHeight - padding)
        edge = 'x'
    
    return x, y, edge

def lastVertex(vertex):
    edge = vertex[2]
    if edge == 'x':
        if(vertex[0] >= imageWidth//2):
            x = imageWidth
        else:
            x = 0
        y = vertex[1]
    else:
        x = vertex[0]
        if(vertex[1] >= imageHeight//2):
            y = imageHeight
        else:
            y = 0

    for i in range(len(vertexJalan) - 1): #cari ulang endVertex jika terlalu dekat degan vertex lain
        x1, y1, _ = vertexJalan[i]
        if int(math.sqrt((x - x1) ** 2 + (y - y1) ** 2)/2) < padding:
            print('cari ulang endvertex untuk: ', x, y, edge)
            if edge == 'x':
                if vertex[1] < imageHeight//2 and vertex[1] >= y1:
                    y = imageHeight
                elif vertex[1] < imageHeight//2 and vertex[1] < y1:
                    y = 0
                elif vertex[1] >= imageHeight//2:
                    y = imageHeight
                else:
                    y = 0
                x = vertex[0]
            else:
                y = vertex[1]
                if vertex[0] < imageWidth//2 and vertex[0] >= x1:
                    x = imageWidth
                elif vertex[0] < imageWidth//2 and vertex[0]  < x1:
                    x = 0
                elif vertex[0] >= imageWidth//2 and vertex[0] > x1:
                    x = imageWidth
                else:
                    x = 0

    endVertex = (x, y, edge)
    vertexJalan.append(endVertex)
    draw.line((vertex[0], vertex[1], endVertex[0], endVertex[1]), fill='black', width=lebarJalan)
    draw.line((vertex[0], vertex[1], endVertex[0], endVertex[1]), fill='white', width=1)

def randomVertex(vertex):
    edge = vertex[2]
    if edge == 'x': #vertex berikutnya punya y yg sama, x beda
        if vertex[0] - imageWidth//2 <= 0: #jika vertex di kiri, next vertex ke kanan
            x = random.randint(vertex[0] + padding, imageWidth - padding)
        else: #jika vertex di kanan, next vertex ke kiri
            x = random.randint(padding, vertex[0] - padding)
        y = vertex[1]
        edge = 'y'
    else:
        x = vertex[0]
        if vertex[1] >= imageHeight//2: #jika vertex di bawah, next vertex ke atas
            y = random.randint(padding, vertex[1] - padding)
        else: #jika vertex di atas, next vertex ke bawah
            y = random.randint(vertex[1] + padding, imageHeight - padding)
        edge = 'x'

    for i in range(len(vertexJalan) - 1): #cari ulang vertex jika terlalu dekat degan vertex lain
        x1, y1, _ = vertexJalan[i]
        if int(math.sqrt((x - x1) ** 2 + (y - y1) ** 2)/2) < padding:
            print('cari ulang vertex untuk: ', x, y, edge)
            return randomVertex(vertex)
        
    return x, y, edge

def nextVertex(vertex):
    edge = vertex[2]
    if edge == 'x':
        #vertex berikutnya punya y yg sama, x beda
        if vertex[0] == 0:
            x = random.randint(padding, imageWidth - padding)
        else:
            x = random.randint(padding, vertex[0] - padding)
        y = vertex[1]
        edge = 'y'
    else:
        x = vertex[0]
        if vertex[1] == imageHeight:
            y = random.randint(padding, vertex[1] - padding)
        else:
            y = random.randint(padding, imageHeight - padding)
        edge = 'x'

    result = (x, y, edge)
    vertexJalan.append(result)
    draw.line((vertex[0], vertex[1], result[0], result[1]), fill='black', width=lebarJalan)
    draw.line((vertex[0], vertex[1], result[0], result[1]), fill='white', width=1)

    vertex = result

    for i in range(jumlahPotongan):
        result = randomVertex(result)

        vertexJalan.append(result)
        draw.line((vertex[0], vertex[1], result[0], result[1]), fill='black', width=lebarJalan)
        draw.line((vertex[0], vertex[1], result[0], result[1]), fill='white', width=1)
        #draw.ellipse((result[0] - 100, result[1] - 100, result[0] + 100, result[1] + 100), fill='red')
        
        if result[0] - vertex[0] > padding or result[1] - vertex[1] > padding:
            lastVertex(result)

        vertex = result
        
    lastVertex(vertex)

startVertex = firstVertex()
vertexJalan.append(startVertex)
nextVertex(startVertex)
whiteLine = [(x, y) for x, y, _ in vertexJalan]
#for i in range(len(whiteLine)-1):
#    draw.line([whiteLine[i], whiteLine[i+1]], fill="white", width=1)
print(vertexJalan)

image.show()