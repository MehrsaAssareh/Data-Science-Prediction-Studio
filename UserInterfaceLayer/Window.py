import ctypes
from ctypes import wintypes
from pathlib import Path
from tkinter import PhotoImage
from ttkbootstrap import Window

APP_WINDOW_SIZE = "1800x950"
APP_USER_MODEL_ID = "DataSciencePredictionStudio.App"


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]


class window(Window):
    def __init__(self, size=APP_WINDOW_SIZE):
        self.set_windows_app_id()
        super().__init__(title="Data Science Prediction Studio", themename="solar")

        self.set_app_icon()
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.center_window(size)
        self.after(200, self.set_app_icon)

    def set_windows_app_id(self):
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
        except Exception:
            pass

    def set_app_icon(self):
        icons_folder = Path(__file__).resolve().parents[1] / 'assets' / 'icons'
        icon_paths = [
            icons_folder / 'app_icon_legacy.ico',
            icons_folder / 'app_icon.ico'
        ]
        png_paths = [
            icons_folder / 'app_icon_256.png',
            icons_folder / 'app_icon_64.png',
            icons_folder / 'app_icon_32.png',
            icons_folder / 'app_icon_16.png'
        ]

        self.icon_load_errors = []

        for icon_path in icon_paths:
            if not icon_path.exists():
                continue

            try:
                self.iconbitmap(str(icon_path))
                self.iconbitmap(default=str(icon_path))
                break
            except Exception as error:
                self.icon_load_errors.append(str(error))

        try:
            self.app_icon_images = [
                PhotoImage(file=str(path))
                for path in png_paths
                if path.exists()
            ]
            if self.app_icon_images:
                self.iconphoto(True, *self.app_icon_images)
        except Exception as error:
            self.icon_load_errors.append(str(error))

    def center_window(self, size):
        width, height = [int(value) for value in size.split("x")]
        self.update_idletasks()

        left, top, right, bottom = self.get_work_area()
        work_width = right - left
        work_height = bottom - top
        horizontal_margin = 40
        vertical_margin = 88

        width = min(width, max(320, work_width - horizontal_margin))
        height = min(height, max(320, work_height - vertical_margin))
        x = left + max(0, int((work_width - width) / 2))
        y = top + max(0, int((work_height - height) / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

    def fit_to_content(self, frame, min_width=980, min_height=700, extra_width=24, extra_height=24):
        self.center_window(APP_WINDOW_SIZE)

    def get_work_area(self):
        try:
            work_area = RECT()
            get_work_area = 0x0030
            success = ctypes.windll.user32.SystemParametersInfoW(get_work_area, 0, ctypes.byref(work_area), 0)
            if success:
                return work_area.left, work_area.top, work_area.right, work_area.bottom
        except Exception:
            pass

        return 0, 0, self.winfo_screenwidth(), self.winfo_screenheight()

    def show(self):
        self.mainloop()
