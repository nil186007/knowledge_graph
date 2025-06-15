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
    return render_template('index.html')

@app.route('/api/add_node', methods=['POST'])
def add_node():
    data = request.json
    node_id = data.get('id')
    node_type = data.get('type')
    node_name = data.get('name')
    
    if not all([node_id, node_type, node_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if node_type not in NODE_TYPES:
        return jsonify({'error': 'Invalid node type'}), 400
    
    G.add_node(node_id, type=node_type, name=node_name)
    return jsonify({'message': 'Node added successfully'})

@app.route('/api/add_edge', methods=['POST'])
def add_edge():
    data = request.json
    source = data.get('source')
    target = data.get('target')
    relationship = data.get('relationship')
    
    if not all([source, target, relationship]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if relationship not in RELATIONSHIP_TYPES:
        return jsonify({'error': 'Invalid relationship type'}), 400
    
    G.add_edge(source, target, relationship=relationship)
    return jsonify({'message': 'Edge added successfully'})

@app.route('/api/get_graph', methods=['GET'])
def get_graph():
    graph_data = {
        'nodes': [],
        'edges': []
    }
    
    for node in G.nodes(data=True):
        graph_data['nodes'].append({
            'id': node[0],
            'type': node[1]['type'],
            'name': node[1]['name']
        })
    
    for edge in G.edges(data=True):
        graph_data['edges'].append({
            'source': edge[0],
            'target': edge[1],
            'relationship': edge[2]['relationship']
        })
    
    return jsonify(graph_data)

@app.route('/api/query_impacts', methods=['GET'])
def query_impacts():
    source = request.args.get('source')
    if not source:
        return jsonify({'error': 'Source node required'}), 400
    
    if source not in G:
        return jsonify({'error': 'Source node not found'}), 404
    
    impacts = []
    for target in nx.descendants(G, source):
        if G.nodes[target]['type'] == 'consequence':
            path = nx.shortest_path(G, source, target)
            impacts.append({
                'consequence': G.nodes[target]['name'],
                'path': [G.nodes[node]['name'] for node in path]
            })
    
    return jsonify(impacts)

@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.json'):
            try:
                # Read the file content as string first
                content = file.read().decode('utf-8')
                print("Received content:", content)  # Debug print
                # Parse the JSON content
                data = json.loads(content)
                print("Parsed data:", data)  # Debug print
                if not isinstance(data, list):
                    return jsonify({'error': 'JSON must be a list of objects'}), 400
                df = pd.DataFrame(data)
                print("DataFrame:", df)  # Debug print
            except json.JSONDecodeError as e:
                print("JSON decode error:", str(e))  # Debug print
                return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
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
                return jsonify({'error': f'Missing required field: {str(e)}'}), 400
            except Exception as e:
                print("Row processing error:", str(e))  # Debug print
                return jsonify({'error': f'Error processing row: {str(e)}'}), 400
        
        return jsonify({'message': 'Data uploaded successfully'})
    
    except Exception as e:
        print("General error:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 400

@app.route('/api/load_sample_data', methods=['POST'])
def load_sample_data():
    try:
        # Read sample data from file
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
        
        # Clear existing graph
        G.clear()
        
        # Add nodes
        for node in sample_data['nodes']:
            G.add_node(node['id'], type=node['type'], name=node['name'])
        
        # Add edges
        for edge in sample_data['edges']:
            G.add_edge(edge['source'], edge['target'], relationship=edge['relationship'])
        
        return jsonify({'message': 'Sample data loaded successfully'})
    
    except Exception as e:
        print(f"Error loading sample data: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
