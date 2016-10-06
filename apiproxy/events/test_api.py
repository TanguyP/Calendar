import datetime
import json
from mock import patch
import os
from unipath import Path

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Event
from apiproxy import constants

class EventApiProxyTest(TestCase):

	def setUp(self):
		# Get a valid authentication token
		token_file_path = Path(os.path.abspath(__file__)).ancestor(2).child(constants.TOKEN_FILE_NAME)
		with open(token_file_path) as token_file:
			self.token = token_file.readline().strip()
		
		# Headers which will be used to call the API proxy, and are also expected in the Calendar42 API call
		self.api_headers = {
			Accept='application/json',
			Content-type='application/json',
			Authorization='Token %s' % self.token,
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
			'participants': ['Alice', 'Bob'],
		}
		Event.objects.get_or_create(
			id=event_data['id'],
			title=event_data['title'],
			participants=constants.PARTICIPANT_SEPARATOR.join(event_data['participants'])
		)
		
		# Call the API
		api_url = reverse('events_with_subscriptions', kwargs={'event_id': event_data['id']})
		api_response = self.get(api_url)
		
		# Assertions
		data = json.loads(api_response.content)
		self.assertEquals(event_data, data)
	
	def check_api_called(self, event_id):
		"""Helper method - Makes sure the Calendar42 API is called when we call the API proxy
		
		@param {str} event_id	The event id with which to call the API proxy
		"""
		api_url = reverse('events_with_subscriptions', kwargs={'event_id': event_id})
		with patch('requests.get') as patched_get:
			api_response = self.get(api_url)
			
			# URLs from the Calendar42 which should have been called
			event_api_url = constants.CALENDAR42_API_BASE_URL + constants.CALENDAR42_API_EVENT.format(event_id)
			participants_api_url = constants.CALENDAR42_API_BASE_URL + constants.CALENDAR42_API_PARTICIPANTS.format(event_id)
			
			patched_get.assert_called_with(event_api_url, headers=self.api_headers)
			patched_get.assert_called_with(participants_api_url, headers=self.api_headers)
	
	def test_event_not_in_cache(self):
		"""Tests the API proxy's behaviour when the event is NOT present at all in the cache"""
		event_id = 'this_does_not_exist_89732'
		self.check_api_called(event_id)
	
	def test_event_cache_outdated(self):
		"""Tests the API proxy's behaviour when the event has been cached BUT is outdated"""
		event = Event.objects.get_or_create(
			id='efgh5678',
			title='Ice Cream Party in Ushuaia',
			participants=['John', 'Jane']
		)
		event.cache_date = datetime.datetime.now() - constants.CACHE_DURATION - datetime.timedelta(seconds=1)
		event.save()
		
		self.check_api_called(event.id)