import json
import os

from watson_developer_cloud import conversation_v1

from __configure.mubby_value import WATSON


class WatsonConversation:
    def __init__(self):
        # 환경변수가 설정 안 되어있을 때도 에러를 반환해야한다.

        # client 마다 객체에 context 를 넣었다가 호출해야하는 것은 아닐까?
        # 대화가 이어지기 위해서는 이전의 context 값이 필요하다.
        # Aibril 에 접근하기 위해서는 watson id 가 필요하다.

        self.__watson_conv_id = ''
        self.__convert = None

    def connect(self):
        try:
            self.__convert = conversation_v1.ConversationV1(
                username=WATSON['watson_username'],
                password=WATSON['watson_password'],
                version=WATSON['watson_version'],
                url=WATSON['watson_url']
            )

        except Exception as e:
            print("can not connect Aibril conversation server >> {}".format(e))
            return False

        return True

    def conversation(self, client_info):
        is_succeed = True

        stt_text = client_info['stt_text']
        context = client_info['watson_context']

        if self.__convert is None:
            is_succeed = self.connect()

        if is_succeed:

            response = self.__convert.message(
                workspace_id=WATSON['watson_workspace'],
                message_input={'text': stt_text},
                context=context
            )

            # response type 출력 해볼 것, json parsing 이 딱히 필요 없을 수도
            json_response = json.dumps(response, indent=2, ensure_ascii=False)
            dict_response = json.loads(json_response)

            try:
                # ==================================================
                # Parsing response
                # 얘만 따로 try, catch 로 감싸서 text 가 없는 경우에도 대비해야 한다.
                # 답이 없을 수도 있다. header 를 먼저 받아와야 한다.
                # header > text > language 순으로 정의해야한다.
                # ==================================================
                result_conv = dict_response['output']['text'][0]
                # check this action
                # 다음 문장 추가해서 읽는 것 같은데, 이건 왜 하는 건가?
                # 아래 두 줄은 없어도 동작이 잘 되었었다.
                # 여러개의 문장을 읽어와서 연결하도록 하기 위해 사용 하는 것 같다.
                if len(dict_response['output']['text']) > 1:
                    result_conv += " " + dict_response['output']['text'][1]
            except Exception as e:
                print('\n\t error >> '.format(e))
                result_conv = "다시 한번 말씀해주세요."

            try:
                header = dict_response['output']['header']
                # print('header type {}'.format(type(header)))
            except Exception as e:
                header = {"command": "chat"}
                print("It dosen't have Header >> {}".format(e))

                # ==================================================
                #  Update context
                # context 안에 변수 넣어서 에이브릴에서 사용하게 할 수 있음.
                # 딕셔너리 value 안에 리스트 혹은 딕셔너리로 사용.
                # 사용 후에 value 삭제 후  update.
                # ==================================================
            context.update(dict_response['context'])

            # test 용
            # self.__context["dir"] = {"aa":"I_am_Leni", "bb":"2"}

            # ==================================================
            #   Check conversation is end or durable
            # ==================================================
            if 'branch_exited' in dict_response['context']['system']:
                conv_flag = True
            else:
                conv_flag = False

                # --------------------------------------------------
                #   << Check Translate >>
                # 언어 설정하는 부분인데, 현재는 통역이 안되서 그냥 반환만 하고 있음.
            try:
                language = (result_conv.split())[-1]
            except Exception as e:
                language = 'trans_ko'
                print("It doesn't have Text >> {}".format(e))

            if language == 'trans_en':
                language = 'en'
            elif language == 'trans_ja':
                language = 'ja'
            elif language == 'trans_zh':
                language = 'zh'
            else:
                language = 'ko'
            # --------------------------------------------------

            client_info['watson_response'] = result_conv

        else:
            header = {'command': 'chat'}
            language = 'ko'
            client_info['watson_response'] = '에이브릴에 접속할 수가 없어요'

        return header, language
