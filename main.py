import get_image

start, end, orbit = get_image.filter()

if orbit == 'A':
    image_path = './Ascending/'
else:
    image_path = './Descending/'

get_image.open_hub(start, end, image_path)
