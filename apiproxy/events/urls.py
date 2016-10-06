from django.conf.urls import include, url
from django.contrib import admin

from apiproxy import constants

urlpatterns = [
    url(
		regex=r'^(?P<event_id>{0})/'.format(constants.EVENT_ID_PATTERN),
		view=views.TODO,
		name='events_with_subscriptions',
	),
]
