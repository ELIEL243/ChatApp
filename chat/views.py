import datetime
import random
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models import Q, Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from ChatApp.settings import DEFAULT_FROM_EMAIL
from chat.models import Employee, Entreprise, Message, ContentMessage, Call, MessageGroupe, EmployeeHasGroup, \
    EmployeeGroup, News


# Create your views here.


def LoginView(request, name):
    if request.method == "POST":
        email = request.POST.get('mail')
        user = User.objects.filter(username=email, employee__entreprise__name=name).first()

        if user is not None:
            username = user.username
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "bienvenue")
                return redirect('home-chat', name=name)
            else:
                messages.error(request, "echec conn")
                return redirect('login', name=name)
    return render(request, 'auth/login.html', context={})


def RegisterView(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        user = User()
        if User.objects.filter(username=mail).first() is None:
            name = request.POST.get('name')
            address = request.POST.get('address')
            password = str(request.POST.get('password'))
            if not mail.__contains__(str(password)):
                entreprise = Entreprise.objects.create(name=name, mail=mail, address=address)
                user.username = mail
                user.email = mail
                user.password = make_password(password)
                user.save()
                Employee.objects.create(name=mail, user=user, entreprise=entreprise, mail=mail)
                subject = "Inscription à ScrollTalk"
                domain = request.get_host()
                url_address = domain + f"/login/{name}"
                message = f'Votre compte à été crée avec succès\nConnectez-vous grace à vos identifiants à l"adresse ' \
                          f'ci-dessous:\n{url_address}\nPour l"administration de votre site voici ' \
                          f'le lien:\n{url_address}/admin'
                recipient_list = [mail]
                send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list)
                return redirect('register-success')
            else:
                messages.warning(request, "duplicate user")
                return redirect('register')

        else:
            messages.error(request, "duplicate user")
            return redirect('register')
    return render(request, 'auth/subscribe.html', context={})


def RegisterSuccessView(request):
    return render(request, 'auth/auth-success.html', context={})


def HomeView(request):
    return render(request, 'index.html', context={})


def CheckCallView(request):
    call = "False"
    calls = Call.objects.filter(receiver__user_id=request.user.id, state=True)
    final_calls = []
    sender_id = None
    receiver_id = None
    unique_call = None
    for item in calls:
        diff = (datetime.datetime.now(datetime.timezone.utc) - item.at_time).total_seconds() // 60
        print(diff)
        if diff <= 1:
            final_calls += [item]
            call = "True"
        else:
            item.state = False
            item.save()
    if len(final_calls) > 0:
        unique_call = final_calls[0]
        sender_id, receiver_id = str(unique_call.caller.id) + str(unique_call.receiver.id)
    return render(request, 'chat/partials/modal-file.html', context={'call': call, 'unique_call': unique_call, 'sender_id': sender_id, 'receiver_id': receiver_id})


@login_required(login_url='home')
def HomeChatView(request, name):
    employee = Employee.objects.get(user=request.user)
    entreprise = Entreprise.objects.get(name=name)
    emp_messages = Message.objects.filter(Q(receiver=employee) | Q(sender=employee)).order_by('-create')
    ref = generate_unique_uid()
    ids = []
    final = []
    for item in emp_messages:
        if item.sender.mail == employee.mail:
            item.sender.mail = item.receiver.mail
        if item.sender.mail not in ids:
            ids += [item.sender.mail]
            final += [item]
    emp_messages = final
    emp_temp = {message.sender.id for message in emp_messages} | {message.receiver.id for message in emp_messages}
    employees = Employee.objects.filter(entreprise=entreprise).exclude(id__in=emp_temp)

    if request.GET.get('name') != "" and request.GET.get('name') is not None:
        name = request.GET.get('name')
        group = EmployeeGroup.objects.create(name=name, entreprise=employee.entreprise)
        EmployeeHasGroup.objects.create(employee=employee, group=group)
        return redirect('add-group', name)

    return render(request, 'chat/apps-chats.html', context={'employee': employee, 'emp_messages': emp_messages,
                                                            'employees': employees, 'ref': ref})


def AddGroupView(request, name):
    groupe = EmployeeGroup.objects.get(name=name)
    employee = Employee.objects.get(user=request.user)
    employees = Employee.objects.filter(entreprise=employee.entreprise)
    employees_grp = EmployeeHasGroup.objects.filter(group=groupe)
    if request.method == "POST":
        emp_name = request.POST.get('name')
        if Employee.objects.filter(name=emp_name).count() > 0:
            emp = Employee.objects.get(name=emp_name)
            EmployeeHasGroup.objects.create(employee=emp, group=groupe)
            messages.success(request, "OK")
    return render(request, 'chat/add-group.html', context={'group': groupe, 'employees': employees, 'employee': employee, 'employees_grp': employees_grp})


@login_required(login_url='home')
def HomeChatGroupView(request, name):
    employee = Employee.objects.get(user=request.user)
    groups = EmployeeHasGroup.objects.filter(employee=employee)
    ref = generate_unique_uid()

    return render(request, 'chat/apps-chats-group.html', context={'employee': employee, 'groups': groups, 'ref': ref})


@login_required(login_url='home')
def GetConversationViewGroup(request, group):
    employee = Employee.objects.get(user=request.user)
    conversations = MessageGroupe.objects.filter(employee_group__name=group)
    group1 = EmployeeGroup.objects.get(name=group)
    return render(request, 'chat/partials/chat-content-group.html',
                  context={'conversations': conversations, 'employee': employee,
                           'room_name': group, 'group': group1})


