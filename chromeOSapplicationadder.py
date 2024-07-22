import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError
import requests
from io import BytesIO
import os
from serpapi import GoogleSearch
from config import SERPAPI_API_KEY  # Import API key from config file

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Entry Creator")
        self.root.geometry("600x700")

        self.font = ("Helvetica", 12)

        self.app_name_label = ttk.Label(root, text="Application Name", font=self.font)
        self.app_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='E')
        self.app_name_entry = ttk.Entry(root, font=self.font)
        self.app_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        self.exec_command_label = ttk.Label(root, text="Command to Execute", font=self.font)
        self.exec_command_label.grid(row=1, column=0, padx=5, pady=5, sticky='E')
        self.exec_command_entry = ttk.Entry(root, font=self.font)
        self.exec_command_entry.grid(row=1, column=1, padx=5, pady=5, sticky='W')

        self.comment_label = ttk.Label(root, text="Comment", font=self.font)
        self.comment_label.grid(row=2, column=0, padx=5, pady=5, sticky='E')
        self.comment_entry = ttk.Entry(root, font=self.font)
        self.comment_entry.grid(row=2, column=1, padx=5, pady=5, sticky='W')

        self.search_button = ttk.Button(root, text="Search for Icon", command=self.search_for_icon, style="TButton")
        self.search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.icon_frame = ttk.Frame(root)
        self.icon_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.selected_icon_label = ttk.Label(root)
        self.selected_icon_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.generate_button = ttk.Button(root, text="Generate .desktop Entry", command=self.generate_desktop_entry, style="TButton")
        self.generate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.desktop_entry_text = tk.Text(root, height=10, width=80, font=self.font)
        self.desktop_entry_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.save_button = ttk.Button(root, text="Save", command=self.save_desktop_entry, style="TButton")
        self.save_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.icon_path = ""

    def search_for_icon(self):
        app_name = self.app_name_entry.get()
        image_urls = self.search_icons(app_name)

        for widget in self.icon_frame.winfo_children():
            widget.destroy()

        for url in image_urls:
            image = self.download_image(url)
            if image:
                img = ImageTk.PhotoImage(image.resize((64, 64)))
                btn = ttk.Button(self.icon_frame, image=img, command=lambda url=url: self.select_icon(url))
                btn.image = img  # keep a reference!
                btn.pack(side=tk.LEFT)

    def search_icons(self, app_name):
        params = {
            "q": f"{app_name} icon",
            "tbm": "isch",
            "ijn": "0",
            "api_key": SERPAPI_API_KEY
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            image_results = results.get('images_results', [])
            image_urls = [image['original'] for image in image_results[:10] if 'original' in image]
            return image_urls
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching images: {e}")
            return []

    def download_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if 'image' not in response.headers.get('content-type'):
                raise UnidentifiedImageError("URL does not contain image data")
            image = Image.open(BytesIO(response.content))
            return image
        except (requests.RequestException, UnidentifiedImageError) as e:
            print(f"Error downloading image: {e}")
            return None

    def select_icon(self, url):
        image = self.download_image(url)
        if image:
            icon_dir = os.path.expanduser('~/.local/share/applications')
            os.makedirs(icon_dir, exist_ok=True)  # Ensure the directory exists
            self.icon_path = os.path.join(icon_dir, f'{self.app_name_entry.get().lower()}.png')
            image.save(self.icon_path)
            img = ImageTk.PhotoImage(image.resize((64, 64)))
            self.selected_icon_label.config(image=img)
            self.selected_icon_label.image = img  # keep a reference!

    def generate_desktop_entry(self):
        app_name = self.app_name_entry.get()
        exec_command = self.exec_command_entry.get()
        comment = self.comment_entry.get()

        desktop_entry = f"""[Desktop Entry]
Name={app_name}
Comment={comment}
Exec={exec_command}
Icon={self.icon_path}
Type=Application
Categories=Utility"""

        self.desktop_entry_text.delete(1.0, tk.END)
        self.desktop_entry_text.insert(tk.END, desktop_entry)

    def save_desktop_entry(self):
        app_name = self.app_name_entry.get()
        desktop_entry_path = os.path.expanduser(f'~/.local/share/applications/{app_name}.desktop')
        with open(desktop_entry_path, 'w') as f:
            f.write(self.desktop_entry_text.get(1.0, tk.END))
        messagebox.showinfo("Saved", f"The .desktop entry has been saved to {desktop_entry_path}")
        self.root.quit()  # Close the application on save success

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
