import ctypes
import client.opuslib as opuslib
import client.opuslib.api.encoder
import client.opuslib.api.decoder

class OpusEncoder():
    def __init__(self, rate=48000, channels=1, application=opuslib.APPLICATION_AUDIO, frame_size=960, max_data_bytes=4000):
        self.rate = rate
        self.channels = channels
        self.application = application
        self.frame_size = frame_size #pyaudio의 1200 frames_per_buffer를 그대로 가져오면 오류 생김!!! opuslib에서 지원하는 크기는 240, 480, 960, 1920, 2880, 3840 등... 960이 가장 적절...
        self.max_data_bytes = max_data_bytes

        # Opus Encoder 초기화
        self.error = ctypes.c_int()
        self.encoder = opuslib.api.encoder.create_state(self.rate, self.channels, self.application)

    def encode(self, pcm):
        # 인코딩
        encoded = opuslib.api.encoder.encode(self.encoder, pcm, self.frame_size, self.max_data_bytes)
        return encoded
    


class OpusDecoder():
    def __init__(self, rate=48000, channels=1):
        self.rate = rate
        self.channels = channels

        # Opus Decoder 초기화
        self.error = ctypes.c_int()
        self.decoder = opuslib.api.decoder.create_state(self.rate, self.channels)

    def decode(self, encoded):
        # 디코딩
        decoded = opuslib.api.decoder.decode(self.decoder, encoded, len(encoded), 960, 0)
        return decoded



class OpusEncoderDestory():
    def __init__(self, encoder):
        self.encoder = encoder

    def destroy(self):
        opuslib.api.encoder.destroy(self.encoder)



class OpusDecoderDestory():
    def __init__(self, decoder):
        self.decoder = decoder

    def destroy(self):
        opuslib.api.decoder.destroy(self.decoder)



if __name__ == "__main__":
    import os
    encoder = OpusEncoder(rate=48000, channels=1, frame_size=960)
    decoder = OpusDecoder(rate=48000, channels=1)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pcm_path = os.path.join(base_dir, "voice_pcm_30s.raw")
    f = open(pcm_path, "rb")
    pcm_bytes = f.read()
    print(f"원래 길이: {len(pcm_bytes)}")
    
    frame_size = 960  # samples
    frame_bytes = frame_size * 2  # int16 = 2 bytes
    usable_len = (len(pcm_bytes) // frame_bytes) * frame_bytes
    pcm_bytes = pcm_bytes[:usable_len]

    encoded_packets = []
    decoded_pcm = bytearray()

    for i in range(0, len(pcm_bytes), frame_bytes):
        frame = pcm_bytes[i:i + frame_bytes]
        encoded = encoder.encode(frame)
        decoded = decoder.decode(encoded)
        encoded_packets.append(encoded)
        decoded_pcm.extend(decoded)

    print(f"총 프레임 수: {len(encoded_packets)}")
    print(f"복원된 PCM 길이: {len(decoded_pcm)}")

