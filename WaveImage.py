'''WaveImage, by Eyusd'''

import numpy as np
from PIL import Image
from PIL import ImageOps
import matplotlib.pyplot as plt

path = "/Users/Eyusd/Downloads/Caspar_David_Friedrich_-_Wanderer_above_the_sea_of_fog.jpg"

#Basically, it pixellate the image and turn it into black and white
#Then it matches the darkness with the frequency of the sine waves
basewidth = 130         #Numbers of pixels for the base (the original aspect ratio is preserved)
img = Image.open(path).convert('LA')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent))/3)
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img = ImageOps.flip(img)
img.load()
data = np.asarray( img, dtype="int32" )

#Replace by any bijection from [0,1] to [0,1] to adjust the overall repartition of the details
def f(x):
    return x**2

#This integrate the step function represented by the darkness value over the axis
arr=[]
for lignes in data:
    l=[0]
    for e in lignes:
        l.append(l[-1]+f(1-e[0]/256))
    arr.append(l)

#This matches the sines with the correct frequenty, and make sure it's continuous
def freq(t,l):
    ind = int(t)
    m = (l[ind+1]-l[ind])
    p = l[ind] - m*ind
    return m*t + p

def s(t,l):
    return 0.8*np.sin(2*np.pi*freq(t,l))

#Change this n to adapt the size of the display
n =7
fig = plt.figure(figsize = (n,n*3*hsize/basewidth))
fig.patch.set_visible(False)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

#The usual shit
for i in range(len(arr)):
    print(i)
    l = arr[i]
    x = np.linspace(0,basewidth,10000)[:-1]
    y = [3*i +1+s(e,l) for e in x]
    plt.plot(x,y,c='black',linewidth=0.7)
plt.savefig("Wanderer.png",dpi=1000)
plt.show()