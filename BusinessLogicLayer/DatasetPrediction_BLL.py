import math
import warnings
import numpy as np
import pandas as pd
from BusinessLogicLayer.DatasetCatalog import get_dataset_by_key, get_dataset_catalog
from DataAccessLayer.DatasetRepository import Dataset_Repository_Class


FIELD_LABEL_OVERRIDES = {
    'abalone': {
        'Length': 'Shell length',
        'Diameter': 'Shell diameter',
        'Height': 'Shell height',
        'Whole weight': 'Whole weight',
        'Shucked weight': 'Shucked weight',
        'Viscera weight': 'Viscera weight',
        'Shell weight': 'Shell weight',
        'Age': 'Age value'
    },
    'userknowledge': {
        'STG': 'Study time for goal materials',
        'SCG': 'Repetition count for goal materials',
        'STR': 'Study time for related materials',
        'LPR': 'Exam performance for related materials',
        'PEG': 'Exam performance for goal materials'
    },
    'realestate': {
        'X1 transaction date': 'Transaction date',
        'X2 house age': 'House age',
        'X3 distance to the nearest MRT station': 'Distance to nearest MRT station',
        'X4 number of convenience stores': 'Number of convenience stores',
        'X5 latitude': 'Latitude',
        'X6 longitude': 'Longitude'
    },
    'carevaluation': {
        'Buying': 'Buying price',
        'Main': 'Maintenance price',
        'Lug_boot': 'Luggage boot size'
    },
    'fertility': {
        'Childish Disease': 'Childhood disease',
        'Accident or Serious Trauma': 'Accident or serious trauma',
        'Sergical Intervention': 'Surgical intervention',
        'High Fevers in Last Year': 'High fever in the last year',
        'Frequency of Alcohol Consumption': 'Alcohol consumption frequency',
        'Smoking Habit': 'Smoking habit',
        'Number of Hours spent sitting per Day': 'Daily sitting hours'
    },
    'bankruptcy': {
        'Industrial Risk': 'Industrial risk',
        'Management Risk': 'Management risk',
        'Financial Flexibility': 'Financial flexibility',
        'Credibility': 'Credibility',
        'Competitiveness': 'Competitiveness',
        'Operating Risk': 'Operating risk'
    },
    'autompg': {
        'cylinders': 'Cylinders',
        'displacement': 'Engine displacement',
        'horsepower': 'Horsepower',
        'weight': 'Vehicle weight',
        'acceleration': 'Acceleration',
        'model year': 'Model year',
        'origin': 'Origin code',
        'car name_encoded': 'Car model code'
    },
    'heart': {
        'CP': 'Chest pain type',
        'TrestBPT': 'Resting blood pressure',
        'Chol': 'Cholesterol',
        'FBS': 'Fasting blood sugar',
        'RestECG': 'Resting ECG result',
        'Thalach': 'Maximum heart rate',
        'Exang': 'Exercise-induced angina',
        'OldPeak': 'ST depression',
        'Slope': 'ST segment slope',
        'Ca': 'Major vessels count',
        'Thal': 'Thalassemia value'
    },
    'dailydemand': {
        'Week of the month': 'Week of the month',
        'Day of the week': 'Day of the week',
        'Non-urgent order': 'Non-urgent orders',
        'Urgent order': 'Urgent orders',
        'Order type A': 'Order type A',
        'Order type B': 'Order type B',
        'Order type C': 'Order type C',
        'Fiscal sector orders': 'Fiscal sector orders',
        'Orders from the traffic controller sector': 'Traffic controller sector orders',
        'Banking orders (1)': 'Banking orders 1',
        'Banking orders (2)': 'Banking orders 2',
        'Banking orders (3)': 'Banking orders 3'
    },
    'blood': {
        'Recency (months)': 'Months since last donation',
        'Frequency (times)': 'Number of donations',
        'Time (months)': 'Months since first donation'
    },
    'beijing': {
        'pm2.5': 'PM2.5 concentration',
        'DEWP': 'Dew point',
        'TEMP': 'Temperature',
        'PRES': 'Pressure',
        'Iws': 'Cumulative wind speed',
        'Is': 'Snow hours',
        'Ir': 'Rain hours'
    },
    'echocardiogram': {
        'age-at-heart-attack': 'Age at heart attack',
        'pericardial-effusion': 'Pericardial effusion',
        'fractional-shortening': 'Fractional shortening',
        'epss': 'EPSS measurement',
        'lvdd': 'Left ventricular dimension',
        'wall-motion-score': 'Wall motion score',
        'wall-motion-index': 'Wall motion index',
        'mult': 'Wall motion multiplier'
    },
    'concrete': {
        'Cement (component 1)(kg in a m^3 mixture)': 'Cement (kg/m^3)',
        'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': 'Blast furnace slag (kg/m^3)',
        'Fly Ash (component 3)(kg in a m^3 mixture)': 'Fly ash (kg/m^3)',
        'Water  (component 4)(kg in a m^3 mixture)': 'Water (kg/m^3)',
        'Superplasticizer (component 5)(kg in a m^3 mixture)': 'Superplasticizer (kg/m^3)',
        'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': 'Coarse aggregate (kg/m^3)',
        'Fine Aggregate (component 7)(kg in a m^3 mixture)': 'Fine aggregate (kg/m^3)',
        'Age (day)': 'Concrete age (days)'
    },
    'liver': {
        'mcv': 'Mean corpuscular volume',
        'alkphos': 'Alkaline phosphatase',
        'sgpt': 'SGPT enzyme level',
        'sgot': 'SGOT enzyme level',
        'gammagt': 'Gamma-GT enzyme level',
        'drinks': 'Alcohol drinks per day'
    },
    'dowjones': {
        'quarter': 'Quarter',
        'open': 'Opening price',
        'high': 'Highest price',
        'low': 'Lowest price',
        'close': 'Closing price',
        'volume': 'Trading volume',
        'percent_change_price': 'Price change percent',
        'percent_change_volume_over_last_wk': 'Volume change from last week',
        'percent_change_next_weeks_price': 'Next week price change percent',
        'days_to_next_dividend': 'Days to next dividend',
        'volume_ratio': 'Volume ratio',
        'volume_delta': 'Volume difference'
    },
    'energy': {
        'X1': 'Relative compactness',
        'X2': 'Surface area',
        'X3': 'Wall area',
        'X4': 'Roof area',
        'X5': 'Overall height',
        'X6': 'Orientation',
        'X7': 'Glazing area',
        'X8': 'Glazing area distribution'
    },
    'glass': {
        'RI': 'Refractive index',
        'Na': 'Sodium',
        'Mg': 'Magnesium',
        'AI': 'Aluminum',
        'Si': 'Silicon',
        'K': 'Potassium',
        'Ca': 'Calcium',
        'Ba': 'Barium',
        'Fe': 'Iron'
    },
    'hepatitis': {
        'Steroid': 'Steroid treatment',
        'Antivirals': 'Antiviral treatment',
        'Fatigue': 'Fatigue symptom',
        'Malaise': 'Malaise symptom',
        'Anorexia': 'Anorexia symptom',
        'Liver_Big': 'Enlarged liver',
        'Liver_Firm': 'Firm liver',
        'Spleen_Palpable': 'Palpable spleen',
        'Spiders': 'Spider angiomas',
        'Albumin': 'Albumin level',
        'Alk_Phosphate': 'Alkaline phosphatase',
        'Bilirubin': 'Bilirubin level',
        'Protime': 'Prothrombin time',
        'Varices': 'Varices present'
    },
    'wholesale': {
        'Fresh': 'Fresh products spending',
        'Milk': 'Milk products spending',
        'Grocery': 'Grocery products spending',
        'Frozen': 'Frozen products spending',
        'Detergents_Paper': 'Detergents and paper spending',
        'Delicassen': 'Delicatessen spending',
        'Channel_2': 'Retail channel indicator',
        'Region_2': 'Region 2 indicator',
        'Region_3': 'Region 3 indicator'
    },
    'istanbulstock': {
        'SP': 'S&P 500 return',
        'DAX': 'DAX return',
        'FTSE': 'FTSE return',
        'NIKKEI': 'Nikkei return',
        'BOVESPA': 'Bovespa return',
        'EU': 'MSCI Europe return',
        'EM': 'MSCI emerging markets return'
    },
    'bikesharing': {
        'season': 'Season',
        'yr': 'Year',
        'mnth': 'Month',
        'hr': 'Hour',
        'holiday': 'Holiday',
        'weekday': 'Weekday',
        'workingday': 'Working day',
        'weathersit': 'Weather situation',
        'temp': 'Temperature',
        'atemp': 'Feels-like temperature',
        'hum': 'Humidity',
        'windspeed': 'Wind speed'
    },
    'occupancy': {
        'Light': 'Light level',
        'CO2': 'CO2 level',
        'HumidityRatio': 'Humidity ratio'
    },
    'censusincome': {
        'fnlwgt': 'Final sample weight',
        'education-num': 'Years of education',
        'marital-status': 'Marital status',
        'capital-gain': 'Capital gain',
        'capital-loss': 'Capital loss',
        'hours-per-week': 'Hours per week',
        'native-country': 'Native country'
    },
    'covid': {
        'DayOfYear': 'Day of year',
        'Lag_1_Cases': 'Previous confirmed cases',
        'Roll_7_Cases': 'Seven-day average cases',
        'Lag_1_Deaths': 'Previous deaths',
        'Lag_1_Recovered': 'Previous recovered cases'
    },
    'autism': {
        'age': 'Age',
        'gender': 'Gender',
        'ethnicity': 'Ethnicity',
        'jundice': 'Jaundice history',
        'austim': 'Family autism history',
        'contry_of_res': 'Country of residence',
        'used_app_before': 'Used screening app before',
        'relation': 'Relation to patient'
    },
    'creditdefault': {
        'LIMIT_BAL': 'Credit limit',
        'SEX': 'Sex',
        'EDUCATION': 'Education',
        'MARRIAGE': 'Marriage status',
        'AGE': 'Age'
    },
    'banknote': {
        'variance': 'Image variance',
        'skewness': 'Image skewness',
        'curtosis': 'Image kurtosis',
        'entropy': 'Image entropy'
    },
    'householdpower': {
        'DayOfWeek': 'Day of week',
        'Sub_metering_1': 'Kitchen sub-metering',
        'Sub_metering_2': 'Laundry sub-metering',
        'Sub_metering_3': 'Water heater / AC sub-metering'
    },
    'onlinenews': {
        'n_tokens_title': 'Title word count',
        'n_tokens_content': 'Article word count',
        'n_unique_tokens': 'Unique word ratio',
        'num_hrefs': 'Number of links',
        'num_self_hrefs': 'Number of self links',
        'num_imgs': 'Number of images',
        'num_videos': 'Number of videos',
        'average_token_length': 'Average word length',
        'num_keywords': 'Number of keywords',
        'self_reference_min_shares': 'Minimum self-reference shares',
        'self_reference_max_shares': 'Maximum self-reference shares',
        'self_reference_avg_sharess': 'Average self-reference shares',
        'global_subjectivity': 'Article subjectivity',
        'rate_positive_words': 'Positive word rate',
        'rate_negative_words': 'Negative word rate',
        'avg_positive_polarity': 'Average positive polarity',
        'max_positive_polarity': 'Maximum positive polarity',
        'avg_negative_polarity': 'Average negative polarity',
        'min_negative_polarity': 'Minimum negative polarity',
        'title_subjectivity': 'Title subjectivity',
        'title_sentiment_polarity': 'Title sentiment polarity',
        'abs_title_subjectivity': 'Absolute title subjectivity',
        'abs_title_sentiment_polarity': 'Absolute title sentiment polarity'
    }
}


