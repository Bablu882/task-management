from django.urls import path
from task.views.user import UserRegisterView, UserLoginView
from task.views.task import UserTaskCreateView, CompleteTaskView
from task.views.search import UserTaskSearch


urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('task/', UserTaskCreateView.as_view()),
    path('task/<int:pk>/', CompleteTaskView.as_view()),
    path('task/search/', UserTaskSearch.as_view()),

]