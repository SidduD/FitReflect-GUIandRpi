import tkinter as tk
import os
import subprocess
import sys



# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))



def run_script(script_path):
    try:
    
        subprocess.Popen(["python", script_path], start_new_session=True)  # start_new_session to make the subprocess independent
        status_label.config(text="Exercise started successfully.", fg="green")
        # root.destroy()  # Close the Tkinter window
        # sys.exit()  # Exit the script
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")




# Create main window
root = tk.Tk()
root.wm_attributes('-fullscreen', True)  # Enable fullscreen mode
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Exercise Selector")
root.configure(background='black') 

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

root.bind("<Escape>", toggle_fullscreen)


image_path = os.path.join(current_dir, "logo.GIF")
photo = tk.PhotoImage(file=image_path)
image_label = tk.Label(root, image=photo,bg='black')
image_label.pack()




# Create labels and buttons
label = tk.Label(root, text="Welcome to FitReflect", font=("Arial", 35, "bold"), fg='white', bg='black')
label.pack()
label2 = tk.Label(root, text="Please Select a Workout", font=("Arial", 18, "bold"), fg='white', bg='black')
label2.pack()

button_frame = tk.Frame(root, bg='black')
button_frame.pack(pady=10, fill='x', expand=True)  # Allow frame to expand and fill available space


def create_button(text, script_path, color, row, column):
    button = tk.Button(button_frame, height=3,width=8, text=text, command=lambda: run_script(script_path), bg=color, fg='white', font=("Arial", 20, "bold"))
    button.grid(row=row, column=column, padx=10, pady=10, sticky='') # Use grid layout with specified row and column, and sticky to center horizontally

# Use grid layout to arrange buttons in a row
create_button("Deadlift", os.path.join(current_dir, "deadliftUI.py"), "darkblue", 0, 0)
create_button("Shoulder\nPress", os.path.join(current_dir, "shoulderPressUI.py"), "darkblue", 0, 1)
create_button("Bicep Curl", os.path.join(current_dir, "bicepCurlUI.py"), "darkblue", 0, 2)
create_button("Squat", os.path.join(current_dir, "squatUI.py"), "darkblue", 0, 3)

status_label = tk.Label(root, text="",fg="white", bg="black")
status_label.pack(pady=5)

# Run the application
root.mainloop()