SUGGESTION_RANGE_OVERRIDES = {
    'abalone': {
        'Age': {'min': 1, 'max': 29, 'mean': 10}
    },
    'bikesharing': {
        'season': {'min': 1, 'max': 4, 'mean': 2},
        'yr': {'min': 0, 'max': 1, 'mean': 1},
        'mnth': {'min': 1, 'max': 12, 'mean': 6},
        'hr': {'min': 0, 'max': 23, 'mean': 12},
        'holiday': {'min': 0, 'max': 1, 'mean': 0},
        'weekday': {'min': 0, 'max': 6, 'mean': 3},
        'workingday': {'min': 0, 'max': 1, 'mean': 1},
        'weathersit': {'min': 1, 'max': 4, 'mean': 1}
    },
    'tripadvisor': {
        'Category 1': {'min': 0, 'max': 4, 'mean': 2},
        'Category 2': {'min': 0, 'max': 4, 'mean': 2},
        'Category 3': {'min': 0, 'max': 4, 'mean': 2},
        'Category 4': {'min': 0, 'max': 4, 'mean': 2},
        'Category 5': {'min': 0, 'max': 4, 'mean': 2},
        'Category 6': {'min': 0, 'max': 4, 'mean': 2},
        'Category 7': {'min': 0, 'max': 4, 'mean': 2},
        'Category 8': {'min': 0, 'max': 4, 'mean': 2},
        'Category 9': {'min': 0, 'max': 4, 'mean': 2},
        'Category 10': {'min': 0, 'max': 4, 'mean': 2}
    }
}


