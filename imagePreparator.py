from PIL import Image

class ImagePreparator():
    def cutImage(self, imagePath):
        with Image.open(imagePath) as im:
            box = (500, 0, 3350, 2100)
            im_croped =  im.crop(box)
            im_croped.save('screenshot.png')