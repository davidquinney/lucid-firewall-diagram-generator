# Comparison of Generated vs Sample Document.json

## Sample document.json Format

The sample Lucid document.json file uses:

1. **BoundingBox Properties**: Uses `w` and `h` instead of `width` and `height`
   ```json
   "boundingBox": {
     "x": 583,
     "y": 840,
     "w": 160,
     "h": 120
   }
   ```

2. **Style Format**: Uses a nested `stroke` object with color, width, and style properties
   ```json
   "style": {
     "stroke": {
       "color": "#6f2131",
       "width": 3.0,
       "style": "solid"
     }
   }
   ```

3. **Data Binding**: Uses collections and data binding with the syntax `{{=@'System Name'}}` and `linkedData` arrays

## Our Generated document.json Format

Our generator was using:

1. **BoundingBox Properties**: Was using `width` and `height` but now updated to use `w` and `h` in line with the sample
   ```json
   "boundingBox": {
     "x": 100,
     "y": 100,
     "w": 400,
     "h": 300
   }
   ```

2. **Style Format**: Uses a flat structure with direct properties
   ```json
   "style": {
     "fillColor": "#d7d7d7",
     "borderColor": "#000000",
     "borderWidth": 1
   }
   ```

3. **No Data Binding**: Uses direct text values without data binding

## Implemented Fix

We've updated our code to use `w` and `h` instead of `width` and `height` in the boundingBox objects. This should fix the API error we encountered.

## Additional Potential Differences

While we've fixed the immediate error, there might be other format differences worth considering:

1. **Style Structure**: We might need to update our style format to use the nested `stroke` object structure
2. **Shape Types**: The sample uses various shape types like "rectangle", "database", "terminator"
3. **Collections**: The sample includes a collections array for data binding

For now, we'll focus on the property name fix and see if that resolves the upload error.
