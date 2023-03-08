import io
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pytube
from pytube import YouTube
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
from urllib.request import urlopen
import ffmpeg
import re
import os
import threading

"""
THINGS TO DO
* Create grids instead of paste for all objects
* Add Pause, Stop, download buttons
"""

# Global Variables
percentage_of_completion = 0
get_video = False
#yt = None


# PASTE LINK function - start loading_thread
def paste_link(a):
    #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Videos')
    #print("The Desktop path is: " + desktop)
    #desktop = desktop + "\last_video.mp4"
    #path = re.sub(r'\\', '/', desktop)
    #print(path)
    loading = threading.Thread(target=loading_thread, daemon=True)
    loading.start()


# Run with paste link
def loading_thread():
    global yt

    # Erase other labels
    downloaded_label.place_forget()
    value_label.place_forget()

    # Place loading data label
    loading_data_label.place(x=200, y=520)
    # Place indeterminate progress bar
    pb_indeterminate.place(x=200, y=550)
    pb_indeterminate.start()

    yt = YouTube(str(link.get()))

    # Set the video title
    # Configurate the label (not place)
    title = yt.streams.first().title
    video_title.config(text=title)

    # Display Thumbnail
    # Configurate the label (not place)
    u = urlopen(yt.thumbnail_url)
    raw_data = u.read()
    u.close()
    image = Image.open(io.BytesIO(raw_data)).resize((320, 240))  # Resize the url image
    image = ImageTk.PhotoImage(image)                           # Convert the image to ImageTk
    thumbnail.image = image                                     # Save reference to image
    thumbnail.config(image=image)

    # Select menu. Run when click the (get video / get audio) buttons
    def get_stream(is_video):
        global get_video
        if is_video:                                            # Set Video menu
            streams = [stream.resolution for stream in          # Get stream resolutions and remove None values
                       yt.streams.filter(adaptive=True, file_extension='mp4', type='video')
                       if stream.resolution is not None]
            # streams = [stream for stream in yt.streams.filter(adaptive=True, file_extension='mp4', type='video')]
            streams = list(dict.fromkeys(streams))              # Remove the duplicates
            print(streams)
            variable.set("Select Video")
            get_video = True

        else:                                                   # Set Audio menu
            streams = [stream.abr for stream in yt.streams.filter(only_audio=True).order_by('abr')]
            streams.reverse()                                   # Reverse the list so the highest res will be on top
            variable.set("Select Audio")
            get_video = False

        # Set menu options to streams
        menu = OptionMenu(root, variable, *streams)
        menu.place(x=500, y=330)

        # PLACE BUTTON (Download)
        Button(root, text='Download', font='san-serif 16 bold', bg='grey', padx=2, command=download).place(x=480, y=500)

    # PLACE BUTTON (Get Video / Get Audio)
    Button(root, text='Get Video', font='san-serif 16 bold', bg='grey', padx=2,
           command=lambda: get_stream(True)).place(x=400, y=250)
    Button(root, text='Get Audio', font='san-serif 16 bold', bg='grey', padx=2,
           command=lambda: get_stream(False)).place(x=600, y=250)

    # Erase the indeterminate progress bar
    pb_indeterminate.place_forget()
    # Erase loading data label
    loading_data_label.place_forget()


def processing_pb_thread(path):
    file_stats = os.stat(path)
    while True:
        print(file_stats)


