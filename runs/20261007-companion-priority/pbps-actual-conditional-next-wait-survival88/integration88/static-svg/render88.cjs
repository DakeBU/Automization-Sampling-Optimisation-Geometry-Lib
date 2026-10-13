const sharp=require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
sharp('docs/module-graph.svg').png().toFile('runs/20261007-companion-priority/pbps-actual-conditional-next-wait-survival88/integration88/static-svg/module-graph.png').then(()=>process.stdout.write('rendered SVG\n')).catch(e=>{process.stderr.write(String(e));process.exit(1);});
