import os
import urllib.request

# aws polly
from boto3 import client
from gtts import gTTS

from __configure.mubby_value import TTS_FILE_NAME


# 어떻게 동작하는지 확인할 것
class TextToSpeech:
    def __init__(self):
        pass

    def text_to_speech(self, client_info, tts_api=None):
        tts_speech = client_info['folder_path'] + TTS_FILE_NAME
        text = client_info['watson_response']
        print('watson_response {} '.format(text))

        if tts_api:
            if tts_api == "google":
                self.google_tts(text, tts_speech)
            elif tts_api == "naver_clova":
                self.naver_tts(text, tts_speech)
            elif tts_api == "aws_polly":
                self.aws_tts(text, tts_speech)
            else:
                print("그런 건 없어 폴리 시켜줄게")
                self.aws_tts(text, tts_speech)
        else:
            self.aws_tts(text, tts_speech)

        return tts_speech

    @staticmethod
    def google_tts(text, tts_speech):
        language = 'ko'
        rec_tts = gTTS(text=text, lang=language, slow=False)
        print("Saving gTTS mp3")
        rec_tts.save(tts_speech)

    @staticmethod
    def naver_tts(text, tts_speech):
        client_id = os.getenv('naver_tts_client_id')
        client_secret = os.getenv('naver_tts_client_secret')
        encText = urllib.parse.quote(text)
        data = "speaker=mijin&speed=0&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()

        if rescode == 200:
            print("Saving Naver-Clova TTS mp3")
            response_body = response.read()
            with open(tts_speech, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

    @staticmethod
    def aws_tts(text, tts_speech):
        polly = client("polly", region_name="ap-northeast-2")

        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Seoyeon")

        stream = response.get("AudioStream")

        with open(tts_speech, 'wb') as f:
            data = stream.read()
            f.write(data)
        print("Saving AWS-Polly TTS mp3")