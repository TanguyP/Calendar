import datetime

# Time during which the Calendar42 API's data are kept in the API proxy's cache
CACHE_DURATION = datetime.timedelta(minutes=4.2)

# Name of the file containing the valid authentication tokens
TOKEN_FILE_NAME = 'tokens.txt'

# Regular expression describing the allowed format for an event ID
EVENT_ID_PATTERN = r'[^/]+'

# Character used to separate multiple participants to an event (because, for the sake of simplicity, participants are stored as a string in the Event's data)
PARTICIPANT_SEPARATOR = ','

# Base URL of the Calendar42 API version used by the API proxy
CALENDAR42_API_BASE_URL = 'https://demo.calendar42.com/api/v2/'

# URL fragment to get information about an event from the Calendar42 API
CALENDAR42_API_EVENT = 'events/{0}/'

# URL fragment to get information about participants from the Calendar42 API
CALENDAR42_API_PARTICIPANTS = 'event-subscriptions/?event_ids=[{0}]'