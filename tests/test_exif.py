from app import read_exif, cover_gps


def test_read():
    x = read_exif('IMG.jpg')
    print(x)


def test_cover_gps():
    x = cover_gps('[99, 48, 897/25]')
    print(x)
