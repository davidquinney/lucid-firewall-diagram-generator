# Lucid Firewall Diagram Generator - Project Plan

## Project Overview

The tool will:
1. Read firewall rules from the Excel document
2. Present a menu for the user to select a Software Type
3. Filter the data based on the selected Software Type
4. Generate a Lucid diagram showing the connections between sources and destinations
5. Package the diagram as a .lucid file (which is a ZIP file containing document.json)

## Technical Approach

### 1. Data Extraction
- Use pandas to read the "External Ports" sheet from the Excel file
- Parse the columns: Software Type, Source, Ports, Transfer Protocol, Destination, Source AZ, Destination AZ

### 2. User Interface
- Create a simple command-line interface with numbered options
- Display a list of available Software Types from the Excel data
- Allow the user to select one Software Type at a time

### 3. Data Processing
- Filter the Excel data based on the selected Software Type
- Group the data by Source AZ and Destination AZ
- Create a mapping of unique sources and destinations

### 4. Diagram Generation
- Create a document.json structure following the Lucid format
- Use rectangles for source and destination boxes
- Organize the diagram by Availability Zones (AZs)
- Create lines connecting sources to destinations
- Add port and protocol information to the lines
- Position elements in a logical layout

### 5. Output Creation
- Package the document.json into a .lucid ZIP file
- Save the output to the specified location

## Project Structure

```
vscode/lucid-generator/
├── main.py                  # Main entry point
├── excel_reader.py          # Excel file reading functionality
├── lucid_generator.py       # Lucid diagram generation logic
├── utils.py                 # Utility functions
└── README.md                # Documentation
```

## Implementation Details

### Excel Reader
```python
def read_excel_data(file_path):
    """Read the Excel file and return the data as a pandas DataFrame"""
    df = pd.read_excel(file_path, sheet_name="External Ports")
    return df

def get_software_types(df):
    """Extract unique software types from the DataFrame"""
    return df["Software Type"].unique().tolist()

def filter_by_software_type(df, software_type):
    """Filter the DataFrame by the selected software type"""
    return df[df["Software Type"] == software_type]
```

### Lucid Generator
```python
def create_document_json(filtered_data):
    """Create the document.json structure for the Lucid diagram"""
    # Group data by AZ
    # Create shapes for sources and destinations
    # Create lines for connections
    # Return the document.json structure
    
def create_lucid_file(document_json, output_path):
    """Create a .lucid file (ZIP) containing the document.json"""
    # Create a temporary directory
    # Write document.json to the directory
    # Create a ZIP file
    # Rename to .lucid
    # Return the path to the .lucid file
```

### Main Program Flow
```python
def main():
    # Load Excel data
    df = read_excel_data(EXCEL_FILE_PATH)
    
    # Get unique software types
    software_types = get_software_types(df)
    
    # Display menu
    print("Select a Software Type:")
    for i, software_type in enumerate(software_types, 1):
        print(f"{i}. {software_type}")
    
    # Get user selection
    selection = int(input("Enter your choice: ")) - 1
    selected_software_type = software_types[selection]
    
    # Filter data
    filtered_data = filter_by_software_type(df, selected_software_type)
    
    # Generate Lucid diagram
    document_json = create_document_json(filtered_data)
    
    # Create .lucid file
    output_path = f"vscode/lucid-generator/{selected_software_type.replace(' ', '_')}.lucid"
    lucid_file_path = create_lucid_file(document_json, output_path)
    
    print(f"Lucid diagram created: {lucid_file_path}")
```

## Sample document.json Structure

Based on the Lucid documentation, here's a simplified example of what the document.json structure would look like for our firewall diagram:

```json
{
  "version": 1,
  "pages": [
    {
      "id": "page1",
      "title": "Firewall Rules - [Software Type]",
      "width": 1500,
      "height": 1000,
      "shapes": [
        {
          "id": "az1_container",
          "type": "rectangle",
          "boundingBox": {
            "x": 100,
            "y": 100,
            "width": 500,
            "height": 400
          },
          "style": {
            "fillColor": "#d7d7d7",
            "borderColor": "#000000",
            "borderWidth": 1
          },
          "text": "AZ1"
        },
        {
          "id": "az2_container",
          "type": "rectangle",
          "boundingBox": {
            "x": 700,
            "y": 100,
            "width": 500,
            "height": 400
          },
          "style": {
            "fillColor": "#d7d7d7",
            "borderColor": "#000000",
            "borderWidth": 1
          },
          "text": "AZ2"
        },
        {
          "id": "source1",
          "type": "rectangle",
          "boundingBox": {
            "x": 150,
            "y": 150,
            "width": 200,
            "height": 100
          },
          "style": {
            "fillColor": "#ffffff",
            "borderColor": "#131313",
            "borderWidth": 1
          },
          "text": "Nutanix CVM"
        },
        {
          "id": "destination1",
          "type": "rectangle",
          "boundingBox": {
            "x": 750,
            "y": 150,
            "width": 200,
            "height": 100
          },
          "style": {
            "fillColor": "#ffffff",
            "borderColor": "#131313",
            "borderWidth": 1
          },
          "text": "release-api.nutanix.com"
        }
      ],
      "lines": [
        {
          "id": "line1",
          "lineType": "straight",
          "endpoint1": {
            "type": "shapeEndpoint",
            "style": "none",
            "shapeId": "source1",
            "position": { "x": 1, "y": 0.5 }
          },
          "endpoint2": {
            "type": "shapeEndpoint",
            "style": "arrow",
            "shapeId": "destination1",
            "position": { "x": 0, "y": 0.5 }
          },
          "stroke": {
            "color": "#131313",
            "width": 1,
            "style": "solid"
          },
          "text": [
            {
              "text": "TCP 80, 443",
              "position": 0.5,
              "side": "middle"
            }
          ]
        }
      ]
    }
  ]
}
```

## AZ Container Organization

The shapes (source and destination rectangles) will be positioned inside their respective AZ containers, just like in the sample diagram provided.

In the document.json structure, we'll ensure that:

1. Each AZ will be represented as a larger rectangle container
2. Source and destination shapes will be positioned inside their respective AZ containers based on the "Source AZ" and "Destination AZ" values from the Excel data
3. The lines connecting sources to destinations will cross between AZs when needed

For example, if we have a rule where:
- Source: "Nutanix CVM" with Source AZ: "Local AZ"
- Destination: "release-api.nutanix.com" with Destination AZ: "Internet Services"

Then:
- The "Nutanix CVM" rectangle will be positioned inside the "Local AZ" container
- The "release-api.nutanix.com" rectangle will be positioned inside the "Internet Services" container
- A line will connect these two rectangles, crossing between the AZ containers

This approach will make the diagram visually clear, showing which components belong to which AZs and how they communicate across AZ boundaries.
