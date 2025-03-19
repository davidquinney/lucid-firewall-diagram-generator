I want to build a tool that can take a list of firewall rules from an excel document and send it to LucidChart via the API. 

This should be in Python, and will read from an excel document named
vscode/lucid-generator/source data/Firewall Template.xlsx

There is a sheet named “External Ports” on the excel document with the following columns

Software Type, Source, Ports, Transfer Protocol, Destination, Source AZ (Used for Diagram Generation), Destination AZ (Used for Diagram Generation)

When running the tool, it will provide a menu for the user to select the software type, and generate the diagram accordingly.

For Lucid to import the data, it must look as follows.

Lucid import files use a .lucid extension and are at a base level a ZIP file which must contain a file named at document.json.
Optional components:
•	CSV files in the /data folder (refer to the Data section)
•	Images in the /images folder (refer to the Images section)
Filesize limitations:
•	.lucid ZIP file contents - 50MB
•	/data folder contents - 1MB
•	/images folder contents - 50MB
•	document.json - 2MB
Example file structure
import.lucid
├── data
│   └── records.csv
├── images
│   └── logo.png
└── document.json
I have a sample diagram called vscode/lucid-generator/source data/sample diagram.svg

Under the vscode/lucid-generator/documentation there is documentation scraped from https://developer.lucid.co/docs/ which has the requirements for JSON etc.

There is also a sample folder named vscode/lucid-generator/sample which contains code samples.

Anything you do, can you please add to a Readme.md and ask me for any input without making assumptions.  Also create a readme.md with steps on how everything works, including what shape data etc you use
