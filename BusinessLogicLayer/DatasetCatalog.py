from Model.DatasetModel import Dataset_Model_Class


def get_dataset_catalog():
    return [
        Dataset_Model_Class(
            1, 'abalone', 'Abalone Ring Count', 'Beginner', 'Environment',
            'Regression', 'Predicted ring count', 'abalone_metadata.json',
            ['abalone_rf.joblib'],
            special_handler='abalone'
        ),
        Dataset_Model_Class(
            2, 'userknowledge', 'Student Knowledge Level', 'Beginner', 'Education/Web',
            'Classification', 'Knowledge level category', 'userknowledge_metadata.json',
            ['userknowledge_rf.joblib']
        ),
        Dataset_Model_Class(
            3, 'realestate', 'Real Estate Price', 'Beginner', 'Real Estate',
            'Regression', 'House price per unit area', 'realestate_metadata.json',
            ['realestate_rf.joblib']
        ),
        Dataset_Model_Class(
            4, 'wireless', 'WiFi Room Location', 'Beginner', 'Mobile/Location',
            'Classification', 'Room location', 'wireless_metadata.json',
            ['wireless_knn.joblib'],
            result_labels={1: 'Room 1', 2: 'Room 2', 3: 'Room 3', 4: 'Room 4'}
        ),
        Dataset_Model_Class(
            5, 'carevaluation', 'Car Acceptability', 'Beginner', 'Automobile',
            'Classification', 'Car acceptability', 'carevaluation_metadata.json',
            ['carevaluation_rf.joblib'],
            result_labels={'unacc': 'Unacceptable', 'acc': 'Acceptable', 'good': 'Good', 'vgood': 'Very good'}
        ),
        Dataset_Model_Class(
            6, 'fertility', 'Fertility Diagnosis', 'Beginner', 'Healthcare/Life',
            'Classification', 'Fertility diagnosis result', 'fertility_metadata.json',
            ['fertility_svm.joblib'],
            result_labels={'N': 'Normal', 'O': 'Altered'}
        ),
        Dataset_Model_Class(
            7, 'bankruptcy', 'Bankruptcy Risk', 'Beginner', 'Finance/Banking',
            'Classification', 'Bankruptcy risk', 'bankruptcy_metadata.json',
            ['bankruptcy_rf.joblib'],
            result_labels={0: 'Non-bankrupt', 1: 'Bankrupt'}
        ),
        Dataset_Model_Class(
            8, 'autompg', 'Auto MPG', 'Intermediate', 'Automobiles',
            'Regression', 'Miles per gallon', 'autompg_metadata.json',
            ['autompg_rf.joblib']
        ),
        Dataset_Model_Class(
            9, 'heart', 'Heart Disease', 'Intermediate', 'Health Sciences',
            'Classification', 'Heart disease presence', 'heart_metadata.json',
            ['heart_rf.joblib'],
            result_labels={0: 'No heart disease', 1: 'Heart disease'},
            special_handler='heart'
        ),
        Dataset_Model_Class(
            10, 'dailydemand', 'Daily Demand Orders', 'Intermediate', 'Business',
            'Regression', 'Total demand orders', 'dailydemand_metadata.json',
            ['dailydemand_rf.joblib']
        ),
        Dataset_Model_Class(
            11, 'blood', 'Blood Donation', 'Intermediate', 'Healthcare/Nonprofit',
            'Classification', 'Blood donation outcome', 'blood_metadata.json',
            ['blood_rf.joblib'],
            result_labels={0: 'Did not donate', 1: 'Donated'}
        ),
        Dataset_Model_Class(
            12, 'beijing', 'Beijing PM2.5 Pollution', 'Intermediate', 'Environment',
            'Regression', 'PM2.5 concentration forecast', 'beijing_metadata.json',
            ['beijing_linear.joblib'],
            notes='Uses sklearn Linear Regression to forecast the next PM2.5 value from current pollution and weather inputs.'
        ),
        Dataset_Model_Class(
            13, 'echocardiogram', 'Heart Attack Survival', 'Intermediate', 'Healthcare',
            'Classification', 'One-year survival outcome', '13-Echocardiogram_metadata.json',
            ['13-Echocardiogram.pkl'],
            result_labels={0.0: 'Did not survive one year', 1.0: 'Survived at least one year'}
        ),
        Dataset_Model_Class(
            14, 'concrete', 'Concrete Strength', 'Intermediate', 'Civil Engineering',
            'Regression', 'Concrete compressive strength', '14-Concrete_metadata.json',
            ['14-Concrete.pkl']
        ),
        Dataset_Model_Class(
            15, 'liver', 'Liver Disorders', 'Intermediate', 'Healthcare',
            'Clustering', 'Liver profile cluster', '15-Liver_metadata.json',
            ['15-Liver_KMeans.pkl']
        ),
        Dataset_Model_Class(
            16, 'dowjones', 'Dow Jones Weekly Return', 'Intermediate', 'Business/Finance',
            'Regression', 'Weekly stock return estimate', '16-DowJones_metadata.json',
            ['16-DowJones.pkl']
        ),
        Dataset_Model_Class(
            17, 'energy', 'Energy Efficiency', 'Intermediate', 'Energy',
            'Regression', 'Heating and cooling load', '17-Energy_metadata.json',
            ['17-Energy_Y1.pkl', '17-Energy_Y2.pkl'],
            output_labels=['Heating load', 'Cooling load']
        ),
        Dataset_Model_Class(
            18, 'glass', 'Glass Type', 'Intermediate', 'Materials',
            'Classification', 'Glass type', '18-Glass_metadata.json',
            ['18-Glass.pkl']
        ),
        Dataset_Model_Class(
            19, 'hepatitis', 'Hepatitis Survival', 'Intermediate', 'Healthcare',
            'Classification', 'Patient survival class', '19-Hepatitis_metadata.json',
            ['19-Hepatitis.pkl'],
            result_labels={0: 'Did not survive', 1: 'Survived'}
        ),
        Dataset_Model_Class(
            20, 'wholesale', 'Wholesale Spending', 'Intermediate', 'Business/Retail',
            'Clustering', 'Wholesale customer segment', '20-Wholesale_metadata.json',
            ['20-Wholesale_KMeans.pkl']
        ),
        Dataset_Model_Class(
            21, 'tripadvisor', 'TripAdvisor Review Groups', 'Intermediate', 'Web',
            'Clustering', 'Traveler review cluster', '21-TripAdvisor_metadata.json',
            ['21-TripAdvisor.pkl']
        ),
        Dataset_Model_Class(
            22, 'istanbulstock', 'Istanbul Stock Exchange', 'Intermediate', 'Business/Finance',
            'Regression', 'ISE 100 return', '22-IstanbulStock_metadata.json',
            ['22-IstanbulStock.pkl']
        ),
        Dataset_Model_Class(
            23, 'bikesharing', 'Bike Sharing Demand', 'Intermediate', 'Transportation',
            'Regression', 'Bike rental count', '23-BikeSharing_metadata.json',
            ['23-BikeSharing.pkl']
        ),
        Dataset_Model_Class(
            24, 'occupancy', 'Room Occupancy', 'Intermediate', 'Energy/Buildings',
            'Classification', 'Room occupancy', '25-Occupancy_metadata.json',
            ['25-Occupancy.pkl'],
            result_labels={0: 'Not occupied', 1: 'Occupied'}
        ),
        Dataset_Model_Class(
            25, 'censusincome', 'Census Income', 'Intermediate', 'Social/Government',
            'Classification', 'Income class', '25-CensusIncome_metadata.json',
            ['25-CensusIncome.pkl'],
            result_labels={0: '<= $50K', 1: '> $50K'}
        ),
        Dataset_Model_Class(
            26, 'covid', 'COVID-19 Cases', 'Intermediate', 'Health Sciences',
            'Regression', 'COVID-19 forecast', '26-Covid_Metadata.json',
            ['26-Covid_Model.pkl'],
            output_labels=['Confirmed cases', 'Deaths', 'Recovered'],
            special_handler='covid'
        ),
        Dataset_Model_Class(
            27, 'autism', 'Autism Spectrum Disorder', 'Advanced', 'Healthcare/Social Sciences',
            'Classification', 'ASD screening class', '27-Autism_metadata.json',
            ['27-Autism.pkl'],
            result_labels={0: 'No ASD indication', 1: 'ASD indication'}
        ),
        Dataset_Model_Class(
            28, 'creditdefault', 'Credit Default', 'Advanced', 'Business/Finance',
            'Classification', 'Credit default outcome', '28-CreditDefault_metadata.json',
            ['28-CreditDefault.pkl'],
            result_labels={0: 'No default', 1: 'Default'}
        ),
        Dataset_Model_Class(
            29, 'banknote', 'Banknote Authentication', 'Advanced', 'Banking/Finance',
            'Classification', 'Banknote authenticity', '29-Banknote_metadata.json',
            ['29-Banknote.pkl'],
            result_labels={0: 'Genuine', 1: 'Forged'}
        ),
        Dataset_Model_Class(
            30, 'householdpower', 'Household Power', 'Advanced', 'Electricity',
            'Regression', 'Global active power estimate', '30-HouseholdPower_metadata.json',
            ['30-HouseholdPower.pkl']
        ),
        Dataset_Model_Class(
            31, 'onlinenews', 'Online News Shares', 'Advanced', 'Business/Web',
            'Regression', 'Predicted share count', '31-OnlineNews_metadata.json',
            ['31-OnlineNews.pkl']
        )
    ]


def get_dataset_by_key(dataset_key):
    for dataset in get_dataset_catalog():
        if dataset.key == dataset_key:
            return dataset

    raise ValueError(f'Unknown dataset: {dataset_key}')
