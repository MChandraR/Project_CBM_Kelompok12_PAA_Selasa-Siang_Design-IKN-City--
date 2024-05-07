from PIL import Image, ImageDraw
import random

imageWidth = 1500
imageHeight = 1500
padding = 200

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
        if(vertex[0] > imageWidth/2):
            x = imageWidth
        else:
            x = 0
        y = vertex[1]
    else:
        x = vertex[0]
        if(vertex[1] > imageHeight/2):
            y = imageWidth
        else:
            y = 0
    lastVertex = (x, y, edge)
    vertexJalan.append(lastVertex)
    draw.line((vertex[0], vertex[1], lastVertex[0], lastVertex[1]), fill='black', width=20)

def randomVertex(vertex):
    edge = vertex[2]
    if edge == 'x':
        #vertex berikutnya punya y yg sama, x beda
        x = random.randint(padding, imageWidth - padding)
        y = vertex[1]
        edge = 'y'
    else:
        x = vertex[0]
        y = random.randint(padding, imageHeight - padding)
        edge = 'x'

    return x, y, edge

def nextVertex(vertex):
    for i in range(5):
        result = randomVertex(vertex)

        vertexJalan.append(result)
        draw.line((vertex[0], vertex[1], result[0], result[1]), fill='black', width=20)
        vertex = result

        extra = random.choice(['x', 'y'])
        if extra == 'x':
            lastVertex(vertex)
        
        lastVertex(vertex)


startVertex = firstVertex()
vertexJalan.append(startVertex)
nextVertex(startVertex)
whiteLine = [(x, y) for x, y, _ in vertexJalan]
draw.line(whiteLine, fill='white')
print(vertexJalan)

image.show()