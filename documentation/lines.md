Lines
Suggest Edits
Line Format
The format to create a line on the Lucid document between two defined points.

Property	Description	
id	ID
Identifier for a given line (must be unique).	Required
lineType	LineType
Type that specifies how the line does, or does not, curve.	Required
endpoint1	Endpoint
The first of two endpoints that specifies how and where the line will end.	Required
endpoint2	Endpoint
The second of two endpoints that specifies how and where the line will end.	Required
stroke	Stroke
Stroke object that defines the look of the line.	Optional
text	Array[LineText]
An array of line text objects. Multiple text objects can be on the same line.	Optional
customData	Array[CustomDatum]
An array of Custom Data objects.	Optional
linkedData	Array[LinkedDatum]
An array of Linked Data objects.	Optional
joints	Array [AbsolutePosition ]
An array of absolute positions that will be used as control points if lineType is set to straight.	Optional
elbowControlPoints	Array [AbsolutePosition ]
An array of absolute positions that will be used as control points if lineType is set to elbow. These points must form 90° angles.	Optional
Line Format

{
    "id": "line1",
    "lineType": "straight",
    "endpoint1": {
        "type": "shapeEndpoint",
        "style": "none",
        "shapeId": "block3",
        "position": { "x": 1, "y": 1 }
    },
    "endpoint2": {
        "type": "lineEndpoint",
        "style": "arrow",
        "lineId": "line2",
        "position": 0.5
    },
    "stroke": {
        "color": "#000000",
        "width": 1,
        "style": "solid"
    },
    "text": [
        {
            "text": "test",
            "position": 0.5,
            "side": "middle"
        }
    ],
    "customData": [
        {
            "key": "TestKey",
            "value": "TestValue"
        }
    ],
    "linkedData": [
        {
            "collectionId": "network",
            "key": "9"
        }
    ],
    "joints": [
        {
            "x": "100",
            "y": "100"
        }
    ]
}
Line Type
Defines the styling of a line's curvature.

Value	Description	Image
straight	A line with no curves.	Straight Line
elbow	A line with elbow (right-angle) curves.	Elbow Line
curved	A line with smooth curves.	Curved Line
Endpoint
Defines where a line should end and the styling of the endpoint.

Property	Description	
type	EndpointType
Type of endpoint to create.	Required
style	EndpointStyle
Style type which determines how the endpoint will appear.	Required
📘
These common endpoint fields are used on each specific type of endpoint.

Endpoint Type
The type of a given endpoint.

Value	Description
lineEndpoint	An endpoint that attaches to another line (see Line Endpoints for details).
shapeEndpoint	An endpoint that attaches to a shape (see Shape Endpoints for details).
positionEndpoint	An endpoint that is positioned somewhere on the canvas independent of a shape or line (see Position Endpoints for details).
Line Endpoint
An endpoint that attaches to another line.

Property	Description	
Base Endpoint Fields	Endpoint fields that are common to each type of endpoint (see Endpoints for details).	
lineId	ID
The id for which line to attach the endpoint to.	Required
position	Double
A relative position specifying where on the target line this endpoint should attach (must be between 0.0-1.0 inclusive).	Required
Line Endpoint

{
    "type": "lineEndpoint",
    "style": "arrow",
    "lineId": "line2",
    "position": 0.5
}
Shape Endpoint
An endpoint that attaches to a shape.

Property	Description	
Base Endpoint Fields	Endpoint fields that are common to each type of endpoint (see Endpoints for details).	
shapeId	ID
The id for which shape to attach the endpoint to.	Required
position	RelativePosition
A relative position specifying where on the target shape this endpoint should attach.	Required
Shape Endpoint

{
    "type": "shapeEndpoint",
    "style": "none",
    "shapeId": "block1",
    "position": { "x": 1, "y": 0.5 }
}
Position Endpoint
An endpoint that is positioned somewhere on the canvas independent of a shape or line.

Property	Description
Base Endpoint Fields	Endpoint fields that are common to each type of endpoint (see Endpoints for details).
position	AbsolutePosition
An absolute position specifying where on the canvas this endpoint should land.
Position Endpoint

{
    "type": "positionEndpoint",
    "style": "arrow",
    "position": { "x": 120, "y": -100 }
}
Endpoint Style
How to style the endpoint.

Value	Description
none	None
aggregation	Aggregation
arrow	Arrow
hollowArrow	Hollow Arrow
openArrow	Open Arrow
async1	Async 1
async2	Async 2
closedSquare	Closed Square
openSquare	Open Square
bpmnConditional	BPMN Conditional
bpmnDefault	BPMN Default
closedCircle	Closed Circle
openCircle	Open Circle
composition	Composition
exactlyOne	Exactly One
generalization	Generalization
many	Many
nesting	Nesting
one	One
oneOrMore	One Or More
zeroOrMore	Zero Or More
zeroOrOne	Zero Or One
Line Text
Defines what text should be displayed on the line and how it's styled.

Property	Description
text	Text
The text to display on the line.
position	Double
A relative position specifying where on the target line this text should appear (must be between 0.0-1.0 inclusive).
side	LineSide
A type that specifies how the text should be displayed on the line.
LineText

{
    "text": "test",
    "position": 0.5,
    "side": "middle"
}
Line Side
The side of a line on which to position an object.

Value	Description
top	The top of the line.
middle	The middle of the line, with the line passing behind the object.
bottom	The bottom of the line.