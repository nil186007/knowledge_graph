import json
import requests

def load_sample_data():
    # Read the sample data
    with open('sample_data.json', 'r') as f:
        data = json.load(f)
    
    # Add nodes
    for node in data['nodes']:
        response = requests.post(
            'http://localhost:5000/api/add_node',
            json=node
        )
        if response.status_code != 200:
            print(f"Error adding node {node['name']}: {response.json().get('error')}")
    
    # Add edges
    for edge in data['edges']:
        response = requests.post(
            'http://localhost:5000/api/add_edge',
            json=edge
        )
        if response.status_code != 200:
            print(f"Error adding edge {edge['source']} -> {edge['target']}: {response.json().get('error')}")

if __name__ == '__main__':
    load_sample_data() 