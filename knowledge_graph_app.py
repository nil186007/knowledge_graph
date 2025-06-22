from flask import Flask, request, jsonify, render_template
import networkx as nx
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Initialize the knowledge graph
G = nx.DiGraph()

# Node types
NODE_TYPES = {
    'activity': 'Activity',
    'factor': 'Environmental Factor',
    'location': 'Geographic Area',
    'consequence': 'Consequence'
}

# Relationship types
RELATIONSHIP_TYPES = [
    'causes',
    'affects',
    'occurs_in',
    'contributes_to',
    'impacts'
]

@app.route('/')
def index():
    print("Serving index page")  # Debug print
    return render_template('index.html')

@app.route('/api/add_node', methods=['POST'])
def add_node():
    try:
        data = request.json
        print(f"Received node data: {data}")  # Debug print
        
        node_id = data.get('id')
        node_type = data.get('type')
        node_name = data.get('name')
        
        print(f"Parsed: id={node_id}, type={node_type}, name={node_name}")  # Debug print
        
        if not all([node_id, node_type, node_name]):
            return jsonify({'error': 'Missing required fields: id, type, name'}), 400
        
        if node_type not in NODE_TYPES:
            return jsonify({'error': f'Invalid node type. Must be one of: {list(NODE_TYPES.keys())}'}), 400
        
        # Add the node to the graph
        G.add_node(node_id, type=node_type, name=node_name)
        print(f"Added node: {node_id} ({node_type}: {node_name})")  # Debug print
        print(f"Graph now has {len(G.nodes())} nodes")  # Debug print
        
        return jsonify({'message': 'Node added successfully'})
    
    except Exception as e:
        print(f"Error adding node: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_edge', methods=['POST'])
def add_edge():
    try:
        data = request.json
        print(f"Received edge data: {data}")  # Debug print
        
        source = data.get('source')
        target = data.get('target')
        relationship = data.get('relationship')
        
        print(f"Parsed: source={source}, target={target}, relationship={relationship}")  # Debug print
        
        if not all([source, target, relationship]):
            return jsonify({'error': 'Missing required fields: source, target, relationship'}), 400
        
        if relationship not in RELATIONSHIP_TYPES:
            return jsonify({'error': f'Invalid relationship type. Must be one of: {RELATIONSHIP_TYPES}'}), 400
        
        # Check if both nodes exist
        source_exists = any(G.nodes[node]['name'] == source for node in G.nodes())
        target_exists = any(G.nodes[node]['name'] == target for node in G.nodes())
        
        if not source_exists:
            return jsonify({'error': f'Source node "{source}" not found'}), 404
        if not target_exists:
            return jsonify({'error': f'Target node "{target}" not found'}), 404
        
        # Find the actual node IDs
        source_id = None
        target_id = None
        for node_id, node_data in G.nodes(data=True):
            if node_data['name'] == source:
                source_id = node_id
            if node_data['name'] == target:
                target_id = node_id
        
        # Add the edge to the graph
        G.add_edge(source_id, target_id, relationship=relationship)
        print(f"Added edge: {source_id} -> {target_id} ({relationship})")  # Debug print
        print(f"Graph now has {len(G.edges())} edges")  # Debug print
        
        return jsonify({'message': 'Edge added successfully'})
    
    except Exception as e:
        print(f"Error adding edge: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_graph', methods=['GET'])
def get_graph():
    graph_data = {
        'nodes': [],
        'edges': []
    }
    
    for node in G.nodes(data=True):
        node_data = {
            'id': node[0],
            'name': node[1].get('name', node[0]),  # Use ID as name if not set
            'type': node[1].get('type', 'unknown')  # Use 'unknown' if type not set
        }
        graph_data['nodes'].append(node_data)
    
    for edge in G.edges(data=True):
        edge_data = {
            'source': edge[0],
            'target': edge[1],
            'relationship': edge[2].get('relationship', 'unknown')  # Use 'unknown' if relationship not set
        }
        graph_data['edges'].append(edge_data)
    
    return jsonify(graph_data)

@app.route('/api/query_impacts', methods=['GET'])
def query_impacts():
    source_name = request.args.get('source')
    if not source_name:
        return jsonify({'error': 'Source node required'}), 400
    
    print(f"Querying impacts for source: {source_name}")  # Debug print
    print(f"Available nodes: {[G.nodes[node]['name'] for node in G.nodes()]}")  # Debug print
    
    # Find the node ID by name
    source_id = None
    for node_id, node_data in G.nodes(data=True):
        if node_data['name'] == source_name:
            source_id = node_id
            break
    
    if source_id is None:
        return jsonify({'error': f'Source node "{source_name}" not found'}), 404
    
    print(f"Found source node ID: {source_id}")  # Debug print
    
    impacts = []
    try:
        for target in nx.descendants(G, source_id):
            if G.nodes[target]['type'] == 'consequence':
                path = nx.shortest_path(G, source_id, target)
                impacts.append({
                    'consequence': G.nodes[target]['name'],
                    'path': [G.nodes[node]['name'] for node in path]
                })
        
        print(f"Found {len(impacts)} impact paths")  # Debug print
        return jsonify(impacts)
    
    except nx.NetworkXNoPath:
        print("No path found to consequences")  # Debug print
        return jsonify([])
    except Exception as e:
        print(f"Error finding impacts: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        print(f"Processing file: {file.filename}")  # Debug print
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            print(f"CSV loaded: {len(df)} rows")  # Debug print
        elif file.filename.endswith('.json'):
            try:
                # Read the file content as string first
                content = file.read().decode('utf-8')
                print("Received content:", content[:200] + "..." if len(content) > 200 else content)  # Debug print
                
                # Parse the JSON content
                data = json.loads(content)
                print("Parsed data type:", type(data))  # Debug print
                
                if isinstance(data, dict) and 'nodes' in data and 'edges' in data:
                    # Direct graph format
                    print("Direct graph format detected")  # Debug print
                    # Clear existing graph
                    G.clear()
                    
                    # Add nodes
                    for node in data['nodes']:
                        G.add_node(node['id'], type=node['type'], name=node['name'])
                    
                    # Add edges
                    for edge in data['edges']:
                        G.add_edge(edge['source'], edge['target'], relationship=edge['relationship'])
                    
                    print(f"Graph updated: {len(G.nodes())} nodes, {len(G.edges())} edges")  # Debug print
                    return jsonify({'message': 'Data uploaded successfully'})
                elif isinstance(data, list):
                    # List of objects format
                    df = pd.DataFrame(data)
                    print(f"JSON list loaded: {len(df)} rows")  # Debug print
                else:
                    return jsonify({'error': 'Invalid JSON format. Expected graph with nodes/edges or list of objects'}), 400
                    
            except json.JSONDecodeError as e:
                print("JSON decode error:", str(e))  # Debug print
                return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Unsupported file format. Please use .csv or .json'}), 400
        
        # Process DataFrame format (for CSV or JSON list)
        if 'df' in locals():
            # Clear existing graph
            G.clear()
            
            # Process the data and add to graph
            for _, row in df.iterrows():
                try:
                    # Add source node
                    source_id = f"{row['source_type']}_{row['source'].replace(' ', '_')}"
                    G.add_node(source_id, type=row['source_type'], name=row['source'])
                    
                    # Add target node
                    target_id = f"{row['target_type']}_{row['target'].replace(' ', '_')}"
                    G.add_node(target_id, type=row['target_type'], name=row['target'])
                    
                    # Add edge
                    G.add_edge(source_id, target_id, relationship=row['relation'])
                except KeyError as e:
                    print("Key error:", str(e))  # Debug print
                    return jsonify({'error': f'Missing required field: {str(e)}. Expected columns: source, source_type, target, target_type, relation'}), 400
                except Exception as e:
                    print("Row processing error:", str(e))  # Debug print
                    return jsonify({'error': f'Error processing row: {str(e)}'}), 400
            
            print(f"Graph updated: {len(G.nodes())} nodes, {len(G.edges())} edges")  # Debug print
        
        return jsonify({'message': 'Data uploaded successfully'})
    
    except Exception as e:
        print("General error:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 400

@app.route('/api/load_sample_data', methods=['POST'])
def load_sample_data():
    try:
        print("Loading sample data...")  # Debug print
        
        # Read sample data from file
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
        
        print(f"Sample data loaded: {len(sample_data['nodes'])} nodes, {len(sample_data['edges'])} edges")  # Debug print
        
        # Clear existing graph
        G.clear()
        
        # Add nodes
        for node in sample_data['nodes']:
            G.add_node(node['id'], type=node['type'], name=node['name'])
        
        # Add edges
        for edge in sample_data['edges']:
            G.add_edge(edge['source'], edge['target'], relationship=edge['relationship'])
        
        print(f"Graph updated: {len(G.nodes())} nodes, {len(G.edges())} edges")  # Debug print
        
        return jsonify({'message': 'Sample data loaded successfully'})
    
    except FileNotFoundError:
        print("sample_data.json file not found")  # Debug print
        return jsonify({'error': 'Sample data file not found'}), 404
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")  # Debug print
        return jsonify({'error': f'Invalid JSON in sample data: {str(e)}'}), 400
    except Exception as e:
        print(f"Error loading sample data: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 400

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working', 'nodes': len(G.nodes()), 'edges': len(G.edges())})

if __name__ == '__main__':
    app.run(debug=True)
