# Generated by Django 2.1 on 2018-08-09 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_mlcommenting', '0003_remove_comment_object_pk'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]