from django.conf.urls import include, url
from django.contrib import admin

from .startup_manager import StartupManager

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^events-with-subscriptions/', include('events.urls'))
]

StartupManager.startup()