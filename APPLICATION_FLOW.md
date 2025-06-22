# Knowledge Graph Application - User Flow & Functionality Guide

## Table of Contents
1. [Application Overview](#application-overview)
2. [Getting Started](#getting-started)
3. [Main Interface](#main-interface)
4. [Adding Entities](#adding-entities)
5. [Creating Relationships](#creating-relationships)
6. [Data Upload](#data-upload)
7. [Loading Sample Data](#loading-sample-data)
8. [Querying Impacts](#querying-impacts)
9. [Graph Interaction](#graph-interaction)
10. [Advanced Features](#advanced-features)
11. [Troubleshooting](#troubleshooting)

## Application Overview

The Environmental Impact Network Knowledge Graph application is a web-based tool for modeling and visualizing environmental impact relationships. It allows users to create, explore, and analyze complex networks of environmental activities, factors, locations, and their consequences.

### Key Features
- **Interactive Graph Visualization**: Zoom, pan, and explore environmental networks
- **Entity Management**: Add activities, factors, locations, and consequences
- **Relationship Creation**: Define causal relationships between entities
- **Data Import**: Upload JSON and CSV files with environmental data
- **Impact Analysis**: Query and visualize impact pathways
- **Real-time Updates**: See changes immediately in the graph

---

## Getting Started

### 1. Application Launch
**Screenshot Placeholder**: `[SCREENSHOT: Application home page showing the main interface with empty graph]`

When you first launch the application, you'll see:
- **Navigation Bar**: Contains the application title and "Load Sample Data" button
- **Left Panel**: Input forms for adding entities and relationships
- **Right Panel**: Graph visualization area (initially empty)
- **Bottom Panel**: Query interface for impact analysis

### 2. Initial Setup
**Screenshot Placeholder**: `[SCREENSHOT: Empty application interface with form panels highlighted]`

The application starts with an empty graph. You can either:
- Load sample data to see a pre-built environmental network
- Start building your own network from scratch
- Upload existing data files

---

## Main Interface

### Interface Layout
**Screenshot Placeholder**: `[SCREENSHOT: Full application interface with all panels labeled]`

The application is divided into three main sections:

#### Left Panel - Input Forms
- **Add New Entity**: Form to create activities, factors, locations, or consequences
- **Add Relationship**: Form to connect entities with causal relationships
- **Upload Data**: Interface for importing JSON or CSV files

#### Center Panel - Graph Visualization
- **Interactive Graph**: D3.js-powered visualization with zoom and pan
- **Zoom Controls**: Buttons for zoom in (+), zoom out (-), and reset
- **Node Types**: Color-coded by entity type (activity, factor, location, consequence)

#### Right Panel - Query Interface
- **Impact Analysis**: Form to query impact pathways from any entity
- **Results Display**: Shows impact paths and consequences

---

## Adding Entities

### Step 1: Select Entity Type
**Screenshot Placeholder**: `[SCREENSHOT: Add Entity form with dropdown showing entity types]`

1. In the "Add New Entity" section, select the entity type:
   - **Activity**: Human activities that cause environmental impacts
   - **Factor**: Environmental factors or conditions
   - **Location**: Geographic areas or regions
   - **Consequence**: Environmental consequences or outcomes

### Step 2: Enter Entity Name
**Screenshot Placeholder**: `[SCREENSHOT: Form with entity type selected and name field highlighted]`

2. Enter a descriptive name for the entity (e.g., "Industrial Manufacturing", "CO2 Emissions")

### Step 3: Submit and Verify
**Screenshot Placeholder**: `[SCREENSHOT: Success message after adding entity]`

3. Click "Add Entity" to create the node
4. The entity appears in the graph with color coding:
   - 🟠 **Orange**: Activities
   - 🟢 **Green**: Factors  
   - 🔵 **Blue**: Locations
   - 🔴 **Red**: Consequences

### Example: Adding an Activity
**Screenshot Placeholder**: `[SCREENSHOT: Graph showing newly added "Industrial Manufacturing" activity node]`

**Entity Type**: Activity
**Entity Name**: Industrial Manufacturing
**Result**: Orange node appears in the graph

---

## Creating Relationships

### Step 1: Select Source Entity
**Screenshot Placeholder**: `[SCREENSHOT: Add Relationship form with source dropdown populated]`

1. In the "Add Relationship" section, select the source entity from the dropdown
   - The dropdown is automatically populated with all existing entities

### Step 2: Select Target Entity
**Screenshot Placeholder**: `[SCREENSHOT: Form with source selected and target dropdown highlighted]`

2. Select the target entity that the source affects or causes

### Step 3: Choose Relationship Type
**Screenshot Placeholder**: `[SCREENSHOT: Relationship type dropdown showing options]`

3. Select the relationship type:
   - **Causes**: Direct causation (e.g., activity causes factor)
   - **Affects**: General impact or influence
   - **Occurs In**: Geographic or contextual location
   - **Contributes To**: Partial contribution to an outcome
   - **Impacts**: Direct impact on consequences

### Step 4: Create Relationship
**Screenshot Placeholder**: `[SCREENSHOT: Graph showing new relationship arrow between nodes]`

4. Click "Add Relationship" to create the connection
5. An arrow appears in the graph showing the relationship direction

### Example: Creating a Causal Relationship
**Screenshot Placeholder**: `[SCREENSHOT: Graph showing "Industrial Manufacturing" → "CO2 Emissions" relationship]`

**Source**: Industrial Manufacturing (Activity)
**Target**: CO2 Emissions (Factor)
**Relationship**: Causes
**Result**: Arrow from activity to factor showing causation

---

## Data Upload

### Supported Formats

#### JSON Format
**Screenshot Placeholder**: `[SCREENSHOT: File upload dialog with JSON file selected]`

The application supports two JSON formats:

**Direct Graph Format**:
```json
{
  "nodes": [
    {"id": "act1", "name": "Activity 1", "type": "activity"},
    {"id": "fact1", "name": "Factor 1", "type": "factor"}
  ],
  "edges": [
    {"source": "act1", "target": "fact1", "relationship": "causes"}
  ]
}
```

**Tabular Format**:
```json
[
  {
    "source": "Activity 1",
    "source_type": "activity",
    "target": "Factor 1", 
    "target_type": "factor",
    "relation": "causes"
  }
]
```

#### CSV Format
**Screenshot Placeholder**: `[SCREENSHOT: CSV file structure example]`

Required columns:
- `source`: Source entity name
- `source_type`: Type of source entity
- `target`: Target entity name
- `target_type`: Type of target entity
- `relation`: Relationship type

### Upload Process
**Screenshot Placeholder**: `[SCREENSHOT: Upload form with file selected]`

1. Click "Choose File" in the "Upload Data" section
2. Select your JSON or CSV file
3. Click "Upload" to process the data
4. The graph updates automatically with the new data

### Upload Results
**Screenshot Placeholder**: `[SCREENSHOT: Success message after successful upload]`

- **Success**: "Data uploaded successfully!" message
- **Error**: Specific error message explaining the issue
- **Graph Update**: New nodes and relationships appear in the visualization

---

## Loading Sample Data

### Quick Start with Sample Data
**Screenshot Placeholder**: `[SCREENSHOT: Navigation bar with "Load Sample Data" button highlighted]`

1. Click the "Load Sample Data" button in the navigation bar
2. The application loads a pre-built environmental impact network

### Sample Data Content
**Screenshot Placeholder**: `[SCREENSHOT: Graph showing sample data with all node types visible]`

The sample data includes:

**Activities**:
- Industrial Manufacturing
- Deforestation
- Agricultural Runoff

**Factors**:
- CO2 Emissions
- Water Pollution
- Soil Erosion

**Locations**:
- Amazon Rainforest
- Ganges River
- Industrial Zone

**Consequences**:
- Global Warming
- Biodiversity Loss
- Water Contamination

### Sample Relationships
**Screenshot Placeholder**: `[SCREENSHOT: Graph showing multiple relationships between sample entities]`

The sample data demonstrates various relationship types:
- Industrial Manufacturing → CO2 Emissions (causes)
- CO2 Emissions → Global Warming (contributes_to)
- Deforestation → Biodiversity Loss (impacts)
- Agricultural Runoff → Water Pollution (causes)

---

## Querying Impacts

### Understanding Impact Analysis
**Screenshot Placeholder**: `[SCREENSHOT: Query interface with explanation of impact analysis]`

Impact analysis helps you understand:
- What consequences result from a specific activity or factor
- The pathway through which impacts occur
- The chain of cause-and-effect relationships

### Step 1: Select Source Entity
**Screenshot Placeholder**: `[SCREENSHOT: Query form with entity dropdown]`

1. In the "Query Impacts" section, select the entity you want to analyze
2. Choose from any existing entity in the graph

### Step 2: Execute Query
**Screenshot Placeholder**: `[SCREENSHOT: Query button being clicked]`

2. Click "Query Impacts" to analyze the impact pathways

### Step 3: Review Results
**Screenshot Placeholder**: `[SCREENSHOT: Impact analysis results showing multiple paths]`

3. The results show:
   - **Impact Paths**: Complete pathways from source to consequences
   - **Path Details**: Step-by-step relationships
   - **Consequences**: Final environmental outcomes

### Example: Analyzing Industrial Manufacturing
**Screenshot Placeholder**: `[SCREENSHOT: Results showing Industrial Manufacturing impact paths]`

**Query**: Industrial Manufacturing
**Results**:
- **Path 1**: Industrial Manufacturing → CO2 Emissions → Global Warming
- **Path 2**: Industrial Manufacturing → Water Pollution → Water Contamination

### Understanding Results
**Screenshot Placeholder**: `[SCREENSHOT: Detailed explanation of impact path structure]`

Each impact path shows:
- **Source**: Starting entity (activity or factor)
- **Intermediates**: Factors or conditions in the pathway
- **Consequence**: Final environmental outcome
- **Relationships**: How each step connects to the next

---

## Graph Interaction

### Zoom and Pan Controls
**Screenshot Placeholder**: `[SCREENSHOT: Graph with zoom controls highlighted]`

#### Zoom Controls
- **Zoom In (+)**: Enlarge the graph view
- **Zoom Out (-)**: Reduce the graph view
- **Reset**: Return to original view

#### Mouse Controls
- **Mouse Wheel**: Zoom in/out
- **Click and Drag**: Pan around the graph
- **Node Drag**: Move individual nodes

### Node Interaction
**Screenshot Placeholder**: `[SCREENSHOT: Hovering over a node showing tooltip]`

- **Hover**: See node details (name and type)
- **Drag**: Reposition nodes manually
- **Click**: Select nodes (future feature)

### Graph Layout
**Screenshot Placeholder**: `[SCREENSHOT: Force-directed layout with nodes positioned automatically]`

The graph uses force-directed layout:
- **Automatic Positioning**: Nodes arrange themselves for optimal viewing
- **Relationship Visualization**: Arrows show direction and type of relationships
- **Color Coding**: Different colors for different entity types
- **Dynamic Updates**: Layout adjusts as you add new entities

### Responsive Design
**Screenshot Placeholder**: `[SCREENSHOT: Application on different screen sizes]`

The interface adapts to different screen sizes:
- **Desktop**: Full layout with all panels visible
- **Tablet**: Responsive layout with collapsible panels
- **Mobile**: Optimized for touch interaction

---

## Advanced Features

### Data Export
**Screenshot Placeholder**: `[SCREENSHOT: Export functionality (future feature)]`

*Future Feature*: Export your graph data in various formats:
- JSON graph format
- CSV relationship format
- Graph visualization images
- Impact analysis reports

### Advanced Queries
**Screenshot Placeholder**: `[SCREENSHOT: Advanced query interface (future feature)]`

*Future Feature*: More sophisticated analysis:
- Multi-step impact analysis
- Impact strength quantification
- Temporal analysis
- Geographic filtering

### Collaboration Features
**Screenshot Placeholder**: `[SCREENSHOT: Collaboration interface (future feature)]`

*Future Feature*: Team collaboration:
- Shared workspaces
- Real-time collaboration
- Version control
- Comment and annotation system

---

## Troubleshooting

### Common Issues and Solutions

#### Graph Not Loading
**Screenshot Placeholder**: `[SCREENSHOT: Error message when graph fails to load]`

**Problem**: Graph visualization doesn't appear
**Solutions**:
- Refresh the page
- Check browser console for errors
- Ensure JavaScript is enabled
- Try a different browser

#### Entity Addition Fails
**Screenshot Placeholder**: `[SCREENSHOT: Error message when adding entity fails]`

**Problem**: "Add Entity" button doesn't work
**Solutions**:
- Check that all required fields are filled
- Ensure entity name is unique
- Verify entity type is selected
- Check for special characters in names

#### Relationship Creation Issues
**Screenshot Placeholder**: `[SCREENSHOT: Error message when creating relationship fails]`

**Problem**: Can't create relationships
**Solutions**:
- Ensure both source and target entities exist
- Check that relationship type is selected
- Verify entities are different (no self-loops)
- Check for duplicate relationships

#### File Upload Problems
**Screenshot Placeholder**: `[SCREENSHOT: File upload error message]`

**Problem**: File upload fails
**Solutions**:
- Check file format (JSON or CSV only)
- Verify file structure matches requirements
- Ensure file size is reasonable (< 10MB)
- Check for encoding issues (use UTF-8)

#### Query Returns No Results
**Screenshot Placeholder**: `[SCREENSHOT: "No impacts found" message]`

**Problem**: Impact analysis returns no results
**Solutions**:
- Verify the source entity exists
- Check that relationships are properly created
- Ensure there are consequence nodes in the graph
- Verify the graph has connected components

### Performance Tips

#### Large Graphs
**Screenshot Placeholder**: `[SCREENSHOT: Performance optimization tips]`

For graphs with many nodes:
- Use zoom to focus on specific areas
- Group related entities together
- Use meaningful entity names
- Limit the number of relationships per entity

#### Browser Optimization
- Use modern browsers (Chrome, Firefox, Safari, Edge)
- Close unnecessary browser tabs
- Clear browser cache if experiencing issues
- Disable browser extensions that might interfere

### Getting Help

#### Error Messages
**Screenshot Placeholder**: `[SCREENSHOT: Help section with error code explanations]`

All error messages include:
- **Error Code**: For technical support
- **Description**: Human-readable explanation
- **Suggested Action**: Steps to resolve the issue

#### Support Resources
- **Documentation**: This user guide
- **Sample Data**: Use "Load Sample Data" for examples
- **Test Suite**: Run tests to verify functionality
- **GitHub Repository**: Source code and issues

---

## Best Practices

### Data Organization
**Screenshot Placeholder**: `[SCREENSHOT: Well-organized graph example]`

1. **Use Descriptive Names**: Clear, specific entity names
2. **Group Related Entities**: Organize by theme or location
3. **Consistent Naming**: Follow naming conventions
4. **Document Relationships**: Use appropriate relationship types

### Graph Design
**Screenshot Placeholder**: `[SCREENSHOT: Clean graph layout example]`

1. **Start Simple**: Begin with core entities and relationships
2. **Add Incrementally**: Build complexity gradually
3. **Validate Connections**: Ensure relationships make sense
4. **Test Queries**: Verify impact analysis works correctly

### Data Quality
**Screenshot Placeholder**: `[SCREENSHOT: Data validation example]`

1. **Check for Duplicates**: Avoid redundant entities
2. **Verify Relationships**: Ensure logical connections
3. **Test Impact Paths**: Validate causal chains
4. **Document Sources**: Keep track of data origins

---

## Conclusion

The Environmental Impact Network Knowledge Graph application provides a powerful platform for modeling and analyzing environmental relationships. By following this guide, you can effectively:

- **Create**: Build comprehensive environmental impact networks
- **Visualize**: Explore complex relationships through interactive graphs
- **Analyze**: Understand causal pathways and consequences
- **Share**: Export and communicate environmental insights

The application's intuitive interface and robust functionality make it accessible to both technical and non-technical users, enabling effective environmental impact analysis and decision-making.

---

**Next Steps**:
1. Start with sample data to understand the interface
2. Create your own environmental network
3. Experiment with different relationship types
4. Analyze impact pathways for your entities
5. Export and share your findings

For technical support or feature requests, please refer to the project documentation or GitHub repository. 