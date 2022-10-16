import io
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pytube
from pytube import YouTube
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
from urllib.request import urlopen

"""
THINGS TO DO
* Combine audio and video to download higher resolutions 
* Erase downloaded label when paste link, click download
* Get 240p and 480p, they are missing
* Create threads to run simultaneously to fix freeze problem when paste link and getting data
* Create grids instead of paste for all objects
"""

# Global Variables
percentage_of_completion = 0
is_pasted = False
is_selected = False
get_video = None


def paste_link_thread():
    root.bind_all("<<Paste>>", paste_link)


def fetch_data_pb():
    """
    while True:
        print("Test")
        if not fetch_data:
            break
    """
    """
    fetch_pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=280)
    fetch_pb.place(x=200, y=165)
    fetch_pb.start()
    """


# PASTE LINK function - get streams
def paste_link(a):
    # Capture the link (url) and locate it from YouTube
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
    image = Image.open(io.BytesIO(raw_data)).resize((320,240))  # Resize the url image
    image = ImageTk.PhotoImage(image)                           # Convert the image to ImageTk
    thumbnail.image = image # Save reference to image
    thumbnail.config(image=image)

    # Place select menu
    def get_stream(is_video):
        global get_video
        if is_video: # Set Video menu
            streams = [stream.resolution for stream in yt.streams.filter(progressive=True)]
            variable.set("Select Video")
            get_video = True

        else: # Set Audio menu
            streams = [stream.abr for stream in yt.streams.filter(only_audio=True).order_by('abr')]
            variable.set("Select Audio")
            get_video = False

        menu = OptionMenu(root, variable, *streams)
        menu.place(x=500, y=330)

    if not globals()["is_pasted"]:
        # Get video and audio buttons that brings options menu
        Button(root, text='Get Video', font='san-serif 16 bold', bg='grey', padx=2, command=lambda: get_stream(True)).place(x=400, y=250)
        Button(root, text='Get Audio', font='san-serif 16 bold', bg='grey', padx=2, command=lambda: get_stream(False)).place(x=600, y=250)
        globals()["is_pasted"] = True


# MENU ON CLICK
def callback(*args):
    #print(f"the variable has changed to '{variable.get()}'")
    if not globals()["is_selected"]:
        # Percentage Label
        value_label.place(x=480, y=400)
        # Progress Bar
        pb.place(x=400, y=420)
        # Download button
        Button(root, text='Download', font='san-serif 16 bold', bg='grey', padx=2, command=download).place(x=480, y=500)
        globals()["is_selected"] = True


# Download Button function
def download():
    # Capture the link (url) and locate it from YouTube
    yt = YouTube(str(link.get()))

    # On Progress Function
    yt.register_on_progress_callback(on_progress)

    # Get video or audio
    if get_video:
        stream = yt.streams.filter(res=variable.get()).first()
    else:
        stream = yt.streams.filter(abr=variable.get()).first()

    stream.download()
    Label(root, text="Downloaded", font="ariel 15", bg="green").place(x=200, y=250)

        #.filter(progressive=True, file_extension='mp4')
        #.order_by('resolution')\
        #.desc()\
        #.first()

# On Progress Function
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    globals()["percentage_of_completion"] = bytes_downloaded / total_size * 100
    print(percentage_of_completion)
    pb['value'] = percentage_of_completion

    # Update current progress percentage
    value_label.config(text=f"Current Progress: %.2f" % percentage_of_completion + "%")
    root.update()


# Root windows
root = Tk()
root.geometry('800x600') # Size of the window
root.resizable(0,0) # Makes the windows adjustable with its features
root.title('YouTube Downloader')
Label(root, text='Download YouTube videos for free', font='san-serif 14').place(x=250, y=30)
link = StringVar()
Label(root, text="Paste your link here", font='san-serif 17 bold').place(x=280, y=90)
Entry(root, width=90, textvariable=link).place(x=130, y=130)  # Link Entry

# Thread(target=fetch_data_pb).start() # Fetch Data Thread

# Paste_link() run when paste the link
variable = StringVar(root)
root.bind_all("<<Paste>>", paste_link)

# Video Title Label
video_title = Label(root, text="", font="ariel 15")
video_title.place(x=10, y=200)

# Thumbnail Label
thumbnail = tk.Label(width=320, height=240)
thumbnail.place(x=10, y=250)

# Set default variable and trace each menu select
variable.trace("w", callback)

# Progress Bar
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)

# Percentage Label
value_label = ttk.Label(root, text="Current Progress: 0.00%")

root.mainloop()
