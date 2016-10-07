import datetime
import json
from mock import Mock, patch
import tzlocal

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from .api_token_reader import ApiTokenReader
from .models import Event
from apiproxy import constants

def get_side_effect(event_id):
	"""Returns custom side effect for requests.get() Mock, based on event ID
	
	In practice, this will be used to have the right mock HTTP responses depending on the URL that was called
	"""
	def side_effect(url, *args, **kwargs):
		if url.endswith(constants.CALENDAR42_API_EVENT.format(event_id)):
			response_text = {'data': [{'id': event_id, 'title': 'bar'}]}
		else:
			response_text = {'data': [{'subscriber': {'first_name': 'Foobar'}}]}
		
		mock_response = Mock()
		mock_response.json = Mock(return_value=response_text)
		
		return mock_response
	
	return side_effect

class EventApiProxyTest(APITestCase):

	def setUp(self):
		# Get a valid authentication token
		self.token = ApiTokenReader.getUserToken(constants.SAMPLE_USER)
		
		# Headers which will be used to call the API proxy, and are also expected in the Calendar42 API call
		self.api_headers = {
			'Accept': 'application/json',
			'Content-type': 'application/json',
			'Authorization': 'Token %s' % self.token,
		}
	
	def get(self, url):
		"""Calls the API proxy with proper authentication
		
		@param {str} url	The API proxy URL to call
		"""
		response = self.client.get(
			url,
			**(self.api_headers)
		)
		return response
	
	def test_event_in_cache(self):
		"""Tests the API proxy's reply when the event is already cached (and not outdated)"""
		
		# Prepare data
		event_data = {
			'id': 'abcd1234',
			'title': 'Coffee Party in Delft',
			'names': ['Alice', 'Bob'],
		}
		Event.objects.get_or_create(
			id=event_data['id'],
			title=event_data['title'],
			names=constants.PARTICIPANT_SEPARATOR.join(event_data['names'])
		)
		
		# Call the API
		api_url = reverse('events_with_subscriptions', kwargs={'event_id': event_data['id']})
		api_response = self.get(api_url)
		
		# Assertions
		data = json.loads(api_response.content)
		self.assertEquals(event_data, data)
	
	def check_api_called(self, event_id, side_effect):
		"""Helper method - Makes sure the Calendar42 API is called when we call the API proxy
		
		@param {str} event_id	The event id with which to call the API proxy
		"""
		api_url = reverse('events_with_subscriptions', kwargs={'event_id': event_id})
		
		with patch('requests.get', side_effect=side_effect) as patched_get:
			self.get(api_url)
			
			# URLs from the Calendar42 API which should have been called
			event_api_url = constants.CALENDAR42_API_BASE_URL + constants.CALENDAR42_API_EVENT.format(event_id)
			participants_api_url = constants.CALENDAR42_API_BASE_URL + constants.CALENDAR42_API_PARTICIPANTS.format(event_id)
			
			patched_get.assert_any_call(event_api_url, headers=self.api_headers)
			patched_get.assert_any_call(participants_api_url, headers=self.api_headers)
	
	def test_event_not_in_cache(self):
		"""Tests the API proxy's behaviour when the event is NOT present at all in the cache"""
		event_id = 'this_does_not_exist_89732'
		self.check_api_called(event_id, get_side_effect(event_id))
	
	def test_event_cache_outdated(self):
		"""Tests the API proxy's behaviour when the event has been cached BUT is outdated"""
		event, _ = Event.objects.get_or_create(
			id='efgh5678',
			title='Ice Cream Party in Ushuaia',
			names=['John', 'Jane']
		)
		now = datetime.datetime.now(tzlocal.get_localzone())
		event.cache_date = now - constants.CACHE_DURATION - datetime.timedelta(seconds=1)
		event.save()
		
		self.check_api_called(event.id, get_side_effect(event.id))