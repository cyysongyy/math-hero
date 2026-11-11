"""把 hard/*.txt（難題原稿）轉成 hard.js。每單元須為 5 選擇 + 3 填充 + 2 應用。"""
import glob, json, os, re, sys

raw = json.load(open('questions.raw.json', encoding='utf-8'))
out, errors = {}, []
TYPE = {'C': '選擇', 'F': '填充', 'W': '應用'}
for path in sorted(glob.glob('hard/*.txt')):
    g = os.path.splitext(os.path.basename(path))[0]
    units = [{'unit': u['unit'], 'qs': []} for u in raw[g]]
    cur = None
    for ln, line in enumerate(open(path, encoding='utf-8').read().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith('##'):
            cur = units[int(line[2:]) - 1]
            continue
        f = line.split('|')
        t = f[0]
        if t == 'C':
            if len(f) != 9:
                errors.append(f'{g}:{ln} 選擇題欄位數 {len(f)}'); continue
            _, q, a, b, c, d, ans, exp, con = f
            if ans not in 'ABCD' or len(ans) != 1:
                errors.append(f'{g}:{ln} 答案字母錯誤')
            if len({a, b, c, d}) < 4:
                errors.append(f'{g}:{ln} 選項重複')
            cur['qs'].append(['選擇', q, f'(A){a} (B){b} (C){c} (D){d}', ans, exp, con, ''])
        elif t in 'FW':
            if len(f) != 6:
                errors.append(f'{g}:{ln} 欄位數 {len(f)}'); continue
            _, q, hint, ans, exp, con = f
            cur['qs'].append([TYPE[t], q, hint, ans, exp, con, ''])
        else:
            errors.append(f'{g}:{ln} 未知類型')
    for i, u in enumerate(units, 1):
        ty = [q[0] for q in u['qs']]
        if (ty.count('選擇'), ty.count('填充'), ty.count('應用')) != (5, 3, 2):
            errors.append(f'{g} 單元{i} 題型數量 {ty.count("選擇")}/{ty.count("填充")}/{ty.count("應用")}')
    out[g] = units
for e in errors:
    print('ERR', e)
open('hard.js', 'w', encoding='utf-8').write('window.HQB=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('grades', len(out), 'questions', sum(len(u['qs']) for us in out.values() for u in us))
sys.exit(1 if errors else 0)
