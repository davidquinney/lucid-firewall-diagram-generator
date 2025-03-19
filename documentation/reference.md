Reference
Suggest Edits
Types
Type	Example	Description
Boolean	true	An RFC7159 JSON boolean value.
String	"title"	An RFC7159 JSON string value.
Number	102 or1.02E2	An RFC7159 JSON number value.
Integer	18567	An integer value formatted as an RFC7159 JSON number value.
Decimal	123.45	A decimal value formatted as an RFC7159 JSON number value.
Color	#32a834	A hexadecimal RGB string representing a color. See Web Colors for implementation details.
DateTime	2020-06-26T16:29:37Z	The date formatted as an RFC3339 timestamp string in the UTC time zone.
Timestamp	1605732868411	Number of milliseconds since the Unix epoch (January 1, 1970 in the UTC timezone).
UUID	110808fd-4553-4316-bccf-4f25ff59a532	A universally unique identifier (UUID) in the canonical textual representation format.
URI	https\://lucid.app/lucidchart/328caaff-08d6-4461-bd52-bb2fbd556420/edit	A uniform resource identifier (URI) as defined in RFC3986.
Array	["in progress"] or [1, 2, 3]	An array of values of other primitive types.
Map	Map[String,String] or Map[String,Optional[String]]	A JSON object as defined in RFC7159.
ID	"block-1"	A string of one to thirty-six characters that are either alphanumeric or one of the following: -_.~
Actions
Actions allow a resource to execute an event when selected. The different types of actions are described below.

GoTo Document
Open another Lucid document.

Property	Description	
documentId	UUID
The Lucid document to open. Action will fail if the documentId does not exist or the user does not have access.	Required
pageId	ID
Page to open on the document. Actions will fail if the page is not valid.	Required
newWindow	Boolean
Open the document in the current window or a new window. The default behavior is to open the document in the same window.	Optional
gotoDocument Action

{
    "type": "gotoDocument",
    "documentId": "110808fd-4553-4316-bccf-4f25ff59a532",
    "pageId": "page1",
    "newWindow": true
}
GoTo Page
Switch to a different page on the current document.

Property	Description	
pageId	ID
Page to open on the current document. Actions will fail if the page is not valid.	Required
gotoPage Action

{
    "type": "gotoPage",
    "pageId": "page1"
}
Hide Layer
Hide one or more layers on the current document.

Property	Description	
layers	Array[ID]
Array of layer IDs to hide.	Required
hideLayer Action

{
    "type": "hideLayer",
    "layers": [
        "layer1",
        "layer2"
    ]
}
Show Layer
Show one or more layers on the current document.

Property	Description	
layers	Array[ID]
Array of layer IDs to show.	Required
showLayer Action

{
    "type": "showLayer",
    "layers": [
        "layer1",
        "layer2"
    ]
}
Toggle Layer
Toggle between hidden or shown for one or more layers on the current document.

Property	Description	
layers	Array[ID]
Array of layer IDs to toggle.	Required
toggleLayer Action

{
    "type": "toggleLayer",
    "layers": [
        "layer1",
        "layer2"
    ]
}
URL
Open a URL in the current window or a new window.

Property	Description	
url	String
The URL to open.	Required
newWindow	Boolean
Open the URL in the current window or a new window. The default behavior is to open the document in the same window.	Optional
url Action

{
    "type": "url",
    "url": "https://www.example.com",
    "newWindow": true
}
Bounding Box
The defined container on the canvas for an object.

Property	Description	
x	Decimal
Absolute x position on the document.	Required
y	Decimal
Absolute y position on the document.	Required
w	Decimal
Width of the bounding box.	Required
h	Decimal
Height of the bounding box.	Required
rotation	Decimal
Rotation of the bounding box in degrees. Rotation is clockwise and bounded between 0 and 360 degrees. Note that not all shapes are affected by rotation.	optional
Box Resource

{
    "x": 5,
    "y": 3,
    "w": 10,
    "h": 15,
    "rotation": 180
}
Data
Provide data to your document that can be referenced within pages and shapes.

Custom Data
Set of key-value pairs embedded within a shape.

Property	Description	
key	String
Name of the data key needed to access the data pair.	Required
value	String
Value to be returned when the key is requested.	Required
Custom Data

{
    "key": "KeyOne",
    "value": "TestOne"
}
Custom Page Data
Set of key-value pairs embedded within a page.

Property	Description	
key	String
Name of the data key needed to access the data pair.	Required
value	String
Value to be returned when the key is requested.	Required
global	Boolean
Add this pair to all shapes on the page. The default state is false.	optional
Custom Page Data

{
    "key": "KeyOne",
    "value": "TestOne",
    "global": true
}
Linked Data
Set of references to data provided in an external datasouce, usually a CSV file included with the provided .lucid standard import file.

Property	Description	
collectionId	ID
Collection source id. Refer to the Data section for more information.	Required
key	String
Value of key field defined by the collection source.	Required
Linked Data

{
    "collectionId": "CollectionOne",
    "key": "9"
}
Position
Position represents a location on the canvas. As x increases, the position moves to the right on the document canvas. As y increases, the position moves down the canvas.

Absolute Position
An exact location on the canvas.

Property	Description	
x	Decimal
Absolute x position on the document. As x increases, the position moves right on the canvas.	Required
y	Decimal
Absolute y position on the document. As y increases, the position moves down the canvas.	Required
Absolute Position Resource

