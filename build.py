"""把 questions.raw.json（由「南一數學測驗成績單」試算表各年級分頁匯出）轉成前端用的 questions.js。
只含題庫；學生名單與作答紀錄分頁不匯出。"""
import json

d = json.load(open('questions.raw.json', encoding='utf-8'))
out = {}
for g, units in d.items():
    out[g] = [
        {
            'unit': u['unit'],
            'qs': [
                [q['type'], q['q'], q['hint'], q['ans'], q['exp'], q['concept'], q['misc']]
                for q in u['questions']
            ],
        }
        for u in units
    ]
js = 'window.QB=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open('questions.js', 'w', encoding='utf-8').write(js)
print(len(js), sum(len(u['qs']) for us in out.values() for u in us))
