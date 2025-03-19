Shapes
Suggest Edits
Shapes are organized into libraries. Currently, JSON standard import supports shapes from the Standard Library, Shape Library, Container Library, Flowchart Library, and Lucidspark Library.

Common Properties
These properties are used on most or all shapes. Properties that are exclusive to a small set of shapes are defined near the shapes they're used on.

Property	Description	
id	ID
Identifier for a given shape (must be unique).	Required
type	String
The type of shape. An example of each shape is listed below.	Required
boundingBox	Bounding Box
The associated Bounding Box for the shape.	Required
style	Style
The style that will apply to the shape.	Optional
text	Text
Text to display on the shape.	Optional
actions	Array[Action]
An array of all actions linked to the shape.	Optional
customData	Array[Custom Data]
An array of all custom data connected to the shape.	Optional
linkedData	Array[Linked Data]
An array of all linked data connected to the shape.	Optional
opacity	Number
A whole number between 0 (transparent) and 100 (completely opaque) inclusive, representing the opacity of the shape. Defaults to 100 when not provided.	Optional
note	Text
Text to add as a note to the shape.	Optional
