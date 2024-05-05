# You can use the `random` module in Python to generate random colors. Here is an example code to generate a random dark color and a random bright color using the `random` module and visualize them using the `matplotlib` library:

# ```python
import random, time, threading
import winreg
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns, webcolors
# importing libraries
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image

import dns.update
import dns.query
import dns.reversename
import dns.rdatatype
import sys, os
import dotenv
dotenv.load_dotenv()
sys.path.insert(0, os.getenv("RESOLVE_PYTHON_PATH") )

# def create_dns_record():
#     ### Create A Record
#     dns_domain = "%s." % (domain) # Set the domain name with a trailing dot (to stop auto substitution of zone)
#     update = dns.update.Update(dns_domain) # Prepare the payload for DNS record update in the given zone/domain (dns_domain)
#     update.replace(new_hostname, TTL, 'A', new_ipaddress) # Inject the record details into the dns.update.Update class
#     response = dns.query.tcp(update, dns.rdatatype.PRIMARY_DNS_SERVER_IP, timeout=5) # Submit the new record to the DNS server to apply the update
#     ### Create reverse entry (PTR)
#     reventry = dns.reversename.from_address(new_ipaddress) # Neat function to generate a reverse entry
#     revzone = ''
#     revzone = '.'.join(dns.name.from_text(str(reventry)).labels[3:]) # Specify the reverse lookup zone based on the reverse IP address.
#     # The labels[X:] property allows you to specify which octet to use.
#     # e.g. 3: will apply the record to the 10.in-addr.arpa zone, whereas 1: will apply it to the 72.23.10.in-addr.arpa zone
#     raction = dns.update.Update(revzone) # Prepare the payload for the DNS record update
#     new_host_fqdn = "%s.%s." % (new_hostname, dns_domain) # Although we are updating the reverse lookup zone, the record needs to point back to the ‘test.example.com’ domain, not the 10.in-addr.arpa domain
#     raction.replace(reventry, TTL, dns.rdatatype.PTR, new_host_fqdn) # Inject the updated record details into the the class, preparing for submission to the DNS server
#     response = dns.query.tcp(raction, dns.rdatatype.PRIMARY_DNS_SERVER_IP, timeout=5) # submit the new record to the DNS server to apply the update
 
# domain = "ayurveda.sytes.net"
# new_ipaddress = "176.201.144.175"
# new_hostname = "server01"
# PRIMARY_DNS_SERVER = "8.8.8.8"
# TTL = "1200"
# create_dns_record()





import random,mss
import colorsys

# import dxcam
# camera = dxcam.create()  # returns a DXCamera instance on primary monitor
# camera.start(target_fps=120)  # Should not be made greater than 160.

# A =dxcam.device_info()
# while True :

#     # The screen part to capture
#     monitor = {"top": 160, "left": 160, "width": 1920, "height": 1080}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

#     # Grab the data
#     left, top = (1920 - 640) // 2, (1080 - 640) // 2
#     right, bottom = left + 640, top + 640
#     region = (left, top, right, bottom)
#     t = time.time()
#     frame = camera.grab(region=region)
#     print(time.time() - t)
#     time.sleep(0.1)
#     #Image.fromarray(frame).show()




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
        #print(e)
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
while not comp:
    comp = fusion.GetCurrentComp()
#s.comp.SetActiveTool(media_in_tool)

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
# while 1:
#     angle_l = [iii for iii in range(random.randint(1,3))]
#     print(angle_l)
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

def get_random_text_style_(operator, min_contrast, font_list):
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

def get_font_s(font):
    font = TTFont(font)
    cmap = font['cmap']
    t = cmap.getcmap(3,1).cmap
    s = font.getGlyphSet()
    units_per_em = font['head'].unitsPerEm

    def getTextWidth(text,pointSize):
        total = 0
        for c in text:
            if ord(c) in t and t[ord(c)] in s:
                total += s[t[ord(c)]].width
            else:
                total += s['.notdef'].width
        total = total*float(pointSize)/units_per_em;
        return total

    text = 'This is a test'

    width = getTextWidth(text,12)

    # print ('Text: "%s"' % text)
    # print ('Width in points: %f' % width)
    # print ('Width in inches: %f' % (width/72))
    # print ('Width in cm: %f' % (width*2.54/72))
    # print ('Width in WP Units: %f' % (width*1200/72))
    return width

