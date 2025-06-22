# Knowledge Graph Application - Test Documentation

## Overview

This document describes the comprehensive test suite for the Environmental Impact Network Knowledge Graph application. The test suite covers all major functionality and ensures the application works correctly across different scenarios.

## Test Structure

### Test Files
- `test_knowledge_graph.py` - Main test suite with all test cases
- `run_tests.py` - Test runner script for running specific test categories
- `test_data.json` - Sample test data for upload testing

### Test Categories

#### 1. Basic Functionality Tests (`basic`)
- **test_index_page**: Verifies the main page loads correctly
- **test_api_test_endpoint**: Tests the API health check endpoint
- **test_get_empty_graph**: Ensures empty graph returns correct structure

#### 2. Node Management Tests (`nodes`)
- **test_add_node_success**: Tests successful node addition
- **test_add_node_missing_fields**: Tests error handling for missing required fields
- **test_add_node_invalid_type**: Tests validation of node types

#### 3. Edge Management Tests (`edges`)
- **test_add_edge_success**: Tests successful edge creation between nodes
- **test_add_edge_missing_source**: Tests error handling for non-existent source nodes
- **test_add_edge_invalid_relationship**: Tests validation of relationship types

#### 4. Data Loading Tests (`data`)
- **test_load_sample_data**: Tests loading pre-defined sample data
- **test_upload_json_data**: Tests uploading JSON format data
- **test_upload_csv_data**: Tests uploading CSV format data

#### 5. Query Functionality Tests (`query`)
- **test_query_impacts_success**: Tests successful impact path queries
- **test_query_impacts_no_source**: Tests error handling for missing source parameter
- **test_query_impacts_invalid_source**: Tests error handling for non-existent source nodes

#### 6. Workflow Tests (`workflow`)
- **test_complete_workflow**: Tests end-to-end workflow (add nodes → add edges → query impacts)
- **test_graph_consistency**: Tests that graph operations maintain data consistency

#### 7. Error Handling Tests (`errors`)
- **test_error_handling**: Tests various error conditions and edge cases

## Running Tests

### Prerequisites
- Flask application server running
- All required dependencies installed
- Python 3.7+ environment

### Test Execution

#### Run All Tests
```bash
python run_tests.py all
```

#### Run Specific Test Categories
```bash
# Basic functionality
python run_tests.py basic

# Node management
python run_tests.py nodes

# Edge management
python run_tests.py edges

# Data loading
python run_tests.py data

# Query functionality
python run_tests.py query

# Complete workflow
python run_tests.py workflow

# Error handling
python run_tests.py errors
```

#### Run Individual Tests
```bash
python run_tests.py test_add_node_success
```

### Test Output

The test runner provides:
- Detailed test execution logs
- Success/failure status for each test
- Summary statistics
- Error details for failed tests

Example output:
```
==================================================
Test Summary for 'all':
Tests run: 18
Failures: 0
Errors: 0
Success rate: 100.0%
```

## Test Coverage

### API Endpoints Tested
- `GET /` - Main page
- `GET /api/test` - Health check
- `GET /api/get_graph` - Retrieve graph data
- `POST /api/add_node` - Add new node
- `POST /api/add_edge` - Add new edge
- `POST /api/load_sample_data` - Load sample data
- `POST /api/upload_data` - Upload data files
- `GET /api/query_impacts` - Query impact paths

### Data Formats Tested
- **JSON Graph Format**: Direct graph structure with nodes and edges
- **CSV Format**: Tabular data with source, target, and relationship columns
- **Sample Data**: Pre-defined environmental impact data

### Error Scenarios Tested
- Missing required fields
- Invalid data types
- Non-existent nodes
- File upload errors
- Invalid file formats
- NetworkX path finding errors

## Test Data

### Sample Data Structure
The test suite uses realistic environmental impact data including:
- **Activities**: Industrial Manufacturing, Deforestation, Agricultural Runoff
- **Factors**: CO2 Emissions, Water Pollution, Soil Erosion
- **Locations**: Amazon Rainforest, Ganges River, Industrial Zone
- **Consequences**: Global Warming, Biodiversity Loss, Water Contamination

### Test Data Files
- `sample_data.json` - Main sample data for testing
- `test_data.json` - Additional test data for upload testing

## Validation Criteria

### Node Validation
- ✅ Valid node types: activity, factor, location, consequence
- ✅ Required fields: id, name, type
- ✅ Unique node IDs
- ✅ Proper data storage in NetworkX graph

### Edge Validation
- ✅ Valid relationship types: causes, affects, occurs_in, contributes_to, impacts
- ✅ Source and target nodes must exist
- ✅ Proper edge storage with relationship attributes
- ✅ Bidirectional relationship validation

### Graph Consistency
- ✅ Node count accuracy
- ✅ Edge count accuracy
- ✅ Data integrity across operations
- ✅ Proper cleanup between tests

### Query Validation
- ✅ Correct path finding algorithms
- ✅ Impact path completeness
- ✅ Error handling for invalid queries
- ✅ Performance with large graphs

## Performance Considerations

### Test Execution Time
- Individual tests: < 0.1 seconds
- Category tests: < 0.5 seconds
- Full test suite: < 2 seconds

### Memory Usage
- Tests use isolated graph instances
- Proper cleanup after each test
- No memory leaks detected

## Continuous Integration

### Automated Testing
The test suite is designed for CI/CD integration:
- Exit codes for automated failure detection
- Detailed logging for debugging
- Isolated test environments
- No external dependencies

### Test Maintenance
- Tests are self-contained
- Clear test descriptions
- Easy to extend with new test cases
- Regular validation of test data

## Troubleshooting

### Common Issues
1. **Flask Server Not Running**: Ensure the Flask app is running before executing tests
2. **Import Errors**: Check that all dependencies are installed
3. **File Permission Issues**: Ensure test files are readable/writable
4. **NetworkX Version**: Verify NetworkX compatibility

### Debug Mode
Tests include detailed logging to help identify issues:
- Request/response logging
- Graph state tracking
- Error message details
- Data validation steps

## Future Enhancements

### Planned Test Additions
- Performance benchmarks
- Load testing with large datasets
- Browser automation tests
- API rate limiting tests
- Security vulnerability tests

### Test Improvements
- Parallel test execution
- Test data generation
- Coverage reporting
- Performance profiling 