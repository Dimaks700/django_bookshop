# Generated by Django 4.0.3 on 2022-05-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0005_alter_book_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
