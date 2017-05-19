"""prototype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from feedback_manager import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<code>\w{16})/$', views.FeedBackView.as_view(), name='show_questions'),
    url(r'view/(?P<feedback_id>\d+)/$', views.ViewFeedback.as_view(), name='view_feedback'),
    url(r'thanks/$', views.FeedbackSubmittedView.as_view(), name='view_thanks'),
    url(r'home/$', views.Home.as_view(), name='home'),
    url(r'avail_time/$', views.avail_time, name='avail_time'),
]

admin.site.site_header = 'Feedback Administration'