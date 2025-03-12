from django.urls import path
from task.views.user import UserRegisterView, UserLoginView, UserTokenRefreshView, \
    UserLogoutView
from task.views.task import UserTaskCreateView, CompleteTaskView, GetAllTaskView, \
    SubscriptionView
from task.views.search import UserTaskSearch


urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('task/', UserTaskCreateView.as_view()),
    path('task/<int:pk>/', CompleteTaskView.as_view()),
    path('task/search/', UserTaskSearch.as_view()),
    path('task/all/', GetAllTaskView.as_view()),
    path('subscribe/', SubscriptionView.as_view()),
    path('token/refresh/', UserTokenRefreshView.as_view()),
    path('logout/', UserLogoutView.as_view()),


]