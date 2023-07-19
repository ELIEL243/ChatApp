# Generated by Django 4.1.7 on 2023-06-28 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_call_receivers_call_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagegroupe',
            name='receivers',
        ),
        migrations.CreateModel(
            name='EmployeeHasGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.employee')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.employeegroup')),
            ],
        ),
    ]
