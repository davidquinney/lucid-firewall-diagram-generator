Data
Suggest Edits
Example file structure

import.lucid
├── data
│   ├── sales-performance.csv
│   └── templates
│       └── email-flow.csv
└── document.json
To import a data set from Google Sheets, Excel, or CSV with your document, include the CSV export of the file in the data directory.

To reference it from the JSON, refer to Linked Data and Collections.

Data files are referenced without including directories. To use the file email-flow.csv shown in the example file structure, the collection data source would be defined as "dataSource": "email-flow.csv", not "dataSource": "templates/email-flow.csv".

🚧
Important: The data directory is not allowed to exceed 1MB.

Collections
Property	Description
id	ID
Identifier for a collection that linked data objects will reference.
dataSource	String
File reference.
Collection

{
  "id": "sales-performance",
  "dataSource": "sales-performance.csv"
}
Supported Media
Extension	Description
.txt	Text file
.csv	Comma-Separated Values
Example usage

...
    "collections": [
        {
            "id": "sales-performance",
            "dataSource": "sales-performance.csv"
        },
        {
            "id": "email-flow",
            "dataSource": "email-flow.csv"
        }
    ]
...
    "linkedData": [
        {
            "collectionId": "email-flow",
            "key": 1
        }
    ]
...