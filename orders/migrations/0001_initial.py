# Generated by Django 3.2 on 2021-08-14 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('addresses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50, verbose_name='Fullname')),
                ('address', models.TextField(max_length=500, verbose_name='Address')),
                ('delivery_instructions', models.TextField(blank=True, default='', max_length=500, verbose_name='Delivery instructions')),
                ('phone', models.CharField(max_length=11, verbose_name='Phone Number')),
                ('post_code', models.CharField(max_length=20, verbose_name='Post Code')),
                ('paid', models.BooleanField(default=False, verbose_name='Is Paid')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='addresses.city', verbose_name='City')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='addresses.province', verbose_name='Province')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Order Product',
                'verbose_name_plural': 'Order Products',
            },
        ),
        migrations.CreateModel(
            name='OrderOptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Option Price')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_options', to='store.option', verbose_name='Related Option')),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_items', to='orders.orderproductitem', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Option Related To Ordering Product',
                'verbose_name_plural': 'Options Related To Ordering Products',
            },
        ),
        migrations.CreateModel(
            name='OrderFeatureItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Feature Price')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_features', to='store.feature', verbose_name='Related Feature')),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_items', to='orders.orderproductitem', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Feature Related To Ordering Product',
                'verbose_name_plural': 'Features Related To Ordering Products',
            },
        ),
    ]
