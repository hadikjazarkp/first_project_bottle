# Generated by Django 4.2.6 on 2023-11-02 13:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_main_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cover_image', models.ImageField(upload_to='Logo_img/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
