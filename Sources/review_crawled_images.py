import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import glob

# Danh sách keyword (gốc)
keywords = [
    "biển số xe",
    "biển số xe Việt Nam",
    "biển số xe máy",
    "biển số xe hơi",
    "biển số xe tải",
    "biển số ô tô",
    "biển số xe buýt",
    "biển số xe khách",
    "biển số xe container",
    "biển số xe công an",
    "biển số xe quân đội",
    "ảnh xe có biển số",
    "xe đang chạy có biển số",
    "biển số xe trước",
    "biển số xe sau",
    "biển số rõ nét",
    "ảnh biển số xe máy",
    "ảnh biển số xe ô tô",
    "góc chụp biển số xe",
    "biển số xe cũ",
    "biển số xe mới",
    "xe máy đang chạy biển số",
    "xe đậu có biển số",
    "xe biển số tỉnh"
]

# Đường dẫn thư mục chứa ảnh (cần chạy từ Sources/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Dataset/Crawl/bing"))


class ImageReviewer:
    def __init__(self, base_dir, keyword_folders):
        self.root = tk.Tk()
        self.root.title("Image Reviewer")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.image_label = tk.Label(self.root, bg="white")
        self.image_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=10)

        self.btn_delete = tk.Button(btn_frame, text="❌ Delete", command=self.delete_image, bg="red", fg="white")
        self.btn_delete.pack(side=tk.LEFT, padx=10)

        self.btn_skip = tk.Button(btn_frame, text="➡️ Next", command=self.next_image, bg="green", fg="white")
        self.btn_skip.pack(side=tk.LEFT, padx=10)

        self.image_paths = self.load_images(base_dir, keyword_folders)
        self.index = 0

        if not self.image_paths:
            messagebox.showinfo("Info", "Không tìm thấy ảnh.")
            self.root.quit()
        else:
            self.show_image()

        self.root.mainloop()

    def load_images(self, base_dir, folders):
        image_paths = []
        for kw in folders:
            folder_path = os.path.join(base_dir, kw.replace(" ", "_"))
            if os.path.isdir(folder_path):
                for ext in ('*.jpg', '*.jpeg', '*.png', '*.bmp'):
                    image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
        return sorted(image_paths)

    def show_image(self):
        if self.index < len(self.image_paths):
            path = self.image_paths[self.index]
            try:
                img = Image.open(path)
                img.thumbnail((700, 500))
                self.tk_img = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.tk_img)
                self.root.title(f"{self.index + 1}/{len(self.image_paths)} - {path}")
            except Exception as e:
                print(f"Lỗi mở ảnh {path}: {e}")
                self.next_image()
        else:
            messagebox.showinfo("Hoàn tất", "Đã duyệt xong tất cả ảnh.")
            self.root.quit()

    def delete_image(self):
        if self.index < len(self.image_paths):
            img_path = self.image_paths[self.index]
            os.remove(img_path)
            print(f"Đã xóa: {img_path}")
            self.image_paths.pop(self.index)
            self.show_image()

    def next_image(self):
        self.index += 1
        self.show_image()


if __name__ == "__main__":
    ImageReviewer(BASE_DIR, keywords)
