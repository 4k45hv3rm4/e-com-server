# Generated by Django 4.0.4 on 2022-04-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdata',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='product'),
        ),
    ]