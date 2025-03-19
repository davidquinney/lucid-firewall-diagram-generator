# Lucid Firewall Diagram Generator

A Python tool that reads firewall rules from an Excel document and generates network diagrams in Lucid format.

## Description

This tool generates Lucid diagrams from firewall rules stored in an Excel spreadsheet. It allows users to:

- Select a specific Software Type from the Excel data
- Generate a network diagram showing connections between sources and destinations
- Organize the diagram by Availability Zones (AZs)
- Package the diagram as a `.lucid` file for import into Lucid tools

## Requirements

- Python 3.8+
- Required Python packages:
  - pandas
  - openpyxl
  - zipfile

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Set up a virtual environment and install the required packages:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install the required packages
pip install pandas openpyxl
```

## Usage

1. Activate the virtual environment:
```bash
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

2. Run the tool:
```bash
python main.py
```

3. Select a Software Type from the menu
4. The tool will generate a `.lucid` file in the output directory
5. You will be prompted whether you want to upload the diagram to Lucid
   - If yes, enter your Lucid API key when prompted
   - The diagram will be uploaded to Lucid and a URL will be provided

## File Structure

- The Excel spreadsheet must have a sheet named "External Ports"
- Required columns:
  - Software Type
  - Source
  - Ports
  - Transfer Protocol
  - Destination  
  - Source AZ (Used for Diagram Generation)
  - Destination AZ (Used for Diagram Generation)

## Lucid API Integration

The tool includes a feature to upload diagrams directly to Lucid via their API.

To use this feature:
1. You'll need a valid Lucid API key with appropriate permissions
2. When prompted, enter your API key
3. The tool will attempt to upload the diagram and provide a URL if successful

> **Note:** The API upload feature may require specific API permissions or additional configuration. If you encounter errors such as "Failed to create document: No document ID returned", consider using the manual import method instead. The `.lucid` file is always saved locally regardless of API upload success.

## Structure of a .lucid File

A `.lucid` file is essentially a ZIP file that contains:
- `document.json` - The main file defining the diagram structure
- Optional folders for data (`/data`) and images (`/images`)

## Output

The tool will create a `.lucid` file in the project directory named after the selected Software Type.
