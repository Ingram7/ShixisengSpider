

import os
from PIL import Image

x = y = 0
line = 20
path = 'image'
NewImage = Image.new('RGB', (128*line, 128*line))
for i in os.listdir(path):
    i = os.path.join(path, i)
    try:
        img = Image.open(i)
        print(img)
        img = img.resize((128, 128), Image.ANTIALIAS)
        NewImage.paste(img, (x * 128, y * 128))
        x += 1
    except IOError:
        print('sad')
        x -= 1
    if x == line:
        x = 0
        y += 1
    if (x + line * y) == line * line:
        break
NewImage.save("logo.jpg")
