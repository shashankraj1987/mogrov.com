// Preview the published static output without a Python installation.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..', 'public');
const port = Number(process.env.PORT || 8000);
const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json',
  '.md': 'text/markdown; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
};

http.createServer((request, response) => {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
  } catch {
    response.writeHead(400).end('Bad request');
    return;
  }

  const oldDevTrack = {
    '/devtrack/wiki.html': '/wiki/devtrack/',
    '/devtrack/download.html': '/downloads/devtrack/',
    '/devtrack/privacy.html': '/wiki/devtrack/privacy.html',
    '/download/devtrack': '/downloads/devtrack/',
    '/download/devtrack/': '/downloads/devtrack/',
  };
  if (oldDevTrack[pathname]) {
    response.writeHead(301, { Location: oldDevTrack[pathname] + new URL(request.url, 'http://localhost').search }).end();
    return;
  }
  if (pathname === '/runtime-narrative/docs' || pathname === '/runtime-narrative/docs/') {
    response.writeHead(301, { Location: '/wiki/runtime-narrative/' }).end();
    return;
  }
  if (pathname.startsWith('/runtime-narrative/docs/')) {
    response.writeHead(301, { Location: pathname.replace('/runtime-narrative/docs/', '/wiki/runtime-narrative/') }).end();
    return;
  }

  let file = path.resolve(root, '.' + pathname);
  if (file !== root && !file.startsWith(root + path.sep)) {
    response.writeHead(403).end('Forbidden');
    return;
  }
  try {
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    response.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(response);
  } catch {
    response.writeHead(404).end('Not found');
  }
}).listen(port, '127.0.0.1', () => {
  console.log(`Serving ${root} at http://127.0.0.1:${port}/`);
});
