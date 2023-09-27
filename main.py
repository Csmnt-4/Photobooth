import threading
import time
import tkinter as tk
from io import BytesIO
from tkinter import ttk

import cv2
import simpleaudio as sa
from PIL import Image, ImageTk

import win32clipboard
from os import path

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)


def save_image_start():
    save_image_thread = threading.Thread(target=save_image)
    save_image_thread.daemon = True
    save_image_thread.start()


def send_to_clipboard():
    output = BytesIO()
    last_image = Image.open(path.abspath(path.join(path.dirname(__file__), "images/photoboothImage.jpg")))
    last_image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    last_image.close()
    output.close()


def save_image():
    global number_of_photos
    defined_number_of_photos = int(number_of_photos.get())
    if defined_number_of_photos > 4:
        photobooth_image = Image.new("RGB", (1084, 1232), (250, 250, 250))
    else:
        photobooth_image = Image.new("RGB", (552, 20 + 404 * defined_number_of_photos), (250, 250, 250))

    # Path to the sound file
    sound_file = path.abspath(path.join(path.dirname(__file__), "sounds/shutterSound.wav"))
    sound_obj = sa.WaveObject.from_wave_file(sound_file)

    # Set the initial time
    start_time = time.time()

    # Define the interval in seconds
    interval = 1.5
    counter = 0

    while counter < defined_number_of_photos:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= interval:
            # Play the sound
            play_obj = sound_obj.play()

            ret, frame = cap.read()
            if ret:
                image_filename = path.abspath(path.join(path.dirname(__file__),
                                                        "images/capturedImage{0}.jpg".format(str(counter - 1))))
                start_time = current_time  # Reset the start time
                cv2.imwrite(image_filename, frame)

                image = Image.open(image_filename)
                image = image.resize((512, 384))
                if defined_number_of_photos > 4:
                    photobooth_image.paste(image, (20 + (counter % 2) * 532, 20 + int(counter / 2) * 404))
                else:
                    photobooth_image.paste(image, (20, 20 + counter * 404))

            counter += 1
            # Wait for the sound to finish playing
            play_obj.wait_done()

    photobooth_image.save(path.abspath(path.join(path.dirname(__file__),
                                                 "images/photoboothImage.jpg")), "JPEG")
    send_to_clipboard()
    photobooth_image.show()
    return


def quit_app():
    cap.release()
    root.destroy()


def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert the OpenCV BGR image to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        label.img = img_tk
        label.config(image=img_tk)

    # Call this function again after a delay (e.g., 10 ms)
    root.after(5, update_frame)


if not cap.isOpened():
    print("Error: Webcam not found or cannot be accessed.")
else:
    root = tk.Tk()
    root.title("Capture Image")

    top_frm = ttk.Frame(root, padding=10)
    bottom_frm = ttk.Frame(root, width=107, height=70, padding=10)

    top_frm.pack()
    bottom_frm.pack()

    ttk.Label(master=top_frm, justify="right", text="Number of photos: ").pack(side="left")
    number_of_photos = tk.StringVar(value="3")

    ttk.Radiobutton(master=top_frm, text='1x3 ', value='3', variable=number_of_photos).pack(side="left")
    ttk.Radiobutton(master=top_frm, text='1x4 ', value='4', variable=number_of_photos).pack(side="left")
    ttk.Radiobutton(master=top_frm, text='2x3', value='6', variable=number_of_photos).pack(side="left")
    ttk.Label(master=top_frm, text="\t\t").pack(side="left")

    ttk.Button(master=top_frm, text="Copy to clipboard", command=send_to_clipboard ).pack(side="right")
    ttk.Button(master=top_frm, text="Create image", command=save_image_start).pack(side="right")

    # Create a label widget to display the frames
    label = ttk.Label(master=bottom_frm, width=107)
    label.pack()

    update_frame_thread = threading.Thread(target=update_frame)
    update_frame_thread.daemon = True
    update_frame_thread.start()

    # Start the tkinter main loop to display the window
    root.mainloop()

    # Start updating the displayed frame
    cap.release()
