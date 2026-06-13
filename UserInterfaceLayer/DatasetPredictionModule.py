from pathlib import Path
from tkinter import PhotoImage, StringVar, messagebox as msg
from tkinter.ttk import Labelframe
from ttkbootstrap import Button, Combobox, Entry, Frame, Label
from ttkbootstrap import DANGER, INFO, OUTLINE, PRIMARY, SECONDARY, SUCCESS, WARNING
from BusinessLogicLayer.DatasetPrediction_BLL import DatasetPrediction_BLL_Class
from .FormLayout import apply_readonly_value_style


class DatasetPredictionFrame(Frame):
    def __init__(self, main_view, window, dataset_key):
        super().__init__(window)

        self.main_view = main_view
        self.dataset_key = dataset_key
        self.dataset_bll = DatasetPrediction_BLL_Class()
        self.dataset = self.dataset_bll.get_dataset(dataset_key)
        self.fields = self.dataset_bll.get_input_fields(dataset_key)
        self.field_columns = self.get_field_column_count()
        self.input_variables = {}
        self.input_widgets = {}
        self.placeholder_entries = {}
        self.images_folder = Path(__file__).resolve().parents[1] / 'assets' / 'page_images'
        self.page_photo_image = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_summary()
        self.create_body()

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self)

    def create_header(self):
        self.header_bar = Frame(self)
        self.header_bar.grid(row=0, column=0, padx=14, pady=(5, 3), sticky='ew')
        self.header_bar.grid_columnconfigure(0, weight=1)

        self.header = Label(
            self.header_bar,
            text=self.dataset.display_name,
            style=PRIMARY,
            font=('Arial', 16, 'bold')
        )
        self.header.grid(row=0, column=0, sticky='w')

        self.back_button = Button(
            self.header_bar,
            text='Back To Main Page',
            bootstyle=OUTLINE + WARNING,
            command=self.back
        )
        self.back_button.grid(row=0, column=1, sticky='e')

    def get_dataset_page_image(self):
        image_path = self.get_dataset_image_path()
        if image_path is None:
            return None

        try:
            return PhotoImage(file=str(image_path))
        except Exception:
            return None

    def get_dataset_image_path(self):
        matches = sorted(self.images_folder.glob(f'{self.dataset.dataset_id:02d}_*.png'))
        if not matches:
            return None

        return matches[0]

    def create_summary(self):
        self.summary_frame = Labelframe(self, text='Dataset Information', style=SUCCESS)
        self.summary_frame.grid(row=1, column=0, padx=14, pady=(0, 10), sticky='ew')
        for column in range(8):
            self.summary_frame.grid_columnconfigure(column, weight=1)

        summary_values = [
            ('Method', self.dataset.method),
            ('Target', self.dataset.target),
            ('Domain', self.dataset.domain)
        ]

        for column, (label_text, value_text) in enumerate(summary_values):
            Label(self.summary_frame, text=f'{label_text}:', font=('Arial', 9, 'bold')).grid(
                row=0, column=column * 2, padx=(10, 2), pady=8, sticky='w'
            )
            value_label = Label(self.summary_frame, text=value_text)
            value_label.grid(row=0, column=column * 2 + 1, padx=(2, 10), pady=8, sticky='w')

        if self.dataset.notes:
            self.note_label = Label(self.summary_frame, text=self.dataset.notes, style=INFO)
            self.note_label.grid(row=1, column=0, columnspan=8, padx=10, pady=(0, 8), sticky='w')

    def create_body(self):
        self.body_frame = Frame(self)
        self.body_frame.grid(row=2, column=0, padx=14, pady=(0, 14), sticky='nsew')
        self.body_frame.grid_columnconfigure(0, weight=5)
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(0, weight=1)

        self.create_input_panel()
        self.create_result_panel()

    def create_input_panel(self):
        self.input_panel = Labelframe(self.body_frame, text='Prediction Inputs', style=SUCCESS)
        self.input_panel.grid(row=0, column=0, padx=(0, 8), sticky='nsew')
        self.input_panel.grid_columnconfigure(0, weight=1)
        self.input_panel.grid_rowconfigure(0, weight=1)

        self.input_frame = Frame(self.input_panel)
        self.input_frame.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        for column in range(self.field_columns):
            self.input_frame.grid_columnconfigure(column, weight=1, uniform='input_fields')

        self.create_input_fields()

        self.action_frame = Frame(self.input_panel)
        self.action_frame.grid(row=1, column=0, padx=8, pady=(0, 8), sticky='ew')
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)

        self.predict_button = Button(
            self.action_frame,
            text='Predict',
            bootstyle=SUCCESS,
            command=self.predict
        )
        self.predict_button.grid(row=0, column=0, padx=(0, 6), sticky='ew', ipady=4)

        self.clear_button = Button(
            self.action_frame,
            text='Clear Form',
            bootstyle=OUTLINE + SECONDARY,
            command=self.clear_form
        )
        self.clear_button.grid(row=0, column=1, padx=(6, 0), sticky='ew', ipady=4)

    def create_input_fields(self):
        label_wraplength = self.get_label_wraplength()
        entry_width = self.get_entry_width()

        for index, field in enumerate(self.fields):
            row = index // self.field_columns
            column = index % self.field_columns

            field_frame = Frame(self.input_frame)
            field_frame.grid(row=row, column=column, padx=6, pady=4, sticky='nsew')
            field_frame.grid_columnconfigure(0, weight=1)

            field_label = Label(
                field_frame,
                text=f"{field.get('label', field['name'])}:",
                wraplength=label_wraplength,
                justify='left'
            )
            field_label.grid(row=0, column=0, pady=(0, 2), sticky='w')

            variable = StringVar(value=str(field.get('placeholder', field.get('default', ''))))
            self.input_variables[field['name']] = variable

            if field['type'] == 'categorical':
                field_widget = Combobox(
                    field_frame,
                    textvariable=variable,
                    values=field.get('options', []),
                    state='readonly',
                    width=entry_width
                )
            else:
                field_widget = Entry(field_frame, textvariable=variable, width=entry_width)
                self.setup_entry_placeholder(field_widget, field)

            field_widget.grid(row=1, column=0, sticky='ew')
            self.input_widgets[field['name']] = field_widget

    def setup_entry_placeholder(self, entry_widget, field):
        placeholder = str(field.get('placeholder', field.get('default', '')))
        field_name = field['name']

        self.placeholder_entries[field_name] = {
            'widget': entry_widget,
            'placeholder': placeholder,
            'normal_foreground': entry_widget.cget('foreground'),
            'active': True
        }
        entry_widget.configure(foreground='#8A8F98')
        entry_widget.bind('<FocusIn>', lambda event, name=field_name: self.clear_entry_placeholder(name))
        entry_widget.bind('<FocusOut>', lambda event, name=field_name: self.restore_entry_placeholder(name))
        entry_widget.bind('<KeyRelease>', lambda event, name=field_name: self.mark_entry_as_user_value(name))

    def clear_entry_placeholder(self, field_name):
        placeholder_info = self.placeholder_entries.get(field_name)
        if not placeholder_info or not placeholder_info['active']:
            return

        variable = self.input_variables.get(field_name)
        if variable and variable.get() == placeholder_info['placeholder']:
            variable.set('')

        placeholder_info['active'] = False
        placeholder_info['widget'].configure(foreground=placeholder_info['normal_foreground'])

    def restore_entry_placeholder(self, field_name):
        placeholder_info = self.placeholder_entries.get(field_name)
        if not placeholder_info:
            return

        variable = self.input_variables.get(field_name)
        if not variable:
            return

        if variable.get().strip():
            placeholder_info['active'] = False
            placeholder_info['widget'].configure(foreground=placeholder_info['normal_foreground'])
            return

        variable.set(placeholder_info['placeholder'])
        placeholder_info['active'] = True
        placeholder_info['widget'].configure(foreground='#8A8F98')

    def mark_entry_as_user_value(self, field_name):
        placeholder_info = self.placeholder_entries.get(field_name)
        if not placeholder_info:
            return

        variable = self.input_variables.get(field_name)
        if variable and variable.get().strip():
            placeholder_info['active'] = False
            placeholder_info['widget'].configure(foreground=placeholder_info['normal_foreground'])

    def get_field_column_count(self):
        field_count = len(self.fields)
        if field_count >= 40:
            return 5

        if field_count >= 22:
            return 4

        if field_count >= 10:
            return 3

        return 2

    def get_label_wraplength(self):
        wraplength_by_columns = {
            2: 560,
            3: 390,
            4: 300,
            5: 235
        }
        return wraplength_by_columns.get(self.field_columns, 300)

    def get_entry_width(self):
        width_by_columns = {
            2: 36,
            3: 32,
            4: 28,
            5: 24
        }
        return width_by_columns.get(self.field_columns, 28)

    def create_result_panel(self):
        self.result_panel = Labelframe(self.body_frame, text='Prediction Result', style=SUCCESS)
        self.result_panel.grid(row=0, column=1, padx=(8, 0), sticky='nsew')
        self.result_panel.grid_columnconfigure(0, weight=1)

        current_row = 0
        self.page_photo_image = self.get_dataset_page_image()
        if self.page_photo_image:
            self.result_image = Label(self.result_panel, image=self.page_photo_image)
            self.result_image.grid(row=current_row, column=0, padx=12, pady=(12, 10), sticky='ew')
            current_row += 1

        self.result_title = Label(self.result_panel, text='No prediction yet.', style=PRIMARY,
                                  font=('Arial', 13, 'bold'))
        self.result_title.grid(row=current_row, column=0, padx=12, pady=(4, 8), sticky='w')
        current_row += 1

        self.result_body = Label(self.result_panel, text='', justify='left', wraplength=330, font=('Arial', 11))
        self.result_body.grid(row=current_row, column=0, padx=12, pady=(0, 12), sticky='nw')
        current_row += 1

        self.model_status = Label(
            self.result_panel,
            text=self.get_model_status_text(),
            style=INFO,
            justify='left',
            wraplength=330
        )
        self.model_status.grid(row=current_row, column=0, padx=12, pady=(8, 12), sticky='w')

        apply_readonly_value_style(self.result_title)

    def get_model_status_text(self):
        if not self.dataset.model_files:
            return 'Model: lightweight built-in estimate'

        model_names = ', '.join(self.dataset.model_files)
        return f'Model: {model_names}'

    def predict(self):
        try:
            values = self.get_prediction_values()
            result = self.dataset_bll.predict(self.dataset_key, values)
            self.result_title.configure(text=result.get('title', self.dataset.target))
            self.result_body.configure(text='\n'.join(result.get('lines', [])))
        except ValueError as error:
            msg.showwarning('Invalid Input', str(error))
        except Exception as error:
            msg.showerror('Prediction Failed', str(error))

    def clear_form(self):
        for field in self.fields:
            variable = self.input_variables.get(field['name'])
            if variable:
                variable.set(str(field.get('placeholder', field.get('default', ''))))

            if field['name'] in self.placeholder_entries:
                placeholder_info = self.placeholder_entries[field['name']]
                placeholder_info['active'] = True
                placeholder_info['widget'].configure(foreground='#8A8F98')

        self.result_title.configure(text='No prediction yet.')
        self.result_body.configure(text='')

    def get_prediction_values(self):
        values = {}
        for field in self.fields:
            field_name = field['name']
            placeholder_info = self.placeholder_entries.get(field_name)
            if placeholder_info and placeholder_info['active']:
                values[field_name] = str(field.get('default', ''))
                continue

            variable = self.input_variables.get(field_name)
            values[field_name] = variable.get() if variable else ''

        return values

    def back(self):
        self.main_view.switch('Main')
