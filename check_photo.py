import os
from PIL import Image

path_to_image = 'data/train/images'
size_ok = (518, 409)
flag_ok = True

photo = [f for f in os.listdir(path_to_image) 
				if os.path.isfile(os.path.join(path_to_image, f))]

for i in photo:
	size_i = Image.open(path_to_image + '/' + i).size
	if size_ok != size_i:
		print('Image size not good. Size -', size_i,'\n Ok size - ',size_ok)
		flag_ok = False

print('Images -', flag_ok)	 