# Generated by Django 4.1.7 on 2023-06-26 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_contentmessage_extension_alter_contentmessage_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentmessage',
            name='text_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
