"""Collect separately evidenced federal / provincial property records and their dated observations."""
import csv, gzip, io, json
from hashlib import sha256
from datetime import datetime,timezone
from urllib.parse import urlencode
from edition import ROOT, source, elements, txt, num, coordinates, save
SALE='https://donnees-data.tpsgc-pwgsc.gc.ca/br1/bi-rp/bi-rp.csv'
DFRP='https://map-carte.tbs-sct.gc.ca/dfrp-rbif/oddo/dfrp-rbif.zip'
SERVICE='https://idgsi-rpgdi-arcgis.spac-pspc.gc.ca/gisserver/rest/services/Hosted/Public_Land_Bank/FeatureServer/2'
BANK=SERVICE+'/query?'+urlencode({'where':'1=1','outFields':'*','outSR':'4326','f':'json'})
NS='https://data.novascotia.ca/api/views/2kw3-tjdw/rows.csv?accessType=DOWNLOAD'
PAGES=['https://open.canada.ca/data/en/dataset/e7a3accb-d419-4d8a-b612-0a601ba4540c','https://www.canada.ca/en/public-services-procurement/services/infrastructure-buildings/public-lands-homes/bank-mapping-tool.html','https://data.novascotia.ca/d/2kw3-tjdw']
def offers(raw, directory):
    rows=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    names=rows.fieldnames
    def field(row,prefix):
        key=next((s for s in names if s.startswith(prefix)),None)
        if key is None:raise ValueError('Missing property column '+prefix)
        return (row[key] or '').strip()
    records=[]
    for x in rows:
        code=field(x,'Property-Number')
        if not code:raise ValueError('Listed property lacks identifier')
        records.append({'group':'CA','id':'sale-'+code,'property':code,'title':field(x,'Street-address-Adresse-municipale-eng'),
          'place':field(x,'City-Ville'),'province':field(x,'Province-territory-Province-territoire-eng'),
          'kind':'Federal sale listing','status':'Listed for sale','owner':'Public Services and Procurement Canada',
          'geo':None,'source':PAGES[0],'price':field(x,'Price-Prix'),'priceLabel':'Published asking price (CAD)',
          'description':field(x,'Current-Recent-use-Utilisation-actuelle-récente-eng'),'use':field(x,'Type-listing-Type-inscription-eng')})
    by_id={r['property']:r for r in records}
    for e in elements(directory,{'Property'}):
        r=by_id.get(txt(e,'Property_Number'))
        if not r:continue
        positions=[coordinates(txt(p,'Location/Latitude'),txt(p,'Location/Longitude')) for p in e.findall('Parcels/Parcel')]
        positions=[p for p in positions if p]
        if len(positions)==1:r.update(geo=positions[0],position='DFRP parcel reference point')
    return records
def housing(data):
    doc=json.loads(data)
    if 'features' not in doc or doc.get('exceededTransferLimit'):raise ValueError('Incomplete federal land bank response')
    for f in doc['features']:
        a=f['attributes'];g=f.get('geometry') or {};code=a['uniqueid']
        yield {'group':'CA','id':'bank-'+str(code),'property':a.get('property_number') or '', 'title':a.get('property_name') or a['address'],
               'address':a.get('address') or '','place':a['municipality'],'province':a['province_or_territory'],
               'kind':'Housing land bank','status':'Land bank · '+a['status'],'owner':a.get('custodian_name') or '',
               'geo':coordinates(g.get('y'),g.get('x')),'position':'Public Land Bank map point','source':PAGES[1],
               'description':'Identified for potential housing development. The project stage comes from the public land bank.'}
def provincial(raw):
    rows=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    for x in rows:
        year,code,place,description=[x[k].strip() for k in ('Fiscal Year','File No.','Location','Description')]
        digest=sha256((year+'|'+code+'|'+place+'|'+description).encode()).hexdigest()[:12]
        yield {'group':'CA','id':'ns-'+digest,'title':description,'place':place,'province':'Nova Scotia',
               'kind':'Provincial disposal','status':'Recorded disposal','owner':'Province of Nova Scotia','geo':None,
               'source':PAGES[2],'year':year,'file':code,'price':x['Contract Price'].strip(),'priceLabel':'Contract price as filed',
               'description':'Nova Scotia public disposal record. The location field identifies a general area. The published table supplies no parcel coordinates.'}
def archive(current, old, today):
    by_id={r['id']:r for r in current}
    if len(by_id)!=len(current):raise ValueError('Duplicate record key')
    for key,previous in old.items():
        if key not in by_id and key.startswith(('sale-','bank-')):
            by_id[key]={**previous,'status':'No longer listed'}
    for key,r in by_id.items():
        if key.startswith('ns-'):continue
        former=old.get(key,{})
        history=list(former.get('history',[]))
        state=[r.get('status'),r.get('price') or '']
        if not history or history[-1][1:]!=state:history.append([today,*state])
        r['history']=history
    return list(by_id.values())
if __name__=='__main__':
    records=offers(source(SALE,'sale.csv'),source(DFRP,'dfrp.zip'))
    records.extend(housing(source(BANK,'banksites.json')))
    records.extend(provincial(source(NS,'ns.csv')))
    if sum(r['kind']=='Housing land bank' for r in records)<50 or sum(r['kind']=='Provincial disposal' for r in records)<100:raise ValueError('Source coverage incomplete')
    historic=ROOT/'data/CA.json.gz'
    prior={r['id']:r for r in json.loads(gzip.decompress(historic.read_bytes()))} if historic.exists() else {}
    records=archive(records,prior,datetime.now(timezone.utc).date().isoformat())
    save(records,[{'name':n,'url':p,'download':d} for n,p,d in zip(['Federal real estate for sale','Canada Public Land Bank','Nova Scotia real property disposals'],PAGES,[SALE,BANK,NS])])
