from django.urls import path
from .views import LoginView, HomeView, RegisterView, RegisterSuccessView, HomeChatView, GetConversationView, \
    SendMessage, CallView, CheckCallView, HomeChatGroupView, GetConversationViewGroup, SendMessageGroup, \
    GetConversationRefresh, CheckConversationView, AddGroupView, NewsView, GetChatListRefresh

urlpatterns = [
    path('login/<str:name>/', LoginView, name='login'),
    path('register/', RegisterView, name='register'),
    path('', HomeView, name='home'),
    path('register-success/', RegisterSuccessView, name='register-success'),
    path('home-chat/<str:name>', HomeChatView, name='home-chat'),
    path('home-chat-group/<str:name>', HomeChatGroupView, name='home-chat-group'),
    path('get-conversation/<int:sender_id>/<int:receiver_id>', GetConversationView, name='get_conversation'),
    path('check-conversations/<int:sender_id>/<int:receiver_id>', CheckConversationView, name='check-conversations'),
    path('get-conversation-group/<str:group>/', GetConversationViewGroup, name='get_conversation_group'),
    path('get-conversation-refresh/<str:group>/', GetConversationRefresh, name='get_conversation_refresh'),
    path('add-group/<str:name>/', AddGroupView, name='add-group'),
    path('send-msg/', SendMessage, name='send-msg'),
    path('send-msg-group/', SendMessageGroup, name='send-msg-group'),
    path('news/', NewsView, name='news'),
    path('check-call', CheckCallView, name="check-call"),
    path('chat-list', GetChatListRefresh, name="chat-list-refresh"),
    path('call/<str:ref>/<str:state>/', CallView, name="call"),
]
