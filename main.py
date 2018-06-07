# -*- coding:utf-8 -*-

from utils import aibril_conv_module
from utils import stt_module
from utils import tts_module
from utils import audio_converter
from utils import wavefile_sending
from ffmpy import FFmpeg
import socket
import struct
import os

import time

from utils import module_communication

HOST = ''
PORT = 5555
ADDR = (HOST, PORT)
BUFF_SIZE = 1024

ST_PROTO_RECORD = 0x04
ST_PROTO_RECORD_DATA = 0x05
ST_PROTO_RECORD_PAUSE = 0x02
ST_PROTO_RECORD_STOP = 0x01

serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(ADDR)
serverSocket.listen(5)

aibril_conn = aibril_conv_module.WatsonServer()
stt_conn = stt_module.SpeechToText()
tts_conn = tts_module.TextToSpeech()
wave = wavefile_sending.WaveFile()


def pcm2wav(path):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', '2']},
            outputs={''.join([path, '.wav']): '-y'})
    ff.run()


def handler(clientSocket, addr, communi):
    print("accept")
    start = time.time()

    # print("Connected from", addr)
    # buf = clientSocket.recv(1024)
    # print('data > {}'.format(buf))
    f = open('record', 'wb')

    # print('ST_PROTO_RECORD_DATA')
    while True:

        buf = clientSocket.recv(1024)
        # print('data > {}'.format(buf))
        # if buf == b'end':
        #     print('ST_PROTO_RECORD_STOP')
        if buf[-3:] == b'end':
            # print('ST_PROTO_RECORD_STOP')
            f.write(buf[:-3])
            f.close()
            pcm2wav('record')
            os.unlink('record')
            # print('Streaming end.', addr)
            break
        f.write(buf)

    file_recv_time = time.time() - start
    start = time.time()

    RECV_FILE = "record.wav"
    result_audio_stt = stt_conn.audio_stt(RECV_FILE)
    stt_time = time.time()-start
    start = time.time()
    User = result_audio_stt

    result_conversation = aibril_conn.aibril_conv(result_audio_stt)
    aibril_time = time.time()-start
    start = time.time()

    Mubby = result_conversation

    # ===========================================================
    tts_conn.aws_tts(result_conversation)
    aws_tts_time = time.time()-start
    start = time.time()

    SEND_FILE = audio_converter.convert("output_atts.mp3")
    convert_time = time.time()-start
    strat = time.time()

    with open(SEND_FILE, 'rb') as f:
        data = f.read()
    # print("size >> {}".format(len(data)))
    clientSocket.send(str(len(data)).encode())
    a = clientSocket.recv(1024)
    # print("recv{}".format(a))
    communi.sending_wav(clientSocket, SEND_FILE)
    #
    # print('send file name > {}'.format(SEND_FILE))# "output_tts.wav"
    #
    # # SEND_FILE = "output_tts.wav"
    #
    # print('Completed')
    #
    # wave.set_sock(clientSocket, SEND_FILE)
    # wave.include_header()
    what = clientSocket.recv(1024)
    file_send_time = time.time()-start
    # print("what? {} ".format(what))
    clientSocket.close()
    #
    # while True:
    #     print('\nCHOICE{}\n\t- 1. without_header\n\t- 2. include_header\n\t- 0. exit'.format('- ' * 10))
    #     inp = input('>> ')
    #
    #     if inp in ('1', '2'):
    #         wave.set_sock(clientSocket, SEND_FILE)
    #         if inp == '1':
    #             wave.without_header()
    #         elif inp == '2':
    #             wave.include_header()
    #         clientSocket.close()
    #         break
    #     elif inp == '0':
    #         print('STOP PROGRAM')
    #         clientSocket.close()
    #         break
    #     else:
    #         print('- - - plz, choice 1 or 2\n')

    return {"User": User, "Mubby": Mubby, "file_recv_time": file_recv_time, "stt_time": stt_time, "aibril_time": aibril_time, "aws_tts_time": aws_tts_time, "convert_time": convert_time, "file_send_time": file_send_time}


def __print(dic):
    print("\n{}".format('= = ' * 10))
    print("{} >> {}".format("User", dic["User"]))
    print("{} >> {}".format("Mubby", dic["Mubby"]))
    print("{}".format('- - '*10))
    print("{} : {}".format("file_recv_time", dic["file_recv_time"]))
    print("{} : {}".format("stt_time", dic["stt_time"]))
    print("{} : {}".format("aibril_time", dic["aibril_time"]))
    print("{} : {}".format("aws_tts_time", dic["aws_tts_time"]))
    print("{} : {}".format("convert_time", dic["convert_time"]))
    print("{} : {}".format("file_send_time", dic["file_send_time"]))
    print("{}".format('= = ' * 10))

if __name__ == '__main__':
    while True:
        # print('\nServer is running {}'.format('-'*5))
        communi = module_communication.Communication()
        clientSocket, addr = serverSocket.accept()
        times = handler(clientSocket, addr, communi)
        __print(times)

