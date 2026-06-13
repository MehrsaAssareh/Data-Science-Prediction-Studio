# Data Science Prediction Studio

Data Science Prediction Studio is a Python desktop application for a data science final project. The app contains 31 dataset pages based on the Data Science Dojo dataset collection. Each page lets the user enter values, view helpful input suggestions, and receive a prediction or grouping result from a trained machine learning model.

Dataset source: [Data Science Dojo - Datasets for Data Science Skills](https://datasciencedojo.com/blog/datasets-data-science-skills/)

## Project Goal

The goal of this project is to show how different machine learning tasks can be applied to real datasets. Each dataset uses the most suitable prediction approach for its target:

- Classification: used when the result is a category or class label.
- Regression: used when the result is a numeric value.
- Clustering: used when the app groups similar records without a direct class label.

## Main Features

- Main dashboard with 31 dataset buttons.
- Separate prediction page for every dataset.
- Dataset-specific labels, example values, and user-friendly suggestions.
- Larger page images on the right side of each dataset form.
- App icon in the window, taskbar, and main page header.
- Trained models are loaded from saved files, so the app does not retrain models at startup.
- A packaged Windows executable can be built locally in the `dist` folder.

## Prediction Summary

- Classification pages: 15
- Regression pages: 13
- Clustering pages: 3
- Total dataset pages: 31

## Dataset Pages

| # | Dataset Page | Method | Prediction Target |
|---|---|---|---|
| 1 | Abalone Ring Count | Regression | Predicted ring count |
| 2 | Student Knowledge Level | Classification | Knowledge level category |
| 3 | Real Estate Price | Regression | House price per unit area |
| 4 | WiFi Room Location | Classification | Room location |
| 5 | Car Acceptability | Classification | Car acceptability |
| 6 | Fertility Diagnosis | Classification | Fertility diagnosis result |
| 7 | Bankruptcy Risk | Classification | Bankruptcy risk |
| 8 | Auto MPG | Regression | Miles per gallon |
| 9 | Heart Disease | Classification | Heart disease presence |
| 10 | Daily Demand Orders | Regression | Total demand orders |
| 11 | Blood Donation | Classification | Blood donation outcome |
| 12 | Beijing PM2.5 Pollution | Regression | PM2.5 concentration forecast |
| 13 | Heart Attack Survival | Classification | One-year survival outcome |
| 14 | Concrete Strength | Regression | Concrete compressive strength |
| 15 | Liver Disorders | Clustering | Liver profile cluster |
| 16 | Dow Jones Weekly Return | Regression | Weekly stock return estimate |
| 17 | Energy Efficiency | Regression | Heating and cooling load |
| 18 | Glass Type | Classification | Glass type |
| 19 | Hepatitis Survival | Classification | Patient survival class |
| 20 | Wholesale Spending | Clustering | Wholesale customer segment |
| 21 | TripAdvisor Review Groups | Clustering | Traveler review cluster |
| 22 | Istanbul Stock Exchange | Regression | ISE 100 return |
| 23 | Bike Sharing Demand | Regression | Bike rental count |
| 24 | Room Occupancy | Classification | Room occupancy |
| 25 | Census Income | Classification | Income class |
| 26 | COVID-19 Cases | Regression | COVID-19 forecast |
| 27 | Autism Spectrum Disorder | Classification | ASD screening class |
| 28 | Credit Default | Classification | Credit default outcome |
| 29 | Banknote Authentication | Classification | Banknote authenticity |
| 30 | Household Power | Regression | Global active power estimate |
| 31 | Online News Shares | Regression | Predicted share count |

## Tech Stack

- Python
- Tkinter
- ttkbootstrap
- pandas
- numpy
- scikit-learn
- joblib
- matplotlib
- Pillow

## Project Structure

```text
Data Science Prediction Studio
|
|-- Main.py
|-- requirements.txt
|-- README.md
|
|-- BusinessLogicLayer
|   |-- DatasetCatalog.py
|   |-- DatasetPrediction_BLL.py
|
|-- DataAccessLayer
|   |-- data/model loading logic
|
|-- Model
|   |-- dataset model classes
|
|-- UserInterfaceLayer
|   |-- MainView.py
|   |-- MainModule.py
|   |-- DatasetPredictionModule.py
|   |-- Window.py
|
|-- Datasets
|   |-- Models
|       |-- trained model files
|       |-- dataset metadata files
|
|-- assets
|   |-- icons
|   |-- button_images
|   |-- page_images
|
|-- dist
|   |-- DataSciencePredictionStudio
|       |-- DataSciencePredictionStudio.exe
|       |-- _internal
```

The `dist` folder is ignored by Git because it contains large generated build output. If the executable needs to be shared through GitHub, upload the `dist\DataSciencePredictionStudio` folder as a GitHub Release asset instead of committing it directly to the repository.

## How to Run From Python

Install the required libraries:

```powershell
cd "Data Science Prediction Studio"
python -m pip install -r requirements.txt
```

Run the app:

```powershell
python Main.py
```

## How to Run the Windows EXE

Download the Windows package from the GitHub release:

[Download DataSciencePredictionStudio-Windows.zip](https://github.com/MehrsaAssareh/Data-Science-Prediction-Studio/releases/download/v1.0.0/DataSciencePredictionStudio-Windows.zip)

After downloading:

1. Right-click `DataSciencePredictionStudio-Windows.zip`.
2. Choose `Extract All`.
3. Open the extracted `DataSciencePredictionStudio` folder.
4. Run `DataSciencePredictionStudio.exe`.

Important: do not run the exe directly from inside the zip file. Extract the zip first.

Also, keep `DataSciencePredictionStudio.exe` in the same folder as `_internal`. The executable uses the `_internal` folder beside it for Python libraries, trained models, datasets, and image assets.

If the executable has been built locally instead of downloaded from GitHub, open this file:

```text
dist\DataSciencePredictionStudio\DataSciencePredictionStudio.exe
```

## How to Use the App

1. Open the app.
2. Choose one of the 31 dataset buttons from the main page.
3. Enter values in the form fields.
4. Use the shown examples and suggestions to choose reasonable values.
5. Click the prediction button.
6. Read the prediction, class, cluster, or forecast result.
7. Use the back button to return to the main page and choose another dataset.

## Notes

- The app uses saved model files from `Datasets/Models`.
- Metadata files define the form fields, labels, defaults, and suggestion text for each dataset.
- Button images are stored in `assets/button_images`.
- Page images are stored in `assets/page_images`.
- App icons are stored in `assets/icons`.
- The interface is designed with fixed-size pages and compact forms so users can see labels and entries clearly.
