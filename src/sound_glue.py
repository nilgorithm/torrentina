# import imageio File saved as /home/kmd010/.imageio/ffmpeg/ffmpeg.linux64.
import moviepy.editor as mpe
import glob
from pprint import pprint
import re
# from progress.bar import Bar
from itertools import islice
# import difflib # надо будет через это разобраться потом как делать

def index_number(ext: str, path: str)->list:
    arr = [file for file in glob.glob(f"{path}/*.{ext}")]
    res = dict()
    for fp in range(len(arr)):
        cur_arr = re.findall(pattern=r"\d", string=arr[fp])
        nex_arr = re.findall(pattern=r"\d", string=arr[fp-1])
        k = [cur_arr[i] for i in range(len(cur_arr)) if cur_arr[i] != nex_arr[i]]
        if k[0] == '0':
            k.pop(0)
            res["".join(k)] = arr[fp]
        else:
            res["".join(k)] = arr[fp]
    return res


video_path = "/home/kmd010/Downloads/Vinland.Saga.Season2.WEBRip.1080p"
audio_path = "/home/kmd010/Downloads/Vinland.Saga.Season2.WEBRip.1080p/RUS Sound/AniLibria"
video_extension = "mkv" #потом надо сделать рекурсию которая по диру ищет видео
audio_extension = "mka" #потом надо сделать рекурсию которая по диру ищет аудио

d_video = index_number(path=video_path, ext=video_extension)
pprint(d_video)
d_audio = index_number(path=audio_path, ext=audio_extension)
pprint(d_audio)


for k, v in d_video.items():
    my_clip = mpe.VideoFileClip(v)  # видео-файл
    print(my_clip)
    my_clip.write_videofile(video_path+f"/{k}.mp4", audio=d_audio[k], codec="libx264")
#"/home/kmd010/.local/lib/python3.9/site-packages/tqdm/_tqdm.py"
