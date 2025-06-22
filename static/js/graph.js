let graphData = { nodes: [], edges: [] };
let simulation;
let svg, g;
let zoom;

// Initialize the graph
function initGraph() {
    const graphContainer = document.getElementById('graph');
    const width = graphContainer.clientWidth;
    const height = graphContainer.clientHeight;

    // Clear existing SVG
    d3.select('#graph svg').remove();

    // Create SVG with zoom behavior
    svg = d3.select('#graph')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('background-color', '#f8f9fa');

    // Add zoom behavior
    zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {
            g.attr('transform', event.transform);
        });

    svg.call(zoom);

    // Create main group for graph elements
    g = svg.append('g');

    // Add zoom controls
    window.zoomIn = () => {
        svg.transition().duration(300).call(zoom.scaleBy, 1.3);
    };

    window.zoomOut = () => {
        svg.transition().duration(300).call(zoom.scaleBy, 1 / 1.3);
    };

    window.resetZoom = () => {
        svg.transition().duration(300).call(zoom.transform, d3.zoomIdentity);
    };

    // Load initial graph data
    loadGraphData();
}

// Load graph data from server
function loadGraphData() {
    fetch('/api/get_graph')
        .then(response => response.json())
        .then(data => {
            graphData = data;
            updateGraph();
        })
        .catch(error => {
            console.error('Error loading graph data:', error);
        });
}

// Update the graph visualization
function updateGraph() {
    if (!svg) return;

    // Clear existing elements
    g.selectAll('*').remove();

    // Create arrow marker
    svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 20)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke', 'none');

    // Create links
    const link = g.append('g')
        .selectAll('line')
        .data(graphData.edges)
        .enter().append('line')
        .attr('class', 'link')
        .attr('stroke', '#999')
        .attr('stroke-width', 2)
        .attr('marker-end', 'url(#arrowhead)');

    // Create nodes
    const node = g.append('g')
        .selectAll('g')
        .data(graphData.nodes)
        .enter().append('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    // Add circles to nodes
    node.append('circle')
        .attr('r', 8)
        .attr('fill', d => getNodeColor(d.type));

    // Add labels to nodes
    node.append('text')
        .attr('dx', 12)
        .attr('dy', '.35em')
        .text(d => d.name)
        .style('font-size', '12px')
        .style('fill', '#333');

    // Add tooltips
    node.append('title')
        .text(d => `${d.name} (${d.type})`);

    // Create force simulation
    simulation = d3.forceSimulation(graphData.nodes)
        .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(svg.node().clientWidth / 2, svg.node().clientHeight / 2))
        .force('collision', d3.forceCollide().radius(30));

    // Update positions on tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    updateNodeSelects();
}

// Get color for node type
function getNodeColor(type) {
    const colors = {
        'activity': '#ff7f0e',
        'factor': '#2ca02c',
        'location': '#1f77b4',
        'consequence': '#d62728'
    };
    return colors[type] || '#999';
}

// Update node select dropdowns
function updateNodeSelects() {
    const nodes = graphData.nodes.map(n => n.name);
    const selects = ['sourceNode', 'targetNode', 'queryNode'];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Select a node...</option>';
            nodes.forEach(node => {
                const option = document.createElement('option');
                option.value = node;
                option.textContent = node;
                select.appendChild(option);
            });
        }
    });
}

// Add new node
document.getElementById('nodeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const type = document.getElementById('nodeType').value;
    const name = document.getElementById('nodeName').value;
    
    if (name && type) {
        const newNode = {
            id: name,
            name: name,
            type: type
        };
        
        // Send to server
        fetch('/api/add_node', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newNode)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadGraphData(); // Reload graph data
                this.reset();
                alert('Node added successfully!');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding node');
        });
    }
});

// Add new edge
document.getElementById('edgeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const source = document.getElementById('sourceNode').value;
    const target = document.getElementById('targetNode').value;
    const relationship = document.getElementById('relationship').value;
    
    if (source && target && relationship) {
        const newEdge = {
            source: source,
            target: target,
            relationship: relationship
        };
        
        // Send to server
        fetch('/api/add_edge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newEdge)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadGraphData(); // Reload graph data
                this.reset();
                alert('Edge added successfully!');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding edge');
        });
    }
});

// Upload data
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const file = document.getElementById('dataFile').files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/api/upload_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            loadGraphData(); // Reload graph data
            this.reset();
            alert('Data uploaded successfully!');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading data');
    });
});

// Query impacts
document.getElementById('queryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const queryNode = document.getElementById('queryNode').value;
    if (!queryNode) return;
    
    fetch(`/api/query_impacts?source=${encodeURIComponent(queryNode)}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                displayImpacts(data);
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error querying impacts');
        });
});

// Display impacts
function displayImpacts(impacts) {
    const resultsDiv = document.getElementById('queryResults');
    
    if (impacts.length === 0) {
        resultsDiv.innerHTML = '<p class="text-muted">No impacts found for this entity.</p>';
        return;
    }
    
    let html = '<h6>Impact Paths:</h6>';
    impacts.forEach((impact, index) => {
        html += `<div class="impact-path">
            <strong>Path ${index + 1}:</strong> ${impact.path.join(' → ')}
        </div>`;
    });
    
    resultsDiv.innerHTML = html;
}

// Load sample data
function loadSampleData() {
    fetch('/api/load_sample_data', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            loadGraphData(); // Reload graph data
            //alert('Sample data loaded successfully!');
        } else {
            alert('Error loading sample data: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading sample data');
    });
}

// Handle window resize
window.addEventListener('resize', () => {
    if (svg) {
        const graphContainer = document.getElementById('graph');
        const width = graphContainer.clientWidth;
        const height = graphContainer.clientHeight;
        
        svg.attr('width', width).attr('height', height);
        
        // Update force simulation center
        if (simulation) {
            simulation.force('center', d3.forceCenter(width / 2, height / 2));
            simulation.alpha(0.3).restart();
        }
    }
});

// Initialize graph when page loads
document.addEventListener('DOMContentLoaded', initGraph); 