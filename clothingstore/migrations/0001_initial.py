# Generated by Django 4.1.1 on 2022-11-03 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('phonenumber', models.CharField(max_length=14)),
                ('first_name', models.CharField(default='None', max_length=30)),
                ('last_name', models.CharField(default='None', max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('profilepic', models.ImageField(blank=True, default='user.png', null=True, upload_to='')),
                ('id_number', models.CharField(default='None', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30)),
                ('product_category', models.CharField(choices=[('shirt', 'shirt'), ('jeans', 'jeans'), ('shoes', 'shoes')], max_length=14)),
                ('product_price', models.IntegerField()),
                ('product_size', models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], default='medium', max_length=15)),
                ('product_quantity', models.IntegerField()),
                ('product_pic', models.ImageField(upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothingstore.customer')),
                ('product', models.ManyToManyField(to='clothingstore.product')),
            ],
            options={
                'db_table': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(default=0)),
                ('product_price', models.IntegerField(default=0)),
                ('order_status', models.CharField(choices=[('pending', 'pending'), ('out for delivery', 'out for delivery')], default='pending', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothingstore.customer')),
                ('product', models.ManyToManyField(related_name='products', to='clothingstore.product')),
            ],
        ),
    ]
