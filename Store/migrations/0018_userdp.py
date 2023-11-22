# Generated by Django 4.2.6 on 2023-11-20 05:22

import Store.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0017_userprofile_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userdp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='user_img/', validators=[Store.models.validate_image_type])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]