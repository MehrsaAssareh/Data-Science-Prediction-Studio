import json
import os
import importlib
import sys
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

        self.register_legacy_sklearn_modules()
        path = os.path.join(self.models_folder, model_file)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            model = joblib.load(path)

        self.repair_loaded_model(model)
        self.model_cache[model_file] = model
        return model

    def register_legacy_sklearn_modules(self):
        if '_loss' in sys.modules:
            return

        try:
            sys.modules['_loss'] = importlib.import_module('sklearn._loss.loss')
        except Exception:
            pass

    def repair_loaded_model(self, model):
        self.repair_estimator(model, set())

    def repair_estimator(self, estimator, visited):
        if estimator is None:
            return

        estimator_id = id(estimator)
        if estimator_id in visited:
            return
        visited.add(estimator_id)

        if estimator.__class__.__name__ == 'SimpleImputer' and not hasattr(estimator, '_fill_dtype'):
            fill_dtype = getattr(estimator, '_fit_dtype', None)
            if fill_dtype is None and hasattr(estimator, 'statistics_'):
                fill_dtype = estimator.statistics_.dtype
            if fill_dtype is not None:
                estimator._fill_dtype = fill_dtype

        for child in self.get_estimator_children(estimator):
            self.repair_estimator(child, visited)

    def get_estimator_children(self, estimator):
        children = []

        for attribute in ('steps', 'transformers', 'transformers_', 'estimators', 'estimators_'):
            value = getattr(estimator, attribute, None)
            if value is None:
                continue

            for item in value:
                if isinstance(item, tuple):
                    children.extend(part for part in item[1:] if hasattr(part, '__dict__'))
                elif hasattr(item, '__dict__'):
                    children.append(item)

        for attribute in ('estimator', 'base_estimator', 'final_estimator', 'regressor', 'classifier', 'transformer'):
            child = getattr(estimator, attribute, None)
            if hasattr(child, '__dict__'):
                children.append(child)

        return children

    def model_exists(self, model_file):
        if not model_file:
            return False

        return os.path.exists(os.path.join(self.models_folder, model_file))
