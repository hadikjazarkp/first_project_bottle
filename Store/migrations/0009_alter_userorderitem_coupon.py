# Generated by Django 4.2.6 on 2024-01-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_alter_userorderitem_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorderitem',
            name='coupon',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
