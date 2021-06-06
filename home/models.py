from django.db import models


class MenuItem:
    def __init__(self, name=None, img_url=None, target_url=None):
        self.name = name
        self.img_url = img_url
        self.target_url = target_url
