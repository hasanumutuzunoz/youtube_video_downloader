from tkinter import *
from pytube import YouTube

def download():
    # Capture the link (url) and locate it from YouTube
    url = YouTube(str(link.get()))
    # Capture the streams available i.e. 360p, 720p, 1080p. etc.
    video = url.streams.first()
    # Download the video
    video.download()
    Label(root, text="Downloaded", font="ariel 15").place(x=100, y=120)

root = Tk()
root.geometry('500x300') # Size of the window
root.resizable() # Makes the windows adjustable with its features
root.title('YouTube Downloader')
Label(root, text='Download YouTube videos for free', font='san-serif 14').pack()
link = StringVar()
Label(root, text="Paste your link here", font='san-serif 17 bold').place(x=150, y=55)
link_enter = Entry(root, width=70, textvariable=link).place(x=30, y=85)
Button(root, text='Download', font='san-serif 16 bold', bg='grey', padx=2,command= download).place(x=200, y=150)
root.mainloop()