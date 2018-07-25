from __utils.environment_value_check import watson_environment
from __utils.environment_value_check import google_environment

# Client Info
CLIENT = {
    'request_socket_from_client': '',
    'alarm_socket_to_client': '',
    'stt_text': '',
    'folder_path': '',
    'watson_context': {'timezone': 'Asia/Seoul'},
    'watson_response': '',
}

# Client List
CLIENT_LIST = dict()

# Audio
# EXTENSION = ".wav"
STT_FILE_NAME = "input_speech.mp3"
TTS_FILE_NAME = "output_speech.mp3"
RESPONSE_FILE_NAME = "output_speech.wav"

# Network
HOST = ''
REQUEST_PORT = 5555
ALARM_PORT = 5556
REQUEST_ADDR = (HOST, REQUEST_PORT)
ALARM_ADDR = (HOST, ALARM_PORT)

FILE_HEADER_SIZE = 44
FILE_READ_SIZE = 8192
BUF_SIZE = 1024

WATSON = {'watson_username': '', 'watson_password': '',
          'watson_workspace': '', 'watson_url': '', 'watson_version': ''}
for key, value in watson_environment():
    WATSON[key] = value

GOOGLE = google_environment()
