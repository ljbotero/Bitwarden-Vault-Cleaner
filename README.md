# Bitwarden-Vault-Cleaner

The Bitwarden Utility is a Python script for cleaning and optimizing your Bitwarden password manager export. It removes duplicate entries, checks the validity of URLs, and exports cleaned data to new JSON files.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Features

The Bitwarden Vault Cleaner provides the following features to help you clean and optimize your Bitwarden password manager export:
- **Duplicate Entry Removal**: Automatically identifies and removes duplicate entries based on URI, username, and password, ensuring a clean and efficient export.
- **URL Validation**: Checks the validity of URLs within your Bitwarden entries by pinging the base site. If a URL is unreachable, it is removed from the entry's URIs list.
- **Optimized Export**: Exports a cleaned and optimized Bitwarden export JSON file with duplicate entries and invalid URLs removed.
- **Real-time Output**: Progress is displayed in real-time, showing which items are being processed and the reason for deletion (if any). 
- **Customizable Configuration**: Easily configure the utility by adjusting settings such as the input file name, output file names, and URL timeout duration.
- **Detailed Deletion Report**: Generates a separate JSON file containing information about deleted items, including the reason for deletion, for your reference.
- **Skip "https://" or "http://" URIs**: Items with a single "https://" or "http://" URI are retained during processing and are not deleted.
- **User-friendly**: Designed to be easy to use with clear instructions and customizable settings to suit your preferences.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system.
- A Bitwarden password manager export JSON file.

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone Bitwarden-Vault-Cleaner
   ```

2. Navigate to the project directory:

   ```bash
   cd Bitwarden-Vault-Cleaner
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Bitwarden Utility, follow these steps:

1. Place your Bitwarden export JSON file in the project directory.

2. Open the `bitwardenCleaner.py` script and configure the file names and other settings according to your preferences.

3. Run the script:

   ```bash
   python bitwardenCleaner.py
   ```

4. The script will process the input file and generate two output files: one with cleaned data and another with deleted items.

## Configuration

You can customize the behavior of the utility by modifying the following settings in the `bitwarden_cleaner.py` script:

- `input_file_name`: The name of your Bitwarden export JSON file.
- `output_file_name`: The name of the output JSON file containing cleaned data.
- `deleted_file_name`: The name of the output JSON file containing deleted items.
- `timeout_seconds`: The maximum time (in seconds) the utility will wait for a response when pinging URLs.
- Other settings related to URL validation and handling duplicates.

## Output

The Bitwarden-Vault-Cleaner produces two output files:

- `output_file_name`: Contains cleaned and optimized data with duplicate entries removed, and invalid URLs removed from URIs.
- `deleted_file_name`: Contains information about the items that were deleted during the cleaning process, including the reason for deletion.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License 
```
