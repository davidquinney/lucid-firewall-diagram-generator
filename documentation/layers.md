ayers
Suggest Edits
Layers are collections of items, such as shapes, lines, or groups. Layers cannot contain other layers. They are similar to Groups but are more versatile. Layers are used to organize and manage the visual hierarchy of elements within a diagram. You can assign shapes, lines, and groups to different layers and then manipulate the visibility and order of those layers.

Layer Format
Property	Description	
id	ID
Identifier for a given layer (must be unique).	Required
title	String
Title of the layer.	Required
items	Array[ID]
An array of IDs of all Shapes, Lines, and Groups in the layer.	Optional
note	Text
Text to add as a note to the layer.	Optional
customData	Array [Custom Data ]
An array of custom data in the layer. See Custom Data for a description of its purpose.	Optional
linkedData	Array [Linked Data ]
An array of linked data in the layer. See Linked Data for a description of its purpose.	Optional
Layer

{
  "id": "layer1",
  "title": "New Layer",
  "items": [ ... ],
  "note": "Test Note",
  "customData": [ ... ],
  "linkedData": [ ... ]
}