
from django.urls import path
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("developers", views.developers,name="developers"),
    path("bug_list", views.bug_list,name="bug_list"),
    path("changestatus", views.changestatus, name="changestatus"),
    path('update_bug_status/', views.update_bug_status, name='update_bug_status'),
    path('save_change_status', views.save_change_status, name="save_change_status"),
    path('dashboard', views.dashboard, name="dashboard"),
]
