# Generated by Django 4.1 on 2022-12-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_alter_feed_userhash'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='watermark_image',
            field=models.TextField(null=True),
        ),
    ]
