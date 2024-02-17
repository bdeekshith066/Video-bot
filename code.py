!apt -y install -qq aria2
!pip install -q torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 torchtext==0.14.1 torchdata==0.5.1 --extra-index-url https://download.pytorch.org/whl/cu116 -U
!pip install pandas-gbq==0.18.1 -U
# !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/text-to-video-synthesis/resolve/main/hub/damo/text-to-video-synthesis/VQGAN_autoencoder.pth -d /content/models -o VQGAN_autoencoder.pth
# !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/text-to-video-synthesis/resolve/main/hub/damo/text-to-video-synthesis/open_clip_pytorch_model.bin -d /content/models -o open_clip_pytorch_model.bin
# !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/text-to-video-synthesis/resolve/main/hub/damo/text-to-video-synthesis/text2video_pytorch_model.pth -d /content/models -o text2video_pytorch_model.pth
# !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/text-to-video-synthesis/raw/main/hub/damo/text-to-video-synthesis/configuration.json -d /content/models -o configuration.json

# from https://huggingface.co/kabachuha/modelscope-damo-text2video-pruned-weights
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/kabachuha/modelscope-damo-text2video-pruned-weights/resolve/main/VQGAN_autoencoder.pth -d /content/models -o VQGAN_autoencoder.pth
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/kabachuha/modelscope-damo-text2video-pruned-weights/resolve/main/open_clip_pytorch_model.bin -d /content/models -o open_clip_pytorch_model.bin
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/kabachuha/modelscope-damo-text2video-pruned-weights/resolve/main/text2video_pytorch_model.pth -d /content/models -o text2video_pytorch_model.pth
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/kabachuha/modelscope-damo-text2video-pruned-weights/raw/main/configuration.json -d /content/models -o configuration.json

!pip install -q open_clip_torch pytorch_lightning
!pip install -q git+https://github.com/camenduru/modelscope
!sed -i -e 's/\"tiny_gpu\": 1/\"tiny_gpu\": 0/g' /content/models/configuration.json

import os
os._exit(0)


import torch, random, gc
from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys

torch.manual_seed(random.randint(0, 2147483647))
pipe = pipeline('text-to-video-synthesis', '/content/models')

!mkdir /content/videos


import gc
import datetime
from IPython.display import HTML

# Assuming you have already imported necessary libraries like torch, pipe, and OutputKeys

# Clear CUDA cache and garbage collect to free up memory
with torch.no_grad():
    torch.cuda.empty_cache()
gc.collect()

# Input text for generating video
test_text = {
    'text': 'panda eat bamboo',
}

# Generating video with adjusted parameters
num_frames = 150  # Adjust the number of frames to increase the duration
fps = 24  # Adjust the frames per second if needed
output_video_path = pipe(test_text, num_frames=num_frames, fps=fps)[OutputKeys.OUTPUT_VIDEO]

# Output file path for the new video
new_video_path = f'/content/videos/{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.mp4'

# Use ffmpeg to convert video format and save the new video
!ffmpeg -y -i {output_video_path} -c:v libx264 -c:a aac -strict -2 {new_video_path} >/dev/null 2>&1

# Print paths of original and new videos
print(output_video_path, '->', new_video_path)


from IPython.display import HTML
from base64 import b64encode

!cp {new_video_path} /content/videos/tmp.mp4
mp4 = open('/content/videos/tmp.mp4','rb').read()

decoded_vid = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML(f'<video width=400 controls><source src="{decoded_vid}" type="video/mp4"></video>')
