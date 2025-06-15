// Initialize the graph visualization
let svg, simulation;
let nodes = [], links = [];

// Set up the SVG container
function initGraph() {
    // Clear any existing SVG
    d3.select('#graph').selectAll('*').remove();
    
    const container = document.getElementById('graph');
    const width = container.clientWidth;
    const height = Math.max(400, container.clientHeight); // Minimum height of 400px

    // Set container height
    container.style.height = height + 'px';

    svg = d3.select('#graph')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])
        .attr('style', 'max-width: 100%; height: auto;');

    // Add tooltip
    const tooltip = d3.select('body')
        .append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('padding', '5px')
        .style('border', '1px solid #ddd')
        .style('border-radius', '3px');

    // Initialize force simulation
    simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id).distance(150))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(60));

    // Create link group
    const link = svg.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#999')
        .style('stroke-opacity', 0.6)
        .style('stroke-width', 2);

    // Create node group
    const node = svg.append('g')
        .attr('class', 'nodes')
        .selectAll('.node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', d => `node ${d.type}`)
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    // Add circles to nodes with different colors based on type
    node.append('circle')
        .attr('r', 10)
        .style('fill', d => {
            switch(d.type) {
                case 'activity': return '#ff7f0e';
                case 'factor': return '#1f77b4';
                case 'location': return '#2ca02c';
                case 'consequence': return '#d62728';
                default: return '#999';
            }
        });

    // Add labels to nodes
    node.append('text')
        .attr('dx', 15)
        .attr('dy', 4)
        .text(d => d.name)
        .style('font-size', '12px')
        .style('font-family', 'Arial');

    // Add tooltip events
    node.on('mouseover', function(event, d) {
        tooltip.transition()
            .duration(200)
            .style('opacity', .9);
        tooltip.html(`Type: ${d.type}<br/>Name: ${d.name}`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
        tooltip.transition()
            .duration(500)
            .style('opacity', 0);
    });

    // Update simulation
    simulation.nodes(nodes).on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    simulation.force('link').links(links);
}

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

// Update graph data
function updateGraph() {
    fetch('/api/get_graph')
        .then(response => response.json())
        .then(data => {
            nodes = data.nodes;
            links = data.edges;
            initGraph();
            updateSelects();
        })
        .catch(error => console.error('Error:', error));
}

// Update select dropdowns
function updateSelects() {
    const nodeSelects = ['sourceNode', 'targetNode', 'queryNode'];
    nodeSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        select.innerHTML = '';
        nodes.forEach(node => {
            const option = document.createElement('option');
            option.value = node.id;
            option.text = `${node.name} (${node.type})`;
            select.appendChild(option);
        });
    });
}

// Load sample data
function loadSampleData() {
    fetch('/api/load_sample_data', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            updateGraph();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Form submission handlers
document.getElementById('nodeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const nodeType = document.getElementById('nodeType').value;
    const nodeName = document.getElementById('nodeName').value;
    const nodeId = `${nodeType}_${Date.now()}`;

    fetch('/api/add_node', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: nodeId,
            type: nodeType,
            name: nodeName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            updateGraph();
            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('edgeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const source = document.getElementById('sourceNode').value;
    const target = document.getElementById('targetNode').value;
    const relationship = document.getElementById('relationship').value;

    fetch('/api/add_edge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            source: source,
            target: target,
            relationship: relationship
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            updateGraph();
            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('dataFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file to upload');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    console.log('Uploading file:', file.name);  // Debug log

    fetch('/api/upload_data', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Response status:', response.status);  // Debug log
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);  // Debug log
        if (data.message) {
            updateGraph();
            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Upload error:', error);  // Debug log
        alert('Error uploading file: ' + error.message);
    });
});

document.getElementById('queryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const source = document.getElementById('queryNode').value;
    const resultsDiv = document.getElementById('queryResults');

    fetch(`/api/query_impacts?source=${source}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                resultsDiv.innerHTML = data.map(impact => `
                    <div class="impact-path">
                        <strong>Consequence:</strong> ${impact.consequence}<br>
                        <strong>Path:</strong> ${impact.path.join(' → ')}
                    </div>
                `).join('');
            } else {
                resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            }
        })
        .catch(error => console.error('Error:', error));
});

// Initialize the graph when the page loads
window.addEventListener('load', updateGraph);

// Handle window resize
window.addEventListener('resize', function() {
    const width = document.getElementById('graph').clientWidth;
    const height = document.getElementById('graph').clientHeight;
    svg.attr('width', width).attr('height', height);
    simulation.force('center', d3.forceCenter(width / 2, height / 2));
    simulation.alpha(0.3).restart();
}); 