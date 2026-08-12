import urllib.request
import urllib.parse
import re

queries = [
    'bilesik faiz nedir nasil calisir',
    'yatirim fonlari nedir tefas',
    'enflasyon nedir ekonomi 101',
    'bilanco okuma rehberi temel analiz',
    'temettu nedir temettu emekliligi',
    'borsa istanbul hisse senedi yatirimi'
]

for q in queries:
    url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(q)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = list(dict.fromkeys(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)))
        print(f"=== Query: {q} ===")
        for vid in video_ids[:3]:
            vurl = f'https://www.youtube.com/watch?v={vid}'
            vreq = urllib.request.Request(vurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            vhtml = urllib.request.urlopen(vreq).read().decode('utf-8')
            tmatch = re.search(r'<title>(.*?)</title>', vhtml)
            title = tmatch.group(1).replace(' - YouTube', '').encode('ascii', 'ignore').decode('ascii') if tmatch else 'Unknown'
            print(f'  ID: {vid} | Title: {title}')
    except Exception as e:
        print(f'Error for {q}: {e}')
