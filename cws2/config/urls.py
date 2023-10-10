"""cws2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from cws2.views.auth import CreateAccountView, LoginView, LogoutView
from cws2.views.index import DashboardView
from cws2.views.language import (
    EditLanguageView,
    IndexLanguageView,
    NewLanguageView,
    ShowLanguageView,
)
from cws2.views.static import AboutView, ContactView, DonateView, PrivacyView
from cws2.views.user import EditUserView, ShowUserView

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # user
    path("@<str:user>", ShowUserView.as_view(), name="user.show"),
    path("profile", EditUserView.as_view(), name="user.edit"),
    # language
    path(
        "@<str:user>/<slug:language>",
        ShowLanguageView.as_view(),
        name="language.show",
    ),
    path(
        "@<str:user>/<slug:language>/edit",
        EditLanguageView.as_view(),
        name="language.edit",
    ),
    path("languages", IndexLanguageView.as_view(), name="language.index"),
    path("languages/new", NewLanguageView.as_view(), name="language.new"),
    # auth
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", CreateAccountView.as_view(), name="register"),
    # static
    path("about", AboutView.as_view(), name="about"),
    path("contact", ContactView.as_view(), name="contact"),
    path("donate", DonateView.as_view(), name="donate"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
    # index
    path("", DashboardView.as_view(), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
