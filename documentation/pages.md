Pages
Suggest Edits
A Page object represents all of the shapes, lines, groups, and layers contained on a single page of a given Lucid document.

Page Format
The format to define a page in JSON is shown below:

Property	Description	
id	ID
Identifier for a given page (must be unique).	Required
title	String
Page display title.	Required
settings	Page Settings
Data with settings to apply to the page. Pages are created with default settings when this data is omitted.	Optional
shapes	Array[Shape]
An array of all shapes in the page.	Optional
dataBackedShapes	Array[Data Backed Shape]
An array of all shapes in the page.	Optional
lines	Array[Line]
An array of all lines in the page.	Optional
groups	Array[Group]
An array of all groups in the page.	Optional
layers	Array[Layer]
An array of all layers in the page.	Optional
customData	Array[Custom Page Data]
See Custom Page Data for a description of it's purpose.	Optional
Page

{
    "id": "page1",
    "title": "Main Plan",
    "settings": {
        "size": {
            "type": "letter",
            "format": "landscape"
        }
    },
    "shapes": [ ... ],
    "lines": [ ... ],
    "groups": [ ... ],
    "layers": [ ... ],
    "customData": [ ... ]
}
Page Settings
This data is used to set the page settings upon creation. Each field is optional and falls back on its default value when omitted.

Property	Description	
fillColor	Color
Determines the background color of the canvas. When omitted, the fill color defaults to #f2f3f5 for Lucidspark documents, and white for Lucidchart documents.	Optional
infiniteCanvas	Boolean
Determines if the canvas extends infinitely. When omitted, Lucidspark documents default to true, and Lucidchart documents default to false.	Optional
autoTiling	Boolean
Determines if the canvas extends when an item is moved outside the boundaries of the page. When omitted, defaults to true. When infiniteCanvas is true, this setting will not affect the page.	Optional
size	Page Size
Sets the size of the page. When infiniteCanvas is true, this setting will not affect the page. When omitted, defaults to a standard letter size with a portrait format.	Optional
Page Settings

{
    "fillColor": "#333",
    "infiniteCanvas": true,
    "autoTiling": false,
    "size": {
        "type": "custom",
        "w": 1000,
        "h": 1500
    }
}
Page Size
This data is used to set the size of the page. Page sizes can either be provided as standard sizes or as a custom size with specified height and width.

Standard Page Sizes
Property	Description	
type	letter, legal, executive, a3, a4, a5, tabloid, folio, statement
Sets the dimensions of the page. All options are standard sizes that can be found on Wikipedia's page on paper sizes.	Required
format	portrait, landscape
Determines the orientation of the page. A value of portrait sets the height to be taller and the width to be shorter, and landscape behaves inversely. When omitted, this field defaults to portrait.	Optional
Page Settings

{
    "type": "executive",
    "format": "landscape"
}
Custom Page Size
Property	Description	
type	custom
This field specifies that the page size is custom, rather than a standard size.	Required
w	Number
Sets the width of the page in pixels. This value is restricted to between 1 and 20,000 inclusive.	Required
h	Number
Sets the height of the page in pixels. This value is restricted to between 1 and 20,000 inclusive.	Required
Page Settings

{
    "type": "custom",
    "w": 1000,
    "h": 1500
}