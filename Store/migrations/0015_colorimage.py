# Generated by Django 4.2.6 on 2023-11-18 05:29

import Store.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0014_cart_user_cart_variant_cart_variant_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cover_image', models.ImageField(upload_to='variant/', validators=[Store.models.validate_image_type])),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colorimages', to='Store.variant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
