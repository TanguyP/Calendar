from django.conf.urls import url

from apiproxy import constants
from . import views

urlpatterns = [
    url(
		regex=r'^(?P<event_id>{0})/?'.format(constants.EVENT_ID_PATTERN),
		view=views.EventView.as_view(),
		name='events_with_subscriptions',
	),
]
