# Generated by Django 3.2 on 2021-08-15 18:16

from django.db import migrations
import introduction.models_utils


class Migration(migrations.Migration):

    dependencies = [
        ('introduction', '0002_alter_teammember_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='clip',
            field=introduction.models_utils.FileFieldRestricted(blank=True, upload_to=introduction.models_utils.clip_directory_path),
        ),
    ]