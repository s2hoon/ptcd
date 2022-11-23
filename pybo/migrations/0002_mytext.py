# Generated by Django 4.1.1 on 2022-09-13 09:26

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='myText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('contents', models.CharField(max_length=200)),
                ('img_url', models.CharField(max_length=200)),
                ('board_text', ckeditor.fields.RichTextField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]