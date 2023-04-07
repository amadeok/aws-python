# You can use the `random` module in Python to generate random colors. Here is an example code to generate a random dark color and a random bright color using the `random` module and visualize them using the `matplotlib` library:

# ```python
import random, time, threading
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns, webcolors
# importing libraries
import numpy as np
import time
import matplotlib.pyplot as plt


import random
import colorsys



# creating initial data values
# of x and y
# x = np.linspace(0, 10, 100)
# y = np.sin(x)
#  # to run GUI event loop
# plt.ion()
#figure, ax = plt.subplots(figsize=(10, 8))
#line1, = ax.plot(x, y)
#plt.xlabel("X-axis")
#plt.ylabel("Y-axis")

def random_color():
  red = random.randint(0, 255)
  green = random.randint(0, 255)
  blue = random.randint(0, 255)

  # To ensure that the color is bright and clear
  while (red + green + blue) < 383:
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

  return (red, green, blue)

#fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 4))
def to_hex(r,g,b, norm=False):
        if norm:
            r =int(255*r)
            g = int(255*g)
            b = int(255*b)
        return '#%02X%02X%02X' % (r,g,b)





# Have colormaps separated into categories:
# http://matplotlib.org/examples/color/colormaps_reference.html
cmaps = [
           ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ]


# nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps)
# gradient = np.linspace(0, 1, 256)
# gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, name, nrows):
    fig, ax = plt.subplots(nrows=nrows)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    ax.set_title(cmap_category + ' colormaps', fontsize=14)

    #for ax, name in zip(axes, cmap_list):
    ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
    pos = list(ax.get_position().bounds)
    x_text = pos[0] - 0.01
    y_text = pos[1] + pos[3]/2.
    fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
   # for ax in axes:
    ax.set_axis_off()

fonts = ['Open Sans', 'Arial Rounded MT Bold', 'Bauhaus 93', 'Berlin Sans FB', 'Cambria Math', 'Comic Sans MS', 'Eras Bold ITC', 'Eras Demi ITC', 'Gill Sans Ultra Bold Condensed', 'Harrington', 'High Tower Text', 'Imprint MT Shadow', 'Jokerman', 'Kristen ITC',"Maiandra GD","Matura MT Script Capitals","MS PGothic","MV Boli","Trebuchet MS","Tw Cen MT","Tw Cen MT Condensed Extra Bold","Ubuntu","Open Sans"]
#ret = plt.get_cmap("Paired")
#colors = ret.colors

#plot_color_gradients("Qualitative", "Paired", 1)

#plt.show()
def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def get_color_name(hex_code="", rgb=None, norm=False):
    xx = None; hex = None
    try:
        if len(hex_code):
            rgb = webcolors.hex_to_rgb(hex_code)

        #if norm:
        #    rgb = tuple(val*255.0 for val in rgb)    
        xx = tuple(int(val*255) for val in rgb) if norm else rgb
        hex = rgb_to_hex(xx[0], xx[1], xx[2])

        color_name = webcolors.rgb_to_name(xx )
        
        return xx, color_name, hex
        
    except Exception as e:
        print(e)
        return xx, "", hex
    
import math
def lum(v):
    v /= 255
    if v <= 0.03928:
        return  v / 12.92 
    else:
        return math.pow((v + 0.055) / 1.055, 2.4);

def luminance(r, g, b):
  a = [r, g, b] = lum(r), lum(g), lum(b)

  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;

def contrast(rgb1, rgb2):
  lum1 = luminance(rgb1[0], rgb1[1], rgb1[2]);
  lum2 = luminance(rgb2[0], rgb2[1], rgb2[2]);
  brightest = max(lum1, lum2);
  darkest = min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05)


import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
comp = fusion.GetCurrentComp()
textp = comp.ActiveTool()

inputs = textp.GetInputList().values()
names = ["Layout Angle X"]
for inp in inputs:
    name = inp.GetAttrs()["INPS_Name"]
    print("### " + name)
    if name in names:
        attrs =inp.GetAttrs ()
        for key, val in attrs.items():
            print("###### ", key.ljust(30), " ", val)

ff = []
while 1:
    angle_l = [iii for iii in range(random.randint(1,3))]
    print(angle_l)


def get_random_text_style(operator, min_contrast, font_list):
    pastel_palette = sns.color_palette("pastel", 100)
    dark_palette = sns.color_palette("dark", 100)

    while 1: 
        p_cc = random.choice(pastel_palette)
        d_cc = random.choice(dark_palette)
        c = contrast([e*255 for e in p_cc]  , [e*255 for e in d_cc])
        if c > min_contrast:
            break
    rgb_tuple1, color_name, hex1 = get_color_name(rgb=p_cc, norm=True)
    operator.Red1, operator.Green1, operator.Blue1 =  p_cc
    rgb_tuple2, color_name, hex2 = get_color_name(rgb=d_cc, norm=True)
    operator.Red2, operator.Green2, operator.Blue2 =  d_cc
    operator.Font = random.choice(font_list)
    operator.Thickness2 = 0.2
    operator.ElementShape2 = random.randint(1,2)
    print(operator.GetInput("Style"))


import numpy as np
point = np.array([0.5,0.855])
vec = np.array([1,1]) #Don't need unit vectors
disp = 1

dirs_l = [(1,0), (-1, 0), (0, 1), (0, -1), (1,1), (-1,-1), (-1,1), (1,-1) ]

def point_displacement(point, vec, disp):
    nn = np.linalg.norm(vec)
    unit_vec = vec / nn
    return point + disp * unit_vec

print(point_displacement(point, vec, disp))
x1 = [0 for elem in dirs_l]# np.linspace(0, 10, 30)
y1 = [0 for elem in dirs_l]#np.linspace(0, 10, 30)
for i, dir in enumerate(dirs_l):
    d = dir[0:2]
    p = point_displacement(point, d, 1)
    x1[i] = p[0]
    y1[i] = p[1]
x1 += [point[0]]
y1 += [point[1]]

plt.plot(x1, y1, 'o', color='black');
plt.show()
for _ in range(5000):
    new_y = np.sin(x-0.5*_)
 #   line1.set_xdata(x)
 #   line1.set_ydata(new_y)
    


    print()
    get_random_text_style(textp, 6, fonts)


    # ax[0].set_title('Random Dark Color')
    # ax[0].set_facecolor(hex1)
    # ax[1].set_title('Random Bright Color')
    # ax[1].set_facecolor(hex2)
    # #ax[2].set_facecolor(hex3)

    # #figure.canvas.draw()
    # #figure.canvas.flush_events()
    # fig.canvas.flush_events()
    time.sleep(0.1)

    # generate a random dark color
    
# ```

# This code generates a random dark color by selecting three random values between 0 and 128 for the red, green, and blue channels respectively, and then formatting the RGB values into a hexadecimal string. It generates a random bright color by selecting a random value from a list of CSS4 colors and converting it to a hexadecimal string using the `to_hex` function from the `matplotlib.colors` module.

# The code then visualizes the colors using a matplotlib figure with two subplots, each with a title and a face color set to the randomly generated colors. Finally, it calls `plt.show()` to display the figure.