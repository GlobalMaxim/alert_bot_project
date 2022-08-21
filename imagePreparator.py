from PIL import Image

class ImagePreparator():
    def cutImage(self, imagePath):
        with Image.open(imagePath) as im:
            box = (200, 0, 1680, 1050)
            im_croped =  im.crop(box)
            im_croped.save('screenshot.png')
