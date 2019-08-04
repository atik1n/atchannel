from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from board import views as board

urlpatterns = [
	url(r'test/', board.test),
	url(r'^.*/', board.board),
]
