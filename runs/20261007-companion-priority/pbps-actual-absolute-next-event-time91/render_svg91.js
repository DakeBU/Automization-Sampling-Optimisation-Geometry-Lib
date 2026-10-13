const fs = require('fs');
const sharp = require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const output = 'runs/20261007-companion-priority/pbps-actual-absolute-next-event-time91/integration91/static-svg';
fs.mkdirSync(output, {recursive:true});
sharp('docs/module-graph.svg').png().toFile(output+'/module-graph.png').then(info=>console.log(JSON.stringify(info)));
