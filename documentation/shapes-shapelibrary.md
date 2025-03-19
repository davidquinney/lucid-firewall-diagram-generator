Shape Library
Suggest Edits
Circle
Circle Block

Circle Block

{
    "id": "shape5",
    "type": "circle",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Cloud
Cloud Block

Cloud Block

{
    "id": "shape6",
    "type": "cloud",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Cross
Property	Description	
indent	Indent
Determines the behavior of the indent on the shape.	Optional
Cross Block

Cross Block

{
    "id": "shape7",
    "type": "cross",
    "boundingBox": { ... },
    "style": { ... },
    "indent": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Indent
A set of values that determines the appearance of the shape. Values must be between 0 and 0.5.

Property	Description	
x	Decimal
A value that determines the size of the horizontal indent.	Required
y	Decimal
A value that determines the size of the vertical indent.	Required
Indent Resource

{
    "x": 0.25,
    "y": 0.25
}
Diamond
Diamond Block

Diamond Block

{
    "id": "shape8",
    "type": "diamond",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Double Arrow
Double Arrow Block

Double Arrow Block

{
    "id": "shape9",
    "type": "doubleArrow",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Flexible Polygon
Property	Description	
vertices	Array[RelativePosition]
An array of positions. Must have between 3 and 100 vertices inclusive. Defines the border of the shape relative to the bounding box.	Required
Flexible Polygon Block

Flexible Polygon Block

{
    "id": "shape10",
    "type": "flexiblePolygon",
    "boundingBox": { ... },
    "style": { ... },
    "vertices": [ ... ],
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Hexagon
Hexagon Block

Hexagon Block

{
    "id": "shape11",
    "type": "hexagon",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Isosceles Triangle
Isosceles Triangle Block

Isosceles Triangle Block

{
    "id": "shape12",
    "type": "isoscelesTriangle",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Octagon
Octagon Block

Octagon Block

{
    "id": "shape13",
    "type": "octagon",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Pentagon
Pentagon Block

Pentagon Block

{
    "id": "shape14",
    "type": "pentagon",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Poly-Star
Property	Description	
shape	Poly-Star Shape
Defines the shape of the star.	Required
PolyStar Block

Poly-Star Block

{
    "id": "shape15",
    "type": "polyStar",
    "boundingBox": { ... },
    "style": { ... },
    "shape": { ... },
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Poly-Star Shape
Property	Description	
numPoints	Number
The number of points on the star. Must be between 3 and 25.	Required
innerRadius	Number
The fraction of the total shape from the center of the star to each inner point. Must be between 0 and 1.	Required
Poly-Star Shape Resource

{
    "numPoints": 5,
    "innerRadius": 0.5
}
Rectangle
Default Block

Rectangle Block

{
    "id": "shape16",
    "type": "rectangle",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Right Triangle [shapes-right-triangle-block]
Right Triangle Block

Right Triangle Block

{
    "id": "shape17",
    "type": "rightTriangle",
    "boundingBox": { ... },
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Single Arrow
Property	Description	
orientation	Single Arrow Orientation
Determines the direction of the arrow. Defaults to "right".	Optional
Single Arrow Block

Single Arrow Block

{
    "id": "shape18",
    "type": "singleArrow",
    "boundingBox": { ... },
    "orientation": "right",
    "style": { ... },
    "text": "Text",
    "actions": [ ... ],
    "customData": [ ... ],
    "linkedData": [ ... ],
    "opacity": 100,
    "note": "Test Note"
}
Single Arrow Orientation
Determines the direction of the arrow.

Value	Description
right	A rightward-facing arrow.
left	A leftward-facing arrow.
up	An upward-facing arrow.
down	A downward-facing arrow.
