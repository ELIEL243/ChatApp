from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Entreprise(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    mail = models.EmailField(blank=True, default="test@gmail.com")
    address = models.TextField(max_length=1000, blank=True, default="")

    def __str__(self):
        return self.name


class Post(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    img = models.ImageField(upload_to='user-profiles', blank=True)
    name = models.CharField(max_length=255, null=False)
    mail = models.EmailField(null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    initial = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        initial = self.name.split(' ')
        final_initial = ""
        for i in initial:
            final_initial += i[0]
        self.initial = final_initial
        super(Employee, self).save(*args, **kwargs)


class ContentMessage(models.Model):
    text_message = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='send-files', null=True, blank=True)
    extension = models.CharField(max_length=10, blank=True)

    @property
    def check_content(self):
        if self.text_message is None:
            return False  # si le contenu n'est pas un message
        return True  # si le contenu est un message

    def __str__(self):
        if self.text_message is not None:
            return self.text_message
        else:
            return self.file.name


class Message(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='sender')
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='receiver')
    message_content = models.ForeignKey(ContentMessage, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class EmployeeGroup(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    initial = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        initial = self.name.split(' ')
        final_initial = ""
        for i in initial:
            final_initial += i[0]
        self.initial = final_initial
        super(EmployeeGroup, self).save(*args, **kwargs)


class EmployeeHasGroup(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    group = models.ForeignKey(EmployeeGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name + " " + self.group.name


class MessageGroupe(models.Model):
    employee_group = models.ForeignKey(EmployeeGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, related_name='sender1')
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
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reveiver_caller', null=True)
    type = models.ForeignKey(CallType, on_delete=models.CASCADE, null=True, blank=True)
    at_time = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.caller.name


class News(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.employee.name + "- -" + self.content
