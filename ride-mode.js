/* Aankomstmelding voor precies de gekozen laadlocatie; geen achtergrondbelofte. */
(function(root){
'use strict';
function targetFromChoice(choice,destination){
 if(!choice||choice.destination!==String(destination).trim())return null;
 const old=String(choice.key||'').split('|').slice(-2),coords=choice.coords||{lat:Number(old[0]),lng:Number(old[1])};
 if(!Number.isFinite(coords.lat)||!Number.isFinite(coords.lng)||coords.lat<50||coords.lat>54||coords.lng<3||coords.lng>8)return null;
 return {key:choice.key,name:String(choice.name||'Gekozen laadlocatie'),coords:{lat:coords.lat,lng:coords.lng}};
}
function readAvailability(feature,now=Date.now()){
 const unknown=detail=>({state:'unknown',detail});
 const p=feature?.properties;if(!p||!Array.isArray(p.availabilities))return unknown('Geen passende rechtstreekse NDW-status ontvangen.');
 const entries=p.availabilities.filter(a=>a.connector_type==='IEC_62196_T2'&&String(a.power_type||'').startsWith('AC'));
 if(!entries.length)return unknown('Geen AC Type 2-status ontvangen.');
 let free=0,total=0;
 for(const a of entries){if(a.available==null||a.total==null||a.available===''||a.total==='')return unknown('Onvolledige beschikbaarheidsgegevens.');const f=Number(a.available),t=Number(a.total);if(!Number.isInteger(f)||!Number.isInteger(t)||f<0||t<0||f>t)return unknown('Onjuiste beschikbaarheidsaantallen.');free+=f;total+=t}
 if(!total)return unknown('Geen AC Type 2-aansluiting bevestigd.');
 const updated=Date.parse(p.last_updated),age=now-updated;
 if(!Number.isFinite(updated)||age<0||age>900000)return {...unknown('NDW-status ouder dan 15 minuten of tijdstip onbekend.'),free,total,updated:Number.isFinite(updated)?updated:null};
 return {state:free>0?'available':'unavailable',free,total,updated,detail:free>0?'NDW meldt een vrije AC Type 2-aansluiting.':'NDW meldt geen vrije AC Type 2-aansluiting.'};
}
function createController(o){
 let active=false,watchId=null,generation=0,busy=false,lastScan=null,lastPosition=null,lock=null,target=null,announced=null,lastSpoken=-Infinity;
 const now=o.now||Date.now,visible=()=>o.document.visibilityState==='visible';
 const status=text=>o.status(text,active);
 function say(text){try{o.speak(text)}catch(e){status('Gesproken melding mislukt. Controleer het geluid wanneer je stilstaat.')}}
 async function acquireLock(token){
  if(!o.wakeLock){status('Aankomstmelding actief voor '+target.name+'. Houd de planner zichtbaar en ontgrendeld.');return}
  try{const value=await o.wakeLock.request('screen');if(!active||token!==generation||!visible()){await value.release();return}lock=value;status('Aankomstmelding actief voor '+target.name+' · scherm wakker.');value.addEventListener?.('release',()=>{if(lock===value){lock=null;if(active)status(visible()?'Schermvergrendeling niet tegengehouden. Houd de planner zichtbaar.':'Aankomstmelding onderbroken: planner niet zichtbaar.')}})}catch(e){if(active&&token===generation)status('Scherm wakker houden niet gelukt. Aankomstmelding werkt alleen met zichtbare, ontgrendelde planner.')}
 }
 function stop(message='Ritstand gestopt.'){
  active=false;generation++;busy=false;if(watchId!==null){o.geo?.clearWatch(watchId);watchId=null}if(lock){const old=lock;lock=null;Promise.resolve(old.release()).catch(()=>{})}o.cancelSpeech?.();status(message);
 }
 async function position(p){
  if(!active||!visible()||busy)return;
  const at=now(),lat=p?.coords?.latitude,lng=p?.coords?.longitude,accuracy=p?.coords?.accuracy;
  if(!Number.isFinite(lat)||!Number.isFinite(lng)||Math.abs(lat)>90||Math.abs(lng)>180||!Number.isFinite(accuracy)||accuracy<0||accuracy>75||!Number.isFinite(p.timestamp)||Math.abs(at-p.timestamp)>20000){status('Wachten op recente GPS met maximaal 75 m opgegeven afwijking.');return}
  const coords={lat,lng};
  if(lastScan!==null&&(at-lastScan<15000||(o.distance(lastPosition,coords)<100&&at-lastScan<45000)))return;
  const token=generation;busy=true;lastScan=at;lastPosition=coords;const current=()=>active&&generation===token&&visible();
  try{
   const result=await o.scan(coords,target,current);if(!current())return;
   if(!Number.isFinite(result?.driveMeters)||result.driveMeters<0)throw Error('Geen bevestigde rijafstand ontvangen.');
   o.render({...result,target});
   if(result.driveMeters>2000){status('Nog '+(result.driveMeters/1000).toLocaleString('nl-NL',{maximumFractionDigits:1})+' km rijden naar '+target.name+'. Melding volgt rond 2 km.');return}
   const availability=result.availability||{state:'unknown',detail:'Status niet bevestigd.'};
   const text=availability.state==='available'?'Vrij gemeld':availability.state==='unavailable'?'Niet vrij gemeld':'Beschikbaarheid niet te bevestigen';status(text+' bij '+target.name+'. '+availability.detail);
   if(availability.state===announced||at-lastSpoken<30000)return;
   const message=availability.state==='available'?'Er is volgens NDW een vrije Type 2 aansluiting.':availability.state==='unavailable'?'Er is volgens NDW geen vrije Type 2 aansluiting.':'De beschikbaarheid kon niet actueel worden bevestigd.';
   say('Je nadert je gekozen laadlocatie, '+target.name+'. '+message+' Beschikbaarheid kan vóór aankomst veranderen.');announced=availability.state;lastSpoken=at;
  }catch(e){if(current())status('Rijafstand naar de gekozen laadpaal kon niet worden gecontroleerd. Geen aankomstmelding bevestigd: '+String(e.message||e))}finally{if(generation===token)busy=false}
 }
 async function start(value){
  if(active)return;
  if(!o.geo||!o.canSpeak){status('Locatie of gesproken meldingen niet ondersteund in deze browser.');return}
  if(!visible()){status('Open de planner op de voorgrond voordat je start.');return}
  if(!value?.coords||!Number.isFinite(value.coords.lat)||!Number.isFinite(value.coords.lng)||!value.key){status('Kies eerst een laadpaal via Dit is mijn keuze onder Laden.');return}
  target={...value,coords:{...value.coords}};active=true;generation++;const token=generation;lastScan=null;lastPosition=null;announced=null;lastSpoken=-Infinity;
  say('Aankomstmelding gestart voor '+target.name+'. Rond twee kilometer rijafstand controleer ik de beschikbaarheid.');status('Wachten op locatietoestemming en GPS.');
  try{watchId=o.geo.watchPosition(p=>{position(p)},e=>{if(active&&token===generation)stop(e.code===1?'Locatietoestemming geweigerd. Ritstand gestopt.':'GPS niet beschikbaar. Ritstand gestopt; controleer dit wanneer je stilstaat.')},{enableHighAccuracy:true,maximumAge:10000,timeout:20000})}catch(e){stop('Locatie volgen kon niet starten.');return}
  if(active&&token===generation)await acquireLock(token);
 }
 o.document.addEventListener?.('visibilitychange',()=>{if(!active)return;if(!visible()){o.cancelSpeech?.();status('Aankomstmelding onderbroken: planner niet zichtbaar. Geen betrouwbare achtergrondmeldingen.')}else{lastScan=null;status('Wachten op nieuwe GPS voor de gekozen laadpaal.');acquireLock(generation)}});
 return {start,stop,position,isActive:()=>active};
}
const api={targetFromChoice,readAvailability,createController};root.RideMode=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