class DatasetPrediction_BLL_Class:
    def __init__(self):
        self.dataset_repository = Dataset_Repository_Class()

    def get_datasets(self):
        return get_dataset_catalog()

    def get_dataset(self, dataset_key):
        return get_dataset_by_key(dataset_key)

    def get_metadata(self, dataset_key):
        dataset = self.get_dataset(dataset_key)
        return self.dataset_repository.get_metadata(dataset.metadata_file)

    def get_input_fields(self, dataset_key):
        dataset = self.get_dataset(dataset_key)
        metadata = self.get_metadata(dataset_key)

        if dataset.special_handler == 'abalone':
            return self.apply_field_labels(dataset.key, metadata, self.get_abalone_fields(metadata))

        if dataset.special_handler == 'covid':
            return self.apply_field_labels(dataset.key, metadata, self.get_covid_fields(metadata))

        fields = []
        for feature_name in self.get_feature_names(metadata):
            fields.append(self.create_field(feature_name, metadata, dataset.key))

        return self.apply_field_labels(dataset.key, metadata, fields)

    def get_abalone_fields(self, metadata):
        fields = [
            self.create_categorical_field(
                'Sex',
                ['Female', 'Infant', 'Male'],
                'Female',
                {'Female': 'Female', 'Infant': 'Infant', 'Male': 'Male'},
                'text'
            )
        ]
        for feature_name in self.get_feature_names(metadata):
            if feature_name in ('Sex_I', 'Sex_M'):
                continue

            fields.append(self.create_field(feature_name, metadata, 'abalone'))

        return fields

    def get_feature_names(self, metadata):
        return metadata.get('feature_names') or list(metadata.get('features', {}).keys())

    def apply_field_labels(self, dataset_key, metadata, fields):
        for field in fields:
            field['label'] = self.get_field_label(dataset_key, metadata, field['name'])

        return fields

    def get_field_label(self, dataset_key, metadata, field_name):
        category_map = metadata.get('category_map', {})
        if field_name in category_map:
            return f"{category_map[field_name]} rating"

        dataset_labels = FIELD_LABEL_OVERRIDES.get(dataset_key, {})
        if field_name in dataset_labels:
            return dataset_labels[field_name]

        if field_name.startswith('Wifi'):
            return f"WiFi signal {field_name.replace('Wifi', '')}"

        if field_name.startswith('stock_'):
            return f"{field_name.replace('stock_', '')} stock indicator"

        if field_name.startswith('A') and field_name.endswith('_Score') and field_name[1:-6].isdigit():
            question_number = field_name[1:-6]
            return f"Screening question A{question_number} score"

        if field_name.startswith('PAY_AMT'):
            month_number = field_name.replace('PAY_AMT', '')
            return f"Previous payment amount {month_number}"

        if field_name.startswith('BILL_AMT'):
            month_number = field_name.replace('BILL_AMT', '')
            return f"Bill statement amount {month_number}"

        if field_name.startswith('PAY_'):
            month_number = field_name.replace('PAY_', '')
            if month_number == '0':
                return 'Most recent repayment status'

            return f"Repayment status {month_number} months ago"

        if field_name.startswith('LDA_'):
            topic_number = int(field_name.replace('LDA_', '')) + 1
            return f"Topic strength {topic_number}"

        if field_name.startswith('kw_'):
            return self.humanize_keyword_label(field_name)

        if field_name.startswith('data_channel_is_'):
            channel = field_name.replace('data_channel_is_', '')
            channel_names = {
                'bus': 'Business',
                'socmed': 'Social media'
            }
            return f"{channel_names.get(channel, channel.title())} channel"

        if field_name.startswith('weekday_is_'):
            weekday = field_name.replace('weekday_is_', '').title()
            return f"Published on {weekday}"

        if field_name.startswith('self_reference_'):
            return self.humanize_label(field_name.replace('self_reference_', 'Self-reference '))

        return self.humanize_label(field_name)

    def humanize_keyword_label(self, field_name):
        replacements = {
            'kw_min_min': 'Minimum keyword shares',
            'kw_max_min': 'Maximum of minimum keyword shares',
            'kw_avg_min': 'Average minimum keyword shares',
            'kw_min_max': 'Minimum maximum keyword shares',
            'kw_max_max': 'Maximum keyword shares',
            'kw_avg_max': 'Average maximum keyword shares',
            'kw_min_avg': 'Minimum average keyword shares',
            'kw_max_avg': 'Maximum average keyword shares',
            'kw_avg_avg': 'Average keyword shares'
        }
        return replacements.get(field_name, self.humanize_label(field_name))

    def humanize_label(self, field_name):
        label = str(field_name).replace('_', ' ').replace('-', ' ')
        label = ' '.join(label.split())
        words = []
        acronyms = {'co2': 'CO2', 'pm2.5': 'PM2.5', 'sgpt': 'SGPT', 'sgot': 'SGOT'}

        for word in label.split(' '):
            lower_word = word.lower()
            if lower_word in acronyms:
                words.append(acronyms[lower_word])
            elif word.isupper() and len(word) <= 5:
                words.append(word)
            else:
                words.append(word.capitalize())

        return ' '.join(words)

    def create_field(self, feature_name, metadata, dataset_key=None):
        ordinal_maps = metadata.get('ordinal_maps', {})
        categorical_options = metadata.get('categorical_options', {})
        categorical_columns = set(metadata.get('categorical_cols', []))
        binary_columns = set(metadata.get('binary_cols', []))
        feature_info = metadata.get('features', {}).get(feature_name, {})
        feature_ranges = dict(metadata.get('feature_ranges', {}))
        feature_ranges.update(metadata.get('numeric_features', {}))
        feature_ranges.update(SUGGESTION_RANGE_OVERRIDES.get(dataset_key, {}))
        range_info = feature_ranges.get(feature_name) or feature_info or {}

        if feature_name in ordinal_maps:
            options = list(ordinal_maps[feature_name].keys())
            return self.create_categorical_field(feature_name, options, options[0], ordinal_maps[feature_name],
                                                 'number')

        if feature_name in categorical_options:
            options = [str(option) for option in categorical_options[feature_name]]
            return self.create_categorical_field(feature_name, options, options[0], None, 'text')

        if feature_name in binary_columns:
            return self.create_categorical_field(feature_name, ['0', '1'], '0', None, 'number')

        if feature_name.startswith('stock_'):
            return self.create_categorical_field(feature_name, ['0', '1'], '0', None, 'number')

        if feature_info.get('type') == 'categorical':
            options = [str(option) for option in feature_info.get('options', [])]
            default = options[0] if options else ''
            return self.create_categorical_field(feature_name, options, default, None, 'number')

        if feature_name in categorical_columns or feature_name in binary_columns:
            options = self.get_options_from_range(range_info)
            if options:
                return self.create_categorical_field(feature_name, options,
                                                     self.get_default_option(options, range_info),
                                                     None, 'number')

        if self.looks_like_binary_indicator(feature_name, range_info):
            return self.create_categorical_field(feature_name, ['0', '1'], '0', None, 'number')

        return self.create_numerical_field(feature_name, range_info)

    def create_categorical_field(self, name, options, default, value_map=None, cast='text'):
        return {
            'name': name,
            'type': 'categorical',
            'options': options,
            'default': str(default),
            'value_map': value_map or {},
            'cast': cast
        }

    def create_numerical_field(self, name, range_info):
        default, suggestion_source = self.get_suggested_number(range_info)
        suggested_value = self.format_default(default)
        return {
            'name': name,
            'type': 'numerical',
            'default': suggested_value,
            'placeholder': self.create_number_suggestion(suggestion_source, default, range_info),
            'min': range_info.get('min'),
            'max': range_info.get('max'),
            'cast': 'number'
        }

    def get_suggested_number(self, range_info):
        if 'mean' in range_info and range_info.get('mean') is not None:
            return range_info.get('mean'), 'Avg'

        if 'min' in range_info and 'max' in range_info:
            minimum = float(range_info.get('min'))
            maximum = float(range_info.get('max'))
            return (minimum + maximum) / 2, 'Mid'

        return range_info.get('min', 0), 'Try'

    def create_number_suggestion(self, suggestion_source, value, range_info):
        suggestion = f'{suggestion_source} {self.format_suggestion_number(value)}'
        if 'min' in range_info and 'max' in range_info:
            minimum = self.format_suggestion_number(range_info.get('min'))
            maximum = self.format_suggestion_number(range_info.get('max'))
            suggestion = f'{suggestion} | {minimum}-{maximum}'

        return suggestion

    def get_options_from_range(self, range_info):
        if 'min' not in range_info or 'max' not in range_info:
            return []

        minimum = range_info['min']
        maximum = range_info['max']
        if not self.is_integer_like(minimum) or not self.is_integer_like(maximum):
            return []

        minimum = int(minimum)
        maximum = int(maximum)
        if maximum - minimum > 40:
            return []

        return [str(value) for value in range(minimum, maximum + 1)]

    def get_default_option(self, options, range_info):
        mean_value = range_info.get('mean')
        if mean_value is None:
            return options[0]

        rounded = str(int(round(float(mean_value))))
        return rounded if rounded in options else options[0]

    def looks_like_binary_indicator(self, feature_name, range_info):
        if not range_info:
            return False

        minimum = range_info.get('min')
        maximum = range_info.get('max')
        if minimum != 0 and minimum != 0.0:
            return False

        if maximum != 1 and maximum != 1.0:
            return False

        name = feature_name.lower()
        markers = ('_is_', 'is_', 'stock_', 'sex_', 'channel_', 'region_')
        return any(marker in name or name.startswith(marker) for marker in markers)

    def get_covid_fields(self, metadata):
        first_country = metadata.get('countries', ['Australia'])[0]
        latest_state = metadata.get('latest_states', {}).get(first_country, {})
        last_cases = latest_state.get('last_7_cases', [0])
        rolling_cases = sum(last_cases) / max(1, len(last_cases))

        return [
            self.create_categorical_field('Country', metadata.get('countries', []), first_country, None, 'text'),
            self.create_numerical_field('DayOfYear', {'min': 1, 'max': 366, 'mean': 60}),
            self.create_numerical_field('Lag_1_Cases',
                                        {'min': 0, 'max': 1000000, 'mean': latest_state.get('cum_cases', 0)}),
            self.create_numerical_field('Roll_7_Cases', {'min': 0, 'max': 1000000, 'mean': rolling_cases}),
            self.create_numerical_field('Lag_1_Deaths',
                                        {'min': 0, 'max': 100000, 'mean': latest_state.get('last_death', 0)}),
            self.create_numerical_field('Lag_1_Recovered',
                                        {'min': 0, 'max': 1000000, 'mean': latest_state.get('last_recov', 0)})
        ]

    def predict(self, dataset_key, raw_values):
        dataset = self.get_dataset(dataset_key)
        metadata = self.get_metadata(dataset_key)

        if dataset.special_handler == 'beijing_pm25':
            values = self.convert_raw_values(dataset_key, raw_values)
            return self.predict_beijing_pm25(values)

        if dataset.special_handler == 'abalone':
            return self.predict_abalone(dataset, metadata, raw_values)

        if dataset.special_handler == 'heart':
            return self.predict_heart(dataset, metadata, raw_values)

        if dataset.special_handler == 'covid':
            return self.predict_covid(dataset, raw_values)

        values = self.convert_raw_values(dataset_key, raw_values)
        features = self.get_feature_names(metadata)

        if not dataset.model_files:
            return self.predict_fallback(dataset, values)

        results = []
        for index, model_file in enumerate(dataset.model_files):
            model = self.dataset_repository.get_model(model_file)
            prediction = self.predict_with_retry(model, features, values, raw_values, dataset_key)
            label = self.get_output_label(dataset, index)
            results.append((label, prediction))

        return self.format_prediction_result(dataset, metadata, results)

    def predict_with_retry(self, model, features, values, raw_values, dataset_key):
        try:
            return self.predict_single_model(model, features, values)
        except Exception:
            retry_values = self.convert_raw_values(dataset_key, raw_values, numeric_categorical_retry=True)
            return self.predict_single_model(model, features, retry_values)

    def predict_single_model(self, model, features, values):
        frame = pd.DataFrame([[values[feature] for feature in features]], columns=features)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            prediction = model.predict(frame)
        return self.flatten_prediction(prediction)

    def convert_raw_values(self, dataset_key, raw_values, numeric_categorical_retry=False):
        fields = self.get_input_fields(dataset_key)
        values = {}

        for field in fields:
            name = field['name']
            label = field.get('label', name)
            raw_value = raw_values.get(name, field.get('default', ''))
            value_map = field.get('value_map') or {}

            if raw_value in value_map:
                values[name] = value_map[raw_value]
                continue

            if field.get('cast') == 'number' or numeric_categorical_retry:
                values[name] = self.to_number(raw_value, label)
            else:
                values[name] = str(raw_value).strip()

        return values

    def predict_covid(self, dataset, raw_values):
        label_encoder = self.dataset_repository.get_model('26-Covid_LabelEncoder.pkl')
        model = self.dataset_repository.get_model(dataset.model_files[0])
        country = str(raw_values.get('Country', '')).strip()
        if not country:
            raise ValueError('Country is required.')

        country_encoded = int(label_encoder.transform([country])[0])
        features = ['Country_Encoded', 'DayOfYear', 'Lag_1_Cases', 'Roll_7_Cases', 'Lag_1_Deaths', 'Lag_1_Recovered']
        values = {
            'Country_Encoded': country_encoded,
            'DayOfYear': self.to_number(raw_values.get('DayOfYear'), 'DayOfYear'),
            'Lag_1_Cases': self.to_number(raw_values.get('Lag_1_Cases'), 'Lag_1_Cases'),
            'Roll_7_Cases': self.to_number(raw_values.get('Roll_7_Cases'), 'Roll_7_Cases'),
            'Lag_1_Deaths': self.to_number(raw_values.get('Lag_1_Deaths'), 'Lag_1_Deaths'),
            'Lag_1_Recovered': self.to_number(raw_values.get('Lag_1_Recovered'), 'Lag_1_Recovered')
        }
        prediction = self.predict_single_model(model, features, values)
        results = [(self.get_output_label(dataset, index), value) for index, value in enumerate(prediction)]
        return self.format_prediction_result(dataset, {}, results)

    def predict_beijing_pm25(self, values):
        pm25 = values.get('pm2.5', 0)
        dew_point = values.get('DEWP', 0)
        temperature = values.get('TEMP', 0)
        pressure = values.get('PRES', 1013)
        wind_speed = values.get('Iws', 0)
        snow_hours = values.get('Is', 0)
        rain_hours = values.get('Ir', 0)

        estimate = (
                0.72 * pm25
                + 0.85 * max(0, dew_point + 10)
                - 0.35 * temperature
                + 0.04 * abs(pressure - 1013)
                - 0.03 * wind_speed
                + 1.25 * snow_hours
                + 1.50 * rain_hours
        )
        estimate = max(0, estimate)

        return {
            'title': 'PM2.5 concentration forecast',
            'lines': [f'Estimated PM2.5 concentration: {self.format_number(estimate)}'],
            'raw_prediction': estimate
        }

    def predict_abalone(self, dataset, metadata, raw_values):
        values = self.convert_raw_values(dataset.key, raw_values)
        sex = str(raw_values.get('Sex', 'Female')).strip()
        values['Sex_I'] = 1.0 if sex == 'Infant' else 0.0
        values['Sex_M'] = 1.0 if sex == 'Male' else 0.0

        features = self.get_feature_names(metadata)
        model = self.dataset_repository.get_model(dataset.model_files[0])
        prediction = self.predict_single_model(model, features, values)
        return self.format_prediction_result(dataset, metadata, [('', prediction)])

    def predict_heart(self, dataset, metadata, raw_values):
        values = self.convert_raw_values(dataset.key, raw_values)
        model = self.dataset_repository.get_model(dataset.model_files[0])
        discretizer = self.dataset_repository.get_model('heart_kbd.joblib')
        columns_to_bin = metadata.get('columns_to_bin', [])
        remaining_columns = metadata.get('remaining_cols', [])

        binned_frame = pd.DataFrame(
            [[values[column] for column in columns_to_bin]],
            columns=columns_to_bin
        )
        binned_values = discretizer.transform(binned_frame)
        if hasattr(binned_values, 'toarray'):
            binned_values = binned_values.toarray()

        remaining_values = np.array([[values[column] for column in remaining_columns]])
        prepared_values = np.hstack([binned_values, remaining_values])
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            prediction = self.flatten_prediction(model.predict(prepared_values))
        return self.format_prediction_result(dataset, metadata, [('', prediction)])

    def predict_fallback(self, dataset, values):
        numeric_values = [value for value in values.values() if isinstance(value, (int, float))]
        estimate = sum(numeric_values) / max(1, len(numeric_values))
        return {
            'title': dataset.target,
            'lines': [f'Prediction: {self.format_number(estimate)}'],
            'raw_prediction': estimate
        }

    def format_prediction_result(self, dataset, metadata, results):
        lines = []
        raw_values = []

        for label, prediction in results:
            if isinstance(prediction, list):
                for index, value in enumerate(prediction):
                    output_label = self.get_output_label(dataset, index)
                    lines.append(f'{output_label}: {self.format_value(dataset, metadata, value)}')
                    raw_values.append(value)
                continue

            formatted_value = self.format_value(dataset, metadata, prediction)
            if label:
                lines.append(f'{label}: {formatted_value}')
            else:
                lines.append(f'Prediction: {formatted_value}')
            raw_values.append(prediction)

            if dataset.method == 'Clustering':
                description = metadata.get('cluster_descriptions', {}).get(str(int(prediction)))
                if description:
                    lines.append(f'Cluster pattern: {description}')

        return {
            'title': dataset.target,
            'lines': lines,
            'raw_prediction': raw_values
        }

    def format_value(self, dataset, metadata, value):
        if isinstance(value, np.generic):
            value = value.item()

        labels = dataset.result_labels
        if value in labels:
            return labels[value]

        string_value = str(value)
        if string_value in labels:
            return labels[string_value]

        target_mapping = metadata.get('target_mapping', {})
        if string_value in target_mapping:
            return target_mapping[string_value]

        if dataset.method == 'Clustering':
            try:
                return f'Cluster {int(value)}'
            except Exception:
                return f'Cluster {value}'

        if isinstance(value, (int, float)):
            return self.format_number(value)

        return string_value

    def get_output_label(self, dataset, index):
        if index < len(dataset.output_labels):
            return dataset.output_labels[index]

        if len(dataset.model_files) > 1:
            return f'Model {index + 1}'

        return ''

    def flatten_prediction(self, prediction):
        if isinstance(prediction, np.ndarray):
            prediction = prediction.tolist()

        if isinstance(prediction, list):
            if len(prediction) == 1:
                value = prediction[0]
                if isinstance(value, list):
                    return value
                return value
            return prediction

        return prediction

    def to_number(self, value, field_name):
        text = str(value).strip()
        if not text:
            raise ValueError(f'{field_name} is required.')

        try:
            number = float(text)
        except ValueError:
            raise ValueError(f'{field_name} must be a number.')

        if math.isfinite(number):
            return number

        raise ValueError(f'{field_name} must be a valid number.')

    def format_default(self, value):
        if value is None:
            return '0'

        if isinstance(value, str):
            return value

        if self.is_integer_like(value):
            return str(int(float(value)))

        return f'{float(value):.4f}'.rstrip('0').rstrip('.')

    def format_number(self, value):
        value = float(value)
        if abs(value) >= 1000:
            return f'{value:,.2f}'

        return f'{value:.4f}'.rstrip('0').rstrip('.')

    def format_suggestion_number(self, value):
        value = float(value)
        absolute_value = abs(value)

        if absolute_value >= 1_000_000:
            return f'{value / 1_000_000:.2f}M'.rstrip('0').rstrip('.')

        if absolute_value >= 1_000:
            return f'{value / 1_000:.2f}k'.rstrip('0').rstrip('.')

        if self.is_integer_like(value):
            return str(int(value))

        if absolute_value >= 10:
            return f'{value:.2f}'.rstrip('0').rstrip('.')

        return f'{value:.3f}'.rstrip('0').rstrip('.')

    def is_integer_like(self, value):
        try:
            return float(value).is_integer()
        except Exception:
            return False
