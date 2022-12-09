# Generated by Django 4.1.4 on 2022-12-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Книги', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AddField(
            model_name='book',
            name='author_name',
            field=models.CharField(default='Автор', max_length=255),
            preserve_default=False,
        ),
    ]
