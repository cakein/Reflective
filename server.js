// server.js - Simple file server for the Feedback Dashboard
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// Configuration
const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

// MIME types
const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.txt': 'text/plain',
    '.log': 'text/plain'
};

// Create the HTTP server
const server = http.createServer((req, res) => {
    // Parse the request URL
    const parsedUrl = url.parse(req.url);
    let pathname = parsedUrl.pathname;
    
    // Normalize the path (default to index.html for root)
    if (pathname === '/' || pathname === '') {
        pathname = '/index.html';
    }
    
    // Determine the file path
    let filePath;
    
    // Check if this is a request for a log file
    if (pathname.startsWith('/output/')) {
        // This is a log file request, use the actual path
        filePath = path.join(__dirname, pathname);
    } else {
        // This is a static file request
        filePath = path.join(PUBLIC_DIR, pathname);
    }
    
    // Get the file extension
    const extname = path.extname(filePath);
    const contentType = MIME_TYPES[extname] || 'application/octet-stream';
    
    // Read the file
    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // File not found
                res.writeHead(404);
                res.end('File not found');
            } else {
                // Server error
                res.writeHead(500);
                res.end(`Server Error: ${err.code}`);
            }
        } else {
            // Success - return the file
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});