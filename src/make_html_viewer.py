"""Create a single-file browser viewer with the current GLB embedded."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parents[1]
glb = base64.b64encode((ROOT / "exports" / "visual_model.glb").read_bytes()).decode("ascii")
html = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hubble Pan / Tilt Stand — Interactive Assembly</title>
<style>
:root{color-scheme:dark;--bg:#111820;--panel:#1b2631;--line:#314253;--text:#edf3f8;--muted:#a7b5c2;--accent:#ffad55;--blue:#72b7e7}
*{box-sizing:border-box}html,body{height:100%;margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}body{display:grid;grid-template-columns:320px 1fr;overflow:hidden}
aside{background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column;min-height:0;z-index:2}.brand{padding:20px 18px 15px;border-bottom:1px solid var(--line)}.brand h1{font-size:18px;line-height:1.2;margin:0 0 7px}.brand p{margin:0;color:var(--muted);font-size:12px}.actions{display:flex;gap:8px;padding:13px 14px;border-bottom:1px solid var(--line)}button{font:inherit;color:var(--text);background:#293a49;border:1px solid #466074;border-radius:7px;padding:8px 11px;cursor:pointer}button:hover{background:#354b5d}button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}.groups{overflow:auto;padding:7px 10px 15px;flex:1}.group{border-bottom:1px solid #2a3946;padding:3px 0}.group-head{display:flex;align-items:center;gap:9px;padding:8px 5px;font-weight:650}.group-head input{accent-color:var(--accent)}.group-name{flex:1}.focus-btn{padding:3px 8px;font-size:11px;color:var(--blue);background:transparent;border:0}.focus-btn:hover{background:#2a3946}.parts{padding:0 0 5px 29px;color:var(--muted);font-size:12px}.parts summary{cursor:pointer;padding:3px 0 5px}.part-list{list-style:none;padding:0;margin:1px 0 3px}.part-list li{display:flex;align-items:flex-start;gap:7px;padding:4px 3px}.part-list input{accent-color:var(--accent);margin-top:3px}.part-list label{cursor:pointer}.selection{border-top:1px solid var(--line);padding:13px 16px;min-height:74px}.selection b{display:block;color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.07em}.selection span{color:var(--muted);font-size:12px}.note{padding:0 16px 14px;color:#91a1af;font-size:11px}.stage{position:relative;min-width:0;min-height:0;background:#dce4ea}.stage canvas{display:block;width:100%;height:100%;touch-action:none}.help{position:absolute;left:16px;top:14px;padding:8px 11px;background:#101820dc;border:1px solid #ffffff22;border-radius:8px;color:#d9e4ed;font-size:12px;pointer-events:none}.badge{position:absolute;right:16px;top:14px;padding:7px 10px;background:#101820dc;border:1px solid #ffffff22;border-radius:8px;color:#d9e4ed;font-size:11px;pointer-events:none}.loading{position:absolute;inset:0;display:grid;place-items:center;color:#13202b;font-weight:650}.error{color:#8b1c1c;background:#fff;padding:20px;max-width:620px;border-radius:10px}
@media(max-width:760px){body{grid-template-columns:1fr;grid-template-rows:42% 58%}.stage{grid-row:1}.stage canvas{height:100%}aside{grid-row:2;border-right:0;border-top:1px solid var(--line)}.brand{padding:10px 13px}.brand h1{font-size:16px}.brand p{display:none}.actions{padding:7px 10px}.groups{padding-top:3px}.selection{min-height:58px;padding:8px 12px}.note{display:none}}
</style>
</head>
<body>
<aside>
  <header class="brand"><h1>Hubble Pan / Tilt Stand</h1><p>Interactive assembly map · drag to orbit · scroll to zoom · click a part to identify it</p></header>
  <div class="actions"><button id="reset">Reset view</button><button id="all">Show all parts</button></div>
  <div class="groups" id="groups"><div style="padding:14px;color:var(--muted)">Loading the 3D assembly…</div></div>
  <div class="selection"><b id="selected-name">Nothing selected</b><span id="selected-desc">Click a part in the model or focus it from the list.</span></div>
  <div class="note">The Hubble and LEGO interface are illustrative approximations. The side cross geometry and clearances need checking against the physical set.</div>
</aside>
<main class="stage" id="stage"><div class="loading" id="loading">Preparing interactive model…</div><div class="help">Left drag: orbit · Wheel: zoom · Right drag: pan · Click: identify</div><div class="badge">105 mm nominal side-pivot spacing</div></main>
<script id="embedded-glb" type="application/octet-stream">__MODEL_BASE64__</script>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const stage=document.getElementById('stage'), loading=document.getElementById('loading');
const scene=new THREE.Scene(); scene.background=new THREE.Color(0xdce4ea);
const camera=new THREE.PerspectiveCamera(42,1,0.1,5000); camera.up.set(0,1,0);
const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.outputColorSpace=THREE.SRGBColorSpace; renderer.toneMapping=THREE.ACESFilmicToneMapping; renderer.toneMappingExposure=1.15; stage.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xffffff,0x64707c,2.1));
const key=new THREE.DirectionalLight(0xffffff,2.4);key.position.set(-380,520,460);scene.add(key);
const fill=new THREE.DirectionalLight(0xc4ddff,1.25);fill.position.set(420,180,-300);scene.add(fill);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.07;controls.screenSpacePanning=true;controls.minDistance=90;controls.maxDistance=1500;
const raycaster=new THREE.Raycaster(), pointer=new THREE.Vector2();let modelRoot,homeTarget=new THREE.Vector3(),homePosition=new THREE.Vector3(),currentHighlight=null,originalMaterials=null,meshes=[];
const readable={base:'Base shell',pan_deck:'Pan deck / yoke mounting plate',pan_drive_adapter:'Pan servo horn adapter — 14 mm M3 pattern',pan_servo_horn_reference:'Pan 25T metal horn plate (reference)',pan_servo_reference:'Pan servo envelope',servo_retainer_A:'Pan servo retainer rail A',servo_retainer_B:'Pan servo retainer rail B',turntable_bearing_envelope:'Turntable bearing envelope',yoke_left:'Tilt yoke — motor side',yoke_right:'Tilt yoke — passive side',tilt_bearing_left:'608 bearing — drive side',tilt_servo_horn_reference:'25T metal horn plate (reference)',tilt_drive_socket:'Printed LEGO cross adapter + M3 flange',tilt_passive_printed_pivot:'Printed passive pivot — runs in yoke bore',tilt_servo_bracket:'Tilt servo bracket',tilt_servo_retainer:'Add-on servo case cradle',tilt_servo_retainer_lid:'Servo cradle lid',tilt_servo_reference:'Tilt servo envelope'};
function niceName(n){if(readable[n])return readable[n];return n.replace(/\s*\|\s*/g,' — ').replace(/\.\d+$/,'');}
const rules=[
  ['Base & pan servo',n=>n==='base'||n.startsWith('servo_retainer_')||n==='pan_servo_reference'],
  ['Pan platform & 25T horn',n=>n==='pan_deck'||n==='pan_drive_adapter'||n==='pan_servo_horn_reference'||n==='turntable_bearing_envelope'],
  ['U-shaped tilt yoke',n=>n==='yoke_left'||n==='yoke_right'],
  ['Driven side — motor, horn, cradle & cross socket',n=>n==='tilt_bearing_left'||n==='tilt_drive_socket'||n==='tilt_servo_horn_reference'||n==='tilt_servo_bracket'||n==='tilt_servo_retainer'||n==='tilt_servo_retainer_lid'||n==='tilt_servo_reference'||n.toLowerCase().includes('drive')],
  ['Passive side — printed cross pivot',n=>n==='tilt_passive_printed_pivot'||n.toLowerCase().includes('idler')],
  ['Port solar wing',n=>n.toLowerCase().startsWith('port ')],
  ['Starboard solar wing',n=>n.toLowerCase().startsWith('starboard ')],
  ['Telescope envelope',n=>true]
];
function groupFor(name){for(let i=0;i<rules.length-1;i++)if(rules[i][1](name))return i;return rules.length-1}
function focusObject(obj){const box=new THREE.Box3().setFromObject(obj),center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3()),r=Math.max(size.x,size.y,size.z,20);controls.target.copy(center);const dir=camera.position.clone().sub(controls.target).normalize();camera.position.copy(center).addScaledVector(dir,r*2.5);camera.near=Math.max(.1,r/200);camera.far=5000;camera.updateProjectionMatrix();controls.update();}
function restoreHighlight(){if(!currentHighlight)return;currentHighlight.material=originalMaterials;currentHighlight=null;originalMaterials=null}
function highlight(obj){restoreHighlight();currentHighlight=obj;originalMaterials=obj.material;const mats=Array.isArray(obj.material)?obj.material:[obj.material];const clones=mats.map(m=>{const c=m.clone();if(c.emissive){c.emissive.set(0xffa537);c.emissiveIntensity=.65}return c});obj.material=Array.isArray(obj.material)?clones:clones[0]}
function describe(n){const l=n.toLowerCase();if(l.includes('servo_horn'))return 'Simplified Feetech-compatible 25T horn reference. Four cardinal M3 holes use the 14 mm pitch circle shown in the STS3215 accessory drawing; verify your physical plate.';if(l.includes('tilt_servo_retainer_lid'))return 'Separate lid closes the case cradle with four M3 screws into heat-set inserts.';if(l.includes('tilt_servo_retainer'))return 'Add-on U cradle surrounds the servo case. Its flange uses the existing tilt-bracket slots; longer M3 bolts clamp cradle, bracket and yoke together.';if(l.includes('tilt_drive_socket'))return 'Printed coupling: its inward-facing female LEGO cross bore passes through the journal; its outer flange bolts to the horn with four M3 screws.';if(l.includes('passive_printed_pivot'))return 'Bearing-free passive side: this printed part fills the right yoke’s 22 mm bore, keys onto the opposite LEGO cross feature, and rotates directly against the printed yoke. Its sliding fit needs a physical test.';if(l.includes('cross axle | drive')||l.includes('shoulder | drive'))return 'Motor side: keyed cross-shaped interface transmits tilt torque.';if(l.includes('cross axle | idler')||l.includes('shoulder | idler'))return 'Opposite side: printed cross pivot supports the telescope and rotates in the yoke bore.';if(l.includes('yoke'))return 'One of the two upright arms; the pan deck joins their feet beneath the telescope.';if(l.includes('bearing'))return '608 bearing supports radial load at the tilt axis.';if(l.includes('tilt_servo'))return 'Simplified Feetech STS3215 servo envelope; the real mounting and horn stack need fit checking.';if(l.includes('pan_')||l.includes('turntable'))return 'Pan adapter uses the same 14 mm four-hole 25T horn pattern as the tilt adapter; the four square holes separately attach the pan deck.';if(l==='base')return 'Stationary base. Omit this group when printing only the tilt module.';return 'Approximate display geometry included to make the assembly easier to understand.'}
function buildList(){const host=document.getElementById('groups');host.replaceChildren();const grouped=rules.map(()=>[]);for(const o of meshes)grouped[groupFor(o.name)].push(o);
  rules.forEach((rule,i)=>{if(!grouped[i].length)return;const section=document.createElement('section');section.className='group';const head=document.createElement('div');head.className='group-head';const cb=document.createElement('input');cb.type='checkbox';cb.checked=true;cb.setAttribute('aria-label','Show '+rule[0]);const title=document.createElement('span');title.className='group-name';title.textContent=rule[0];const focus=document.createElement('button');focus.className='focus-btn';focus.textContent='Focus';focus.title='Frame this group';head.append(cb,title,focus);section.append(head);
    const details=document.createElement('details');details.className='parts';const summary=document.createElement('summary');summary.textContent=`Parts (${grouped[i].length})`;details.append(summary);const ul=document.createElement('ul');ul.className='part-list';
    grouped[i].forEach((o,j)=>{const li=document.createElement('li'),partCb=document.createElement('input'),label=document.createElement('label');partCb.type='checkbox';partCb.checked=true;partCb.id=`g${i}p${j}`;label.htmlFor=partCb.id;label.textContent=niceName(o.name);partCb.addEventListener('change',()=>{o.visible=partCb.checked;cb.checked=grouped[i].every(x=>x.visible)});label.addEventListener('click',()=>{highlight(o);focusObject(o);document.getElementById('selected-name').textContent=niceName(o.name);document.getElementById('selected-desc').textContent=describe(o.name)});li.append(partCb,label);ul.append(li)});details.append(ul);section.append(details);
    cb.addEventListener('change',()=>{for(const o of grouped[i])o.visible=cb.checked;for(const inp of ul.querySelectorAll('input'))inp.checked=cb.checked});focus.addEventListener('click',()=>{const v=grouped[i].filter(o=>o.visible);if(!v.length)return;const box=new THREE.Box3();v.forEach(o=>box.expandByObject(o));const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3()),r=Math.max(size.x,size.y,size.z,30);controls.target.copy(center);const dir=camera.position.clone().sub(controls.target).normalize();camera.position.copy(center).addScaledVector(dir,r*1.7);controls.update()});host.append(section);
  });
}
function fail(err){loading.innerHTML='<div class="error"><b>Could not load the viewer.</b><br>'+String(err)+'<br><br>This single-file page loads the Three.js viewer code from jsDelivr, so it needs an internet connection. Reopen the HTML while online.</div>';console.error(err)}
try{
 const raw=atob(document.getElementById('embedded-glb').textContent.trim());const bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
 new GLTFLoader().parse(bytes.buffer,'',gltf=>{
   modelRoot=gltf.scene;scene.add(modelRoot);modelRoot.traverse(o=>{if(!o.isMesh)return;if(o.name==='Ground'){o.visible=false;return}meshes.push(o);o.userData.name=o.name});
   const box=new THREE.Box3();for(const o of meshes)box.expandByObject(o);const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());homeTarget.copy(center);const span=Math.max(size.x,size.y,size.z);homePosition.copy(center).add(new THREE.Vector3(-.9,.8,1.15).normalize().multiplyScalar(span*1.55));controls.target.copy(homeTarget);camera.position.copy(homePosition);camera.near=.1;camera.far=5000;camera.updateProjectionMatrix();controls.update();buildList();loading.remove();
 },fail);
}catch(e){fail(e)}
renderer.domElement.addEventListener('pointerdown',e=>{if(e.button!==0)return;const rect=renderer.domElement.getBoundingClientRect();pointer.x=((e.clientX-rect.left)/rect.width)*2-1;pointer.y=-((e.clientY-rect.top)/rect.height)*2+1;raycaster.setFromCamera(pointer,camera);const hit=raycaster.intersectObjects(meshes.filter(x=>x.visible),false)[0];if(hit){const o=hit.object;highlight(o);document.getElementById('selected-name').textContent=niceName(o.name);document.getElementById('selected-desc').textContent=describe(o.name)}});
document.getElementById('reset').addEventListener('click',()=>{controls.target.copy(homeTarget);camera.position.copy(homePosition);camera.updateProjectionMatrix();controls.update();restoreHighlight();document.getElementById('selected-name').textContent='Nothing selected';document.getElementById('selected-desc').textContent='Click a part in the model or focus it from the list.'});
document.getElementById('all').addEventListener('click',()=>{for(const o of meshes)o.visible=true;for(const c of document.querySelectorAll('.groups input'))c.checked=true});
function resize(){const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()}new ResizeObserver(resize).observe(stage);resize();
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera)});
</script>
</body></html>'''
target = ROOT / "Hubble_Assembly_Viewer.html"
target.write_text(html.replace("__MODEL_BASE64__", glb), encoding="utf-8")
print(f"Wrote {target} ({target.stat().st_size / 1024 / 1024:.2f} MiB)")
