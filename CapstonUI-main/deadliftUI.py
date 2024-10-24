import tkinter as tk
import os
import subprocess
import sys

import asyncio
import websockets
import json
# Initialize stopwatch variables
counter = 0
running = False

async def send_socket_message(text):
    uri = "ws://169.254.69.69:8765"   # Replace with your WebSocket server URI
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                data = {"source": "USER_INTERFACE",
                        "destination": "ALL",
                        "workout_title": text
                        }  # Message to send
                await websocket.send(json.dumps(data))

                if (text == "STOP"):
                    await websocket.close()
                break
        except Exception as e:
            print(f"Connection failed: {e}")
            await asyncio.sleep(1)  # Wait for a second before trying to reconnect

# Function to increment the counter
def counter_label(label):
    def count():
        if running:
            global counter
            # Convert counter to HH:MM:SS format
            hours, remainder = divmod(counter, 3600)
            minutes, seconds = divmod(remainder, 60)
            display = f"{hours:02}:{minutes:02}:{seconds:02}"

            label.config(text=display)
            label.after(1000, count)
            counter += 1
    count()
# Start the stopwatch
def start(label):
    asyncio.run(send_socket_message("Deadlift"))
    global running
    running = True
    counter_label(label)
    start_button.config(state='disabled')
    stop_button.config(state='normal')
    reset_button.config(state='normal')

# Stop the stopwatch
def stop():
    global running
    start_button.config(state='normal')
    stop_button.config(state='disabled')
    reset_button.config(state='normal')
    running = False

# Reset the stopwatch
def reset(label):
    global counter
    counter = 0

    # If reset is pressed after pressing stop.
    if not running:
        reset_button.config(state='disabled')
        label.config(text='Hit Start to begin workout timer!')

    # If reset is pressed while the stopwatch is running.
    else:
        label.config(text='Starting...')

# Create main window
root = tk.Tk()
root.title("Bicep Curl")
root.attributes('-fullscreen', True)  # Enable fullscreen mode
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(background='black') 



current_dir = os.path.dirname(os.path.abspath(__file__))
def run_script(script_path):
    try:
        asyncio.run(send_socket_message("STOP"))
        subprocess.Popen(["python", script_path], start_new_session=True)  # start_new_session to make the subprocess independent
        status_label.config(text="Back to workout selector.", fg="green")
        root.destroy()  # Close the Tkinter window
        sys.exit()  # Exit the script
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")


def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

root.bind("<Escape>", toggle_fullscreen)


# Create labels and buttons
image_path = os.path.join(current_dir, "logo.GIF")
photo = tk.PhotoImage(file=image_path)
image_label = tk.Label(root, image=photo,bg='black')
image_label.pack()
label = tk.Label(root, text="Dead Lift", font=("Arial", 35, "bold"),fg='white', bg='black')
label.pack(pady=20)



status_label = tk.Label(root, text="", bg="black")
status_label.pack(pady=5)

# Stopwatch label
stopwatch_label = tk.Label(root, text="Hit Start to begin workout timer!", fg="white", bg='black', font=("Arial", 30))
stopwatch_label.pack()

# Frame for stopwatch control buttons
controls_frame = tk.Frame(root, bg='black')
controls_frame.pack( pady=20)

# Start button
start_button = tk.Button(controls_frame, height=3, width=20, text='Start', state='normal', command=lambda: start(stopwatch_label),font=("Arial", 10),bg="Cadet Blue")
start_button.pack(side='left', padx=5)

# Stop button
stop_button = tk.Button(controls_frame, height=3, width=20, text='Stop', state='disabled', command=stop, font=("Arial", 10),bg="Cadet Blue")
stop_button.pack(side='left', padx=5)

# Reset button
reset_button = tk.Button(controls_frame, height=3, width=20, text='Reset', state='disabled', command=lambda: reset(stopwatch_label), font=("Arial", 10),bg="Cadet Blue")
reset_button.pack(side='left', padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10, fill='x', expand=True)  # Allow frame to expand and fill available space



def create_button(text, script_path, color):
    button = tk.Button(button_frame,height=3, text=text, command=lambda: run_script(script_path), bg=color, fg='black',font=("Arial", 12,"bold"))
    button.pack(side=tk.LEFT, expand=True, fill='both', padx=10)  # Buttons expand and fill available space


create_button("Back to Workout Selector", os.path.join(current_dir, "main.py"), "lightblue")
# Main application loop
root.mainloop()
