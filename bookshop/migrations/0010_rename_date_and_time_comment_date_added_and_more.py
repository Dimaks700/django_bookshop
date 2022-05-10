# Generated by Django 4.0.3 on 2022-05-09 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0009_comment_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date_and_time',
            new_name='date_added',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bookshop.book'),
        ),
    ]