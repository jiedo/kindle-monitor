#include <stdio.h>
#include <X11/Xlib.h>

int main()
{
  Display *display;
  Window currwin;      /* root window the pointer is in */
  Window inwin;      /* root window the pointer is in */
  Window inchildwin; /* child win the pointer is in */
  int rootx, rooty; /* relative to the "root" window; we are not interested in these,
                       but we can't pass NULL */
  int childx, childy;  /* the values we are interested in */
  unsigned int mask;   /* status of the buttons */

  display = XOpenDisplay(NULL);
  int revert_to;
  XGetInputFocus(display, &currwin, &revert_to);
  XQueryPointer(display, currwin, &inwin,  &inchildwin,
		&rootx, &rooty, &childx, &childy, &mask);
  printf("relative to active window: %d,%d\n", rootx, rooty);
  (void)XCloseDisplay(display); /* and close the display */
  return 0;
}
