# Generated by Django 4.1.7 on 2023-04-14 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CallType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ContentMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_message', models.TextField(null=True)),
                ('file', models.FileField(upload_to='send-files')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='user-profiles')),
                ('name', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=254)),
                ('initial', models.CharField(blank=True, default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('mail', models.EmailField(blank=True, default='test@gmail.com', max_length=254)),
                ('address', models.TextField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('entreprise', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.entreprise')),
            ],
        ),
        migrations.CreateModel(
            name='MessageGroupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('employee_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.employeegroup')),
                ('message_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.contentmessage')),
                ('receivers', models.ManyToManyField(related_name='receivers1', to='chat.employee')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender1', to='chat.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('message_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.contentmessage')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='chat.employee')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='chat.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employeegroup',
            name='entreprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.entreprise'),
        ),
        migrations.AddField(
            model_name='employee',
            name='entreprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.entreprise'),
        ),
        migrations.AddField(
            model_name='employee',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.post'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_time', models.DateTimeField(auto_now_add=True)),
                ('close_at', models.DateTimeField()),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caller', to='chat.employee')),
                ('receivers', models.ManyToManyField(related_name='receivers', to='chat.employee')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.calltype')),
            ],
        ),
    ]
