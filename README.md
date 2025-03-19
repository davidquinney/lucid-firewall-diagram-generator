# Lucid Firewall Diagram Generator

A Python tool that reads firewall rules from an Excel document and generates network diagrams in Lucid format.

> **Note:** The diagrams generated will need adjustment. The main purpose is to get all the elements in an editable Lucid document that can easily be modified in the future.

## Description

This tool generates Lucid diagrams from firewall rules stored in an Excel spreadsheet. It allows users to:

- Select a specific Software Type from the Excel data
- Generate a network diagram showing connections between sources and destinations
- Organize the diagram by Availability Zones (AZs)
- Package the diagram as a `.lucid` file for import into Lucid tools
- Optionally upload the diagram directly to Lucid via their API

## Features

- **Automated Diagram Creation**: Convert complex firewall rules into visual network diagrams
- **AZ-Based Layout**: Automatically organize network entities by Availability Zones
- **Selective Diagram Generation**: Create diagrams for specific software types or components
- **Lucid Integration**: Direct upload capability to Lucid with API key
- **Customizable Visualization**: Adjusts entity sizes and layouts based on content complexity

## Requirements

- Python 3.8+
- Required Python packages:
  - pandas
  - openpyxl
  - requests (for API integration)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/davidquinney/lucid-firewall-diagram-generator.git
   cd lucid-firewall-diagram-generator
   ```

2. Set up a virtual environment and install the required packages:
   ```bash
   # Create a virtual environment
   python3 -m venv venv

   # Activate the virtual environment
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Install the required packages
   pip install pandas openpyxl requests
   ```

## Usage

1. Prepare your Excel file following the format in the [Excel Template Guide](sample/EXCEL_TEMPLATE.md).

2. Place your Excel file in the `source data` directory.

3. Activate the virtual environment:
   ```bash
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

4. Run the tool:
   ```bash
   python main.py
   ```

5. Select your Excel file from the list of available files.

6. Select a Software Type from the menu.

7. The tool will generate a `.lucid` file in the `output` directory.

8. You will be prompted whether you want to upload the diagram to Lucid:
   - If yes, enter your Lucid API key when prompted
   - The diagram will be uploaded to Lucid and a URL will be provided

## Excel File Format

The Excel file must follow a specific format:

- Must contain a sheet named "External Ports"
- Required columns:
  - Software Type - The type of software/infrastructure for categorization
  - Source - The source entity of the network traffic
  - Ports - Port numbers (comma-separated or ranges with hyphens)
  - Transfer Protocol - The protocol used (TCP, UDP, TCP/UDP, ICMP)
  - Destination - The destination entity of the network traffic
  - Source AZ - Availability Zone for the source (used for diagram layout)
  - Destination AZ - Availability Zone for the destination (used for diagram layout)

For detailed instructions and examples, see the [Excel Template Guide](sample/EXCEL_TEMPLATE.md).

## Excel File Requirements

The Excel file must:
- Be placed in the `source data` directory
- Contain a sheet named "External Ports"
- Follow the column structure described in the [Excel Template Guide](sample/EXCEL_TEMPLATE.md)

A sample Excel file is included in the repository to help you get started with the correct format.

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

The generated `.lucid` file can only be imported into Lucid using the API. The tool handles this upload process automatically when you provide your API key.

## Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs and feature requests
2. Improve documentation
3. Add more sample templates for different use cases
4. Submit pull requests with bug fixes or new features

Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
