const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const out = 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/integration106/static-svg';
fs.mkdirSync(out, { recursive: true });
sharp('docs/module-graph.svg', { density: 120 }).resize({ width: 1800 }).png().toFile(path.join(out, 'module-graph106.png')).then(() => console.log('Rendered current shared overview; visual inspection pending.'));
