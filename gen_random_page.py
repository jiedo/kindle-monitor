import random

x, y = 536, 724
# for i in range(1552256):
for i in range(100):
    x = random.randint(0, 1070)
    y = random.randint(0, 1446)
    w = random.randint(0, (1072-x)/8+1)
    h = random.randint(0, 1448-y)
    c = random.randint(3, 3)

    # x, y, w, h, c = 0, 0, 1072/8, 1448, 3
    # print 3, x, y
    print "%d%s%s%s%s%s%s%s%s%s" % (
        c,
        chr(x%256), chr(x/256),
        chr(y%256), chr(y/256),
        chr(w%256), chr(w/256),
        chr(h%256), chr(h/256),
        "".join([chr(random.randint(0, 255)) for i in range(w*h)]))

# x,y,w,h = 0, 0, 0, 0
# print "%d%s%s%s%s%s%s%s%s" % (1,
#                               chr(x%256), chr(x/256),
#                               chr(y%256), chr(y/256),
#                               chr(w%256), chr(w/256),
#                               chr(h%256), chr(h/256))

x,y,w,h = 0, 0, 0, 0
print "%d%s%s%s%s%s%s%s%s" % (0,
                              chr(x%256), chr(x/256),
                              chr(y%256), chr(y/256),
                              chr(w%256), chr(w/256),
                              chr(h%256), chr(h/256))
# print 1, 0, 0
# print 0, 0, 0
# print "%d%04d%04d" % (1, 0, 0)
# print "%d%04d%04d" % (0, 0, 0)
