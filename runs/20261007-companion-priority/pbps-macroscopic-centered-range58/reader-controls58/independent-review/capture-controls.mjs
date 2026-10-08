import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';

const site=path.resolve('_site'), output=path.resolve('runs/20261007-companion-priority/pbps-macroscopic-centered-range58/reader-controls58/independent-review/browser');
fs.mkdirSync(output);
const downloads=path.join(output,'downloads');fs.mkdirSync(downloads);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const server=http.createServer((req,res)=>{
 let p=path.resolve(site,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!p.startsWith(site+path.sep)){res.writeHead(403);res.end();return;}
 try{if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');
  const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml'};
  res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(fs.readFileSync(p));
 }catch{res.writeHead(404);res.end();}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/`, profile=path.join(output,'chrome-profile');
const stderr=fs.openSync(path.join(output,'chrome.stderr.log'),'w');
const browser=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',[
 '--headless=new','--disable-extensions','--disable-default-apps','--disable-gpu','--no-first-run','--no-default-browser-check',
 '--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore',stderr],windowsHide:true});
const exit=new Promise(r=>browser.once('exit',(code,signal)=>r({code,signal})));let ws,id=0;
const pending=new Map(), events=[], records=[];
function call(method,params={},sessionId){return new Promise((resolve,reject)=>{
 const request=++id,timer=setTimeout(()=>{pending.delete(request);reject(new Error('CDP timeout '+method));},45000);
 pending.set(request,{resolve:v=>{clearTimeout(timer);resolve(v);},reject:e=>{clearTimeout(timer);reject(e);}});
 ws.send(JSON.stringify({id:request,method,params,...(sessionId?{sessionId}:{})}));
});}
let success=false;
try{
 let ports;for(let i=0;i<150;i++){try{ports=fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').trim().split('\n');break;}catch{await delay(100);}}
 if(!ports)throw Error('Owned browser port unavailable');
 ws=new WebSocket(`ws://127.0.0.1:${ports[0]}${ports[1]}`);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else if(m.method?.startsWith('Browser.download'))events.push(m);};


 const target=await call('Target.createTarget',{url:'about:blank'});
 const {sessionId}=await call('Target.attachToTarget',{targetId:target.targetId,flatten:true});
 await call('Page.enable',{},sessionId);await call('Runtime.enable',{},sessionId);
 await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1800,deviceScaleFactor:1,mobile:false},sessionId);
 async function evaluate(expression){const x=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true},sessionId);if(x.exceptionDetails)throw Error(JSON.stringify(x.exceptionDetails));return x.result.value;}
 async function navigate(rel){await call('Page.navigate',{url:base+rel},sessionId);await call('Page.bringToFront',{},sessionId);
  await evaluate(`(async()=>{for(let i=0;i<300;i++){if(document.readyState==='complete')break;await new Promise(r=>setTimeout(r,100));}if(document.readyState!=='complete')throw Error('page readiness');if(window.MathJax?.startup?.promise)await window.MathJax.startup.promise;await document.fonts.ready;return true;})()`);
 }

 await navigate('example-cases/samplewiki/companions/proximal-bouncy-particle.html');
 const observed=await evaluate(`(()=>{const ids=['l2-pullback-range','pbps-macroscopic-centered-range','pbps-centered-macro-defect-gap'];return ids.map(id=>({id,panes:['statement','proof'].map(role=>{const p=document.getElementById(id).querySelector('.inline-lean-'+role);return {role,initiallyFolded:!p.open,copyLabel:p.querySelector('[data-lean-copy]').textContent,downloadLabel:p.querySelector('a[download]').textContent};})}));})()`);
 if(observed.some(r=>r.panes.some(p=>!p.initiallyFolded)))throw Error('fresh pane not folded');
 const geometry=await evaluate(`(async()=>{const p=document.getElementById('pbps-macroscopic-centered-range').querySelector('.inline-lean-statement');p.open=true;await new Promise(r=>setTimeout(r,300));const a=p.querySelector(':scope > .lean-source-actions');for(let i=0;i<4;i++){window.scrollTo(0,window.scrollY+a.getBoundingClientRect().top-120);await new Promise(r=>setTimeout(r,300));}const r=a.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)throw Error('actual actions offscreen');return {publicationID:'pbps-macroscopic-centered-range',role:'statement',actions:{x:r.x,y:r.y,width:r.width,height:r.height},viewport:{width:innerWidth,height:innerHeight},scrollY,copyLabel:a.querySelector('button').textContent,downloadLabel:a.querySelector('a').textContent,downloadHref:a.querySelector('a').getAttribute('href'),layoutRechecked:true};})()`);
 const png=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},sessionId);fs.writeFileSync(path.join(output,'companion-controls-corrected.png'),Buffer.from(png.data,'base64'));
 success=true;await call('Browser.close');ws.close();ws=undefined;const closed=await exit;
 fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({status:'INDEPENDENT_CORRECTED_COMPANION_VISUAL_CAPTURE',observed,geometry,ownedBrowserExit:closed,ownedBrowserPID:browser.pid,noClipboardAccess:true,noDownloadClick:true},null,2)+'\n');
}finally{
 if(ws){try{await call('Browser.close');}catch{browser.kill();}ws.close();}else if(browser.exitCode===null)browser.kill();
 const browserExit=await exit;fs.closeSync(stderr);await new Promise(r=>server.close(r));
 const resolved=fs.realpathSync(profile);if(!resolved.startsWith(fs.realpathSync(output)+path.sep))throw Error('ephemeral profile scope violation');fs.rmSync(resolved,{recursive:true,force:true});
 fs.writeFileSync(path.join(output,'closure.json'),JSON.stringify({status:'CLOSED',success,wrapperPID:process.pid,ownedBrowserPID:browser.pid,actualBrowserExit:browserExit,HTTPServer:'CLOSED',Browser:'CLOSED',ephemeralOwnedProfileRemovedAfterActualExit:true,compiler:'NOT_STARTED_CLOSED'},null,2)+'\n');
}
console.log('Independent corrected controls capture PASS; owned browser/server CLOSED.');
