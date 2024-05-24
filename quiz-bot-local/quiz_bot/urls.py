
from django.contrib import admin
from django.urls import path, include
# from core.views import quiz_page

from core.reply_factory import quiz_page, reset_quiz_view
from core.views import chat

urlpatterns = [
    path("", chat, name="chat"),
    path('quiz/', quiz_page, name='quiz_page'),
    path('reset/', reset_quiz_view, name='reset_quiz'),
    # path("admin/", admin.site.urls),
]