def get_random_text_style(operator, min_contrast, font_list, _):
    font__ = font_list[_] #random.choice(font_list)
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
    operator.Thickness2 = 0.2
    operator.ElementShape2 = random.randint(1,2)
    operator.Level2 = 1# {1: 'Text', 2: 'Line', 3: 'Word', 4: 'Character'}
    operator.Round2 = 0.23
    time.sleep(0.0)

    operator.Font =  font__ 
    operator.Style = "Regular"
    
    font_path = fonts_[font__]["Regular"] 
    try:
        bb = get_font_s(font_path)
        # font = ImageFont.truetype(font_path , 12)
        # bb = font.getlength('X')
    except:
        bb = -1
    
    
    #print(fonts[_], bb)

    print(f"n {_} | font {font__} | size {bb} || {operator.GetInput('Font')}, c1 {hex1} c2 {hex2} , Shape: {operator.GetInput('ElementShape2')}")

import numpy as np
point = np.array([0.5,0.855])
vec = np.array([1,1]) #Don't need unit vectors
disp = 1

dirs_l = [(1,0), (-1, 0), (0, 1), (0, -1), (1,1), (-1,-1), (-1,1), (1,-1) ]



fonts_ =  fusion.FontManager.GetFontList()
fonts = list(fonts_.keys())
black_list = ["AmpleSoundTab", "Blackadder ITC", "Bookshelf Symbol 7", "Edwardian Script ITC", "Freestyle Script", "Fusion Shapes", "Gill Sans MT Ext Condensed Bold", "HoloLens MDL2 Assets", "Javanese Text", "Juice ITC", "Kunstler Script", "Marlett", "MingLiU-ExtB", "MS Outlook", "MS Reference Specialty", "MT Extra", "Onyx", "Palace Script MT", "Parchment", "Playbill", "Sans Serif Collection", "Segoe Fluent Icons", "Segoe MDL2 Assets", "SWGamekeys MT", "Symbol", "Vladimir Script", "Webdings", "Wingdings", "Wingdings 2", "Wingdings 3", "Lucida Console", "Consolas", "Courier New", "Droid Sans Mono", "Footlight MT Light", "Niagara Solid", "Niagara Engraved", "Rage Italic", "UI Emoji"]

black_list_too_big =  ['Algerian', 'AmpleSoundTab', 'AniMe Matrix - MB_EN', 'Arial Rounded MT Bold', 'Blackadder ITC', 'Bookman Old Style', 'Broadway', 'Cascadia Code', 'Cascadia Mono', 'Castellar', 'Century', 'Century Schoolbook', 'Comic Sans MS', 'Consolas', 'Cooper Black', 'Copperplate Gothic Bold', 'Copperplate Gothic Light', 'Courier New', 'Edwardian Script ITC', 'Elephant', 'Engravers MT', 'Eras Bold ITC', 'Felix Titling', 'Fira Mono', 'Footlight MT Light', 'Franklin Gothic Heavy', 'Freestyle Script', 'Gill Sans MT Ext Condensed Bold', 'Gill Sans Ultra Bold', 'Goudy Stout', 'HoloLens MDL2 Assets', 'Ink Free', 'Javanese Text', 'Jokerman', 'Juice ITC', 'Kristen ITC', 'Kunstler Script', 'Lucida Bright', 'Lucida Console', 'Lucida Fax', 'Lucida Sans', 'Lucida Sans Typewriter', 'Lucida Sans Unicode', 'Matura MT Script Capitals', 'MS Reference Sans Serif', 'MV Boli', 'Niagara Engraved', 'Niagara Solid', 'OCR A Extended', 'Onyx', 'Palace Script MT', 'Parchment', 'Playbill', 'Rage Italic', 'Ravie', 'Rockwell Extra Bold', 'ROG Fonts', 'Sans Serif Collection', 'Segoe Fluent Icons', 'Segoe MDL2 Assets', 'Segoe Print', 'Segoe Script', 'Showcard Gothic', 'SimSun-ExtB', 'Snap ITC', 'Stencil', 'Verdana', 'Vladimir Script', 'Wide Latin', 'Neue Haas Grotesk Text Pro', 'Rockwell Nova', 'Verdana Pro']

