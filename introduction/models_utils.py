from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _



# * Upload file pathes
def benefir_directory_path(instance, filename) :
    file_type = filename.split('.')[1]
    return f'benefits/images/{instance.title}.{file_type}'

def team_member_directory_path(instance, filename) :
    file_type = filename.split('.')[1]
    return f'members/images/{instance.fullname}.{file_type}'

def clip_directory_path(instance, filename):
    file_type = filename.split('.')[1]
    return f'services/clips/{instance.title}.{file_type}'

def pdf_directory_path(instance, filename):
    file_type = filename.split('.')[1]
    return f'services/pdfs/{instance.title}.{file_type}'

def banner_directory_path(instance, filename):
    file_type = filename.split('.')[1]
    return f'banner/images/{instance.title}.{file_type}'


# * Filefield (restricted type)
class FileFieldRestricted(models.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", ['video/mp4', ])
        return super(FileFieldRestricted, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):      
        data = super(FileFieldRestricted, self).clean(*args, **kwargs)
        file = data.file

        try:
            content_type = file.content_type
            if not content_type in self.content_types:
                raise ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
            
        return data