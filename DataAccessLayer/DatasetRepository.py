import json
import os
import warnings
import joblib


class Dataset_Repository_Class:
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.models_folder = os.path.join(self.project_root, 'Datasets', 'Models')
        self.metadata_cache = {}
        self.model_cache = {}

    def get_metadata(self, metadata_file):
        if metadata_file in self.metadata_cache:
            return self.metadata_cache[metadata_file]

        path = os.path.join(self.models_folder, metadata_file)
        with open(path, 'r', encoding='utf-8') as metadata_reader:
            metadata = json.load(metadata_reader)

        self.metadata_cache[metadata_file] = metadata
        return metadata

    def get_model(self, model_file):
        if not model_file:
            return None

        if model_file in self.model_cache:
            return self.model_cache[model_file]

        path = os.path.join(self.models_folder, model_file)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            model = joblib.load(path)

        self.model_cache[model_file] = model
        return model

    def model_exists(self, model_file):
        if not model_file:
            return False

        return os.path.exists(os.path.join(self.models_folder, model_file))
