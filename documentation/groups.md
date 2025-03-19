Groups
Suggest Edits
Groups are collections of items, such as shapes, lines, or other groups. Groups cannot contain layers. Groups allow you to combine multiple items into a single, manageable unit. When you group items, you can move, resize, or format them collectively, treating the group as a single object. This is particularly useful when you want to maintain the relative positions of multiple items or when you want to apply formatting or actions to a set of items simultaneously.

Group Format
Property	Description	
id	ID
Identifier for a given group (must be unique).	Required
items	Array[ID]
An array of IDs of all Shapes, Lines, and Groups in the group.	Optional
note	Text
Text to add as a note to the group.	Optional
customData	Array[Custom Data]
An array of custom data in the group. See Custom Data for a description of its purpose.	Optional
linkedData	Array[Linked Data]
An array of linked data in the group. See Linked Data for a description of its purpose.	Optional
Group

{
  "id": "group1",
  "items": [ ... ],
  "note": "Test Note",
  "customData": [ ... ],
  "linkedData": [ ... ]
}