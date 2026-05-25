import pyaudio


p = pyaudio.PyAudio()

input_info = p.get_default_input_device_info()
output_info = p.get_default_output_device_info()

print(input_info)
# print(output_info)

# get_device_info_by_index(int deviceIndex) -> dict
# {'index', 'structVersion', 'name', 'hostApi', 'maxInputChannels', 'maxOutputChannels',
#  'defaultLowInputLatency', 'defaultLowOutputLatency', 'defaultHighInputLatency', 'defaultHighOutputLatency', 'defaultSampleRate'}