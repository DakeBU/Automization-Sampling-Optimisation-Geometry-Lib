// Static SVG rasterization only; no browser automation or page claims.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const sharp = require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const out = 'runs/20261007-companion-priority/pbps-actual-nonaccumulation78/integration78/static-svg';
async function main() {
  fs.mkdirSync(out);
  const input = 'docs/module-graph.svg';
  const output = path.join(out, 'module-graph.png');
  await sharp(input, {density:144}).png().toFile(output);
  fs.writeFileSync(path.join(out, 'render.json'), JSON.stringify({
    input, output,
    input_sha256: crypto.createHash('sha256').update(fs.readFileSync(input)).digest('hex'),
    output_sha256: crypto.createHash('sha256').update(fs.readFileSync(output)).digest('hex'),
    renderer: 'bundled sharp/libvips SVG rasterizer',
    browser_used: false, page_visual_acceptance: false, viewed_by_root: false,
  }, null, 2) + '\n');
  console.log(output);
}
main().catch(e => { console.error(e); process.exitCode = 1; });
