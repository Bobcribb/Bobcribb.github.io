#!/usr/bin/env python3
"""Check the deployed inventory and every listed page; no content mutations."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'User-Agent':'MYTHOS-publication-check/1.0','Cache-Control':'no-cache'}),timeout=25) as response:
                return response.status,response.headers.get('Content-Type',''),response.read()
        except Exception:
            if attempt==2:raise
            time.sleep(2)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',default='https://bobmythos.fr')
    parser.add_argument('--output',default='/tmp/mythos-live-verification.json')
    args=parser.parse_args()
    expected=json.loads(Path('_site/catalog/entries.json').read_text())
    # Wait for propagation, but fail visibly if the newly deployed inventory
    # cannot be identified. A 200 from an older site is not publication proof.
    remote=None
    for attempt in range(6):
        try:
            _,_,body=fetch(args.base+'/catalog/entries.json?verify='+str(int(time.time())))
            remote=json.loads(body)
            if remote==expected:break
        except Exception:pass
        time.sleep(10)
    if remote!=expected:raise RuntimeError('Le catalogue public ne correspond pas à cette publication')
    urls=['/']+[entry['url'] for entry in expected['entries']]
    urls += [item['url'] for item in json.loads(Path('_site/catalog/reading-pdfs.json').read_text())]
    def check(path):
        try:
            status,kind,body=fetch(args.base+path)
            pdf=path.endswith('.pdf')
            valid=status==200 and (body.startswith(b'%PDF') if pdf else b'<html' in body.lower())
            return {'url':path,'status':status,'valid':valid,'bytes':len(body)}
        except Exception as error:return {'url':path,'valid':False,'error':str(error)}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,urls))
    failures=[r for r in results if not r['valid']]
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'base_url':args.base,'checked':len(results),'failures':failures,'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Pages publiques vérifiées :',len(results),' ; erreurs :',len(failures))
    if failures:raise RuntimeError(json.dumps(failures[:10],ensure_ascii=False))


if __name__=='__main__':main()
