# Desktop Entry Creator

Desktop Entry Creator is a Python application that allows users to create .desktop entries for installed applications on Chrome OS. This application lets users search for application icons using SerpAPI, select an icon, and generate a .desktop entry for the application.

## Features

- Search for application icons using SerpAPI.
- Select and preview an icon for the application.
- Generate and save .desktop entries for installed applications.

## Requirements

- Python 3.x
- `requests` library
- `pillow` library
- `serpapi` library
- google-search-results library
- `tkinter` (comes pre-installed with Python)

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/desktop-entry-creator.git
    cd desktop-entry-creator
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries:**
    ```bash
    pip install requests pillow serpapi google-search-results
    ```

4. **Add your SerpAPI key to `config.py`:**
    ```python
    # config.py
    SERPAPI_API_KEY = "YOUR_SERPAPI_API_KEY"
    ```

5. **Run the application:**
    ```bash
    python chromeOSapplicationadder.py
    ```

## Usage

1. Enter the application name, command to execute, and an optional comment.
2. Click the "Search for Icon" button to search for application icons.
3. Select an icon from the displayed results.
4. Click the "Generate .desktop Entry" button to generate the entry.
5. Click the "Save" button to save the .desktop entry.

## Create Alias (Optional)

You can create an alias to run this script easily from the terminal:

1. Open your `.bashrc` file:
    ```bash
    nano ~/.bashrc
    ```

2. Add the following alias (replace `/path/to/your/project` with the actual path):
    ```bash
    alias myscript='source /path/to/your/project/venv/bin/activate && python /path/to/your/project/chromeOSapplicationadder.py && deactivate'
    ```

3. Save and close the file, then reload `.bashrc`:
    ```bash
    source ~/.bashrc
    ```

4. Now you can run the script using:
    ```bash
    myscript
    ```

## License

This project is licensed under the MIT License.
