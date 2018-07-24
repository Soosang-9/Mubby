import os

from __utils.aibril_connector import WatsonConversation
from __utils.socket_module import SocketAction
from __utils import audio_converter

from __configure.mubby_value import *
from __utils.stt_module import SpeechToText
from __utils.tts_module import TextToSpeech

__aibril = WatsonConversation()
__stt = SpeechToText()
__tts = TextToSpeech()

def understand_func(client_info, socket_action=None):
    if socket_action:
        __stt.speech_to_text(client_info, 'google_streaming', socket_action)
    else:
        __stt.speech_to_text(client_info, 'google')

    header, language = __aibril.conversation(client_info)

    return header, language


def response_func(client_info):
    speech_path = client_info['folder_path'] + RESPONSE_FILE_NAME
    # 파일 위치 다시 확인 할 것.
    speech_file_name = __tts.text_to_speech(client_info, 'aws_polly')
    audio_converter.convert(speech_file_name, speech_path)


def make_user_dir(client_ip):
    if not os.path.exists('__user_audio/{}'.format(client_ip)):
        print('\tmake "{}" dir'.format(client_ip))
        os.system('mkdir __user_audio/{}'.format(client_ip))


# def pcm2wav(client):
#     # print("client.getpeername()[0] >> {}".format(client.getpeername()[0]))
#     path = "__user_audio/"+client.getpeername()[0]+"/input"
#
#     input_file = open(path, 'wb')
#     while True:
#         data = __client_socket.receiving(client)
#         # print("data {}".format(data))
#         if data[-3:] == b'end':
#             print('ST_PROTO_RECORD_STOP')
#             input_file.write(data[:-3])
#             input_file.close()
#             audio_converter.pcm2wav(path, EXTENSION)
#             os.unlink(path)
#             break
#         input_file.write(data)
#
#     return path+EXTENSION
