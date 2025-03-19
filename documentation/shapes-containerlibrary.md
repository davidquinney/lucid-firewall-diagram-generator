Container Library
Suggest Edits
Brace Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Braces Container

Brace Container Block

{
    "id": "shape19",
    "type": "braceContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Bracket Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Bracket Container

Bracket Container Block

{
    "id": "shape20",
    "type": "bracketContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Circle Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Circle Container

Circle Container Block

{
    "id": "shape21",
    "type": "circleContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Diamond Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Diamond Container

Diamond Container Block

{
    "id": "shape22",
    "type": "diamondContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Pill Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Pill Container

Pill Container Block

{
    "id": "shape23",
    "type": "pillContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Rectangle Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Rectangle Container

Rectangle Container Block

{
    "id": "shape24",
    "type": "rectangleContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Rounded Rectangle Container
This shape's bounding box is incompatible with the rotation property.

Property	Description	
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Rounded Rectangle Container

Rounded Rectangle Container Block

{
    "id": "shape25",
    "type": "roundedRectangleContainer",
    "boundingBox": { ... },
    "style": { ... },
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Swim Lanes
This shape's bounding box is incompatible with the rotation property.

Property	Description	
vertical	Boolean
Determines orientation of the swim lanes.	Required
titleBar	Title Bar
Defines the behavior of the title bar of the swim lane.	Required
lanes	Array[Swim Lane]
An array of swim lanes.	Required
magnetize	Boolean
Determines whether shapes within the container move with the container. Defaults to true.	Optional
Advances Swimlane Container

Swim Lanes Block

{
    "id": "shape26",
    "type": "swimLanes",
    "boundingBox": { ... },
    "style": { ... },
    "vertical": false,
    "titleBar": { ... },
    "lanes": [ ... ],
    "magnetize": true,
    "actions": [ ... ],
    "customData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Title Bar
Property	Description	
height	Number
The height of the title bar.	Required
verticalText	Boolean
Determines the orientation of the title text.	Required
Title Bar Resource

{
  "height": 50,
  "verticalText": true
}
Swim Lane
Property	Description	
title	String
The title text of a swim lane.	Required
width	Number
The width of a swim lane. All individual lane widths must add up to total swim lanes width or height, depending on orientation.	Required
headerFill	Color
Hexadecimal string representing a RGB or RGBA color value for the header fill.	Required
laneFill	Color
Hexadecimal string representing a RGB or RGBA color value for the lane fill.	Required
Swim Lane Resource

{
  "title": "Swim lane 1",
  "width": 300,
  "headerFill": "#635DFF",
  "laneFill": "#F2F3F5"
}
