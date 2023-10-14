# Generated by Django 4.2.6 on 2023-10-14 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_alter_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique=True),
        ),
    ]
