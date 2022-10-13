import tkinter as tk
from tkinter import *
from tkinter import ttk
import pytube
from pytube import YouTube

percentage_of_completion = 0
is_pasted = False
is_selected = False


# Option Menu Select Changed Function
def callback(*args):
    #print(f"the variable has changed to '{variable.get()}'")
    if not globals()["is_selected"]:
        # Percentage Label
        value_label.place(x=180, y=330)
        # Progress Bar
        pb.place(x=100, y=350)
        # Download button
        Button(root, text='Download', font='san-serif 16 bold', bg='grey', padx=2, command=download).place(x=200, y=400)
        globals()["is_selected"] = True


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


# Click Button function
def download():
    # Detect 2 digit itags
    # If 18. character is " "
    if (variable.get())[18] == " ":
        my_itag = int((variable.get())[15:17])
    # 3 Digit itags
    else:
        my_itag = int((variable.get())[15:18])

    # Capture the link (url) and locate it from YouTube
    yt = YouTube(str(link.get()))

    # On Progress Function
    yt.register_on_progress_callback(on_progress)

    # Video = selected itag stream
    video = yt.streams.get_by_itag(my_itag)
        #.filter(progressive=True, file_extension='mp4')
        #.order_by('resolution')\
        #.desc()\
        #.first()

    # Download the video
    video.download()
    Label(root, text="Downloaded", font="ariel 15", bg="green").place(x=200, y=250)


# Paste link function
def paste_link(a):
    str_link = str(link.get())
    yt = YouTube(str_link)

    # Options Menu

    w = OptionMenu(root, variable, *yt.streams.filter(progressive=True))

    if not globals()["is_pasted"]:
        w.place(x=200, y=200)
        #w.grid(column=1, row=0, columnspan=2, padx=100, pady=200)
        globals()["is_pasted"] = True



# Root windows
root = Tk()
root.geometry('500x500') # Size of the window
root.resizable(0,0) # Makes the windows adjustable with its features
root.title('YouTube Downloader')
Label(root, text='Download YouTube videos for free', font='san-serif 14').place(x=120, y=30)
link = StringVar()
Label(root, text="Paste your link here", font='san-serif 17 bold').place(x=150, y=90)
Entry(root, width=70, textvariable=link).place(x=30, y=130)  # Link Entry

# Run get_streams() when paste the link
variable = StringVar(root)
root.bind_all("<<Paste>>", paste_link)

# Set default variable and trace each menu select
variable.set("Select an option")
variable.trace("w", callback)

root.update()

# Progress Bar
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)


# Percentage Label
value_label = ttk.Label(root, text="Current Progress: 0.00%")


root.mainloop()