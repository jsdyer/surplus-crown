import {facts,tabular,href,node,primaryColumns} from './view.mjs';
export const config={slug:'surplus-crown',groups:{CA:'Canada'},defaultGroup:'CA',defaultQuery:'',center:[55,-94],zoom:4,allKind:'All three collections',allStatus:'Every recorded status',allOwner:'All publishers and custodians',extras:[['','All locations'],['ns','Nova Scotia'],['bc','British Columbia'],['mapped','With a map position'],['priced','With a price record'],['history','Status or price changed since capture']]};
export function qualifies(r,k){return !k||({ns:r.province==='Nova Scotia',bc:r.province==='British Columbia',mapped:!!r.geo,priced:!!r.price,history:r.history?.length>1})[k]}
export const extraTerms=r=>[r.description,r.year,r.file,r.use,r.price];
export function details(r,d){
 facts(d,[['Custodian or publisher',r.owner],['Recorded address',r.address],['Property type',r.use],['Federal property ID',r.property],['Provincial file',r.file],['Fiscal year',r.year],[r.priceLabel||'Recorded price',r.price],['Map location',r.geo?r.position:'No official coordinates in this extract']]);
 d.append(node('p',r.description||'The public file lists the address and the asking terms available at its publication date.'));
 if(r.history)tabular(d,'First observation of each change',['Observed on','Published status','Asking price (CAD)'],r.history);
 href(d,'Open the source collection',r.source);
 if(r.property&&['Nova Scotia','British Columbia'].includes(r.province))href(d,'Search this property ID in Federal Property Atlas','https://coolcode.ca/federal-property-atlas/?region='+(r.province==='Nova Scotia'?'NS':'BC')+'&q='+encodeURIComponent(r.property));
}
export const columns=()=>[...primaryColumns,['Source collection',r=>r.source],['Asking or recorded price',r=>r.price],['Price basis',r=>r.priceLabel],['Fiscal year',r=>r.year],['Provincial file',r=>r.file]];

export const sorts=[['','Record name'],['place','Municipality / area',(a,b)=>a.place.localeCompare(b.place)],['fiscal','Latest disposal year',(a,b)=>(b.year||'').localeCompare(a.year||'')]];