{
    "x": 5.0,
    "y": 3.5
}
Relative Position
A position relative to the length or width of another line or shape. Expressed as a decimal percentage from 0 to 1. A value of 0 represents the start of the shape or line, with 1 representing the end. A value of 0.5 would be the middle. For a block, 0,0 represents the top-left corner and 1,1 represents the bottom-right.

Property	Description	
x	Decimal
Relative x position along the line or shape.	Required
y	Decimal
Absolute y position along the line or shape.	Required
Relative Position Resource

{
    "x": 0.25,
    "y": 0.75
}
Style
The combined background and border style of a shape.

Property	Description	
fill	Fill
Fill of the shape. The default fill is a solid white background.	optional
stroke	Stroke
Stroke of the line or shape border. The default stroke is a solid 1px black line.	optional
rounding	Integer
Rounding value for the shape border, equal to double the pixel value of the corner radius.	optional
Resource

{
    "fill": {
      "type": "color",
      "color": "#ffffff"
    },
    "stroke": {
      "color": "#6f2131",
      "width": 3,
      "style": "solid"
    },
    "rounding": 10
}
Fill
Defines a shape's background. Can be a color or image.

Property	Description	
type	String
Type of content to fill the shape with. The Standard Import accepts "color" or "image" (see fill types below).	Required
Color Fill
Fills the shape with a color.

Property	Description	
color	Color
Hexadecimal string representing a RGB or RGBA color value.	Required
Fill with Color

{
    "type": "color",
    "color": "#800080"
}
Image Fill
Fills the shape with an image. The image can be provided either within the images directory of the provided .lucid file (see Images), or as a url to an external image.

Property	Description	
ref	String
Refer to the Images section for how to reference images. Importing will fail if the file can not be found.	
url	URL
URL address pointing to an image. Importing will not check the validity of the image link.	
imageScale	Image Scale
Defines the way the image fills the shape. This field defaults to stretch if nothing is provided.	optional
Fill with Image Ref

{
    "type": "image",
    "ref": "image.png",
    "imageScale": "fit"
}
Fill with Image URL

{
    "type": "image",
    "url": "https://www.example.com/images/logo.png",
    "imageScale": "stretch"
}
Image Scale Types
Value	Description
fit	Resizes the image to fit within a specified container while maintaining its aspect ratio, ensuring the entire image is visible with possible empty space around it.
fill	Resizes the image to completely fill a specified container, possibly cropping parts of the image to maintain the container's aspect ratio, ensuring the container is entirely covered by the image.
stretch	Resizes the image to fill a specified container without maintaining the original aspect ratio, potentially causing distortion if the aspect ratios differ.
original	Displays the image at its original size without resizing, showing only a portion if the container is smaller than the image.
tile	Repeats the image to fill the entire container both horizontally and vertically, creating a tiled pattern suitable for textures or backgrounds.
Stroke
Define the look of a line or border. May affect other aspects of certain shapes.

Property	Description	
color	Color
Hexadecimal string representing a RGB color to fill the line or border. The color defaults to black.	optional
width	Integer
Width of the line or border in pixels. The width defaults to 1px.	optional
style	Stroke Style
Style of the line or border. The stroke style defaults to solid.	optional
Resource

{
    "color": "#ffffff",
    "width": 10,
    "style": "solid"
}
Stroke Style
Defines the look of a drawn line. Affects the border and other aspects of certain shapes.

Value	Description	Image
solid	A solid line.	Solid Stroke
dashed	A dashed line.	Dashed Stroke
dotted	A dotted line.	Dotted Stroke
Text
Text to display on the shape or line. Formatting of the text can be by provided via raw HTML.

If a font size is not provided, all shapes will default to using auto-scaling font size.

Property	Description	
text	String
Display text or Text and style formatting via the HTML style attribute.	Required
Resource - No formatting

{
    "text": "Shape title"
}
Text Style
Text can be formatted via provding an HTML Style string. Any HTML style attributes not listed will be ignored. Some shapes may have a different default for certain fields based on their typical usage.

Value	Default
color	black
font-family	Liberation Sans
font-size	10pt
font-style	normal
font-weight	normal
text-align	center
text-decoration	none
vertical-align	center
Resource - HTML Formatting

{
    "text": "<p style=\"font-size: 5pt;text-align: left;color: green\">A paragraph with HTML formatting.</p>"
}
Text Markup
HTML markup can be provided in text to further format customize its behavior:

Markup	Behavior
<br>	Force a line break in the contained text.
<b></b>	Apply bold to the contained text.
<strong></strong>	Apply bold to the contained text.
<i></i>	Apply italic to the contained text.
<em></em>	Apply italic to the contained text.
<s></s>	Apply strike-through to the contained text.
<strike></strike>	Apply strike-through to the contained text.
<u></u>	Apply underline to the contained text.
<a></a>	Create an href within the contained text.
<ol></ol>	Create an ordered-list within the contained text.
<ul></ul>	Create an unordered-list within the contained text.
<li></li>	Create a list-item within an ordered or un-unordered list within the contained text.
Resource - Ordered List via HTML Markup

{
    "text": "<ol><li><b>bold</b></li><li><a href=\"https://www.example.com\">visit example.com</a></li></ol>"
}
