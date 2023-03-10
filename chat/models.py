from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    img = models.ImageField(upload_to='user-profiles', null=True)
    name = models.CharField(max_length=255, null=False)
    mail = models.EmailField(null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ContentMessage(models.Model):
    text_message = models.TextField(null=True)
    file = models.FileField(upload_to='send-files')

    @property
    def check_content(self):
        if self.text_message is None:
            return False  # si le contenu n'est pas un message
        return True  # si le contenu est un message


class Message(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='sender')
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='receiver')
    message_content = models.ForeignKey(ContentMessage, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class EmployeeGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MessageGroupe(models.Model):
    employee_group = models.ForeignKey(EmployeeGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='sender1')
    receivers = models.ManyToManyField(Employee, related_name='receivers1')
    message_content = models.ForeignKey(ContentMessage, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CallType(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Call(models.Model):
    caller = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='caller')
    receivers = models.ManyToManyField(Employee, related_name='receivers')
    type = models.ForeignKey(CallType, on_delete=models.CASCADE)
    at_time = models.DateTimeField(auto_now_add=True)
    close_at = models.DateTimeField()

    def __str__(self):
        return self.caller.name
