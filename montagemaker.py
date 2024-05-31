import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, CENTER
from moviepy.editor import ImageSequenceClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from PIL import Image, ImageTk
import numpy as np
from proglog import ProgressBarLogger


class MyBarLogger(ProgressBarLogger):

    def __init__(self,imageToVideoConverter):
        super().__init__()
        # self.value = 0
        self.converter =imageToVideoConverter

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def bars_callback(self, bar, attr, value,old_value=None):
        # Every time the logger progress is updated, this function is called        
        percentage = (value / self.bars[bar]['total']) * 100
        # print(bar,attr,percentage)
        self.converter.progress['value'] = percentage
        self.converter.master.update_idletasks()
    
    def callback(self, **changes):
        pass
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        # for (parameter, value) in changes.items():
            # self.value = value
            

            # print ('Parameter %s is now %s' % (parameter, value))

class ImageToVideoConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to Video Converter")

        self.logger = MyBarLogger(self)

        self.currentInputPath = '/home/shayan/Pictures/Screenshots'
        self.currentOutputPath = '/home/shayan/Pictures/Screenshots'
        self.thumbnailSize = (200,200)

        # Center the window on the screen
        window_width = 1000
        window_height = 1200
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        master.configure(bg="#F2F2F2")

        # Title label
        self.title_label = tk.Label(master, text="Image to Video Converter", font=("Helvetica", 20, "bold"), bg="#F2F2F2", fg="#333")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # Label to show selected images
        self.label = tk.Label(master, text="No images selected", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # Button to browse individual files
        self.browse_button = tk.Button(master, text="Browse Files", font=("Helvetica", 12), command=self.browse_files, bg="#4CAF50", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.browse_button.grid(row=2, column=0, padx=10, pady=5)

        # Button to browse a folder
        self.browse_folder_button = tk.Button(master, text="Browse Folder", font=("Helvetica", 12), command=self.browse_folder, bg="#2196F3", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.browse_folder_button.grid(row=2, column=1, padx=10, pady=5)

        # Duration Label
        self.duration_label = tk.Label(master, text="Choose image duration (seconds)", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.duration_label.grid(row=3, column=0, columnspan=3, pady=(0, 5))

        # Entry for image duration
        self.duration_entry = tk.Entry(master, font=("Helvetica", 12), bg="white", fg="#333", relief=tk.FLAT)
        self.duration_entry.grid(row=4, column=0, columnspan=3, pady=(0, 10))

        # Transition Label
        self.transition_label = tk.Label(master, text="Choose transition", font=("Helvetica", 12), bg="#F2F2F2", fg="#333")
        self.transition_label.grid(row=5, column=0, columnspan=3, pady=(0, 5))

        # Option Menu for transition
        self.transition_var = tk.StringVar(value="None")
        self.transition_menu = tk.OptionMenu(master, self.transition_var, "None", "Fade")
        self.transition_menu.config(font=("Helvetica", 12), bg="white", fg="#333", relief=tk.FLAT)
        self.transition_menu.grid(row=6, column=0, columnspan=3, pady=(0, 10))

        # Button to decrease image preview size
        self.browse_button = tk.Button(master, text="-", font=("Helvetica", 12), command=self.decrease_prev_size, fg="white", relief=tk.FLAT, bd=0)
        self.browse_button.grid(row=7, column=0, padx=0, pady=5)

        # Toggle for image previews
        self.preview_var = tk.BooleanVar()
        self.preview_checkbox = tk.Checkbutton(master, text="Show Image Previews", variable=self.preview_var, font=("Helvetica", 12), bg="#F2F2F2", fg="#333", command=self.update_image_listbox)
        self.preview_checkbox.grid(row=7, column=1, columnspan=3, pady=(0, 10))

        # Button to increase image preview size
        self.browse_button = tk.Button(master, text="+", font=("Helvetica", 12), command=self.decrease_prev_size, fg="white", relief=tk.FLAT, bd=0)
        self.browse_button.grid(row=7, column=2, padx=0, pady=5)

        # Scrollable Text widget for image files with previews
        self.text_frame = tk.Frame(master)
        self.text_frame.grid(row=8, column=0, columnspan=3, pady=10)
        self.scrollbar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL)
        self.image_text = tk.Text(self.text_frame, width=50, height=10, yscrollcommand=self.scrollbar.set, wrap="none")
        self.scrollbar.config(command=self.image_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_text.pack(side=tk.LEFT, fill=tk.BOTH)

        # Delete selected button
        self.delete_button = tk.Button(master, text="Delete Selected", font=("Helvetica", 12), command=self.delete_selected, bg="#F44336", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.delete_button.grid(row=9, column=0, columnspan=3, pady=5)


        # Convert button
        self.convert_button = tk.Button(master, text="Convert to Video", font=("Helvetica", 12), command=self.convert_to_video, bg="#FF9800", fg="white", relief=tk.FLAT, bd=0, padx=10, pady=5)
        self.convert_button.grid(row=10, column=0, columnspan=3, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=11, column=0, columnspan=3, pady=10)

        self.file_paths = []
        self.photos = {}
        self.checkbuttons = []

        # Define the protocol for closing the window
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def decrease_prev_size(self):
        self.thumbnailSize = (self.thumbnailSize[0]-30,self.thumbnailSize[1]-30)
        self.update_image_listbox()

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(initialdir=self.currentInputPath, title="Select Images", filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")), multiple=True)
        if len(self.file_paths)>0:
            self.currentInputPath = os.path.dirname(file_paths[-1])
        if file_paths:
            self.file_paths.extend(file_paths)
            self.update_image_listbox()
            self.label.config(text=f"{len(self.file_paths)} images selected")

    def browse_folder(self):
        folder_path = filedialog.askdirectory(initialdir="self.currentInputPath", title="Select Folder")
        if folder_path:
            self.currentInputPath = folder_path
        if folder_path:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.file_paths.append(os.path.join(folder_path, file))
            self.update_image_listbox()
            self.label.config(text=f"{len(self.file_paths)} images selected")

    def update_image_listbox(self):
        self.image_text.delete(1.0, tk.END)
        self.photos.clear()
        self.checkbuttons.clear()
        for idx, file_path in enumerate(self.file_paths):
            var = tk.BooleanVar()
            checkbutton = tk.Checkbutton(self.text_frame, variable=var, bg="#F2F2F2")
            self.checkbuttons.append((checkbutton, var))
            self.image_text.window_create(tk.END, window=checkbutton)
            tag = f"image_{idx}"
            if self.preview_var.get():
                try:
                    image = Image.open(file_path)
                    image.thumbnail(self.thumbnailSize, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.photos[file_path] = photo
                    self.image_text.image_create(tk.END, image=photo)
                    self.image_text.insert(tk.END, f" {os.path.basename(file_path)}\n", tag)
                except Exception as e:
                    self.image_text.insert(tk.END, f"{os.path.basename(file_path)}\n", tag)
            else:
                self.image_text.insert(tk.END, f"{os.path.basename(file_path)}\n", tag)

    def delete_selected(self):
        indices_to_delete = [idx for idx, (_, var) in enumerate(self.checkbuttons) if var.get()]
        if not indices_to_delete:
            messagebox.showwarning("Warning", "Please select items to delete.")
            return

        for idx in reversed(indices_to_delete):
            del self.file_paths[idx]
            del self.checkbuttons[idx]

        self.update_image_listbox()
        self.label.config(text=f"{len(self.file_paths)} images selected")

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

    def convert_to_video(self):
        if not self.file_paths:
            print("No images selected!")
            messagebox.showwarning("Warning", "No images selected!")
            return

        output_file = filedialog.asksaveasfilename(initialdir=self.currentOutputPath,defaultextension=".mp4", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        
        if output_file:
            self.currentOutputPath = os.path.dirname(self.currentOutputPath)
            clips = []
            target_size = (2560, 1440)
            duration = int(self.duration_entry.get()) if self.duration_entry.get().isdigit() else 5
            for file_path in (self.file_paths):
                image = self.resize_image(file_path, target_size)
                clips.append(np.array(image))
                self.progress['value'] += (50 / len(self.file_paths))
                self.master.update_idletasks()

            video_clips = []
            for i, img_array in enumerate(clips):
                img_clip = ImageSequenceClip([img_array], durations=[duration])
                if self.transition_var.get() == "Fade" and i > 0:
                    img_clip = fadein(img_clip, 1)
                if self.transition_var.get() == "Fade" and i < len(clips) - 1:
                    img_clip = fadeout(img_clip, 1)
                video_clips.append(img_clip)

            final_clip = concatenate_videoclips(video_clips, method="compose")

            # Use the progress bar for video file writing
            # def update_progress_bar(current, total):
            #         self.progress['value'] = 50 + (50 * current / total)
            #         self.master.update_idletasks()

            final_clip.write_videofile(output_file, codec="libx264", fps=30, logger=self.logger)
            print("Video saved successfully at:", output_file)
            messagebox.showinfo("Success", "Video saved successfully!")
            self.progress['value'] = 0

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
