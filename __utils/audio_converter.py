import os
from ffmpy import FFmpeg
import wave


def convert(input_audio, output_convert_audio):
    # ================ Audio converter =================
    #   - mp3 to wav
    #   - sample rate(22050Hz to 44100Hz)
    #   - channel(mono to stereo)
    # ==================================================

    # if audios[-1][-3:] == "mp3":
    #     audios[-1] = audio_converter(audios[-1][:-3])
    # 모든 오디오를 채널, 비트 수 다 맞춰서 컨버터 해줘야 하는데 ㅠ.ㅠ 어뜨카니..
    # 확인해서 안 되어있는거만 바꾸지뭐 ... 힘듦다..

    cmd_convert = "ffmpeg -i {} -ar 44100 -ac 2 -y {}".format(input_audio, output_convert_audio)
    os.system(cmd_convert)
    print("Convert mp3 to wav")


def pcm2wav(path, extension):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', '2']},
            outputs={''.join([path, extension]): '-y'})
    ff.run()


# 파일 합치는 부분, 이 부분도 함수로 만들 것.
# 어떻게 동작하는지 documents 보고 정확하게 확인 할 것.
# audio = 'usr/' + sock.getpeername()[0] + '/output_tts.wav'
# out_audio 에는 최종 audio_path, audio_list 에는 통합할 오디오들의 path 가 들어가 있어야 한다.
def combine_audios(out_audio, audio_list):
    with wave.open(out_audio, "wb") as output:
        for file_in in audio_list:
            with wave.open(file_in, 'rb') as wav_in:
                if not output.getnframes():
                    output.setparams(wav_in.getparams())
                output.writeframes(wav_in.readframes(wav_in.getnframes()))