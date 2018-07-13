# 통신부분에 대한 것을 여기다 모아야 한다.
# 현재는 그냥 동작 돌 수 있도록 가져다 놓았다.
# 추후 수정 필요 꼭
# 커넥팅 후에 꼭!
# 꼬옥!
# 꼭!
import socket

from __configure.mubby_value import BUF_SIZE, FILE_HEADER_SIZE, FILE_READ_SIZE


# 메시지 형태를 구분하는 구분자 역활 함수를 집어 넣어야 한다.
# app-text, app-voice, mubby-voice 등등..
class Socket:
    def __init__(self, address_port=None):
        if address_port:
            self.__server = socket.socket()
            self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server.bind(address_port)
            self.__server.listen(5)
        else:
            print("에러에러 소켓 정의가 잘못 되었음")
            exit(1)

    def getting_server(self):
        return self.__server
    #
    # def setting_sock(self, client):
    #     self.client = client


class SocketAction:
    def __init__(self, client_info):
        self.__client = client_info['request_socket_from_client']
        self.__audio_path = client_info['folder_path']

    def receiving(self):
        # self.client.recv(BUF_SIZE)
        data = self.__client.recv(BUF_SIZE)
        return data
        # 수신 후 해야 할 동작이 있는 경우 여기다가 작성 한다.

    def sending(self, data):
        # 받을 때 에러가 생기는 경우 대비를 해야할 것 같지 아니하지 않니..?
        # self.client.send(data)
        # answer = self.client.recv(BUF_SIZE)

        self.__client.send(data)
        answer = self.__client.recv(BUF_SIZE)
        print('here_re_answer > {}'.format(answer))

        if answer == b'ack' or answer == b'spk':
            return True
        else:
            return False

    def closing(self):
        try:
            self.__client.close()
            return True
        except:
            return False

    def sending_wav(self, file_name):
        audio_path = self.__audio_path + file_name
        answer = self.receiving()
        if answer == b'tel':
            with open(audio_path, "rb") as wave_file:
                data = wave_file.read()
                is_success = self.sending(self.__client, str(len(data)).encode())

            if is_success:
                with open(audio_path, "rb") as wave_file:
                    count = 0
                    data = wave_file.read(FILE_HEADER_SIZE)
                    if self.sending(self.__client, data):
                        while True:
                            data = wave_file.read(FILE_READ_SIZE)
                            if len(data) == 0:
                                break
                            else:
                                count += 1
                                print('\t- data len >> ', len(data))
                                print('\t- data count >> ', count)
                                if not self.sending(self.__client, data):
                                    break

    def get_data(self):
        # 스트레오 그대로 두고 32000으로 보내면 된다.
        # 파일형식으로 넘길 때는 2채널 스트레오를 모노로 변경해주어야 했는데
        # 다이렉트로 전송은 왠일인지 스트레오로 인식하지 않는다.
        # f1 = open('1channel_record', 'wb')
        # f2 = open('2channel_record', 'wb')
        data = self.receiving()
        print("len >> {}".format(len(data[3:])))
        print("rec check >> {}".format(data[:3]))
        if data[:3] == b'rec':
            if len(data) > 3:
                # f2.write(data[3:])
                yield data[3:]
            print("go to while")
            while True:
                data = self.receiving()
                # print("data type >> {}".format(type(data)))
                # print("len >> {}".format(len(data)))
                # print('end {}'.format(data))
                # print("data[-3:] {}".format(data[-3:]))
                if data[-3:] == b'end':
                    if len(data) > 3:
                        # f2.write(data[:-3])
                        yield data[:-3]
                    # f2.close()
                    break
                # f2.write(data)
                yield data
