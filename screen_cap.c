//gcc `pkg-config --libs --cflags atk gdk-2.0` screen_cap.c  -o screen_cap
// gcc `pkg-config --cflags --libs x11` `pkg-config --libs --cflags atk gdk-2.0` screen_cap.c  -o screen_cap


#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gdk/gdk.h>
#include <X11/Xlib.h>

int main(int argc, char **argv)
{
    gdk_init(&argc, &argv);
    GdkWindow *w = gdk_get_default_root_window();
    gint width=1072, height=1448;
    int size_of_data = width*height;
    guchar data[size_of_data/8];
    guchar last_data[size_of_data/8];

    /* Display *display; */
    /* Window currwin;      /\* root window the pointer is in *\/ */
    /* Window inwin;      /\* root window the pointer is in *\/ */
    /* Window inchildwin; /\* child win the pointer is in *\/ */
    /* int rootx, rooty, last_rootx, last_rooty; /\* relative to the "root" window; we are not interested in these, */
    /*                      but we can't pass NULL *\/ */
    /* int childx, childy;  /\* the values we are interested in *\/ */
    /* unsigned int mask;   /\* status of the buttons *\/ */
    /* display = XOpenDisplay(NULL); */
    /* int revert_to; */
    /* XGetInputFocus(display, &currwin, &revert_to); */

    for(;;) {
        GdkPixbuf *pb = gdk_pixbuf_get_from_drawable(NULL,
                                                     GDK_DRAWABLE(w),
                                                     NULL,
                                                     2160,0,0,0,width,height);
        if(pb == NULL) break;
        guchar *img = gdk_pixbuf_get_pixels(pb);
        for(int k=0; k<size_of_data/8; k++) {
            int base_k = k*3*8;
            guchar byte = 0;
            for(int i=0;i<8;i++) {
                guchar r = img[base_k];
                guchar g = img[base_k+1];
                guchar b = img[base_k+2];
                if(r < 200 || g < 200 || b < 200) {
                    byte += (1<<i);
                }
                base_k += 3;
            }
            data[k] = byte;
        }
        g_object_unref(pb);

        /* XQueryPointer(display, currwin, &inwin,  &inchildwin, */
        /*               &rootx, &rooty, &childx, &childy, &mask); */
        /* rootx -= 2160; */
        /* if (abs(rootx - last_rootx) > 1 || abs(rooty - last_rooty) > 1) { */
        /*     last_rootx = rootx; */
        /*     last_rooty = rooty; */
        /*     printf("2%c%c%c%c%c%c%c%c\n", */
        /*            rootx%256, rootx/256, */
        /*            rooty%256, rooty/256, */
        /*            0,0, */
        /*            0,0); */
        /*     fflush(stdout); */
        /* } */

        if (0 == memcmp(data, last_data, size_of_data/8)) {
            continue;
        } else {
            memcpy(last_data, data, size_of_data/8);
        }

        printf("3%c%c%c%c%c%c%c%c",
               0,0,0,0,
               (width/8)%256, (width/8)/256,
               height%256, height/256);
        for(int k=0; k<size_of_data/8; k++) {
            printf("%c", data[k]);
        }
        printf("\n");
        fflush(stdout);
    }
    printf("0%c%c%c%c%c%c%c%c\n",
           0,0,0,0,0,0,0,0);

    /* XCloseDisplay(display); */
    return 0;
}
