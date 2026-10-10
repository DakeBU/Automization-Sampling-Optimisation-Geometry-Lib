const fs = require('fs');
const crypto = require('crypto');
const sharp = require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const dir='runs/20261007-companion-priority/pbps-actual-small-time-continuity82/integration82/static-svg';
const input='docs/module-graph.svg', output=dir+'/module-graph.png';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
  const raw=fs.readFileSync(input);
  await sharp(raw,{density:90}).resize({width:1800,withoutEnlargement:true}).png().toFile(output);
  fs.writeFileSync(dir+'/render.json',JSON.stringify({input,output,input_sha256:hash(raw),output_sha256:hash(fs.readFileSync(output)),renderer:'bundled sharp/libvips SVG rasterizer',browser_used:false,page_visual_acceptance:false,viewed_by_root:false},null,2)+'\n');
  process.stdout.write(output+'\n');
})();
