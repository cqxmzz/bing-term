import urllib2
import urllib, cStringIO
from PIL import Image
import random
from bisect import bisect
import sys

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

greyscale = [
            " ",
            " ",
            ".,-",
            "_ivc=!/|\\~",
            "gjez2]/(YL)t[+T7Vf",
            #"mdK4ZGbNDXY5P*Q",
            #"W8KMA",
            "#%$"
            ]
 
# zonebounds=[36,72,108,144,180,216,252]
zonebounds=[36,72,108,144,252]
zonebounds = [256-(256-x)/2.5 for x in zonebounds]

imageCount = "1"
useColor = False
if len(sys.argv) >= 2:
    imageCount = sys.argv[1]
    if len(sys.argv) >= 3:
        useColor = True

bingUrl = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=" + imageCount
imageProfile = urllib2.urlopen(bingUrl).read()

imageProfileLength = len(imageProfile)

urlFrontIdx = -1
urlEndIdx = -1

urlNum = int(imageCount)
if urlNum >= 9:
    urlNum = 1

for i in range(imageProfileLength):
    if i < imageProfileLength-5 and imageProfile[i] == 'u' and imageProfile[i+1] == 'r' and imageProfile[i+2] == 'l' and imageProfile[i+3] == '\"':
        urlFrontIdx = i+6
        urlNum = urlNum - 1
        if urlNum != 0:
            continue
        for j in range(i+6, imageProfileLength):
            if imageProfile[j] == '\"':
                urlEndIdx = j
                break;
    if urlEndIdx > 0:
        break;
imageUrl = "http://bing.com/" + imageProfile[urlFrontIdx:urlEndIdx]


file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
im = Image.open(file)
im=im.resize((getTerminalSize()[0], getTerminalSize()[0]/4),Image.BILINEAR)

rgb_im = im.convert('RGB')
im=im.convert("L")

if useColor == False:
    str=""
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            lum=255-im.getpixel((x,y))
            row=bisect(zonebounds,lum)
            possibles=greyscale[row]
            str=str+possibles[random.randint(0,len(possibles)-1)]
        str=str+"\n"
    print str
else:
    difLimit = 50
    str=""
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            ch = "#"
            r, g, b = rgb_im.getpixel((x, y))
            if r < 128 and g < 128 and b < 128:
                color = '\033[30;40m'
            if r < 128 and g < 128 and b >= 128:
                color = '\033[34;40m'
            if r < 128 and g >= 128 and b < 128:
                color = '\033[32;40m'
            if r >= 128 and g < 128 and b < 128:
                color = '\033[31;40m'
            if r < 128 and g >= 128 and b >= 128:
                color = '\033[36;40m'
            if r >= 128 and g < 128 and b >= 128:
                color = '\033[35;40m'
            if r >= 128 and g >= 128 and b < 128:
                color = '\033[33;40m'
            if r >= 128 and g >= 128 and b >= 128:
                color = '\033[37;40m'
            m = (r + g + b) / 3
            dif = abs(r-m) + abs(g-m) + abs(b-m)
            if dif < difLimit:
                lum=255-im.getpixel((x,y))
                row=bisect(zonebounds,lum)
                possibles=greyscale[row]
                ch = possibles[random.randint(0,len(possibles)-1)]
                color = '\033[37;40m'
            str=str+color+ch
        str=str+"\n"
    print str

print('\033[0m' + "Bing!\n")








