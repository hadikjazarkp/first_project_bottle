# Generated by Django 4.2.6 on 2023-11-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoryy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='cat_imgs/')),
            ],
        ),
    ]
