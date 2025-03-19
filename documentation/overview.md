Overview
Suggest Edits
The Lucid Standard Import offers the ability to format JSON that can be used to import shapes, lines, groups, and more into a new Lucidchart or Lucidspark board.

The Standard Import can be accessed via Lucid's Import Document REST API endpoint, where the file and title are provided through the form data. If no title is specified, the document will be automatically assigned the name of the file.

The import request has an additional required product field where the user specifies the new document's product. The two currently-supported products are lucidchart and lucidspark.

The Lucid Standard Import is evolving and over time more features may be added. If there is something missing, submit and request feedback in our Community feedback space.

Explore below to see the wide variety of objects we support as well as details on the format of each.

📘
Due to the evolving nature of Lucid documents, an unchanged Standard Import file may produce varying results over time.

Example Request

curl 'https://api.lucid.co/documents'\
     --request 'POST'\
     --header 'Authorization: Bearer <OAuth 2.0 Access Token>'\
     --header 'Lucid-Api-Version: 1'\
     --form 'file=@<location>/import.lucid;type=x-application/vnd.lucid.standardImport'\
     --form 'title=New Document'\
     --form 'product=lucidchart'\
     --form 'parent=1234'
Getting Started
Lucid import files use a .lucid extension and are at a base level a ZIP file which must contain a file named at document.json.

Optional components:

CSV files in the /data folder (refer to the Data section)
Images in the /images folder (refer to the Images section)
Filesize limitations:

.lucid ZIP file contents - 50MB
/data folder contents - 1MB
/images folder contents - 50MB
document.json - 2MB
Example file structure

import.lucid
├── data
│   └── records.csv
├── images
│   └── logo.png
└── document.json
Example Import Files
Here are some .lucid ZIP file examples you can reference or use in your own projects.

Basic Example
Filesystem Diagram Example
Org Chart Diagram Example
Flow Diagram Example
Network Diagram Example
Vangogh Art Example
Each link directs you to a folder in GitHub that contains a .lucid ZIP file, a folder containing the unzipped contents of the ZIP file, and a brief description of the example.

Example Import Usages
You can also find examples of how to use the Standard Import in the /standard-import folder in Lucid's repository of Sample Lucid REST Applications.

These examples solve some common use cases with the Standard Import. More information on how to use them "out-of-the-box" can be found in their respective README.md files.

BPMN Converter
Jira History Importer
Basic Document Format
The basic document format consists of a version tag, zero or more collections, and one or more pages, containing zero or more lines, shapes, groups, and/or layers.

All items within the document (pages, shapes, lines, layers, etc.) require a unique ID.

For information on the specific format of each JSON object, refer to each object's section of the documentation.

Property	Description	
version	Number
The specified version of the standard import to use.	Required
pages	Array[Pages]
An array of page objects that define what shapes, groups, lines, etc. will be present on the specified page. Note that a minimum of one page is required.	Required
documentSettings	Document Settings
Data with settings to apply to the whole document. Documents are created with default settings when this data is omitted.	Optional
collections	Array[Collections]
An array of collection objects to draw data from.	Optional
extensionBootstrapData	Bootstrap Data
Bootstrap data for a specific extension package.	Optional
Document Object

{
    "version": 1,
    "collections": [
        {
            "id": "network",
            "dataSource": "Network.csv"
        }
    ],
    "pages": [
        {
            "id": "page1",
            "title": "Main Plan",
            "shapes": [...],
            "lines": [...],
            "groups": [...],
            "layers": [...]
        }
    ],
    "documentSettings": {
        "units": "cm"
    },
    "extensionBootstrapData": {
        "packageId": "74672098-cf36-492c-b8e6-2c4233549cd3",
        "extensionName": "sheets-adapter",
        "minimumVersion": "1.4.0",
        "data": {
            "a": 1,
            "b": 2
        }
    }
}
Document Settings
This data is used to set the document settings upon creation.

Property	Description	
units	cm, in, pt, px
Units of measurement that the document will display. Options are centimeters, inches, points, or pixels respectively. Defaults to inches when omitted.	Optional
Document Settings Resource

{
    "units": "in"
}
Bootstrap Data
Bootstrap data can be attached to the created document to be consumed by a specific Extension Package. See Bootstrap Data for documents created via API for usage.

Property	Description
packageId	String
Id of the extension package which will consume this data
extensionName	String
Name of the editor extension which will consume this data
Note: this is the name field of an editor extension found in your manifest.json file.
minimumVersion	String
Minimum version of the extension package which will consume this data.
data	Map[String, String]
Data to provide to the extension package.
Data Resource

{
    "packageId": "74672098-cf36-492c-b8e6-2c4233549cd3",
    "extensionName": "sheets-adapter",
    "minimumVersion": "1.4.0",
    "data": {
      "a": 1,
      "b": 2
    }
}
Updated 6 months ago

