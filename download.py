from pytube import YouTube
import requests
import os
import shutil
from pathlib import Path
from os import path
import time
import ffmpeg
thumbnail = "" 
yt1 = ''

print('Hello! Please enter your youtube url:')
url = input("Enter url: ")
yt = YouTube(url)
last_chars = url[-11:]

#create directory
path1 = Path(last_chars)
if os.path.isdir(path1):
    print('Url already downloaded! Look for the directory with the same youtube id as', last_chars) 
    quit()
else:
    path1.mkdir(parents=True)


def get_image(thumbnail): # from Pavel Pančocha on stackoverflow. Good man!
    image_name = path.split(yt.thumbnail_url)[1] 
    try:
        image = requests.get(yt.thumbnail_url)
    except OSError:
        return False
    if image.status_code == 200:
        base_dir = path.join(path.dirname(path.realpath(__file__)), path1)
        with open(path.join(base_dir, image_name), "wb") as f:
            f.write(image.content)
        return image_name
base_dir = path.join(path.dirname(path.realpath(__file__)), path1)

def let_user_pick(options):
    print("What do you want to download?:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None
options = ["Thumbnail", "Video", "Audio", "Thumbnail and Video", "Thumbnail and Audio"]
res = let_user_pick(options)

def download1080():
    yt.streams.filter(res='1080p').first().download(output_path=base_dir, filename="tempvideo.mp4",)
    yt.streams.filter(only_audio=True).first().download(output_path=base_dir, filename="tempaudio.mp4")
    video, audio = ffmpeg.input(path.join(base_dir, "tempvideo.mp4")), ffmpeg.input(path.join(base_dir, "tempaudio.mp4"))
    output = path.join(base_dir, "video.mp4")
    (
        ffmpeg
            .concat(video, audio, v=1, a=1)
            .output(output)
            .global_args('-loglevel', 'quiet')
            .run()
    )
    os.remove(path.join(base_dir, "tempvideo.mp4"))
    os.remove(path.join(base_dir, "tempaudio.mp4")) 
    
def download1440():
    yt.streams.filter(res='1440p').first().download(output_path=base_dir, filename="tempvideo.mp4",)
    yt.streams.filter(only_audio=True).first().download(output_path=base_dir, filename="tempaudio.mp4")
    video, audio = ffmpeg.input(path.join(base_dir, "tempvideo.mp4")), ffmpeg.input(path.join(base_dir, "tempaudio.mp4"))
    output = path.join(base_dir, "video.mp4")
    (
        ffmpeg
            .concat(video, audio, v=1, a=1)
            .output(output)
            .global_args('-loglevel', 'quiet')
            .run()
    )
    os.remove(path.join(base_dir, "tempvideo.mp4"))
    os.remove(path.join(base_dir, "tempaudio.mp4")) 

if options[res] == "Thumbnail":
    get_image(thumbnail)
    
if options[res] == "Video":
    def let_user_pick(options):
        print("What size do you want the video?:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i) - 1
        except:
            pass
        return None
    options = ["144p", "360p", "720p", "1080p", "1440p"]
    res = let_user_pick(options)
    if options[res] == "144p":
        print('Downloding the video...')
        yt.streams.filter(res='144p').first().download(output_path=base_dir)
    if options[res] == "360p":
        print('Downloding the video...')
        yt.streams.filter(res='360p').first().download(output_path=base_dir)
    if options[res] == "720p":
        print('Downloding the video...')
        yt.streams.filter(res='720p').first().download(output_path=base_dir)
    if options[res] == "1080p":
        print('Downloding the video. This may take longer due to youtube being bad.')
        download1080()
    if options[res] == "1440p":
        print('Downloding the video. This may take longer due to youtube being bad.')
        download1440()
if options[res] == "Audio":
    print("Downloading the best audio...")
    yt.streams.filter(only_audio=True).first().download(output_path=base_dir)
    
if options[res] == "Thumbnail and Video":
    def let_user_pick(options):
        print("What size do you want the video?:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i) - 1
        except:
            pass
        return None
    options = ["144p", "360p", "720p", "1080p", "1440p"]
    res = let_user_pick(options)
    if options[res] == "144p":
        print('Downloding the video...')
        print("Downloading the thumbnail...")
        get_image(thumbnail)
        yt.streams.filter(res='144p').first().download(output_path=base_dir)
    if options[res] == "360p":
        print('Downloding the video...')
        yt.streams.filter(res='360p').first().download(output_path=base_dir)
        print("Downloading the thumbnail...")
        get_image(thumbnail)
    if options[res] == "720p":
        print('Downloding the video...')
        yt.streams.filter(res='720p').first().download(output_path=base_dir)
        print("Downloading the thumbnail...")
        get_image(thumbnail)
    if options[res] == "1080p":
        print('Downloding the video. This may take longer due to youtube being bad.')
        download1080()
        print("Downloading the thumbnail...")
        get_image(thumbnail) 
    if options[res] == "1440p":
        print('Downloding the video. This may take longer due to youtube being bad.')
        download1440()
        print("Downloading the thumbnail...")
        get_image(thumbnail)
        
if options[res] == "Thumbnail and Audio":
    print("Downloading the best audio...")
    yt.streams.filter(only_audio=True).first().download(output_path=base_dir)
    print("Downloading the thumbnail...")
    get_image(thumbnail)
