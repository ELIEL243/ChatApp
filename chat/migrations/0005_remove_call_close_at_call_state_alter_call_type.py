# Generated by Django 4.1.7 on 2023-06-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_contentmessage_text_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='call',
            name='close_at',
        ),
        migrations.AddField(
            model_name='call',
            name='state',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.calltype'),
        ),
    ]
