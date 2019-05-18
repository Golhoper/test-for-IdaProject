from django.db import models


class ImageModel(models.Model):
    hash = models.TextField(primary_key=True)
    img = models.ImageField(upload_to="articles/")

    class Meta:
        db_table = "image_bt"