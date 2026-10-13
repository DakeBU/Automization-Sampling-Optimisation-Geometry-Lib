const fs=require('fs');
const crypto=require('crypto');
const sharp=require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const out='runs/20261007-companion-priority/pbps-actual-physical-time-law81/integration81/static-svg';
fs.mkdirSync(out,{recursive:true});
const input='docs/module-graph.svg';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 await sharp(input,{density:160}).resize({width:2100}).png().toFile(out+'/module-graph.png');
 fs.writeFileSync(out+'/render.json',JSON.stringify({input,output:out+'/module-graph.png',input_sha256:hash(input),output_sha256:hash(out+'/module-graph.png'),renderer:'bundled sharp/libvips SVG rasterizer',browser_used:false,page_visual_acceptance:false,viewed_by_root:false},null,2)+'\n');
 console.log('Rendered affected static SVG; actual viewing pending.');
})().catch(e=>{console.error(e);process.exit(1)});
