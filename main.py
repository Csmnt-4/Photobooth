import threading
import time
import cv2
import tkinter as tk
from tkinter import ttk

import simpleaudio as sa
from PIL import Image, ImageTk

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)
white_screen_image = Image.open("images/emptyScreen.jpg")
is_white_screen = False


def save_image_start():
    save_image_thread = threading.Thread(target=save_image)
    save_image_thread.daemon = True
    save_image_thread.start()


def save_image():
    global is_white_screen
    photobooth_image = Image.new("RGB", (1084, 1232), (250, 250, 250))

    # Path to the sound file
    sound_file = "sounds/shutterSound.wav"
    sound_obj = sa.WaveObject.from_wave_file(sound_file)

    # Set the initial time
    start_time = time.time()

    # Define the interval in seconds
    interval = 2.5
    counter = 1

    while counter <= 6:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= interval:
            # Play the sound
            play_obj = sound_obj.play()

            is_white_screen = True
            counter += 1

            ret, frame = cap.read()
            if ret:
                image_filename = "images/capturedImage" + str(counter - 1) + ".jpg"
                start_time = current_time  # Reset the start time
                cv2.imwrite(image_filename, frame)

                image = Image.open(image_filename)
                image = image.resize((512, 384))
                photobooth_image.paste(image, (20 + (1 - counter % 2) * 532, 20 + int(counter / 2 - 1) * 404))

            # Wait for the sound to finish playing
            play_obj.wait_done()
            time.sleep(1)
            is_white_screen = False

    photobooth_image.save("images/photoboothImage.jpg", "JPEG")
    photobooth_image.show()
    return


def quit_app():
    cap.release()
    root.destroy()


def update_frame():
    global is_white_screen
    ret, frame = cap.read()
    if ret:
        # Convert the OpenCV BGR image to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if is_white_screen:
            # Update the label with white image
            label.img = ImageTk.PhotoImage(image=white_screen_image)
            label.config(image=ImageTk.PhotoImage(image=white_screen_image), text="", background="white")
        else:
            # Convert the RGB frame to a PhotoImage
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
    bottom_frm = ttk.Frame(root, width=106, height=70, padding=10)

    top_frm.pack()
    bottom_frm.pack()

    ttk.Button(master=top_frm, text="Save Image", command=save_image_start).pack(side="left")
    ttk.Button(master=top_frm, text="Quit", command=quit_app).pack(side="right")

    # Create a label widget to display the frames
    label = ttk.Label(master=bottom_frm, width=106)
    label.pack()

    update_frame_thread = threading.Thread(target=update_frame)
    update_frame_thread.daemon = True
    update_frame_thread.start()

    # Start the tkinter main loop to display the window
    root.mainloop()

    # Start updating the displayed frame
    cap.release()
