import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import ImageSequenceClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from PIL import Image
import numpy as np

class ImageToVideoConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to Video Converter")

        # Center the window on the screen
        window_width = 1000
        window_height = 1000
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.title_label = tk.Label(master, text="Image to Video Converter", font=("Helvetica", 20, "bold"), bg="#F2F2F2", fg="#333")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Label to show selected images
        self.label = tk.Label(master, text="No images selected", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Button to browse individual files
        self.browse_button = tk.Button(master, text="Browse Files", font=("Helvetica", 12), command=self.browse_files, bg="#4CAF50", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.browse_button.grid(row=2, column=0, padx=10, pady=5)

        # Button to browse a folder
        self.browse_folder_button = tk.Button(master, text="Browse Folder", font=("Helvetica", 12), command=self.browse_folder, bg="#2196F3", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.browse_folder_button.grid(row=2, column=1, padx=10, pady=5)

        # Duration Label
        self.duration_label = tk.Label(master, text="Choose image duration (seconds)", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.duration_label.grid(row=3, column=0, columnspan=2, pady=(0, 5))

        # Entry for image duration
        self.duration_entry = tk.Entry(master, font=("Helvetica", 12), bg="white", fg="#333", relief=tk.FLAT,width=3)
        self.duration_entry.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Transition Label
        self.transition_label = tk.Label(master, text="Choose transition", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.transition_label.grid(row=5, column=0, columnspan=2, pady=(0, 5))

        # Option Menu for transition
        self.transition_var = tk.StringVar(value="None")
        self.transition_menu = tk.OptionMenu(master, self.transition_var, "None", "Fade")
        self.transition_menu.config(font=("Helvetica", 12), bg="white", fg="#333", relief=tk.FLAT)
        self.transition_menu.grid(row=6, column=0, columnspan=2, pady=(0, 10))

        # Frame to contain the listbox and delete button
        self.image_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, width=50, height=10)
        self.image_listbox.grid(row=7, column=0, columnspan=2, pady=10)

        self.delete_button = tk.Button(master, text="Delete Selected", font=("Helvetica", 12), command=self.delete_selected, bg="#F44336", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.delete_button.grid(row=8, column=0, columnspan=2, pady=5)

        # Convert button
        self.convert_button = tk.Button(master, text="Convert to Video", font=("Helvetica", 12), command=self.convert_to_video, bg="#FF9800", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.convert_button.grid(row=9, column=0, columnspan=2, pady=10)

     

        # Protocol for closing the window
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.file_paths = []

        # Define the protocol for closing the window
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(initialdir="/home/shayan/Pictures/Screenshots", title="Select Images", filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if file_paths:
            self.file_paths.extend(file_paths)
            self.update_image_listbox()
            self.label.config(text=f"{len(self.file_paths)} images selected")

    def update_label(self):
        self.label.config(text=f"{len(self.file_paths)} images selected")

    def browse_folder(self):
        folder_path = filedialog.askdirectory(initialdir="~", title="Select Folder")
        if folder_path:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.file_paths.append(os.path.join(folder_path, file))
            self.update_image_listbox()
            self.label.config(text=f"{len(self.file_paths)} images selected")

    def update_image_listbox(self):
        self.image_listbox.delete(0, tk.END)
        for file_path in self.file_paths:
            self.image_listbox.insert(tk.END, file_path)
        # self.add_delete_buttons()

    def delete_selected(self):
        selected_indices = self.image_listbox.curselection()
        selected_files = [self.file_paths[i] for i in selected_indices]
        for file in selected_files:
            self.file_paths.remove(file)
        self.update_image_listbox()
        self.label.config(text=f"{len(self.file_paths)} images selected")

    # def add_delete_buttons(self):
    #     # Remove existing delete buttons
    #     for button in self.delete_buttons:
    #         button.destroy()
    #     self.delete_buttons.clear()

    #     # Add delete buttons for each item in listbox
    #             # Image Listbox
    #     # self.image_listbox = tk.Listbox(self.inner_frame, selectmode=tk.SINGLE, width=50, height=10, font=("Helvetica", 12), bg="white", fg="#333", relief=tk.FLAT)
    #             # Image Listbox
    #     self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    #     # Add delete buttons for each item in listbox
    #     for i in range(self.image_listbox.size()):
    #         delete_button = tk.Button(self.inner_frame, text="-", font=("Helvetica", 12), command=lambda index=i: self.delete_item(index), bg="#FF5722", fg="white", relief=tk.FLAT, bd=0, height=1)
    #         delete_button.pack(anchor='w', padx=(0, 5), pady=(0, 5))
    #         self.delete_buttons.append(delete_button)

    #     # Update the scroll region of the canvas
    #     self.canvas.update_idletasks()
    #     self.canvas.config(scrollregion=self.canvas.bbox("all"))

    #     # Update the scroll region of the canvas
    #     self.canvas.update_idletasks()
    #     self.canvas.config(scrollregion=self.canvas.bbox("all"))



    # def delete_item(self, index):
    #     self.file_paths.pop(index)
    #     self.update_image_listbox()

    def resize_image(self, image_path, target_size):
        image = Image.open(image_path)
        aspect_ratio = min(target_size[0] / image.width, target_size[1] / image.height)
        new_size = (int(image.width * aspect_ratio), int(image.height * aspect_ratio))
        resized_image = image.resize(new_size, Image.LANCZOS)

        new_image = Image.new("RGB", target_size, (255, 255, 255))
        left = (target_size[0] - new_size[0]) // 2
        top = (target_size[1] - new_size[1]) // 2
        new_image.paste(resized_image, (left, top))

        return new_image
    
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def convert_to_video(self):
        
        if self.duration_entry.get()=="" or not self.is_number(self.duration_entry.get()) or float(self.duration_entry.get())<=0:
            messagebox.showwarning("Warning", "Duration is not a valid number")
            return

        if not self.file_paths:
            print("No images selected!")
            messagebox.showwarning("Warning", "No images selected!")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        if output_file:
            print("Converting images to video...")
            clips = []
            target_size = (2560, 1440)
            for file_path in self.file_paths:
                image = self.resize_image(file_path, target_size)
                clips.append(np.array(image))

            video_clips = []
            for i, img_array in enumerate(clips):
                img_clip = ImageSequenceClip([img_array], durations=[6])
                if self.transition_var.get() == "Fade" and i > 0:
                    img_clip = fadein(img_clip, 2)
                if self.transition_var.get() == "Fade" and i < len(clips) - 1:
                    img_clip = fadeout(img_clip, 2)
                video_clips.append(img_clip)

            final_clip = concatenate_videoclips(video_clips, method="compose")
            final_clip.write_videofile(output_file, codec="libx264",fps=30)
            print("Video saved successfully at:", output_file)
            messagebox.showinfo("Success", "Video saved successfully!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    app = ImageToVideoConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
