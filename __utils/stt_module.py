from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# [END import_libraries]s

import speech_recognition as sr

from __configure.mubby_value import STT_FILE_NAME

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class SpeechToText:
    def __init__(self):
        pass

    def speech_to_text(self, client_info, stt_api=None, socket_action=None):
        file_name = client_info['folder_path'] + STT_FILE_NAME
        stt_text = ''

        if stt_api:
            if stt_api == "google":
                stt_text = self.google_stt(file_name)
            elif stt_api == "google_streaming":
                stt_text = self.google_stt_streaming(socket_action)
            else:
                print("그런 건 없어 스트리밍 시켜줄게")
                stt_text = self.google_stt(file_name)
        else:
            stt_text = self.google_stt(file_name)

        client_info['stt_text'] = stt_text

    def google_stt(self, file_name):
        print("file_name >> {}".format(file_name))

        with sr.AudioFile(file_name) as source:
            r = sr.Recognizer()
            audio = r.record(source)
            try:
                stt_text = r.recognize_google(audio, show_all=False, language='ko_KR')
                print("Success Google STT")
            except Exception as e:
                print("Google STT false >> {}".format(e))
                stt_text = ''

        # print("self.output_stt >> {}".format(output_stt))

        return stt_text

    @staticmethod
    def listen_print_loop(responses):
        """
            Iterates through server responses and prints them.

            The responses passed is a generator that will block until a response
            is provided by the server.

            Each response may contain multiple results, and each result may contain
            multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
            print only the transcription for the top alternative of the top result.

            In this case, responses are provided for interim results as well. If the
            response is an interim one, print a line feed at the end of it, to allow
            the next result to overwrite it, until the response is a final one. For the
            final one, print a newline to preserve the finalized transcription.
        """
        text = ''
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                # print(transcript + overwrite_chars)
                text = transcript + overwrite_chars

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0

        return text

    def google_stt_streaming(self, socket_action):
            # See http://g.co/cloud/speech/docs/languages
            # for a list of supported languages.
            language_code = 'ko-KR'  # a BCP-47 language tag

            # for content in comuni.get_data(client_record):
            #     print("Type >> {}".format(type(content)))

            client = speech.SpeechClient()
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code)
            streaming_config = types.StreamingRecognitionConfig(
                config=config,
                interim_results=True)
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in socket_action.get_data())

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            stt_text = self.listen_print_loop(responses)
            # 아무말도 안 하면 어떻게 될까 궁금하네 해보자.
            return stt_text
