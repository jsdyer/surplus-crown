import gzip,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SourceTests(unittest.TestCase):
 def test_provenance_and_row_identity(self):
    meta=json.loads((ROOT/'data/status.json').read_text())
    rows=[r for key in meta['groups'] for r in json.loads(gzip.decompress((ROOT/'data'/(key+'.json.gz')).read_bytes()))]
    self.assertEqual(len(rows),meta['count'])
    self.assertEqual(len(set(x['id'] for x in rows)),meta['count'])
    self.assertEqual(sum(bool(x['geo']) for x in rows),meta['mapped'])
    self.assertTrue(all(x['url'].startswith('https://') for x in meta['sources']))
 def test_disappearance_is_retained_and_dated(self):
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    from refresh import archive
    old={'sale-test':{'id':'sale-test','status':'Listed for sale','price':'100','history':[['2026-10-01','Listed for sale','100']]}}
    changed=archive([],old,'2026-11-01')[0]
    self.assertEqual(changed['status'],'No longer listed')
    self.assertEqual(len(archive([],{changed['id']:changed},'2026-11-02')[0]['history']),2)
