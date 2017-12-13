import gtk
class screenshot:
    def __init__(self):
        self.img_width = gtk.gdk.screen_width()
        self.img_height = gtk.gdk.screen_height()

        self.screengrab = gtk.gdk.Pixbuf(
            gtk.gdk.COLORSPACE_RGB,
            False,
            8,
            self.img_width,
            self.img_height)

    def take(self):
        self.screengrab.get_from_drawable(
            gtk.gdk.get_default_root_window(),
            gtk.gdk.colormap_get_system(),
            0, 0, 0, 0,
            self.img_width,
            self.img_height)

        return self.screengrab.get_pixels()

if __name__ == '__main__':
    import time
    screenshot = screenshot()
    ti = time.time()
    print len(screenshot.take())
    tii = time.time()
    print tii-ti
