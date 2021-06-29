from django.urls import path
from .views import index, signup, login

urlpatterns = [
    path('', index, name='homepage'),
    path('signup/', signup),
    path('login/', login)
]
