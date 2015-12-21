import botticelli as bt


def main():
    img = bt.BottiImg()
    pic = "us_flag"
    img.load_image("img/us_flag.gif")

    #for stars in xrange(1, 51):
    #    bt.modelize_image(img, [stars,], pic)
    #    print "Stars:", stars
    #for stripes in xrange(1, 14):
    #    bt.modelize_image(img, [50, stripes], pic)
    #    print "Stripes:", stripes

    layer_sets = (
        [50, 16], [50, 32], [50, 50], [50, 50, 8], [50, 50, 16], [50, 50, 32], [50, 50, 50]
    )
    for lay in layer_sets:
        bt.modelize_image(img, lay, pic)



if __name__ == "__main__":
    main()