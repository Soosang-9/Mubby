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

    # while client_info['request_socket_from_client']:
    if client_info:
        try:
            # 01. STT Streaming
            header, language = understand_func(client_info, socket_action)
            print("header >> {}\nlanguage >> {}".format(header, language))
        except Exception as e:
            print('\t★ default function error >> {}'.format(e))

        try:
            # 02. What should the server do?
            # Aibril 의 header.command 를 이용하여 어떤 동작을 할 것인지 정한다.

            if header['command'] == "chat":
                # tts 에 다녀온다.
                response_func(client_info)

            elif header['command'] == "weather":
                # aibril 과 대화를 한 번 더 하고 tts 에 다녀온다.
                output_audio_path = weather_func()

            elif header['command'] == "music":
                # (현재) tts 에 다녀오고 파일을 합치고 나서 반환한다.
                # ps. 클라이언트와 상의해보고 동작방법을 바꿔야 할 수도 있다.
                output_audio_path = music_func()
            else:
                print("기본 음성 들어가게 해야하는데ㅔㅔㅔㅔㅔ")
                # 잘못된 접근이라는 것을 알려주어야 한다.

        except Exception as e:
            print('\t★ 함수명 function error >> {}'.format(e))

        try:
            # < The server sent data to client_info >
            # 음성 파일을 돌려주어야 한다. (확인)
            # output_audio_path = "__user_audio/"+sock.getpeername()[0] + "/output_tts.wav"
            print("out_audio_path >> {}".format(client_info['folder_path'] + RESPONSE_FILE_NAME))
            socket_action.sending_wav(RESPONSE_FILE_NAME)

        except Exception as e:
            print('\t★ __send time out error >> {}'.format(e))

        finally:
             if socket_action.closing():
                client_info['request_socket_from_client'] = ''

    else:
        print('info가 선언이 안될 수 있나 지금 상황에.. 몰라.. 일단.. 뭐.. 안되면.. 생각해보자..')

    print("Thread end")