black_list+= black_list_too_big #fonts too big

black_list_n = [2, 13, 17, 49, 66, 68, 76, 86, 92, 94, 96, 111, 124, 131, 134, 136, 146, 150, 153, 156, 166, 168, 169, 184, 186, 199, 200, 202, 203, 204]
fonts_f = []
for k, f in fonts_.items():
    if not "Regular" in  f:
        continue
    try:
        w = get_font_s(f["Regular"])
        if w < 70 and not k in black_list:
            fonts_f.append(k)
        elif not k in black_list_too_big:
            black_list_too_big.append(k)
    except Exception as e:print(e)
    
    #fonts_f = [f for k, p in fonts if get_font_s(fonts_[fonts[_]]) < 70]
print("\n\n", black_list_too_big)
from PIL import ImageFont
import PIL
PIL.__version__
def get_available_fonts_win():
    fonts_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
    num_fonts = winreg.QueryInfoKey(fonts_key)[1]
    available_fonts = []
    for i in range(num_fonts):
        font_name, font_path = winreg.EnumValue(fonts_key, i)[:2]
        available_fonts.append((font_name, font_path))
    winreg.CloseKey(fonts_key)
    return available_fonts
    
wf = get_available_fonts_win()
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

max_size = 1100
for _ in range(5000):
    #new_y = np.sin(x-0.5*_)
 #   line1.set_xdata(x)
 #   line1.set_ydata(new_y)
    # try:
    # fn = fonts[_]
    # font_size = 24
    if not "Regular" in  fonts_[fonts_f[_]]:
        continue
    # font_path = fonts_[fonts[_]]["Regular"]  # Replace with the path to your font file

    # font = ImageFont.truetype(font_path , 12)
    # bb = font.getlength('A')

    # print(fonts[_], bb)
    # continue
    if fonts_f[_] in black_list:
        continue
    print()
    get_random_text_style(textp, 6, fonts_f, _)


    # ax[0].set_title('Random Dark Color')
    # ax[0].set_facecolor(hex1)
    # ax[1].set_title('Random Bright Color')
    # ax[1].set_facecolor(hex2)
    # #ax[2].set_facecolor(hex3)

    # #figure.canvas.draw()
    # #figure.canvas.flush_events()
    # fig.canvas.flush_events()
    time.sleep(0.1)
    n = 0
    # generate a random dark color
    
# ```

# This code generates a random dark color by selecting three random values between 0 and 128 for the red, green, and blue channels respectively, and then formatting the RGB values into a hexadecimal string. It generates a random bright color by selecting a random value from a list of CSS4 colors and converting it to a hexadecimal string using the `to_hex` function from the `matplotlib.colors` module.

# The code then visualizes the colors using a matplotlib figure with two subplots, each with a title and a face color set to the randomly generated colors. Finally, it calls `plt.show()` to display the figure.


# def point_displacement(point, vec, disp):
#     nn = np.linalg.norm(vec)
#     unit_vec = vec / nn
#     return point + disp * unit_vec

# print(point_displacement(point, vec, disp))
# x1 = [0 for elem in dirs_l]# np.linspace(0, 10, 30)
# y1 = [0 for elem in dirs_l]#np.linspace(0, 10, 30)
# for i, dir in enumerate(dirs_l):
#     d = dir[0:2]
#     p = point_displacement(point, d, 1)
#     x1[i] = p[0]
#     y1[i] = p[1]
# x1 += [point[0]]
# y1 += [point[1]]

# plt.plot(x1, y1, 'o', color='black');
# plt.show()