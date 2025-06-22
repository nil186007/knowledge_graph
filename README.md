# Environmental Impact Network

A web-based Knowledge Graph application for modeling and visualizing relationships between environmental factors, human activities, geographic locations, and ecological consequences.

## Features

- Interactive visualization of environmental impact relationships
- Add and manage nodes (activities, factors, locations, consequences)
- Create relationships between nodes
- Query impact paths
- Upload data via CSV/JSON files
- Load sample data for demonstration

## Project Structure

```
.
├── knowledge_graph_app.py    # Main Flask application
├── requirements.txt          # Python dependencies
├── sample_data.json         # Sample data for demonstration
├── static/
│   ├── css/
│   │   └── style.css        # Custom styling
│   └── js/
│       └── graph.js         # D3.js visualization and interactions
└── templates/
    └── index.html           # Main application interface
```

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nil186007/knowledge_graph.git
cd knowledge_graph
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated.

2. Start the Flask application:
```bash
python knowledge_graph_app.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Troubleshooting Common Issues

### Port 5000 Already in Use
If you see the error "Address already in use" for port 5000:

1. Find processes using port 5000:
```bash
# On macOS/Linux:
lsof -i :5000 | grep LISTEN

# On Windows:
netstat -ano | findstr :5000
```

2. Kill the processes:
```bash
# On macOS/Linux:
kill -9 <process_id>

# On Windows:
taskkill /PID <process_id> /F
```

3. Restart the Flask application

### PyArrow Warning
If you see a warning about PyArrow:
```bash
pip install pyarrow
```

### Virtual Environment Issues
If you encounter issues with the virtual environment:
```bash
# Remove existing environment
rm -rf venv  # On macOS/Linux
rmdir /s /q venv  # On Windows

# Create new environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Usage Guide

### Loading Sample Data
1. Click the "Load Sample Data" button in the navigation bar
2. The graph will automatically update with sample nodes and relationships

### Adding Nodes
1. Fill in the node details in the "Add Node" form:
   - ID: Unique identifier (e.g., "activity_1")
   - Type: Select from Activity, Environmental Factor, Geographic Area, or Consequence
   - Name: Descriptive name for the node
2. Click "Add Node"

### Creating Relationships
1. Use the "Add Edge" form to create relationships:
   - Select source and target nodes from dropdowns
   - Choose relationship type (causes, affects, occurs_in, contributes_to, impacts)
2. Click "Add Edge"

### Querying Impacts
1. Select a node from the dropdown in the "Query Impacts" section
2. Click "Query Impacts"
3. View the results showing all consequences and their paths

### Uploading Data
1. Prepare your data in CSV or JSON format
2. Use the "Upload Data" section to import your file
3. The graph will update automatically with the new data

## Data Format Examples

### Node Format
```json
{
    "id": "activity_1",
    "type": "activity",
    "name": "Industrial Manufacturing"
}
```

### Edge Format
```json
{
    "source": "activity_1",
    "target": "factor_1",
    "relationship": "causes"
}
```

## Technologies Used

- Backend:
  - Flask (Python web framework)
  - NetworkX (Graph manipulation)
  - Pandas (Data processing)

- Frontend:
  - D3.js (Graph visualization)
  - Bootstrap (UI components)
  - JavaScript (Interactive features)
