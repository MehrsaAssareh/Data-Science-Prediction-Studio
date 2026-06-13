class Dataset_Model_Class:
    def __init__(self,
                 dataset_id: int,
                 key: str,
                 title: str,
                 level: str,
                 domain: str,
                 method: str,
                 target: str,
                 metadata_file: str,
                 model_files=None,
                 result_labels=None,
                 output_labels=None,
                 special_handler: str = None,
                 notes: str = None):
        self.dataset_id = dataset_id
        self.key = key
        self.title = title
        self.level = level
        self.domain = domain
        self.method = method
        self.target = target
        self.metadata_file = metadata_file
        self.model_files = model_files or []
        self.result_labels = result_labels or {}
        self.output_labels = output_labels or []
        self.special_handler = special_handler
        self.notes = notes

    @property
    def display_name(self):
        return f"{self.dataset_id}. {self.title}"
