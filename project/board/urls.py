from django.contrib import admin
from django.urls import path, re_path, include

from board import views as board

urlpatterns = [
	re_path(r'^.*/', board.board),
]
