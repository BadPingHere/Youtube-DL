from pytube import YouTube
import requests
import os
from pathlib import Path
from os import path
import ffmpeg
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from urllib.parse import urlparse

from tkinter import *
import webbrowser

    
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False
    
def open_github():
    webbrowser.open("https://github.com/BadPingHere/Youtube-DL")  
    
def open_about():
    aboutWIndow = Toplevel(root)
    aboutWIndow.title("About The Project")
    aboutWIndow.resizable(False, False)
    aboutWIndow.geometry("750x300")

    Label(aboutWIndow, text ="Youtube Downloader").pack()

    Label(aboutWIndow, text='What is this?', anchor='w', font=("Helvetica", 12, "bold")).pack(fill='both')
    Label(aboutWIndow, text='This is a youtube downloader, allowing you to download video, audio, captions, and thumbnails.', anchor='w').pack(fill='both')

    Label(aboutWIndow, text='How do I use this?', anchor='w', font=("Helvetica", 12, "bold")).pack(fill='both')
    Label(aboutWIndow, text='You insert the URL, select the available options on what you want to download, and if you chose video, select the quality of the video.', anchor='w').pack(fill='both')

    Label(aboutWIndow, text='I\'m running into x issue, what do I do?', anchor='w', font=("Helvetica", 12, "bold")).pack(fill='both')
    Label(aboutWIndow, text='Please sumbit a issue report on my github.', anchor='w').pack(fill='both')

def open_settings():
    settingsWindow = Toplevel(root)
    settingsWindow.title("Settings")
    settingsWindow.resizable(False, False)
    settingsWindow.geometry("600x300")
    Label(settingsWindow, text = 'There are no settings. After all, there is no UI. This is a cli turned into a gui. Not much to add.', font=('calibre',10)).pack()

def submit_URL():
    global yt
    global path1
    global base_dir
    global last_chars
    
    url=url_var.get()
    uri_validator(url)
    if uri_validator(url) == True:
        yt = YouTube(url)
        #create directory
        last_chars = url[-11:]
        path1 = Path(last_chars)
        base_dir = path.join(path.dirname(path.realpath(__file__)), path1)
        if os.path.isdir(path1):
            print('Url already downloaded! Look for the directory with the same youtube id as', last_chars) 
            quit()
        else:
            path1.mkdir(parents=True)
        option_selecter()
    else:
        print("Invalid url! Make sure to include the http:// markers in a url.")

def get_image(): # from Pavel Pančocha on stackoverflow. Good man!
    thumb_url = yt.thumbnail_url.split('?')[0] # Fixes issue with some url's where parameters were included in the thumb url process
    image_name = path.split(thumb_url)[1]
    try:
        image = requests.get("http://img.youtube.com/vi/%s/0.jpg" % yt.video_id)
    except OSError:
        return False
    if image.status_code == 200:
        base_dir = path.join(path.dirname(path.realpath(__file__)), path1)
        with open(path.join(base_dir, image_name), "wb") as f:
            f.write(image.content)
        return image_name

def download_captions():
    file_to_open = base_dir+"\captions.srt"
    transcript = YouTubeTranscriptApi.get_transcript(last_chars, languages=['en']) # you can change the language to something else
    formatter = SRTFormatter()
    srt_formatted = formatter.format_transcript(transcript)
    with open(file_to_open, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_formatted)

root = Tk() 
root.geometry("800x400")
root.title("Youtube Downloader")

menu = Menu(root) 
root.config(menu=menu)
settingsmenu = Menu(menu, tearoff=False) 
menu.add_cascade(label='Settings', command=open_settings) 
helpmenu = Menu(menu, tearoff=False) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About', command=open_about) # general information
helpmenu.add_command(label='Github', command=open_github)  # Add a command to open GitHub


url_var=StringVar()
url_var.set("")
url_label = Label(root, text = 'Youtube URL:', font=('calibre',10, 'bold'))
url_var = Entry(root,textvariable = url_var, font=('calibre',10,'normal'))
sub_btn=Button(root,text = 'Submit', command = submit_URL)
url_label.grid(row=0,column=0)
url_var.grid(row=0,column=1)
sub_btn.grid(row=2,column=1)

def options_submitted():
    curselection = option_list.curselection()
    selected_items = [option_list.get(index) for index in curselection]
    for index, selected_item in enumerate(selected_items):
        if selected_item == "Thumbnail":
            get_image()
        elif selected_item == "Video":
            resolution_selecter()
        elif selected_item == "Audio":
            yt.streams.filter(only_audio=True).first().download(output_path=base_dir)
        elif selected_item == "Captions":
            download_captions()

def download1080plus(resolution):
    yt.streams.filter(res=resolution).first().download(output_path=base_dir, filename="tempvideo.mp4",)
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
    
def option_selecter():
    global option_list
    
    Label(root, text="What do you want to download?", font=('calibre', 10, 'bold')).grid(row=3, column=0, columnspan=2)
    option_list = Listbox(root, height=4, selectmode='multiple')
    options = ["Thumbnail", "Video", "Audio", "Captions"]
    for item in options:
        option_list.insert(END, item)
    option_list.grid(row=4, column=0, columnspan=2)
    submit_button = Button(root, text="Submit", command=options_submitted)
    submit_button.grid(row=5, column=0, columnspan=2)

def resolution_submitted():
    curselection = resolution_list.curselection()
    selected_items = [resolution_list.get(index) for index in curselection]
    for selected_item in selected_items:
        if selected_item == "144p" or selected_item == "360p" or selected_item == "720p":
            yt.streams.filter(res=selected_item).first().download(output_path=base_dir)
        elif selected_item == "1080p" or selected_item == "1440p":
            download1080plus(selected_item)

def resolution_selecter():
    global resolution_list
    
    Label(root, text="What video resolution do you want to download?", font=('calibre', 10, 'bold')).grid(row=3, column=0, columnspan=2)
    resolution_list = Listbox(root, height=5)
    options = ["144p", "360p", "720p", "1080p", "1440p"]
    for item in options:
        resolution_list.insert(END, item)
    resolution_list.grid(row=4, column=0, columnspan=2)
    submit_button = Button(root, text="Submit", command=resolution_submitted)
    submit_button.grid(row=5, column=0, columnspan=2)
    
mainloop()