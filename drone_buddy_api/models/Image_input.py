from django.db import models


class ImageInput(models.Model):
    image = models.ImageField(upload_to='images/')
    engine_configurations = models.TextField()

    def __str__(self):
        return str(self.engine_configurations)
