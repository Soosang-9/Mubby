import time

from __function.default import *
from __function.music import *
from __function.weather import *

from __configure.mubby_value import RESPONSE_FILE_NAME
from __utils.socket_module import SocketAction


# < If select find old client_info >
# 각 try 별로 isSuccess 를 달아서 실패하면 더 이상 동작하지 않게 해야할 것 같다.
# 이하 내용을 client_info = 1 class 형식으로 담아서 주고 받아야 하지 않을까 싶다.
def action_thread(client_info=None):
    socket_action = SocketAction(client_info)

    if client_info:

        # 01. STT Streaming
        header, language = understand_func(client_info, socket_action)
        print("header >> {}\nlanguage >> {}".format(header, language))

        # 02. What should the server do?
        try:
            if header['command'] == "chat":
                response_path = response_func(client_info)

            elif header['command'] == "weather":
                # aibril 과 대화를 한 번 더 하고 tts 에 다녀온다.
                output_audio_path = weather_func()

            elif header['command'] == "music":
                # (현재) tts 에 다녀오고 파일을 합치고 나서 반환한다.
                # ps. 클라이언트와 상의해보고 동작방법을 바꿔야 할 수도 있다.
                output_audio_path = music_func()
            else:
                raise AttributeError
                # 잘못된 접근이라는 것을 알려주어야 한다.
        except Exception as exc:
            # tts 동작을 하지 않고 그냥 파일을 보내준다, header 가 잘못 되었으니까
            print('★ACTION: what sholud the server do [ {} ]'.format(exc))

        try:
            # < The server sent data to client_info >
            print("out_audio_path >> {}".format(response_path))
            socket_action.sending_wav(response_path)

        except Exception as exc:
            print('\t★ACTION: sending_wav [ {} ]'.format(exc))

        finally:
             if socket_action.closing():
                client_info['request_socket_from_client'] = ''

    else:
        print('info가 선언이 안될 수 있나 지금 상황에.. 몰라.. 일단.. 뭐.. 안되면.. 생각해보자..')

    print("Thread end")
