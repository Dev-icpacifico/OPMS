from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_page, name="page"),              # /chat/
    path("history", views.get_history, name="history"),  # /chat/history
    path("messages", views.post_message, name="post"),   # /chat/messages
    path("stream", views.stream_response, name="stream") # /chat/stream
]
