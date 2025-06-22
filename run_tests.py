#!/usr/bin/env python3
"""
Test Runner for Knowledge Graph Application
Run specific test categories or all tests
"""

import sys
import unittest
from test_knowledge_graph import TestKnowledgeGraphApp

def run_specific_tests(test_patterns):
    """Run tests that match specific patterns"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for pattern in test_patterns:
        suite.addTests(loader.loadTestsFromName(f'test_knowledge_graph.TestKnowledgeGraphApp.{pattern}'))
    
    return suite

def run_test_category(category):
    """Run tests for a specific category"""
    categories = {
        'basic': [
            'test_index_page',
            'test_api_test_endpoint',
            'test_get_empty_graph'
        ],
        'nodes': [
            'test_add_node_success',
            'test_add_node_missing_fields',
            'test_add_node_invalid_type'
        ],
        'edges': [
            'test_add_edge_success',
            'test_add_edge_missing_source',
            'test_add_edge_invalid_relationship'
        ],
        'data': [
            'test_load_sample_data',
            'test_upload_json_data',
            'test_upload_csv_data'
        ],
        'query': [
            'test_query_impacts_success',
            'test_query_impacts_no_source',
            'test_query_impacts_invalid_source'
        ],
        'workflow': [
            'test_complete_workflow',
            'test_graph_consistency'
        ],
        'errors': [
            'test_error_handling'
        ]
    }
    
    if category not in categories:
        print(f"Unknown category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return None
    
    return run_specific_tests(categories[category])

def main():
    """Main test runner"""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [all|basic|nodes|edges|data|query|workflow|errors|specific_test_name]")
        print("\nCategories:")
        print("  all        - Run all tests")
        print("  basic      - Basic functionality tests")
        print("  nodes      - Node management tests")
        print("  edges      - Edge management tests")
        print("  data       - Data loading and upload tests")
        print("  query      - Impact querying tests")
        print("  workflow   - Complete workflow tests")
        print("  errors     - Error handling tests")
        print("  specific   - Run a specific test (e.g., test_add_node_success)")
        return
    
    test_type = sys.argv[1]
    
    if test_type == 'all':
        # Run all tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestKnowledgeGraphApp)
    elif test_type in ['basic', 'nodes', 'edges', 'data', 'query', 'workflow', 'errors']:
        # Run category tests
        suite = run_test_category(test_type)
        if suite is None:
            return
    else:
        # Run specific test
        suite = run_specific_tests([test_type])
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary for '{test_type}':")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    if result.failures or result.errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main() 