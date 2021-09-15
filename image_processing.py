import uuid

import PIL
import cv2
from PIL import Image

'''
    replace all the constants (the one in caps) with your own lists
'''


class ProcessImage:
    image_extensions = ['png', 'jpg', 'jpeg']

    def __init__(self, temp_directory):
        self.temp_directory = temp_directory
        self.temp_files = []

    def convert_image_bw(self, file_path):
        im_gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        thresh, bw_image = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        file_name = 'processed_signature_bw.png'

        cv2.imwrite(self.temp_directory + file_name, bw_image)
        self.temp_files.append(self.temp_directory + file_name)
        return self.temp_directory + file_name

    def remove_background(self, file_path, target_path=None):
        if list(filter(file_path.lower().endswith, self.image_extensions)):
            print('\nRemoving background from image')
            file_path = self.convert_image_bw(file_path)
            image = Image.open(file_path)

            image = image.convert('RGBA')
            image_data = image.getdata()
            new_data = []
            for item in image_data:
                # in this i'm removing all lighter shades which have rgb value
                # greater than or equal to 110
                if item[0] >= 110 and item[1] >= 110 and item[2] >= 110:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            image.putdata(new_data)
            file_name = 'processed_signature.png'

            if not target_path:
                image.save(self.temp_directory + file_name, 'PNG')
            else:
                target_path = str(uuid.uuid4()) + ".png"
                image.save(target_path, "PNG")
                self.temp_files.append(target_path)
                return target_path, self.temp_files
            self.temp_files.append(self.temp_directory + file_name)
            return self.temp_directory + file_name, self.temp_files
        return None

    def compress_image(self, file_path, width=None, height=None, output_file_name=None):
        if list(filter(file_path.lower().endswith, self.image_extensions)) or True:
            image = Image.open(file_path)
            image_size = image.size
            if not width:
                width = image_size[0]
            if not height:
                height = image_size[1]
            wpercent = (width / float(image_size[0]))
            hsize = int((float(image_size[1]) * float(wpercent)))
            image = image.resize((width, hsize), PIL.Image.ANTIALIAS)
            if output_file_name:
                file_name = output_file_name + '_compressed.png'
            else:
                file_name = 'compressed.png'
            image.save(self.temp_directory + file_name)
            return self.temp_directory + file_name
        return None

    def rotate_image(self, image_path, angle):
        color_image = Image.open(image_path)
        rotated_image_path = self.temp_directory + 'image_rotated' + str(angle) + '.png'
        color_image.rotate(angle, expand=True).save(rotated_image_path)
        return rotated_image_path
