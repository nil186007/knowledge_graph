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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## Usage

### Loading Sample Data
- Click the "Load Sample Data" button in the navigation bar to load the demonstration data.

### Adding Nodes
1. Fill in the node details in the "Add Node" form:
   - ID: Unique identifier
   - Type: Select from Activity, Environmental Factor, Geographic Area, or Consequence
   - Name: Descriptive name for the node

### Creating Relationships
1. Use the "Add Edge" form to create relationships:
   - Select source and target nodes
   - Choose relationship type (causes, affects, occurs_in, contributes_to, impacts)

### Querying Impacts
1. Select a node from the dropdown in the "Query Impacts" section
2. Click "Query Impacts" to see all consequences and their paths

### Uploading Data
- Use the "Upload Data" section to import data from CSV or JSON files
- File format should match the sample data structure

## Data Format

### Node Format
```json
{
    "id": "unique_id",
    "type": "activity|factor|location|consequence",
    "name": "Node Name"
}
```

### Edge Format
```json
{
    "source": "source_node_id",
    "target": "target_node_id",
    "relationship": "causes|affects|occurs_in|contributes_to|impacts"
}
```

## Troubleshooting

### Port 5000 Already in Use
If you see the error "Address already in use" for port 5000:

1. Find processes using port 5000:
```bash
lsof -i :5000 | grep LISTEN
```

2. Kill the processes:
```bash
kill -9 <process_id>
```

3. Restart the Flask application

### PyArrow Warning
If you see a warning about PyArrow:
- This is a deprecation warning and doesn't affect functionality
- To resolve, install PyArrow:
```bash
pip install pyarrow
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

## Contributing

Feel free to submit issues and enhancement requests! 