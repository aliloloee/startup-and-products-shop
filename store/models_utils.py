from django.db import models


def image_directory_path (instance, filename) :
    return f"products/{instance.product.pk}/{filename}"

def transparent_image_directory_path (instance, filename) :
    return f"products/transparent-images/{filename}"

class LowerCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()