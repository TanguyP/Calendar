import datetime
import logging
import tzlocal

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from .api_action_caller import EventDetailsAPIActionCaller, EventParticipantsAPIActionCaller
from .api_token_reader import ApiTokenReader
from .models import Event
from apiproxy import constants

logger = logging.getLogger(__name__)

class EventView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)

	def get(self, request, event_id, format=None):
		token = ApiTokenReader.getUserToken(request.user.username)
			
		try:
			event = Event.objects.get(id=event_id)
			
			# Cached event is outdated => call API to update it
			if event.is_outdated():
				event_details = EventDetailsAPIActionCaller(token).call(event_id)
				event_participants = EventParticipantsAPIActionCaller(token).call(event_id)
				
				event.id = event_details['id']
				event.title = event_details['title']
				event.names = constants.PARTICIPANT_SEPARATOR.join(event_participants)
				event.cache_date = datetime.datetime.now(tzlocal.get_localzone())
				
				event.save()
				
		# Nothing in cache for this event => call the API and store result in cache
		except ObjectDoesNotExist:
			event_details = EventDetailsAPIActionCaller(token).call(event_id)
			event_participants = EventParticipantsAPIActionCaller(token).call(event_id)
			event = Event.objects.create(
				id=event_details['id'],
				title=event_details['title'],
				names=constants.PARTICIPANT_SEPARATOR.join(event_participants),
			)
			
		return Response(event.get_as_serializable())