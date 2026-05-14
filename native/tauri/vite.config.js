import { defineConfig } from 'vite';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..', '..');

export default defineConfig({
  server: {
    host: '127.0.0.1',
    port: 1420,
    strictPort: true,
  },
  plugins: [{
    name: 'ai-desk-meter-runtime-files',
    configureServer(server) {
      server.middlewares.use('/runtime/status.json', (_req, res) => {
        const p = resolve(root, 'runtime', 'status.json');
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Cache-Control', 'no-store');
        if (!existsSync(p)) {
          res.statusCode = 404;
          res.end(JSON.stringify({ runtime_connected: false, muse_connected: false, status: 'No active Muse', mode: 'not connected' }));
          return;
        }
        res.end(readFileSync(p, 'utf8'));
      });
      server.middlewares.use('/docs/index.html', (_req, res) => {
        const p = resolve(root, 'docs', 'index.html');
        res.setHeader('Content-Type', 'text/html');
        res.end(readFileSync(p, 'utf8'));
      });
      server.middlewares.use('/DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html', (_req, res) => {
        const p = resolve(root, 'DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html');
        res.setHeader('Content-Type', 'text/html');
        res.end(readFileSync(p, 'utf8'));
      });
    }
  }]
});
