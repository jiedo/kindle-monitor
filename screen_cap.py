import time
import sys
import gtk

class Screenshot:
    def __init__(self):
        self.img_width = 1072
        self.img_height = 1448

        self.screengrab = gtk.gdk.Pixbuf(
            gtk.gdk.COLORSPACE_RGB,
            False,
            8,
            self.img_width,
            self.img_height)
        self.root = gtk.gdk.get_default_root_window()
        self.colormap = gtk.gdk.colormap_get_system()

    def take(self):
        self.screengrab.get_from_drawable(
            self.root,
            self.colormap,
            0, 0, 0, 0,
            self.img_width,
            self.img_height)
        return self.screengrab.get_pixels()


def main():
    n = int(sys.argv[1])
    ss = Screenshot()
    for count in range(n):
        make_shot(ss)
    x,y,w,h = 0, 0, 0, 0
    print "%d%s%s%s%s%s%s%s%s" % (0,
                                  chr(x%256), chr(x/256),
                                  chr(y%256), chr(y/256),
                                  chr(w%256), chr(w/256),
                                  chr(h%256), chr(h/256))

def make_shot(screenshot):
    img = screenshot.take()
    data = [0]*(len(img)/3/8)
    base = [1, 2, 4, 8, 16, 32, 64, 128]
    for k in range(len(img)/3/8):
        base_k = k*3*8
        byte = 0
        for i in range(8):
            r = img[base_k]
            g = img[base_k+1]
            b = img[base_k+2]
            # gray = (ord(r)*30 + ord(g)*59 + ord(b)*11 + 50) / 100
            if ord(r) < 200 or ord(g) < 200 or ord(b) < 200:
                byte += base[i]
            base_k += 3
        data[k] = byte

    x, y, w, h, c = 0, 0, 1072/8, 1448, 3
    print "%d%s%s%s%s%s%s%s%s%s" % (
        c,
        chr(x%256), chr(x/256),
        chr(y%256), chr(y/256),
        chr(w%256), chr(w/256),
        chr(h%256), chr(h/256),
        "".join([chr(i) for i in data]))

if __name__ == '__main__':
    main()
