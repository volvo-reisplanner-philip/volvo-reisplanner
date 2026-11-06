/* Reproduceerbare berekeningen zonder netwerk of opgeslagen sleutels. */
(function(root){
'use strict';
const number=value=>{const text=String(value??'').trim();if(!/^(?:\d+(?:[.,]\d*)?|[.,]\d+)$/.test(text))return 0;const x=Number(text.replace(',','.'));return Number.isFinite(x)&&x>=0?x:0};
function trip(v){
 const n=k=>number(v[k]);
 const out=n('outkm'),back=n('backkm'),cap=v.season==='winter'?61:v.season==='summer'?81:n('manualCapacity');
 const home=Math.min(out+back,n('range'),cap),homeOutbound=Math.min(out,home),remainingHome=home-homeOutbound;
 const extra=Math.min(Math.max(0,back-remainingHome),n('rangeAfter'),Math.max(0,cap-remainingHome));
 const petrolKm=Math.max(0,out-homeOutbound)+Math.max(0,back-remainingHome-extra);
 const usedKwh=extra*n('elecUse')/100,sessionKwh=v.sessionMode==='full'?n('chargeKwh'):usedKwh;
 const hc=home*n('elecUse')/100*n('homePrice'),cc=sessionKwh*n('publicPrice')+(sessionKwh>0?n('startFee'):0),pc=petrolKm*n('fuelUse')/100*n('petrolPrice');
 return {out,back,home,extra,petrolKm,hc,cc,pc,sessionKwh,total:hc+cc+pc};
}
// Vergelijk de volledige betaling op bestemming met dezelfde rit zonder bijladen.
// Energie die overblijft krijgt binnen deze rit geen besparingswaarde.
function chargingAdvice(v){
 const required=['homePrice','range','rangeAfter','outkm','backkm','elecUse','fuelUse','petrolPrice','publicPrice','startFee','chargeKwh'];
 if(required.some(k=>! /^(?:\d+(?:[.,]\d*)?|[.,]\d+)$/.test(String(v[k]??'').trim())))return {kind:'unknown'};
 if(v.season==='manual'&&number(v.manualCapacity)<=0)return {kind:'unknown'};
 const n=k=>number(v[k]),r=trip(v);
 if(n('elecUse')<=0||n('fuelUse')<=0||n('chargeKwh')<=0)return {kind:'unknown'};
 const electricKm=Math.min(r.extra,n('chargeKwh')*100/n('elecUse'));
 const petrolSaved=electricKm*n('fuelUse')/100*n('petrolPrice');
 const sessionCost=n('chargeKwh')*n('publicPrice')+n('startFee');
 const withoutCharging=r.hc+(r.petrolKm+r.extra)*n('fuelUse')/100*n('petrolPrice');
 const withCharging=withoutCharging-petrolSaved+sessionCost,saving=petrolSaved-sessionCost;
 const kind=electricKm===0?'unneeded':Math.abs(saving)<0.005?'equal':saving>0?'charge':'petrol';
 return {kind,electricKm,petrolSaved,sessionCost,withoutCharging,withCharging,saving};
}
function tariff(t,kwh,o={},now=Date.now()){
 if(!t||t.valuta!=='EUR'||!Number.isFinite(kwh)||kwh<=0||!Array.isArray(t.prijsopbouw)||t.prijsopbouw.length!==1)return null;
 // Ignore no restrictions silently: unsupported tariffs remain explicitly unknown.
 for(const [key,after] of [['geldig_vanaf',true],['geldig_tot',false]])if(t[key]){const date=Date.parse(t[key]);if(!Number.isFinite(date)||(after?date>now:date<=now))return null}
 if(t.minimumprijs!=null||t.maximumprijs!=null||(t.type&&!['REGULAR','AD_HOC','AD_HOC_PAYMENT'].includes(t.type)))return null;
 const e=t.prijsopbouw[0],conditions=e.voorwaarden||{};
 if(Object.keys(conditions).some(k=>!['start_date','end_date'].includes(k)))return null;
 const today=new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Amsterdam',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(now));
 for(const [key,after] of [['start_date',true],['end_date',false]])if(conditions[key]&&(!/^\d{4}-\d{2}-\d{2}$/.test(conditions[key])||(after?today<conditions[key]:today>conditions[key])))return null;
 const chargeMin=number(o.chargeMinutes),parkMin=number(o.parkingMinutes);
 if(parkMin<chargeMin||!Array.isArray(e.componenten)||!e.componenten.length)return null;
 const components={},types=new Set();let energy=null,flat=0,time=0,parking=0;
 for(const c of e.componenten){
  const type=c.type,price=Number(c.prijs),vat=Number(c.btw??0),step=Number(c.stap??1);
  if(!['ENERGY','FLAT','TIME','PARKING_TIME'].includes(type)||types.has(type)||c.prijs==null||!Number.isFinite(price)||price<0||!Number.isFinite(vat)||vat<0||vat>100||!Number.isInteger(step)||step<=0)return null;
  // A missing VAT percentage is not evidence of 0% VAT.
  if(o.vatMode!=='inclusive'&&c.btw==null&&price>0)return null;
  types.add(type);
  let quantity;
  if(type==='ENERGY')quantity=Math.ceil(kwh*1000/step)*step/1000;
  else if(type==='FLAT')quantity=1;
  else if(type==='TIME')quantity=chargeMin/60;
  else quantity=(parkMin-chargeMin)/60;
  components[type]={net:price*quantity,gross:0,unitPrice:price,vat,quantity,step};
 }
 // OCPI: round TIME and PARKING_TIME once together; final dimension gets rounding.
 const tc=components.TIME,pc=components.PARKING_TIME;
 if(pc&&parkMin>chargeMin){const seconds=pc.quantity*3600;const roundingBase=tc?parkMin*60:seconds;pc.quantity+=(Math.ceil(roundingBase/pc.step)*pc.step-roundingBase)/3600}
 else if(tc)tc.quantity=Math.ceil(chargeMin*60/tc.step)*tc.step/3600;
 for(const [type,c] of Object.entries(components)){
  c.net=c.unitPrice*c.quantity;c.gross=c.net*(o.vatMode==='inclusive'?1:1+c.vat/100);
  if(type==='ENERGY')energy=c.unitPrice;else if(type==='FLAT')flat=c.gross;else if(type==='TIME')time=c.gross;else parking=c.gross;
 }
 const ndwTotal=Object.values(components).reduce((sum,c)=>sum+c.gross,0),extras=number(o.shuttelFee)+kwh*number(o.shuttelMarkup)+number(o.parkingFee);
 return {total:ndwTotal+extras,ndwTotal,extras,energy,flat,time,parking,components,vatMode:o.vatMode,tariffType:t.type||null};
}
// Unknown tariffs cannot be ranked as more expensive: present every unknown separately.
function rank(candidates){const order=(a,b)=>(a.tariff?.total??Infinity)-(b.tariff?.total??Infinity)||a.walk-b.walk;return [...candidates.filter(x=>x.tariff).sort(order).slice(0,3),...candidates.filter(x=>!x.tariff).sort((a,b)=>a.walk-b.walk)]}
const api={number,trip,tariff,rank,chargingAdvice};root.PlannerCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
