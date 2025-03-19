import json
import os
import shutil
import tempfile
import zipfile
import uuid
import pandas as pd

class LucidGenerator:
    """
    Class to generate Lucid diagrams from firewall rules
    """
    
    def __init__(self, filtered_data, software_type):
        """
        Initialize the Lucid Generator
        
        Args:
            filtered_data (pd.DataFrame): DataFrame containing the filtered firewall rules
            software_type (str): The selected software type
        """
        self.filtered_data = filtered_data
        self.software_type = software_type
        self.entities_by_az = {}
        self.az_list = []
        self.entity_id_map = {}
        
        # Define layout parameters for a strict 4x4 grid
        self.start_x = 100
        self.start_y = 100
        self.grid_cols = 4
        self.grid_rows = 4
        
        # Maximum allowed y-coordinate to ensure all elements stay within page bounds
        self.max_y_coordinate = 2300  # Increased from 1800 to accommodate larger containers
        
        # Base container dimensions (will be dynamically adjusted based on content)
        self.min_container_width = 300  # Minimum width for each AZ container (increased from 250)
        self.min_container_height = 300  # Minimum height for each AZ container (increased from 250)
        self.horizontal_spacing = 150  # Spacing between AZs horizontally
        self.vertical_spacing = 150    # Spacing between AZs vertically
        
        # Entity dimensions
        self.entity_width = 220  # Increased from 180 to better fit text
        self.entity_height = 60  # Base height to fit text
        self.entity_vertical_spacing = 25  # Increased from 15 for better spacing
        self.entity_horizontal_spacing = 20  # Horizontal spacing between entities
        self.min_entity_height = 40  # Minimum height for any entity, regardless of space constraints
        
        # Create a grid position map for easy reference
        # This ensures all AZs are properly aligned on a 4x4 grid
        self.grid_positions = {}
        # Increased horizontal and vertical spacing to avoid container overlaps
        grid_h_spacing = 450  # Increased from self.horizontal_spacing
        grid_v_spacing = 350  # Increased from self.vertical_spacing
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = self.start_x + col * grid_h_spacing
                y = self.start_y + row * grid_v_spacing
                self.grid_positions[(row, col)] = {"x": x, "y": y}
        
    def _preprocess_data(self):
        """
        Preprocess the data to extract AZs and entities
        """
        from excel_reader import get_unique_az_values, get_unique_entities
        
        # Get unique AZ values
        self.az_list = get_unique_az_values(self.filtered_data)
        
        # Get unique entities by AZ
        self.entities_by_az = get_unique_entities(self.filtered_data)
        
        # Create entity ID mapping
        self._create_entity_id_map()
        
    def _create_entity_id_map(self):
        """
        Create a mapping of entity names to unique IDs
        """
        entity_id = 1
        
        # Process each AZ
        for az in self.az_list:
            if az not in self.entities_by_az:
                continue
                
            # Process sources
            for source in self.entities_by_az[az]["sources"]:
                if source not in self.entity_id_map:
                    self.entity_id_map[source] = f"entity_{entity_id}"
                    entity_id += 1
            
            # Process destinations
            for dest in self.entities_by_az[az]["destinations"]:
                if dest not in self.entity_id_map:
                    self.entity_id_map[dest] = f"entity_{entity_id}"
                    entity_id += 1
    
    def _create_document_json(self):
        """
        Create the document.json structure for the Lucid diagram
        
        Returns:
            dict: The document.json structure
        """
        self._preprocess_data()
        
        # Initialize the document
        # Increase page dimensions to accommodate all AZs with dynamic sizing
        document = {
            "version": 1,
            "pages": [
                {
                    "id": "page1",
                    "title": f"Firewall Rules - {self.software_type}",
                    "width": 2000,  # Increased from 1500 to accommodate wider containers
                    "height": 2500,  # Increased from 2000 to accommodate taller containers
                    "shapes": [],
                    "lines": []
                }
            ]
        }
        
        # Create shapes for AZ containers
        az_containers = self._create_az_containers()
        document["pages"][0]["shapes"].extend(az_containers)
        
        # Create shapes for entities (sources and destinations)
        entity_shapes = self._create_entity_shapes()
        document["pages"][0]["shapes"].extend(entity_shapes)
        
        # Create lines for connections
        connection_lines = self._create_connection_lines()
        document["pages"][0]["lines"].extend(connection_lines)
        
        return document
    
    def _create_az_containers(self):
        """
        Create container shapes for each AZ with dynamic sizing based on content
        
        Returns:
            list: List of container shapes
        """
        containers = []
        
        # Define specific grid positions for key AZs according to requirements
        az_grid_positions = {
            # Client Network at top left
            "Client network": (0, 0),  # (row, col) - top left
            
            # AZ3 at the top
            "AZ3": (0, 1),  # top, second column
            
            # Internet Services and External Services must always be on the right
            "Internet Services": (0, 3),  # top right
            "External Services": (1, 3),  # right side, second row
            
            # Local AZ in middle left
            "Local AZ": (2, 0),  # left side, third row
            
            # AZ1 must always be at bottom left
            "AZ1": (3, 0),  # bottom left
            
            # AZ2 must always be bottom right
            "AZ2": (3, 3)   # bottom right
        }
        
        # Create a list of available grid positions (excluding reserved positions)
        available_positions = []
        reserved_positions = set(az_grid_positions.values())
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if (row, col) not in reserved_positions:
                    available_positions.append((row, col))
        
        # First pass: Calculate required dimensions for each AZ based on content
        az_dimensions = {}
        for i, az in enumerate(self.az_list):
            # Default dimensions for empty AZs
            container_width = self.min_container_width
            container_height = self.min_container_height
            
            # Count entities and calculate space requirements
            if az in self.entities_by_az:
                entity_count = 0
                max_entity_width = 0
                total_entity_height = 0
                
                # Process sources
                if "sources" in self.entities_by_az[az]:
                    for source in self.entities_by_az[az]["sources"]:
                        entity_count += 1
                        
                        # Adjust width based on text length and content
                        text_length = len(source)
                        entity_width = self.entity_width
                        entity_height = self.entity_height
                        
                        # More aggressive scaling for longer text
                        if text_length > 40:
                            entity_width = max(entity_width, 350)  # Much wider for very long text
                        elif text_length > 30:
                            entity_width = max(entity_width, 300)  # Wider for very long text
                        elif text_length > 20:
                            entity_width = max(entity_width, 250)  # Wide for long text
                        
                        # Special handling for text with parentheses
                        has_parentheses = "(" in source and ")" in source
                        if has_parentheses:
                            # Add 10% additional width for text with parentheses
                            entity_width = int(entity_width * 1.1)
                            
                        # Adjust height based on text length
                        if text_length > 35:
                            entity_height = max(entity_height, 80)  # Much taller for very long text
                        elif text_length > 25:
                            entity_height = max(entity_height, 70)  # Taller for long text
                        
                        # Add additional height for text with parentheses
                        if has_parentheses:
                            entity_height = max(entity_height, entity_height + 10)
                            
                        max_entity_width = max(max_entity_width, entity_width)
                        total_entity_height += entity_height
                
                # Process destinations (that aren't already counted as sources)
                if "destinations" in self.entities_by_az[az]:
                    for dest in self.entities_by_az[az]["destinations"]:
                        if "sources" not in self.entities_by_az[az] or dest not in self.entities_by_az[az]["sources"]:
                            entity_count += 1
                            
                            # Adjust width based on text length and content
                            text_length = len(dest)
                            entity_width = self.entity_width
                            entity_height = self.entity_height
                            
                            # More aggressive scaling for longer text
                            if text_length > 40:
                                entity_width = max(entity_width, 350)  # Much wider for very long text
                            elif text_length > 30:
                                entity_width = max(entity_width, 300)  # Wider for very long text
                            elif text_length > 20:
                                entity_width = max(entity_width, 250)  # Wide for long text
                            
                            # Special handling for text with parentheses
                            has_parentheses = "(" in dest and ")" in dest
                            if has_parentheses:
                                # Add 10% additional width for text with parentheses
                                entity_width = int(entity_width * 1.1)
                                
                            # Adjust height based on text length
                            if text_length > 35:
                                entity_height = max(entity_height, 80)  # Much taller for very long text
                            elif text_length > 25:
                                entity_height = max(entity_height, 70)  # Taller for long text
                            
                            # Add additional height for text with parentheses
                            if has_parentheses:
                                entity_height = max(entity_height, entity_height + 10)
                                
                            max_entity_width = max(max_entity_width, entity_width)
                            total_entity_height += entity_height
                
                # Calculate spacing between entities
                spacing = (entity_count - 1) * self.entity_vertical_spacing if entity_count > 1 else 0
                
                # Calculate container dimensions with padding
                if entity_count > 0:
                    # More padding for containers with many entities
                    horizontal_padding = 60  # 30px padding on each side
                    vertical_padding = 80    # 40px padding top and bottom
                    
                    # Add additional padding for containers with many entities
                    if entity_count > 5:
                        horizontal_padding += 20  # Extra padding for many entities
                        vertical_padding += entity_count * 5  # Scale padding with entity count
                    
                    # Calculate container dimensions with padding
                    container_width = max(self.min_container_width, max_entity_width + horizontal_padding)
                    container_height = max(self.min_container_height, total_entity_height + spacing + vertical_padding)
                    
                    # Apply more aggressive height calculation for containers with many entities
                    if entity_count > 5:
                        # Add additional height based on entity count - significantly increased multiplier
                        additional_height = (entity_count - 5) * 60  # Increased from 20 to 60
                        container_height = container_height + additional_height  # Always add the additional height
                    
                    # Add extra padding for safety
                    container_height += 50  # Add extra padding to ensure all entities fit
            
            az_dimensions[az] = {
                "width": container_width,
                "height": container_height
            }
        
        # Create container for each AZ
        available_position_index = 0
        for i, az in enumerate(self.az_list):
            # Get grid position for this AZ
            if az in az_grid_positions:
                row, col = az_grid_positions[az]
            else:
                # Use the next available grid position
                if available_position_index < len(available_positions):
                    row, col = available_positions[available_position_index]
                    available_position_index += 1
                else:
                    # Fallback if we run out of grid positions (shouldn't happen with 4x4 grid)
                    row, col = (2, 2)  # Default to center if all positions are taken
            
            # Get the x, y coordinates for this grid position
            position = self.grid_positions[(row, col)]
            x_position = position["x"]
            y_position = position["y"]
            
            # Get the calculated dimensions for this AZ
            container_width = az_dimensions[az]["width"]
            container_height = az_dimensions[az]["height"]
            
            # Ensure y-coordinate doesn't exceed the maximum allowed value
            if y_position > self.max_y_coordinate - container_height:
                y_position = self.max_y_coordinate - container_height
            
            # Create the container with dynamic dimensions based on content
            container = {
                "id": f"az_{i+1}",
                "type": "rectangle",
                "boundingBox": {
                    "x": x_position,
                    "y": y_position,
                    "w": container_width,
                    "h": container_height
                },
                "style": {
                    "fill": {
                        "type": "color",
                        "color": "#d7d7d7"
                    },
                    "stroke": {
                        "color": "#d7d7d7",
                        "width": 2,
                        "style": "solid"
                    }
                },
                "text": f"<p style=\"font-family: Liberation Sans;font-size: 9pt;text-align: center;margin-top: 10px;\">{az}</p><p style=\"font-family: Liberation Sans;font-size: 9pt;text-align: center;\"><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br></p>"
            }
            
            # Store the container dimensions for validation later
            az_dimensions[az]["container"] = container
            
            containers.append(container)
        
        return containers
    
    def _analyze_connections(self):
        """
        Analyze connections between entities to optimize placement
        
        Returns:
            dict: Connection information for optimizing entity placement
            set: Set of source entity IDs
            dict: Connection weight matrix for component ordering
        """
        # Create a dictionary to store connection information
        connections = {}
        
        # Create a set of all source entity IDs
        source_entity_ids = set()
        for az in self.az_list:
            if az in self.entities_by_az:
                for source in self.entities_by_az[az]["sources"]:
                    if source in self.entity_id_map:
                        source_entity_ids.add(source)
        
        # Create a connection weight matrix for optimizing component ordering
        # This will track how many connections exist between each pair of components
        connection_weights = {}
        
        # Analyze connections
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            
            if pd.isna(source) or pd.isna(destination):
                continue
            
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
            
            # Initialize connection info if not exists
            if source not in connections:
                connections[source] = {"targets": set(), "source_az": None, "connection_count": 0}
            if destination not in connections:
                connections[destination] = {"targets": set(), "source_az": None, "connection_count": 0}
            
            # Add connection
            connections[source]["targets"].add(destination)
            connections[source]["connection_count"] += 1
            connections[destination]["connection_count"] += 1  # Count incoming connections too
            
            # Store source AZ
            source_az = None
            dest_az = None
            for _, row2 in self.filtered_data.iterrows():
                if row2["Source"] == source:
                    source_az = row2["Source AZ (Used for Diagram Generation)"]
                if row2["Destination"] == destination:
                    dest_az = row2["Destination AZ (Used for Diagram Generation)"]
                if source_az and dest_az:
                    break
            
            if source_az:
                connections[source]["source_az"] = source_az
            if dest_az:
                connections[destination]["source_az"] = dest_az
            
            # Update connection weight matrix
            if source_az == dest_az:  # Only track connections within the same AZ for ordering
                # Create entity pair key (always sort to ensure consistency)
                entity_pair = tuple(sorted([source, destination]))
                
                if entity_pair not in connection_weights:
                    connection_weights[entity_pair] = 0
                connection_weights[entity_pair] += 1
        
        return connections, source_entity_ids, connection_weights
    
    def _pre_analyze_connections(self):
        """
        Pre-analyze connections to count how many connections each entity has
        
        Returns:
            dict: Dictionary mapping entity IDs to connection counts
        """
        connection_counts = {}
        
        # First pass to count connections
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            
            if pd.isna(source) or pd.isna(destination):
                continue
            
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
                
            source_id = f"{self.entity_id_map[source]}_source"
            
            # Get unique entity IDs for destinations
            # If destination is also a source, use the source ID
            dest_id = f"{self.entity_id_map[destination]}_dest"
            
            # Create a set of all source entity IDs
            source_entity_ids = set()
            for az in self.az_list:
                if az in self.entities_by_az:
                    for src in self.entities_by_az[az]["sources"]:
                        if src in self.entity_id_map:
                            source_entity_ids.add(f"{self.entity_id_map[src]}_source")
            
            if f"{self.entity_id_map[destination]}_source" in source_entity_ids:
                dest_id = f"{self.entity_id_map[destination]}_source"
            
            # Increment connection count for source
            if source_id not in connection_counts:
                connection_counts[source_id] = 0
            connection_counts[source_id] += 1
            
            # Increment connection count for destination
            if dest_id not in connection_counts:
                connection_counts[dest_id] = 0
            connection_counts[dest_id] += 1
        
        return connection_counts
    
    def _validate_container_bounds(self, az, entity_shapes):
        """
        Validate and adjust container bounds if entities exceed them
        
        Args:
            az (str): The AZ name
            entity_shapes (list): List of entity shapes in this AZ
            
        Returns:
            bool: True if container was adjusted, False otherwise
        """
        if az not in self.az_list or not entity_shapes:
            return False
            
        # Get the container for this AZ
        container = None
        for az_info in self.az_dimensions.values():
            if "container" in az_info and az_info["container"]["text"].startswith(f"<p style=\"font-family: Liberation Sans;font-size: 9pt;text-align: center;margin-top: 10px;\">{az}</p>"):
                container = az_info["container"]
                break
                
        if not container:
            return False
            
        # Get container bounds
        container_x = container["boundingBox"]["x"]
        container_y = container["boundingBox"]["y"]
        container_width = container["boundingBox"]["w"]
        container_height = container["boundingBox"]["h"]
        
        # Find the extents of all entities
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        
        for shape in entity_shapes:
            entity_x = shape["boundingBox"]["x"]
            entity_y = shape["boundingBox"]["y"]
            entity_width = shape["boundingBox"]["w"]
            entity_height = shape["boundingBox"]["h"]
            
            # Update min/max coordinates
            min_x = min(min_x, entity_x)
            max_x = max(max_x, entity_x + entity_width)
            min_y = min(min_y, entity_y)
            max_y = max(max_y, entity_y + entity_height)
        
        # Always adjust the container to ensure all entities fit with padding
        # This is more aggressive than the previous approach which only adjusted if entities exceeded bounds
        
        # Calculate required container size with generous padding
        required_width = max_x - min_x + 80  # 40px padding on each side
        required_height = max_y - min_y + 100  # 50px padding on top and bottom
        
        # Calculate the new container dimensions
        new_width = max(container_width, required_width)
        new_height = max(container_height, required_height)
        
        # Ensure the container extends below the last entity with extra padding
        bottom_padding = 50  # Extra padding at the bottom
        if max_y + bottom_padding > container_y + new_height:
            new_height = max_y - container_y + bottom_padding
        
        # Apply the new dimensions if they're different from the current ones
        if new_width != container_width or new_height != container_height:
            container["boundingBox"]["w"] = new_width
            container["boundingBox"]["h"] = new_height
            return True
            
        return False
    
    def _create_entity_shapes(self):
        """
        Create shapes for each entity (source and destination) ensuring they fit within their AZ
        
        Returns:
            list: List of entity shapes
        """
        # Store AZ dimensions for container validation
        self.az_dimensions = {}
        shapes = []
        
        # Pre-analyze connections to get connection counts
        connection_counts = self._pre_analyze_connections()
        
        # Define specific grid positions for key AZs (same as in _create_az_containers)
        az_grid_positions = {
            # Client Network at top left
            "Client network": (0, 0),  # top left
            
            # AZ3 at the top
            "AZ3": (0, 1),  # top, second column
            
            # Internet Services and External Services must always be on the right
            "Internet Services": (0, 3),  # top right
            "External Services": (1, 3),  # right side, second row
            
            # Local AZ in middle left
            "Local AZ": (2, 0),  # left side, third row
            
            # AZ1 must always be at bottom left
            "AZ1": (3, 0),  # bottom left
            
            # AZ2 must always be bottom right
            "AZ2": (3, 3)   # bottom right
        }
        
        # Create a mapping of AZ to grid position
        az_to_grid_position = {}
        for az, pos in az_grid_positions.items():
            az_to_grid_position[az] = pos
        
        # For AZs not in the predefined list, assign them to available grid positions
        available_positions = []
        reserved_positions = set(az_grid_positions.values())
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if (row, col) not in reserved_positions:
                    available_positions.append((row, col))
        
        # Assign remaining AZs to available positions
        available_position_index = 0
        for az in self.az_list:
            if az not in az_to_grid_position:
                if available_position_index < len(available_positions):
                    az_to_grid_position[az] = available_positions[available_position_index]
                    available_position_index += 1
                else:
                    # Fallback if we run out of grid positions (shouldn't happen with 4x4 grid)
                    az_to_grid_position[az] = (2, 2)  # Default to center if all positions are taken
        
        # Analyze connections to optimize entity placement
        connections, source_entity_ids, connection_weights = self._analyze_connections()
        
        # Group entities by AZ and sort them based on connection patterns
        entities_by_az_ordered = {}
        
        for az in self.az_list:
            if az not in self.entities_by_az:
                continue
                
            # Get all entities in this AZ
            all_entities = []
            if "sources" in self.entities_by_az[az]:
                all_entities.extend(self.entities_by_az[az]["sources"])
            if "destinations" in self.entities_by_az[az]:
                for dest in self.entities_by_az[az]["destinations"]:
                    if dest not in all_entities:
                        all_entities.append(dest)
            
            # Sort entities based on their connection patterns and weights
            def connection_score(entity):
                if entity not in connections:
                    return 0
                
                # Base score is the total number of connections
                score = connections[entity].get("connection_count", 0)
                
                # Add bonus for entities that are highly connected to each other
                # This helps place related entities adjacent to each other
                for other_entity in all_entities:
                    if other_entity == entity:
                        continue
                        
                    # Check if there's a connection weight between these entities
                    entity_pair = tuple(sorted([entity, other_entity]))
                    if entity_pair in connection_weights:
                        score += connection_weights[entity_pair] * 2  # Give extra weight to intra-AZ connections
                
                return score
            
            all_entities.sort(key=connection_score, reverse=True)
            entities_by_az_ordered[az] = all_entities
        
        # Keep track of vertical position within each AZ
        az_y_positions = {}
        for az in self.az_list:
            # Start components at the top of the container with a small padding
            az_y_positions[az] = self.grid_positions[az_to_grid_position.get(az, (0, 0))]["y"] + 30
        
        # Create shape for each entity by AZ
        for az in self.az_list:
            if az not in entities_by_az_ordered:
                continue
                
            # Get container position from grid
            grid_pos = az_to_grid_position.get(az, (0, 0))
            container_x = self.grid_positions[grid_pos]["x"]
            container_y = self.grid_positions[grid_pos]["y"]
            
            # Calculate available height for entities in this AZ
            # Get the container dimensions (now dynamic)
            container_width = 0
            container_height = 0
            
            # Find the container for this AZ
            for container in self._create_az_containers():
                if container["text"].startswith(f"<p style=\"font-family: Liberation Sans;font-size: 9pt;text-align: center;margin-top: 10px;\">{az}</p>"):
                    container_width = container["boundingBox"]["w"]
                    container_height = container["boundingBox"]["h"]
                    break
            
            # If we couldn't find the container, use default values
            if container_width == 0:
                container_width = self.min_container_width
            if container_height == 0:
                container_height = self.min_container_height
                
            available_height = container_height - 60  # Increased padding from 40 to 60
            
            # Count total entities in this AZ
            entity_count = len(entities_by_az_ordered[az])
            
            # Calculate max height per entity to ensure all fit
            if entity_count > 0:
                max_entity_height = (available_height - (entity_count - 1) * self.entity_vertical_spacing) / entity_count
                # Ensure minimum height
                max_entity_height = max(40, min(max_entity_height, self.entity_height))
            else:
                max_entity_height = self.entity_height
            
            # Keep track of shapes for this AZ for container validation
            az_shapes = []
            
            # Process entities in this AZ
            for entity in entities_by_az_ordered[az]:
                entity_id = self.entity_id_map[entity]
                
                # Determine if this entity is a source, destination, or both
                is_source = False
                if "sources" in self.entities_by_az[az] and entity in self.entities_by_az[az]["sources"]:
                    is_source = True
                
                # Create shape ID based on entity role
                shape_id = f"{entity_id}_source" if is_source else f"{entity_id}_dest"
                
                # Set entity width to fit within container
                entity_width = min(self.entity_width, container_width - 40)  # Ensure it fits with padding
                
                # Adjust entity height based on text length and number of connections
                entity_height = max_entity_height  # Default to calculated max height
                
                # Get the number of connections for this entity from our pre-analysis
                entity_id = f"{entity_id}_source" if is_source else f"{entity_id}_dest"
                connection_count = connection_counts.get(entity_id, 0)
                
                # Adjust height based on text length
                text_length = len(entity)
                # If text is very long, increase height
                if text_length > 50:  # Long text with many commas or special characters
                    text_height_factor = 2.0  # Double the height
                elif text_length > 30:
                    text_height_factor = 1.5  # 50% taller
                elif text_length > 15:
                    text_height_factor = 1.2  # 20% taller
                else:
                    text_height_factor = 1.0  # Standard height
                
                # Apply text length factor
                entity_height = entity_height * text_height_factor
                
                # If this entity has many connections, make it even taller (but still within limits)
                if connection_count > 3:
                    # Increase height based on connection count, but don't exceed container
                    # Use a more aggressive scaling factor to provide more space for connections
                    additional_height = min((connection_count - 3) * 15, 100)
                    entity_height = min(entity_height + additional_height, 
                                       (container_height - (az_y_positions[az] - container_y) - 30))
                
                # Calculate the center position of the container
                container_center_x = container_x + (container_width / 2)
                entity_x = container_center_x - (entity_width / 2)
                
                # Ensure entity stays within container bounds
                if entity_x < container_x + 20:
                    entity_x = container_x + 20
                if entity_x + entity_width > container_x + container_width - 20:
                    entity_x = container_x + container_width - entity_width - 20
                
                # Check if this entity would exceed container height
                if az_y_positions[az] + entity_height > container_y + container_height - 20:
                    # Adjust height to fit, but ensure minimum height
                    entity_height = max(self.min_entity_height, container_y + container_height - 20 - az_y_positions[az])
                    
                    # If we can't fit this entity with minimum height, adjust previous entities to make room
                    if entity_height < self.min_entity_height:
                        # Set to minimum height anyway - we'll overlap slightly if necessary
                        entity_height = self.min_entity_height
                
                # Ensure entity height is at least the minimum height
                # This prevents negative or very small heights that cause API errors
                entity_height = max(self.min_entity_height, entity_height)
                
                # Ensure entity y-coordinate doesn't exceed the maximum allowed value
                if az_y_positions[az] > self.max_y_coordinate - entity_height:
                    az_y_positions[az] = self.max_y_coordinate - entity_height
                
                # Create the entity shape
                shape = {
                    "id": shape_id,
                    "type": "rectangle",
                    "boundingBox": {
                        "x": entity_x,
                        "y": az_y_positions[az],
                        "w": entity_width,
                        "h": entity_height
                    },
                    "style": {
                        "fill": {
                            "type": "color",
                            "color": "#ffffff"
                        },
                        "stroke": {
                            "color": "#131313",
                            "width": 1.5,
                            "style": "solid"
                        }
                    },
                    "text": f"<p style=\"font-family: Liberation Sans;font-size: 9pt;text-align: center;vertical-align: middle;display: flex;justify-content: center;align-items: center;height: 100%;margin: 0;\">{entity}</p>"
                }
                
                shapes.append(shape)
                az_shapes.append(shape)
                az_y_positions[az] += entity_height + self.entity_vertical_spacing
            
            # Validate and adjust container bounds if needed
            self._validate_container_bounds(az, az_shapes)
        
        return shapes
    
    def _create_connection_lines(self):
        """
        Create lines for connections between sources and destinations
        
        Returns:
            list: List of connection lines
        """
        lines = []
        line_id = 1
        
        # Track bidirectional connections to avoid duplicates
        processed_bidirectional = set()
        
        # Create a set of all source entity IDs
        source_entity_ids = set()
        for az in self.az_list:
            if az in self.entities_by_az:
                for source in self.entities_by_az[az]["sources"]:
                    if source in self.entity_id_map:
                        source_entity_ids.add(f"{self.entity_id_map[source]}_source")
        
        # Count connections per entity to distribute endpoints
        # We need to track connections more specifically
        source_to_dest = {}  # Maps source_id -> list of dest_ids
        dest_from_source = {}  # Maps dest_id -> list of source_ids
        
        # Use pre-analyzed connection counts
        connection_counts = self._pre_analyze_connections()
        
        # First pass to count connections
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            
            if pd.isna(source) or pd.isna(destination):
                continue
            
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
                
            source_id = f"{self.entity_id_map[source]}_source"
            dest_id = f"{self.entity_id_map[destination]}_dest"
            
            # If destination is also a source, use the source ID
            if f"{self.entity_id_map[destination]}_source" in source_entity_ids:
                dest_id = f"{self.entity_id_map[destination]}_source"
            
            # Track connections in both directions
            if source_id not in source_to_dest:
                source_to_dest[source_id] = []
            source_to_dest[source_id].append(dest_id)
            
            if dest_id not in dest_from_source:
                dest_from_source[dest_id] = []
            dest_from_source[dest_id].append(source_id)
        
        # Get source and destination AZs for each entity
        entity_az_map = {}
        for az in self.az_list:
            if az not in self.entities_by_az:
                continue
                
            for source in self.entities_by_az[az]["sources"]:
                entity_id = self.entity_id_map[source]
                entity_az_map[f"{entity_id}_source"] = az
                
            for dest in self.entities_by_az[az]["destinations"]:
                if dest not in self.entities_by_az[az]["sources"]:  # Skip if already added as source
                    entity_id = self.entity_id_map[dest]
                    entity_az_map[f"{entity_id}_dest"] = az
        
        # Collect all connections for analysis
        all_connections = []
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            ports = row["Ports"]
            protocol = row["Transfer Protocol"]
            
            if pd.isna(source) or pd.isna(destination) or pd.isna(ports) or pd.isna(protocol):
                continue
            
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
                
            source_id = f"{self.entity_id_map[source]}_source"
            dest_id = f"{self.entity_id_map[destination]}_dest"
            
            # If destination is also a source, use the source ID
            if f"{self.entity_id_map[destination]}_source" in source_entity_ids:
                dest_id = f"{self.entity_id_map[destination]}_source"
                
            all_connections.append({
                "source_id": source_id,
                "dest_id": dest_id,
                "ports": ports,
                "protocol": protocol,
                "source_az": entity_az_map.get(source_id),
                "dest_az": entity_az_map.get(dest_id)
            })
        
        # We no longer use bottom side for connections - all connections use left or right sides only
        # This ensures cleaner diagrams with consistent connection point positioning
        
        # Initialize counters for distributing connection points
        source_current = {k: 0 for k in source_to_dest.keys()}
        dest_current = {k: 0 for k in dest_from_source.keys()}
        
        # Create a more specific mapping for each source-destination pair
        # This ensures each connection gets a unique position
        connection_positions = {}
        
        # First, create a unique key for each source-destination pair
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            ports = row["Ports"]
            protocol = row["Transfer Protocol"]
            
            if pd.isna(source) or pd.isna(destination) or pd.isna(ports) or pd.isna(protocol):
                continue
            
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
                
            source_id = f"{self.entity_id_map[source]}_source"
            dest_id = f"{self.entity_id_map[destination]}_dest"
            
            # If destination is also a source, use the source ID
            if f"{self.entity_id_map[destination]}_source" in source_entity_ids:
                dest_id = f"{self.entity_id_map[destination]}_source"
            
            # Create a unique key for this connection
            connection_key = f"{source_id}:{dest_id}:{protocol}:{ports}"
            
            # Store the connection key
            if connection_key not in connection_positions:
                connection_positions[connection_key] = {
                    "source_id": source_id,
                    "dest_id": dest_id,
                    "protocol": protocol,
                    "ports": ports
                }
        
        # Now assign positions to each connection
        for i, (key, conn) in enumerate(connection_positions.items()):
            source_id = conn["source_id"]
            dest_id = conn["dest_id"]
            
            # Get the number of connections for this source and destination
            source_count = len([k for k, c in connection_positions.items() if c["source_id"] == source_id])
            dest_count = len([k for k, c in connection_positions.items() if c["dest_id"] == dest_id])
            
            # Calculate the index of this connection among all connections for this source/dest
            source_index = len([k for k, c in connection_positions.items() if c["source_id"] == source_id and list(connection_positions.keys()).index(k) < i])
            dest_index = len([k for k, c in connection_positions.items() if c["dest_id"] == dest_id and list(connection_positions.keys()).index(k) < i])
            
            # Apply new positioning logic based on connection count
            # Single connection: middle (y=0.5)
            # Two connections: top and bottom (y=0.2 and y=0.8)
            # Three or more: distributed evenly
            
            if source_count == 1:
                # Single connection: middle
                source_y = 0.5
            elif source_count == 2:
                # Two connections: top and bottom
                source_y = 0.2 if source_index == 0 else 0.8
            else:
                # Three or more: distributed evenly
                source_y = 0.1 + (0.8 * source_index / (source_count - 1))
                
            if dest_count == 1:
                # Single connection: middle
                dest_y = 0.5
            elif dest_count == 2:
                # Two connections: top and bottom
                dest_y = 0.2 if dest_index == 0 else 0.8
            else:
                # Three or more: distributed evenly
                dest_y = 0.1 + (0.8 * dest_index / (dest_count - 1))
            
            # Store the calculated positions
            connection_positions[key]["source_y"] = source_y
            connection_positions[key]["dest_y"] = dest_y
            
            # We no longer use bottom side for connections - all connections use left or right sides only
        
        # Create a structure to track all connections between each source-destination pair
        # This will help us consolidate connections and detect bidirectional traffic
        connection_data = {}
        
        # First pass: collect all connections by source-destination pairs and protocol
        for _, row in self.filtered_data.iterrows():
            source = row["Source"]
            destination = row["Destination"]
            ports = row["Ports"]
            protocol = row["Transfer Protocol"]
            
            # Skip if any required field is missing
            if pd.isna(source) or pd.isna(destination) or pd.isna(ports) or pd.isna(protocol):
                continue
            
            # Get entity IDs
            if source not in self.entity_id_map or destination not in self.entity_id_map:
                continue
                
            source_id = f"{self.entity_id_map[source]}_source"
            dest_id = f"{self.entity_id_map[destination]}_dest"
            
            # If destination is also a source, use the source ID
            if f"{self.entity_id_map[destination]}_source" in source_entity_ids:
                dest_id = f"{self.entity_id_map[destination]}_source"
            
            # Create a direction key (source -> destination)
            direction_key = f"{source_id}:{dest_id}"
            
            # Initialize if not exists
            if direction_key not in connection_data:
                connection_data[direction_key] = {}
            
            # Initialize protocol if not exists
            if protocol not in connection_data[direction_key]:
                connection_data[direction_key][protocol] = set()
            
            # Add ports to this protocol
            # Ensure ports is a string before splitting
            if isinstance(ports, str):
                port_list = [p.strip() for p in ports.split(",")]
            else:
                # If it's not a string (e.g., an integer), convert it to string
                port_list = [str(ports)]
            connection_data[direction_key][protocol].update(port_list)
        
        # Second pass: Detect bidirectional connections and prepare consolidated connections
        consolidated_connections = []
        processed_directions = set()
        
        # Process each direction
        for direction_key, protocols in connection_data.items():
            # Skip if already processed
            if direction_key in processed_directions:
                continue
                
            # Parse source and destination IDs
            source_id, dest_id = direction_key.split(":")
            
            # Check if reverse direction exists
            reverse_key = f"{dest_id}:{source_id}"
            
            # For each protocol in this direction
            for protocol, ports in protocols.items():
                # Sort ports for consistent display
                sorted_ports = sorted(ports)
                ports_str = ", ".join(sorted_ports)
                
                # Check if this is bidirectional (same protocol and ports in both directions)
                is_bidirectional = False
                bidirectional_ports = set()
                
                if reverse_key in connection_data and protocol in connection_data[reverse_key]:
                    # Get ports in reverse direction
                    reverse_ports = connection_data[reverse_key][protocol]
                    
                    # Find common ports (bidirectional)
                    bidirectional_ports = ports.intersection(reverse_ports)
                    
                    if bidirectional_ports:
                        # Create bidirectional connection for common ports
                        sorted_bi_ports = sorted(bidirectional_ports)
                        bi_ports_str = ", ".join(sorted_bi_ports)
                        
                        consolidated_connections.append({
                            "source_id": source_id,
                            "dest_id": dest_id,
                            "protocol": protocol,
                            "ports": bi_ports_str,
                            "is_bidirectional": True
                        })
                        
                        # Mark these ports as processed in both directions
                        processed_directions.add(direction_key)
                        processed_directions.add(reverse_key)
                
                # Handle unidirectional ports (ports that exist only in this direction)
                unidirectional_ports = ports - bidirectional_ports
                
                if unidirectional_ports:
                    sorted_uni_ports = sorted(unidirectional_ports)
                    uni_ports_str = ", ".join(sorted_uni_ports)
                    
                    consolidated_connections.append({
                        "source_id": source_id,
                        "dest_id": dest_id,
                        "protocol": protocol,
                        "ports": uni_ports_str,
                        "is_bidirectional": False
                    })
                
        # Now create the actual lines for the diagram
        # First, group connections by source-destination pair and protocol
        # This allows us to consolidate multiple protocols on a single line
        grouped_connections = {}
        
        # Track used connection points for each entity pair to avoid overlaps
        # This will be used for both cross-AZ and same-AZ connections
        used_connection_points = {}
        
        # Track used connection points for each individual entity to ensure uniqueness
        # This prevents multiple connections from using the same point on a single entity
        entity_used_points = {}
        
        for conn in consolidated_connections:
            source_id = conn["source_id"]
            dest_id = conn["dest_id"]
            is_bidirectional = conn["is_bidirectional"]
            
            # Create a key for this source-destination pair
            if is_bidirectional:
                # For bidirectional connections, use a sorted key to avoid duplicates
                pair_key = tuple(sorted([source_id, dest_id]))
                direction_key = f"{pair_key[0]}:{pair_key[1]}:bidirectional"
            else:
                # For unidirectional connections, preserve direction
                direction_key = f"{source_id}:{dest_id}:unidirectional"
            
            # Initialize if not exists
            if direction_key not in grouped_connections:
                grouped_connections[direction_key] = {
                    "source_id": source_id,
                    "dest_id": dest_id,
                    "is_bidirectional": is_bidirectional,
                    "protocols": {},
                    "connection_index": 0  # Track the index of this connection for this entity pair
                }
            
            # Add protocol and ports
            protocol = conn["protocol"]
            if protocol not in grouped_connections[direction_key]["protocols"]:
                grouped_connections[direction_key]["protocols"][protocol] = []
                # Increment the connection index for each new protocol
                # This ensures different protocols between the same entities use different connection points
                grouped_connections[direction_key]["connection_index"] += 1
            
            grouped_connections[direction_key]["protocols"][protocol].append(conn["ports"])
        
        # Now create lines for each grouped connection
        for direction_key, conn_data in grouped_connections.items():
            source_id = conn_data["source_id"]
            dest_id = conn_data["dest_id"]
            is_bidirectional = conn_data["is_bidirectional"]
            
            # Determine the relative positions of the source and destination AZs
            source_az = entity_az_map.get(source_id)
            dest_az = entity_az_map.get(dest_id)
            
            # Define specific grid positions for key AZs (same as in _create_az_containers)
            az_grid_positions = {
                # Client Network at top left
                "Client network": (0, 0),  # top left
                
                # AZ3 at the top
                "AZ3": (0, 1),  # top, second column
                
                # Internet Services and External Services must always be on the right
                "Internet Services": (0, 3),  # top right
                "External Services": (1, 3),  # right side, second row
                
                # Local AZ in middle left
                "Local AZ": (2, 0),  # left side, third row
                
                # AZ1 must always be at bottom left
                "AZ1": (3, 0),  # bottom left
                
                # AZ2 must always be bottom right
                "AZ2": (3, 3)   # bottom right
            }
            
            # Get grid positions for source and destination AZs
            source_grid_pos = az_grid_positions.get(source_az)
            dest_grid_pos = az_grid_positions.get(dest_az)
            
            # Get the calculated y-positions for this connection
            # Use the first connection between these entities as a reference
            source_y = 0.5  # Default to center
            dest_y = 0.5    # Default to center
            
            # Look for a matching connection in connection_positions
            for key, pos in connection_positions.items():
                if pos["source_id"] == source_id and pos["dest_id"] == dest_id:
                    source_y = pos["source_y"]
                    dest_y = pos["dest_y"]
                    break
                # Also check the reverse direction for bidirectional connections
                elif is_bidirectional and pos["source_id"] == dest_id and pos["dest_id"] == source_id:
                    source_y = pos["dest_y"]  # Swap positions
                    dest_y = pos["source_y"]
                    break
            
            # Create a unique key for this entity pair to track connection points
            entity_pair_key = tuple(sorted([source_id, dest_id]))
            
            # Initialize tracking for this entity pair if not exists
            if entity_pair_key not in used_connection_points:
                used_connection_points[entity_pair_key] = []
                
            # Initialize tracking for individual entities if not exists
            if source_id not in entity_used_points:
                entity_used_points[source_id] = []
            if dest_id not in entity_used_points:
                entity_used_points[dest_id] = []
            
            # Determine which sides to use for connection based on relative positions
            # We only use left (x=0) or right (x=1) sides, never top or bottom
            source_pos = {"x": 0.5, "y": source_y}  # Default to center, will be adjusted to left/right
            dest_pos = {"x": 0.5, "y": dest_y}      # Default to center, will be adjusted to left/right
            
            # Determine if this is a cross-AZ or same-AZ connection
            is_cross_az = source_az != dest_az
            
            if source_grid_pos and dest_grid_pos:
                source_row, source_col = source_grid_pos
                dest_row, dest_col = dest_grid_pos
                
                # Special handling for Client Network connections - always use right side
                if source_az == "Client network":
                    source_pos = {"x": 1, "y": source_y}  # Always use right side of Client Network
                    # Destination should use left side when possible
                    dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                    
                # Get the connection index for this entity pair
                connection_index = grouped_connections[direction_key]["connection_index"]
                
                if is_cross_az:
                    # Cross-AZ connection with improved diagonal handling
                    if source_col != dest_col and source_row != dest_row:
                        # Diagonal connection - special handling based on diagonal type
                        if source_row > dest_row and source_col < dest_col:
                            # Bottom-left to top-right: both use right sides
                            source_pos = {"x": 1, "y": source_y}  # Right side of source
                            dest_pos = {"x": 1, "y": dest_y}      # Right side of destination
                        elif source_row < dest_row and source_col > dest_col:
                            # Top-right to bottom-left: both use left sides
                            source_pos = {"x": 0, "y": source_y}  # Left side of source
                            dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                        elif source_row < dest_row and source_col < dest_col:
                            # Top-left to bottom-right: right-to-left standard
                            source_pos = {"x": 1, "y": source_y}  # Right side of source
                            dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                        else:
                            # Bottom-right to top-left: left-to-right standard
                            source_pos = {"x": 0, "y": source_y}  # Left side of source
                            dest_pos = {"x": 1, "y": dest_y}      # Right side of destination
                    else:
                        # Non-diagonal cross-AZ connection: use standard right-to-left positioning
                        if source_col < dest_col:
                            # Source is to the left of destination
                            source_pos = {"x": 1, "y": source_y}  # Right side of source
                            dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                        elif source_col > dest_col:
                            # Source is to the right of destination
                            source_pos = {"x": 0, "y": source_y}  # Left side of source
                            dest_pos = {"x": 1, "y": dest_y}      # Right side of destination
                        else:
                            # Same column but different rows - use right-to-left
                            if source_row < dest_row:
                                # Source is above destination
                                source_pos = {"x": 1, "y": source_y}  # Right side of source
                                dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                            else:
                                # Source is below destination
                                source_pos = {"x": 0, "y": source_y}  # Left side of source
                                dest_pos = {"x": 1, "y": dest_y}      # Right side of destination
                else:
                    # Same-AZ connection: use consistent sides based on AZ position
                    # Left-side AZs use left side, Right-side AZs use right side
                    
                    # Get the connection index for this entity pair
                    connection_index = grouped_connections[direction_key]["connection_index"]
                    
                    # Determine which side to use based on AZ position
                    # For AZs in columns 0-1 (left side), use left side (x=0)
                    # For AZs in columns 2-3 (right side), use right side (x=1)
                    is_left_side_az = source_col < 2
                    
                    # Set x-coordinates based on AZ position (consistent for all connections in same AZ)
                    source_x = 0 if is_left_side_az else 1
                    dest_x = 0 if is_left_side_az else 1
                    
                    # Calculate a unique y-coordinate for each connection based on connection index
                    # We'll use a more sophisticated distribution to ensure no two connections use the same point
                    
                    # Count total connections for this entity pair to distribute evenly
                    total_connections = len(grouped_connections.keys())
                    
                    # Improved arrow distribution algorithm
                    # Use a progressive distribution based on connection count and index
                    
                    # Get the total number of connections for this entity
                    source_total_connections = len([k for k, c in grouped_connections.items() if c["source_id"] == source_id])
                    dest_total_connections = len([k for k, c in grouped_connections.items() if c["dest_id"] == dest_id])
                    
                    # Calculate the source and destination indices among all connections for these entities
                    source_connection_index = len([k for k, c in grouped_connections.items() 
                                                if c["source_id"] == source_id and 
                                                list(grouped_connections.keys()).index(k) < list(grouped_connections.keys()).index(direction_key)])
                    
                    dest_connection_index = len([k for k, c in grouped_connections.items() 
                                              if c["dest_id"] == dest_id and 
                                              list(grouped_connections.keys()).index(k) < list(grouped_connections.keys()).index(direction_key)])
                    
                    # Create a wider range of base positions for better distribution
                    # More connections = more spread out distribution
                    base_positions = []
                    
                    # Dynamically create positions based on connection count
                    if source_total_connections <= 3:
                        # For few connections, use fixed positions
                        base_positions = [0.2, 0.5, 0.8]
                    elif source_total_connections <= 5:
                        # For medium number of connections, use more positions
                        base_positions = [0.15, 0.3, 0.5, 0.7, 0.85]
                    else:
                        # For many connections, create evenly distributed positions
                        step = 0.7 / (source_total_connections - 1)
                        base_positions = [0.15 + i * step for i in range(source_total_connections)]
                    
                    # Get base positions for source and destination
                    source_base_y = base_positions[min(source_connection_index, len(base_positions) - 1)]
                    
                    # For destination, use a different distribution to avoid straight lines
                    if dest_total_connections <= 3:
                        dest_base_positions = [0.2, 0.5, 0.8]
                    elif dest_total_connections <= 5:
                        dest_base_positions = [0.15, 0.3, 0.5, 0.7, 0.85]
                    else:
                        step = 0.7 / (dest_total_connections - 1)
                        dest_base_positions = [0.15 + i * step for i in range(dest_total_connections)]
                    
                    dest_base_y = dest_base_positions[min(dest_connection_index, len(dest_base_positions) - 1)]
                    
                    # Add protocol-based variation for uniqueness
                    protocol_key = list(conn_data["protocols"].keys())[0]
                    protocol_hash = sum(ord(c) for c in protocol_key) % 10
                    protocol_variation = protocol_hash * 0.01  # Small variation (0.00 to 0.09)
                    
                    # Apply the positions with variations
                    source_y = source_base_y + protocol_variation
                    dest_y = dest_base_y - protocol_variation
                    
                    # Add additional variation based on connection index to ensure uniqueness
                    connection_variation = (connection_index % 3) * 0.02
                    source_y += connection_variation
                    dest_y -= connection_variation
                    
                    # Ensure y-coordinates are within bounds
                    source_y = max(0.1, min(0.9, source_y))
                    dest_y = max(0.1, min(0.9, dest_y))
                    
                    # Apply positions
                    source_pos = {"x": source_x, "y": source_y}
                    dest_pos = {"x": dest_x, "y": dest_y}
                    
                    # Add some variation based on the specific connection index
                    # This ensures that even with the same pattern, different connections use different points
                    variation = (connection_index // 4) * 0.1
                    source_pos["y"] = max(0.1, min(0.9, source_pos["y"] + variation))
                    dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"] - variation))
                    
                    # If x is 0 or 1 (side connection), adjust y to ensure it's within bounds
                    if source_pos["x"] == 0 or source_pos["x"] == 1:
                        source_pos["y"] = max(0.1, min(0.9, source_pos["y"]))
                    if dest_pos["x"] == 0 or dest_pos["x"] == 1:
                        dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"]))
                    
                    # Note: We no longer increment the connection index here
                    # It's now incremented when a new protocol is added to ensure
                    # different protocols use different connection points
            else:
                # If we don't have grid positions, try to determine AZ position from name
                if is_cross_az:
                    # Cross-AZ: right-to-left
                    source_pos = {"x": 1, "y": source_y}  # Right side of source
                    dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                else:
                    # Same-AZ: determine based on AZ name or default logic
                    # AZs with names like "AZ1", "Local AZ", "Client network" are typically on the left
                    left_side_az_patterns = ["AZ1", "AZ3", "Local AZ", "Client network"]
                    is_left_side = any(pattern in source_az for pattern in left_side_az_patterns)
                    
                    if is_left_side:
                        # Left side AZ: use left-to-left
                        source_pos = {"x": 0, "y": source_y}  # Left side of source
                        dest_pos = {"x": 0, "y": dest_y}      # Left side of destination
                    else:
                        # Right side AZ or unknown: use right-to-right
                        source_pos = {"x": 1, "y": source_y}  # Right side of source
                        dest_pos = {"x": 1, "y": dest_y}      # Right side of destination
            
            # Create a unique identifier for this connection point
            # Include protocol in the key to ensure different protocols use different points
            protocol_key = list(conn_data["protocols"].keys())[0]  # Use the first protocol as a representative
            connection_point = (source_pos["x"], source_pos["y"], dest_pos["x"], dest_pos["y"], protocol_key)
            
            # Create a simpler key for position checking (without protocol)
            position_key = (source_pos["x"], source_pos["y"], dest_pos["x"], dest_pos["y"])
            
            # Create keys for individual entity position checking
            source_point_key = (source_pos["x"], source_pos["y"])
            dest_point_key = (dest_pos["x"], dest_pos["y"])
            
            # Check if positions are already used on individual entities or entity pairs
            source_point_used = any(abs(point[0] - source_point_key[0]) < 0.01 and abs(point[1] - source_point_key[1]) < 0.05 for point in entity_used_points[source_id])
            dest_point_used = any(abs(point[0] - dest_point_key[0]) < 0.01 and abs(point[1] - dest_point_key[1]) < 0.05 for point in entity_used_points[dest_id])
            pair_point_used = position_key in [k[:4] for k in used_connection_points[entity_pair_key]]
            
            # If any position is already used, adjust it
            attempts = 0
            while (source_point_used or dest_point_used or pair_point_used) and attempts < 20:
                # Only adjust y positions, with increasingly aggressive offsets
                offset = 0.05 + (attempts * 0.02)  # Increasing offset with each attempt
                
                # Use a more varied adjustment strategy to find unique positions
                if attempts % 4 == 0:
                    source_pos["y"] = max(0.1, min(0.9, source_pos["y"] + offset))
                    dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"] - offset))
                elif attempts % 4 == 1:
                    source_pos["y"] = max(0.1, min(0.9, source_pos["y"] - offset))
                    dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"] + offset))
                elif attempts % 4 == 2:
                    source_pos["y"] = max(0.1, min(0.9, source_pos["y"] + offset * 1.5))
                    dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"] + offset * 0.5))
                else:
                    source_pos["y"] = max(0.1, min(0.9, source_pos["y"] - offset * 0.5))
                    dest_pos["y"] = max(0.1, min(0.9, dest_pos["y"] - offset * 1.5))
                
                # Update the position keys with new coordinates
                position_key = (source_pos["x"], source_pos["y"], dest_pos["x"], dest_pos["y"])
                connection_point = (source_pos["x"], source_pos["y"], dest_pos["x"], dest_pos["y"], protocol_key)
                source_point_key = (source_pos["x"], source_pos["y"])
                dest_point_key = (dest_pos["x"], dest_pos["y"])
                
                # Check if the new positions are still used
                source_point_used = any(abs(point[0] - source_point_key[0]) < 0.01 and abs(point[1] - source_point_key[1]) < 0.05 for point in entity_used_points[source_id])
                dest_point_used = any(abs(point[0] - dest_point_key[0]) < 0.01 and abs(point[1] - dest_point_key[1]) < 0.05 for point in entity_used_points[dest_id])
                pair_point_used = position_key in [k[:4] for k in used_connection_points[entity_pair_key]]
                
                attempts += 1
            
            # Record this connection point as used for both the entity pair and individual entities
            used_connection_points[entity_pair_key].append(connection_point)
            entity_used_points[source_id].append(source_point_key)
            entity_used_points[dest_id].append(dest_point_key)
            
            # Ensure source and destination points are not at the same height when on the same side
            if source_pos["x"] == dest_pos["x"] and abs(source_pos["y"] - dest_pos["y"]) < 0.15:
                # Offset the destination point more significantly to avoid overlap
                dest_pos["y"] = min(0.85, dest_pos["y"] + 0.25)
                
                # Update the connection point in the used list
                used_connection_points[entity_pair_key][-1] = (source_pos["x"], source_pos["y"], dest_pos["x"], dest_pos["y"])
            
            # Format the text for the line
            text_parts = []
            for protocol, ports_list in conn_data["protocols"].items():
                # Combine all ports for this protocol
                all_ports = []
                for ports in ports_list:
                    # Ensure ports is a string before splitting
                    if isinstance(ports, str):
                        all_ports.extend(ports.split(", "))
                    else:
                        # If it's not a string (e.g., an integer), convert it to string
                        all_ports.append(str(ports))
                
                # Remove duplicates and sort
                unique_ports = sorted(set(all_ports))
                ports_text = ", ".join(unique_ports)
                
                text_parts.append(f"{protocol} {ports_text}")
            
            # Join all protocol texts with line breaks
            line_text = "<br>".join([f"<i>{text}</i>" for text in text_parts])
            
            # Create line with appropriate arrow style based on whether it's bidirectional
            line = {
                "id": f"line_{line_id}",
                "lineType": "elbow",
                "endpoint1": {
                    "type": "shapeEndpoint",
                    "style": "arrow" if is_bidirectional else "none",  # Add arrow at start for bidirectional
                    "shapeId": source_id,
                    "position": source_pos
                },
                "endpoint2": {
                    "type": "shapeEndpoint",
                    "style": "arrow",  # Always have arrow at end
                    "shapeId": dest_id,
                    "position": dest_pos
                },
                "stroke": {
                    "color": "#131313",
                    "width": 1.5,
                    "style": "solid"
                },
                "text": [
                    {
                        "text": line_text,
                        "position": 0.5,
                        "side": "middle"
                    }
                ]
            }
            
            lines.append(line)
            line_id += 1
        
        return lines
    
    def create_lucid_file(self, output_path):
        """
        Create a .lucid file (ZIP) containing the document.json
        
        Args:
            output_path (str): Path to the output .lucid file
            
        Returns:
            str: Path to the created .lucid file
        """
        document_json = self._create_document_json()
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write document.json to the temporary directory
            document_path = os.path.join(temp_dir, "document.json")
            with open(document_path, "w") as f:
                json.dump(document_json, f, indent=2)
            
            # Create a ZIP file containing document.json
            with zipfile.ZipFile(output_path, "w") as zip_file:
                zip_file.write(document_path, arcname="document.json")
        
        return output_path


def create_document_json(filtered_data, software_type):
    """
    Create the document.json structure for the Lucid diagram
    
    Args:
        filtered_data (pd.DataFrame): DataFrame containing the filtered firewall rules
        software_type (str): The selected software type
        
    Returns:
        dict: The document.json structure
    """
    generator = LucidGenerator(filtered_data, software_type)
    return generator._create_document_json()

def create_lucid_file(filtered_data, software_type, output_path):
    """
    Create a .lucid file containing the document.json
    
    Args:
        filtered_data (pd.DataFrame): DataFrame containing the filtered firewall rules
        software_type (str): The selected software type
        output_path (str): Path to the output .lucid file
        
    Returns:
        str: Path to the created .lucid file
    """
    generator = LucidGenerator(filtered_data, software_type)
    return generator.create_lucid_file(output_path)