def download_thread():
    # Erase other labels
    downloaded_label.place_forget()


    print("Download thread started")
    #yt = YouTube(str(link.get()))                               # Capture the link (url) and locate it from YouTube
    yt.register_on_progress_callback(on_progress)               # On Progress Function
    #downloads_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')  # get downloads folder path
    get_directory = os.getcwd()  # Get current directory folder
    print(yt.streams)

    # Get video or audio
    # VIDEO
    if get_video:
        value_label.config(text="")
        stream = yt.streams.filter(res=variable.get()).first()  # Filter selected resolution from menu variable
        print("Download thread stream filtered ")
        title = yt.streams.first().title                        # Get video title
        res = int(re.sub(r'p', '', variable.get()))             # Remove "p" and convert to int (e.g. 1080p to 1080)

                # if res > 720:, Combine video and audio files into one file
                # Save it into C:/Users/"USERNAME"/Videos/"VIDEO TITLE".mp4

        stream.download(filename="video.mp4")                   # download video stream
        video = ffmpeg.input("video.mp4")                       # video file input
        audio_stream = yt.streams.filter(only_audio=True).first()  # get audio stream
        audio_stream.download(filename="audio.wav")             # download audio stream
        audio = ffmpeg.input("audio.wav")                       # audio stream input
        file = get_directory + "\\" + title + ".mp4"         # video file path in videos
        path = re.sub(r'\\', '/', file)                         # change \ to / in path

        # Remove the progress bar
        pb.place_forget()

        # Place indeterminate progress bar for combining video
        value_label.config(text="Processing final video...")
        pb_indeterminate.config(length=280)
        pb_indeterminate.place(x=400, y=420)
        pb_indeterminate.start()

        #processing_pb = threading.Thread(target=processing_pb_thread(path), daemon=True)
        #processing_pb.start()

        # COMBINE AUDIO AND VIDEO
        ffmpeg.output(audio, video, path, vcodec='copy', acodec='copy').run(overwrite_output=True)

        pb_indeterminate.place_forget()  # Remove processing progress bar

        # If the video name is too long, print shorter file location path
        if len(file) > 50:
            value_label.config(text="Download Finished! \n\n Location :\n" + file[0:50] + "...")
        else:
            value_label.config(text="Download Finished! \n\n Location :\n" + file)

    # AUDIO
    else:
        stream = yt.streams.filter(abr=variable.get()).first()
        stream.download(get_directory)

    downloaded_label.place(x=200, y=250)                        # Paste downloaded label on thumbnail
    print("Download thread finished")
    # .filter(progressive=True, file_extension='mp4')
    # .order_by('resolution')\
    # .desc()\
    # .first()


# DOWNLOAD BUTTON
def download():
    # Percentage Label
    value_label.place(x=480, y=400)
    # Progress Bar
    pb.place(x=400, y=420)
    # Start the download thread
    threading.Thread(target=download_thread, daemon=True).start()


# On Progress Function
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    globals()["percentage_of_completion"] = bytes_downloaded / total_size * 100
    pb['value'] = percentage_of_completion

    # Update current progress percentage
    value_label.config(text=f"Current Progress: %.2f" % percentage_of_completion + "%")
    root.update()


# Root windows
root = Tk()
root.geometry('800x600')  # Size of the window
root.resizable(0, 0)  # Makes the windows adjustable with its features
root.title('YouTube Downloader')
Label(root, text='Download YouTube videos for free', font='san-serif 14').place(x=250, y=30)
link = StringVar()

Label(root, text="Paste your link here", font='san-serif 17 bold').place(x=280, y=90)

# Link Entry
ent = Entry(root, width=90, textvariable=link)
ent.place(x=130, y=130)
ent.focus() # Select entry when the program opens

# Paste_link() run when paste the link
variable = StringVar(root)
root.bind_all("<<Paste>>", paste_link)

# Video Title Label
video_title = Label(root, text="", font="ariel 15")
video_title.place(x=10, y=200)

# Thumbnail Label
thumbnail = tk.Label(width=320, height=240)
thumbnail.place(x=10, y=250)

# Channel Name Label
channel = tk.Label(root, text="", font="san-serif 14")
channel.place(x=10, y=500)

# Set default variable and trace each menu select
#variable.trace("w", callback)

# Progress Bar
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
pb_indeterminate = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode="indeterminate")

# Percentage Label
value_label = ttk.Label(root, text="Current Progress: 0.00%")

downloaded_label = Label(root, text="Downloaded", font="ariel 15", bg="green")

loading_data_label = Label(root, text='Loading Data...')

root.mainloop()




