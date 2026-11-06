/* vCard-import: uitsluitend namen en postadressen; geen netwerk of contactendatabase. */
(function(root){
'use strict';
const clean=x=>String(x??'').replace(/\r?\n/g,', ').replace(/[\u0000-\u001f]/g,' ').trim();
const unescape=x=>String(x??'').replace(/\\([nN,;\\])/g,(_,c)=>c.toLowerCase()==='n'?'\n':c);
function split(value,separator,quotes=false){let parts=[],part='',escaped=false,quoted=false;for(const c of value){if(escaped){part+='\\'+c;escaped=false;continue}if(c==='\\'){escaped=true;continue}if(quotes&&c==='"'){quoted=!quoted;part+=c;continue}if(c===separator&&!quoted){parts.push(part);part=''}else part+=c}if(escaped)part+='\\';parts.push(part);return parts}
function property(line){let quoted=false,escaped=false;for(let i=0;i<line.length;i++){const c=line[i];if(escaped){escaped=false;continue}if(c==='\\'){escaped=true;continue}if(c==='"')quoted=!quoted;if(c===':'&&!quoted){const h=split(line.slice(0,i),';',true),name=h.shift(),dot=name.lastIndexOf('.');return {name:name.slice(dot+1).toUpperCase(),group:dot>=0?name.slice(0,dot):'',params:h.join(';'),value:line.slice(i+1)}}}return null}
function decode(p){if(!/ENCODING=QUOTED-PRINTABLE/i.test(p.params))return p.value;const charset=(p.params.match(/CHARSET="?([^;\"]+)/i)?.[1]||'utf-8').toLowerCase(),bytes=[];for(let i=0;i<p.value.length;i++){if(p.value[i]==='='&&/^[0-9a-f]{2}$/i.test(p.value.slice(i+1,i+3))){bytes.push(parseInt(p.value.slice(i+1,i+3),16));i+=2}else{const char=p.value.codePointAt(i);if(char>65535)i++;bytes.push(...new TextEncoder().encode(String.fromCodePoint(char)))}}return new TextDecoder(charset).decode(new Uint8Array(bytes))}
function parseVCard(text){
 if(typeof text!=='string'||text.length>5*1024*1024)throw Error('Kies een contactenbestand van maximaal 5 MB. Exporteer zo nodig minder contacten.');
 const lines=[];let pending='';for(const raw of text.replace(/^\uFEFF/,'').split(/\r?\n/)){if(pending&&/ENCODING=QUOTED-PRINTABLE/i.test(pending)&&pending.endsWith('=')){pending=pending.slice(0,-1)+raw}else if(/^[ \t]/.test(raw)&&pending)pending+=raw.slice(1);else{if(pending)lines.push(pending);pending=raw}}if(pending)lines.push(pending);
 const cards=[];let current=null;
 for(const line of lines){if(/^BEGIN:VCARD$/i.test(line)){if(current)throw Error('Het contactenbestand is niet compleet. Exporteer opnieuw als vCard.');current=[]}else if(/^END:VCARD$/i.test(line)){if(current)cards.push(current);current=null}else if(current){const p=property(line);if(p&&['FN','N','ORG','ADR','X-ABLABEL'].includes(p.name))current.push(p)}}
 if(current||!cards.length)throw Error('Geen compleet vCard-contactenbestand gevonden. Gebruik een .vcf-bestand uit Apple Contacten.');
 const entries=[];let withoutAddress=0;
 for(const card of cards){
  const value=name=>{const p=card.find(x=>x.name===name);return p?decode(p):''};
  const structured=split(value('N'),';').map(unescape),name=clean(unescape(value('FN')))||clean([structured[1],structured[2],structured[0]].filter(Boolean).join(' '))||clean(unescape(value('ORG')))||'Contact zonder naam';
  const addresses=card.filter(x=>x.name==='ADR'&&!/VALUE=URI/i.test(x.params));let added=0;
  for(const adr of addresses){const parts=split(decode(adr),';').map(x=>clean(unescape(x)));if(parts.length<3||(!parts[2]&&!parts[3]))continue;
   const labelProperty=card.find(x=>x.name==='X-ABLABEL'&&x.group===adr.group&&adr.group),type=adr.params.toUpperCase();let label=labelProperty?clean(unescape(decode(labelProperty))).replace(/_!<|>!_/g,''):type.includes('HOME')?'thuis':type.includes('WORK')?'werk':'';
   if(/^home$/i.test(label))label='thuis';if(/^work$/i.test(label))label='werk';
   const destination=[parts[2],parts[1],parts[0],parts[5],parts[3],parts[4],parts[6]].filter(Boolean).join(', ');
   entries.push({name:name+(label?' — '+label:addresses.length>1?' — adres '+(added+1):''),destination,source:'contact'});added++;
   if(entries.length>2000)throw Error('Te veel adressen in één import. Kies maximaal 2000 adressen.');
  }
  if(!added)withoutAddress++;
 }
 return {entries,contacts:cards.length,withoutAddress};
}
function fromDevice(contacts){const entries=[];for(const c of contacts||[])for(const a of c.address||[]){const lines=(a.addressLine||[]).map(clean).filter(Boolean);if(!lines.length&&!a.city)continue;entries.push({name:clean(c.name?.[0])||'Contact zonder naam',destination:[...lines,clean(a.postalCode),clean(a.city),clean(a.region),clean(a.country)].filter(Boolean).join(', '),source:'contact'})}return entries}
const key=e=>clean(e.name).toLocaleLowerCase('nl')+'|'+clean(e.destination).toLocaleLowerCase('nl');
function merge(existing,incoming){const entries=[...existing],seen=new Set(entries.map(key));let added=0,duplicates=0;for(const e of incoming){if(!clean(e.name)||!clean(e.destination))continue;const safe={name:clean(e.name),destination:clean(e.destination),source:'contact'};if(seen.has(key(safe))){duplicates++;continue}seen.add(key(safe));entries.push(safe);added++}return {entries,added,duplicates}}
function filterBook(book,query){const q=clean(query).toLocaleLowerCase('nl');return book.map((entry,index)=>({entry,index})).filter(x=>(x.entry.name+' '+x.entry.destination).toLocaleLowerCase('nl').includes(q))}
const api={parseVCard,fromDevice,merge,filterBook};root.ContactsBook=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
