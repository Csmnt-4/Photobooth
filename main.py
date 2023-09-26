# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
import cv2
import tkinter as tk
from tkinter import ttk

# Initialize flags to track button presses
save_pressed = False
quit_pressed = False

# Create a VideoCapture object to access the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("Error: Webcam not found or cannot be accessed.")
else:
    root = tk.Tk()
    root.title("Capture Image")

    save_button = ttk.Button(root, text="Save Image", command=save_image)
    save_button.pack(pady=10)

    quit_button = ttk.Button(root, text="Quit", command=quit_app)
    quit_button.pack(pady=10)

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Webcam Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    root.mainloop()


def save_image():
        ret, frame = cap.read()
        if ret:
            image_filename = "captured_image.jpg"
            cv2.imwrite(image_filename, frame)
            print(f"Image captured and saved as {image_filename}")


    def quit_app():
        cap.release()
        root.destroy()

# image1 = cap.read()
# time.sleep(2)
#
# image2 = cap.read()
#
# image1 = image1.resize((426, 240))
# image1_size = image1.size
# image2_size = image2.size
# new_image = Image.new('RGB', (2 * image1_size[0], image1_size[1]), (250, 250, 250))
# new_image.paste(image1, (0, 0))
# new_image.paste(image2, (image1_size[0], 0))
# new_image.save("images/merged_image.jpg", "JPEG")
# new_image.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
