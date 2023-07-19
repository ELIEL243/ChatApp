# Generated by Django 4.1.7 on 2023-06-26 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_contentmessage_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmessage',
            name='extension',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='contentmessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='send-files'),
        ),
    ]