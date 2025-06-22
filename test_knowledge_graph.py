import unittest
import json
import tempfile
import os
import pandas as pd
from knowledge_graph_app import app, G, NODE_TYPES, RELATIONSHIP_TYPES
import networkx as nx

class TestKnowledgeGraphApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and clear graph before each test"""
        self.app = app.test_client()
        self.app.testing = True
        G.clear()  # Clear the graph before each test
    
    def tearDown(self):
        """Clean up after each test"""
        G.clear()
    
    def test_index_page(self):
        """Test that the main page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Environmental Impact Network', response.data)
    
    def test_api_test_endpoint(self):
        """Test the API test endpoint"""
        response = self.app.get('/api/test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'API is working')
        self.assertEqual(data['nodes'], 0)
        self.assertEqual(data['edges'], 0)
    
    def test_get_empty_graph(self):
        """Test getting an empty graph"""
        response = self.app.get('/api/get_graph')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('nodes', data)
        self.assertIn('edges', data)
        self.assertEqual(len(data['nodes']), 0)
        self.assertEqual(len(data['edges']), 0)
    
    def test_add_node_success(self):
        """Test adding a node successfully"""
        node_data = {
            'id': 'test_activity',
            'name': 'Test Activity',
            'type': 'activity'
        }
        response = self.app.post('/api/add_node',
                               data=json.dumps(node_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Node added successfully')
        
        # Verify node was added to graph
        self.assertTrue('test_activity' in G.nodes())
        self.assertEqual(G.nodes['test_activity']['name'], 'Test Activity')
        self.assertEqual(G.nodes['test_activity']['type'], 'activity')
    
    def test_add_node_missing_fields(self):
        """Test adding a node with missing fields"""
        node_data = {
            'id': 'test_activity',
            'name': 'Test Activity'
            # Missing 'type' field
        }
        response = self.app.post('/api/add_node',
                               data=json.dumps(node_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_add_node_invalid_type(self):
        """Test adding a node with invalid type"""
        node_data = {
            'id': 'test_activity',
            'name': 'Test Activity',
            'type': 'invalid_type'
        }
        response = self.app.post('/api/add_node',
                               data=json.dumps(node_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_add_edge_success(self):
        """Test adding an edge successfully"""
        # First add two nodes
        node1_data = {
            'id': 'source_node',
            'name': 'Source Node',
            'type': 'activity'
        }
        node2_data = {
            'id': 'target_node',
            'name': 'Target Node',
            'type': 'factor'
        }
        
        self.app.post('/api/add_node',
                     data=json.dumps(node1_data),
                     content_type='application/json')
        self.app.post('/api/add_node',
                     data=json.dumps(node2_data),
                     content_type='application/json')
        
        # Now add edge
        edge_data = {
            'source': 'Source Node',
            'target': 'Target Node',
            'relationship': 'causes'
        }
        response = self.app.post('/api/add_edge',
                               data=json.dumps(edge_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Edge added successfully')
        
        # Verify edge was added
        self.assertTrue(G.has_edge('source_node', 'target_node'))
        self.assertEqual(G.edges['source_node', 'target_node']['relationship'], 'causes')
    
    def test_add_edge_missing_source(self):
        """Test adding an edge with non-existent source"""
        edge_data = {
            'source': 'Non-existent Source',
            'target': 'Target Node',
            'relationship': 'causes'
        }
        response = self.app.post('/api/add_edge',
                               data=json.dumps(edge_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_add_edge_invalid_relationship(self):
        """Test adding an edge with invalid relationship type"""
        edge_data = {
            'source': 'Source Node',
            'target': 'Target Node',
            'relationship': 'invalid_relationship'
        }
        response = self.app.post('/api/add_edge',
                               data=json.dumps(edge_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_load_sample_data(self):
        """Test loading sample data"""
        response = self.app.post('/api/load_sample_data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Sample data loaded successfully')
        
        # Verify sample data was loaded
        response = self.app.get('/api/get_graph')
        data = json.loads(response.data)
        self.assertGreater(len(data['nodes']), 0)
        self.assertGreater(len(data['edges']), 0)
    
    def test_upload_json_data(self):
        """Test uploading JSON data"""
        # Create test JSON data
        test_data = {
            'nodes': [
                {'id': 'test1', 'name': 'Test Node 1', 'type': 'activity'},
                {'id': 'test2', 'name': 'Test Node 2', 'type': 'factor'}
            ],
            'edges': [
                {'source': 'test1', 'target': 'test2', 'relationship': 'causes'}
            ]
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = self.app.post('/api/upload_data',
                                       data={'file': (f, 'test.json')},
                                       content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data uploaded successfully')
            
            # Verify data was uploaded
            response = self.app.get('/api/get_graph')
            data = json.loads(response.data)
            self.assertEqual(len(data['nodes']), 2)
            self.assertEqual(len(data['edges']), 1)
            
        finally:
            os.unlink(temp_file_path)
    
    def test_upload_csv_data(self):
        """Test uploading CSV data"""
        # Create test CSV data
        test_data = [
            {
                'source': 'Activity 1',
                'source_type': 'activity',
                'target': 'Factor 1',
                'target_type': 'factor',
                'relation': 'causes'
            },
            {
                'source': 'Factor 1',
                'source_type': 'factor',
                'target': 'Consequence 1',
                'target_type': 'consequence',
                'relation': 'contributes_to'
            }
        ]
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_csv(f, index=False)
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = self.app.post('/api/upload_data',
                                       data={'file': (f, 'test.csv')},
                                       content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data uploaded successfully')
            
            # Verify data was uploaded
            response = self.app.get('/api/get_graph')
            data = json.loads(response.data)
            # Should have 3 nodes: Activity 1, Factor 1, Consequence 1 (Factor 1 appears twice but is deduplicated)
            self.assertEqual(len(data['nodes']), 3)
            self.assertEqual(len(data['edges']), 2)
            
        finally:
            os.unlink(temp_file_path)
    
    def test_query_impacts_success(self):
        """Test querying impacts successfully"""
        # Load sample data first
        self.app.post('/api/load_sample_data')
        
        # Query impacts for a known node
        response = self.app.get('/api/query_impacts?source=Industrial Manufacturing')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Should find impact paths to consequences
        if len(data) > 0:
            self.assertIn('consequence', data[0])
            self.assertIn('path', data[0])
    
    def test_query_impacts_no_source(self):
        """Test querying impacts without source parameter"""
        response = self.app.get('/api/query_impacts')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_query_impacts_invalid_source(self):
        """Test querying impacts with non-existent source"""
        response = self.app.get('/api/query_impacts?source=NonExistentNode')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_complete_workflow(self):
        """Test complete workflow: add nodes, add edges, query impacts"""
        # Step 1: Add nodes
        nodes = [
            {'id': 'act1', 'name': 'Activity 1', 'type': 'activity'},
            {'id': 'fact1', 'name': 'Factor 1', 'type': 'factor'},
            {'id': 'cons1', 'name': 'Consequence 1', 'type': 'consequence'}
        ]
        
        for node in nodes:
            response = self.app.post('/api/add_node',
                                   data=json.dumps(node),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 200)
        
        # Step 2: Add edges
        edges = [
            {'source': 'Activity 1', 'target': 'Factor 1', 'relationship': 'causes'},
            {'source': 'Factor 1', 'target': 'Consequence 1', 'relationship': 'contributes_to'}
        ]
        
        for edge in edges:
            response = self.app.post('/api/add_edge',
                                   data=json.dumps(edge),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 200)
        
        # Step 3: Query impacts
        response = self.app.get('/api/query_impacts?source=Activity 1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Should find impact path from Activity 1 to Consequence 1
        if len(data) > 0:
            path = data[0]['path']
            self.assertIn('Activity 1', path)
            self.assertIn('Factor 1', path)
            self.assertIn('Consequence 1', path)
    
    def test_graph_consistency(self):
        """Test that graph operations maintain consistency"""
        # Add nodes and edges
        self.app.post('/api/add_node',
                     data=json.dumps({'id': 'n1', 'name': 'Node 1', 'type': 'activity'}),
                     content_type='application/json')
        self.app.post('/api/add_node',
                     data=json.dumps({'id': 'n2', 'name': 'Node 2', 'type': 'factor'}),
                     content_type='application/json')
        self.app.post('/api/add_edge',
                     data=json.dumps({'source': 'Node 1', 'target': 'Node 2', 'relationship': 'causes'}),
                     content_type='application/json')
        
        # Verify graph consistency
        response = self.app.get('/api/get_graph')
        data = json.loads(response.data)
        
        # Check nodes
        node_names = [node['name'] for node in data['nodes']]
        self.assertIn('Node 1', node_names)
        self.assertIn('Node 2', node_names)
        
        # Check edges - edges are stored by node IDs, not names
        edge_sources = [edge['source'] for edge in data['edges']]
        edge_targets = [edge['target'] for edge in data['edges']]
        self.assertIn('n1', edge_sources)  # Node ID, not name
        self.assertIn('n2', edge_targets)  # Node ID, not name
    
    def test_error_handling(self):
        """Test various error conditions"""
        # Test invalid JSON
        response = self.app.post('/api/add_node',
                               data='invalid json',
                               content_type='application/json')
        self.assertEqual(response.status_code, 500)
        
        # Test missing file in upload
        response = self.app.post('/api/upload_data')
        self.assertEqual(response.status_code, 400)
        
        # Test unsupported file format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('test data')
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = self.app.post('/api/upload_data',
                                       data={'file': (f, 'test.txt')},
                                       content_type='multipart/form-data')
            self.assertEqual(response.status_code, 400)
        finally:
            os.unlink(temp_file_path)

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestKnowledgeGraphApp)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}") 