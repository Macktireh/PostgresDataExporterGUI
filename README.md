# PostgresDataExporterGUI

PostgresDataExporterGUI is a Python application that allows you to export data from a PostgreSQL database to a CSV file with the option to include images. The application provides a graphical user interface (GUI) for ease of use.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)


## Overview

The application consists of multiple modules organized as follows:

- **service.exception.py:** Defines custom exceptions related to database connections, queries, exporting CSV, and saving images.

- **service.api.py:** Contains classes for handling PostgreSQL connections and processing data from the database. It includes methods for fetching data, exporting data to CSV, and saving images.

- **components.formConnectionDB:** Defines a form for collecting database connection information using custom tkinter components.

- **components.imageIndexForm.py:** Provides a form for specifying whether the dataset includes image columns and the index of the image column.

- **components.input.py:** Implements a custom input component for the GUI.

- **components.progressBar.py:** Defines a progress bar component for visualizing the export progress.

- **components.textarea.py:** Implements a text area component for multiline text input.

- **App:** The main application class that orchestrates the entire GUI. It includes functionality for choosing an export directory, specifying a SQL query, and exporting data to a CSV file.


## Requirements
- Python 3.10
- Dependencies listed in `requirements.txt`


## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Macktireh/PostgresDataExporterGUI.git
    ```
    ```bash
    cd PostgresDataExporterGUI
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    ```

    *for MacOS or Linux*
    ```bash
    source .venv/bin/activate
    ```

    *for Windows*
    ```bash
    .\venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Usage
1. Run the application:
    ```bash
    python app.py
    ```

2. The GUI will appear, allowing you to input database connection details, a SQL query, and specify options for data export.

3. Click on the "Choisir un dossier" button to choose the export directory.

4. Click on the "Exporter" button to execute the data export process.


## License

This project is licensed under the [MIT License](LICENSE).