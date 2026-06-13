from .Window import window


class MainView:
    def __init__(self):
        self.window = window()
        self.frames = {}
        self.frame_factories = {
            "Main": self.create_main_frame
        }

        self.switch("Main")
        self.window.mainloop()

    def add_frame(self, name, frame):
        self.frames[name] = frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def get_frame(self, frame_name):
        if frame_name in self.frames:
            return self.frames[frame_name]

        if frame_name.startswith("Dataset:"):
            frame = self.create_dataset_frame(frame_name.split(":", 1)[1])
            self.add_frame(frame_name, frame)
            return frame

        if frame_name not in self.frame_factories:
            raise ValueError(f"Unknown frame: {frame_name}")

        frame = self.frame_factories[frame_name]()
        self.add_frame(frame_name, frame)
        return frame

    def switch(self, frame_name):
        frame = self.get_frame(frame_name)
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        return frame

    def create_main_frame(self):
        from .MainModule import MainFrame
        return MainFrame(self, self.window)

    def create_dataset_frame(self, dataset_key):
        from .DatasetPredictionModule import DatasetPredictionFrame
        return DatasetPredictionFrame(self, self.window, dataset_key)
