from pathlib import Path
from tkinter import PhotoImage

from ttkbootstrap import Button, Frame, Label
from ttkbootstrap.constants import INFO, OUTLINE, PRIMARY
from BusinessLogicLayer.DatasetCatalog import get_dataset_catalog


BUTTON_COLUMNS = 6


class MainFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.datasets = get_dataset_catalog()
        self.button_images = {}
        self.assets_folder = Path(__file__).resolve().parents[1] / 'assets'
        self.images_folder = self.assets_folder / 'button_images'
        self.icons_folder = self.assets_folder / 'icons'
        self.header_icon_image = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0, padx=18, pady=(14, 8), sticky='w')

        self.header_icon_image = self.get_header_icon_image()
        if self.header_icon_image:
            self.header_icon = Label(self.header_frame, image=self.header_icon_image)
            self.header_icon.grid(row=0, column=0, padx=(0, 10), sticky='w')

        self.header = Label(
            self.header_frame,
            text='Data Science Prediction Studio',
            style=PRIMARY,
            font=('Arial', 17, 'bold')
        )
        self.header.grid(row=0, column=1, sticky='w')

        self.dataset_frame = Frame(self)
        self.dataset_frame.grid(row=2, column=0, padx=16, pady=(0, 18), sticky='nsew')
        for column in range(BUTTON_COLUMNS):
            self.dataset_frame.grid_columnconfigure(column, weight=1, uniform='dataset_buttons')

        self.create_dataset_buttons()

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self)

    def create_dataset_buttons(self):
        for index, dataset in enumerate(self.datasets):
            row = index // BUTTON_COLUMNS
            column = index % BUTTON_COLUMNS
            self.dataset_frame.grid_rowconfigure(row, weight=1, uniform='dataset_button_rows')

            button_text = f'{dataset.display_name}\n{dataset.method}'
            button_image = self.get_dataset_button_image(dataset)
            dataset_button = Button(
                self.dataset_frame,
                text=button_text,
                image=button_image,
                compound='top',
                bootstyle=OUTLINE + INFO,
                command=lambda key=dataset.key: self.open_dataset(key)
            )
            dataset_button.grid(row=row, column=column, padx=6, pady=4, sticky='nsew', ipady=1)

    def get_header_icon_image(self):
        icon_path = self.icons_folder / 'app_icon_48.png'
        if not icon_path.exists():
            return None

        try:
            return PhotoImage(file=str(icon_path))
        except Exception:
            return None

    def get_dataset_button_image(self, dataset):
        image_path = self.get_dataset_image_path(dataset)
        if image_path is None:
            return ''

        try:
            photo_image = PhotoImage(file=str(image_path))
            self.button_images[dataset.key] = photo_image
            return photo_image
        except Exception:
            return ''

    def get_dataset_image_path(self, dataset):
        matches = sorted(self.images_folder.glob(f'{dataset.dataset_id:02d}_*.png'))
        if not matches:
            return None

        return matches[0]

    def open_dataset(self, dataset_key):
        self.main_view.switch(f'Dataset:{dataset_key}')

    def destroy(self):
        self.header_icon_image = None
        self.button_images.clear()
        super().destroy()
