# Generated by Django 3.2 on 2021-08-14 20:11

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import store.models_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', store.models_utils.LowerCharField(max_length=150, verbose_name='Category Name')),
                ('name_en', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Category Name')),
                ('name_fa', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Category Name')),
                ('name_ar', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Category Name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_fa', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_ar', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('transparent_image', models.ImageField(default='images/default.png', help_text='Upload a Transparent image.', upload_to=store.models_utils.transparent_image_directory_path, verbose_name='Transparent Image')),
                ('price', models.DecimalField(decimal_places=0, error_messages={'name': {'max_length': 'The price must be between 0 and 99.999.999 toman'}}, help_text='Maximum 99 milion toman', max_digits=8, verbose_name='Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=0, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 99 milion toman', max_digits=8, null=True, verbose_name='Discount Price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default.png', help_text='Upload a product image', upload_to=store.models_utils.image_directory_path, verbose_name='Image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('alt_text_en', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('alt_text_fa', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('alt_text_ar', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OptionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', store.models_utils.LowerCharField(max_length=150, verbose_name='Title Name')),
                ('name_en', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Title Name')),
                ('name_fa', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Title Name')),
                ('name_ar', store.models_utils.LowerCharField(max_length=150, null=True, verbose_name='Title Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('product', models.ManyToManyField(related_name='titles', to='store.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Option title',
                'verbose_name_plural': 'Option titles',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name_fa', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=0, error_messages={'name': {'max_length': 'The price must be between 0 and 9.999.999 toman'}}, help_text='Maximum 9 milion toman', max_digits=7, verbose_name='Price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='store.optioncategory', verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
                'ordering': ('-created',),
            },
            managers=[
                ('actives', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name_fa', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=0, error_messages={'name': {'max_length': 'The price must be between 0 and 9.999.999 toman'}}, help_text='Maximum 9 milion toman', max_digits=7, verbose_name='Price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('product', models.ManyToManyField(related_name='features', to='store.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Feature',
                'verbose_name_plural': 'Features',
                'ordering': ('-created',),
            },
            managers=[
                ('actives', django.db.models.manager.Manager()),
            ],
        ),
    ]
