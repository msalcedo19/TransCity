from PIL import ImageTk, Image


class ImagesController:
    __images: dict
    __urls: dict

    def urls_images(self):
        train = 'img/circle.png'
        station = 'img/station_v1.png'
        self.__urls['train'] = train
        self.__urls['station'] = station

    def load_images(self) -> dict:
        train_image = Image.open(self.__urls['train'])
        train_image = train_image.resize((15, 15))
        train_image = ImageTk.PhotoImage(train_image)

        station_image = Image.open(self.__urls['station'])
        station_image = station_image.resize((30, 25))
        station_image = ImageTk.PhotoImage(station_image)

        self.__images = {'train': train_image, 'station': station_image}

    def __init__(self):
        self.__images = {}
        self.__urls = {}
        self.urls_images()
        self.load_images()

    def rotate(self, degrees: float, key_image) -> ImageTk:
        url_image = self.__urls[key_image]
        image = Image.open(url_image)
        image = image.resize((25, 25))

        image_rotated = image.rotate(degrees, expand=True)
        image_rotated = ImageTk.PhotoImage(image_rotated)
        return image_rotated

    def get_images(self):
        return self.__images

    def change_image(self, key_image: str, image: ImageTk):
        self.__images[key_image] = image