@login_required(login_url='home')
def GetConversationRefresh(request, group):
    employee = Employee.objects.get(user=request.user)
    conversations = MessageGroupe.objects.filter(employee_group__name=group)
    group1 = EmployeeGroup.objects.get(name=group)
    return render(request, 'chat/partials/chat-group-refresh.html',
                  context={'conversations': conversations, 'employee': employee,
                           'room_name': group, 'group': group1})


@login_required(login_url='home')
def GetConversationView(request, sender_id, receiver_id):
    active = request.user
    employee = Employee.objects.get(user=active)
    chat_with = None
    if sender_id != employee.id:
        chat_with = Employee.objects.get(id=sender_id)
    else:
        chat_with = Employee.objects.get(id=receiver_id)
    conversations = Message.objects.filter(sender_id__in=[sender_id, receiver_id], receiver_id__in=[sender_id, receiver_id]).order_by('create')
    conv = conversations.last()
    if not conv.is_read:
        conv.is_read = True
        conv.save()
    return render(request, 'chat/partials/chat-content.html', context={'conversations': conversations, 'employee': employee, 'chat_with': chat_with, 'room_name': str(sender_id)+str(receiver_id)})


def CheckConversationView(request, sender_id, receiver_id):
    employee = Employee.objects.get(id=sender_id)
    chat_with = Employee.objects.get(id=receiver_id)
    conversations = Message.objects.filter(sender_id__in=[sender_id, receiver_id], receiver_id__in=[sender_id, receiver_id]).order_by('create')

    return render(request, 'chat/partials/chat-content-refresh.html', context={'conversations': conversations, 'employee': employee, 'chat_with': chat_with, 'room_name': str(sender_id)+str(receiver_id)})


def GetChatListRefresh(request):
    employee = Employee.objects.get(user=request.user)
    entreprise = Entreprise.objects.get(name=employee.entreprise.name)
    emp_messages = Message.objects.filter(Q(receiver=employee) | Q(sender=employee)).order_by('-create')
    ids = []
    final = []
    for item in emp_messages:
        if item.sender.mail == employee.mail:
            item.sender.mail = item.receiver.mail
        if item.sender.mail not in ids:
            ids += [item.sender.mail]
            final += [item]
    emp_messages = final
    emp_temp = {message.sender.id for message in emp_messages} | {message.receiver.id for message in emp_messages}
    employees = Employee.objects.filter(entreprise=entreprise).exclude(id__in=emp_temp)

    return render(request, 'chat/partials/chat-list-refresh.html', context={'employee': employee, 'emp_messages': emp_messages,
                                                            'employees': employees})


def get_file_extension(file_name):
    """
    Get the file extension from a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The file extension.
    """

    file_extension = file_name.split(".")[-1]
    return file_extension


def is_empty_or_null(text):
  if not text:
    return True
  elif text.strip() == "":
    return True
  else:
    return False


@login_required(login_url='home')
def SendMessage(request):
    sender = Employee.objects.get(id=request.POST.get('sender-id'))
    receiver = Employee.objects.get(id=request.POST.get('receiver-id'))
    msg_content = None

    if request.method == "POST":

        if not is_empty_or_null(request.POST.get('msg')):
            msg = request.POST.get('msg')
            msg_content = ContentMessage.objects.create(text_message=msg)
            Message.objects.create(sender=sender, receiver=receiver, message_content=msg_content)

        elif request.FILES.get('file1') is not None:
            file = request.FILES.get('file1')
            msg_content = ContentMessage.objects.create(file=file, extension="pdf")
            Message.objects.create(sender=sender, receiver=receiver, message_content=msg_content)
    return HttpResponse("")


@login_required(login_url='home')
def SendMessageGroup(request):
    sender = Employee.objects.get(id=request.POST.get('sender-id'))
    group = EmployeeGroup.objects.get(name=request.POST.get('group'))
    msg_content = None

    if request.method == "POST":

        if not is_empty_or_null(request.POST.get('msg')):
            msg = request.POST.get('msg')
            msg_content = ContentMessage.objects.create(text_message=msg)
            MessageGroupe.objects.create(sender=sender, message_content=msg_content, employee_group=group)

        elif request.FILES.get('file1') is not None:
            file = request.FILES.get('file1')
            msg_content = ContentMessage.objects.create(file=file, extension="pdf")
            MessageGroupe.objects.create(sender=sender, message_content=msg_content, employee_group=group)
    return HttpResponse("")


@login_required(login_url='home')
def CallView(request, ref, state):
    user_owner = None
    room = None
    if state == "true":
        user_owner = request.user
        room = ref

    elif state == "false":
        user_owner = request.user
        room = ref

    return render(request, 'chat/call-video.html', context={'room': room, 'user': user_owner})


def NewsView(request):
    employee = Employee.objects.get(user=request.user)
    news = News.objects.filter(employee__entreprise=employee.entreprise).order_by('-id')

    if request.method == "POST":
        content = request.POST.get('content')
        News.objects.create(employee=employee, content=content)
        messages.success(request, "OK")

    return render(request, 'chat/news.html', context={'news': news, 'employee': employee})


def generate_unique_uid():
    return str(random.randint(1000, 9999))