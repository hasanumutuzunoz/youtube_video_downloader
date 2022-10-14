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

percentage_of_completion = 0
is_pasted = False
is_selected = False


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

    # Get only Resolutions
    resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True)]
    # Resolutions Options Menu
    menu = OptionMenu(root, variable, *resolutions)

    # PLACE THE RES MENU (once) if the link not pasted
    if not globals()["is_pasted"]:
        menu.place(x=500, y=250)
        #w.grid(column=1, row=0, columnspan=2, padx=100, pady=200)
        globals()["is_pasted"] = True


# MENU ON CLICK
def callback(*args):
    #print(f"the variable has changed to '{variable.get()}'")
    if not globals()["is_selected"]:
        # Percentage Label
        value_label.place(x=480, y=330)
        # Progress Bar
        pb.place(x=400, y=350)
        # Download button
        Button(root, text='Download', font='san-serif 16 bold', bg='grey', padx=2, command=download).place(x=480, y=400)
        globals()["is_selected"] = True


# Download Button function
def download():
    # Capture the link (url) and locate it from YouTube
    yt = YouTube(str(link.get()))

    # On Progress Function
    yt.register_on_progress_callback(on_progress)

    # Video = get the stream which we clicked resolution
    video = yt.streams.filter(res=variable.get()).first()
        #.filter(progressive=True, file_extension='mp4')
        #.order_by('resolution')\
        #.desc()\
        #.first()

    # Download the video
    video.download()

    Label(root, text="Downloaded", font="ariel 15", bg="green").place(x=200, y=250)


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

# Run paste_link() when paste the link
variable = StringVar(root)
root.bind_all("<<Paste>>", paste_link)

# Video Title Label
video_title = Label(root, text="", font="ariel 15")
video_title.place(x=10, y=200)

# Thumbnail Label
thumbnail = tk.Label(width=320, height=240)
thumbnail.place(x=10, y=250)

# Set default variable and trace each menu select
variable.set("Select Resolution")
variable.trace("w", callback)

# Progress Bar
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)

# Percentage Label
value_label = ttk.Label(root, text="Current Progress: 0.00%")

root.mainloop()
