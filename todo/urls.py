from django.urls import path
from . import views

urlpatterns = [
path('register/',views.SignUpView.as_view(),name='register'),
path('login/',views.SigninView.as_view(),name='login'),
path('logout/',views.sign_out,name='logout'),
path('todo/add/',views.TodoCreateView.as_view(),name='add-todo'),
path('todo/all/',views.TodoListView.as_view(),name='all-todo'),
path('todo/<int:pk>/status/',views.TodoTrueView.as_view(),name='completed'),
path('todo/<int:pk>/',views.TodoDetailView.as_view(),name='detail'),
path('todo/<int:pk>/change/',views.TodoEditView.as_view(),name='edit'),
path('todo/<int:pk>/remove/',views.todo_delete,name='delete'),
path('password/change/',views.ForgotView.as_view(),name='reset-pwd'),
path('',views.IndexView.as_view(),name='home'),
]