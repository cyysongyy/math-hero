"""逐題自動驗算：能直接算出結果的算式題（選擇/填充），比對標準答案；並檢查答案唯一性、重複題。"""
import glob, os, re, sys, io
from fractions import Fraction
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_num(s):
    s = s.strip().replace(' ', '')
    m = re.fullmatch(r'(\d+)又(\d+)/(\d+)', s)
    if m: return Fraction(int(m[1])) + Fraction(int(m[2]), int(m[3]))
    m = re.fullmatch(r'(\d+)/(\d+)', s)
    if m: return Fraction(int(m[1]), int(m[2]))
    m = re.fullmatch(r'\d+(\.\d+)?', s.replace(',', ''))
    if m: return Fraction(s.replace(',', ''))
    return None

def mixed_to_frac(expr):
    # 1 又 1/2 -> (1+1/2)
    return re.sub(r'(\d+)\s*又\s*(\d+)/(\d+)', r'(\1+Fraction(\2,\3))', expr)

def evaluate(expr):
    e = expr.replace('＋', '+').replace('－', '-').replace('×', '*').replace('÷', '/').replace('（', '(').replace('）', ')').replace('　', ' ')
    e = mixed_to_frac(e)
    e = re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)/(\d+)(?![\w.])', r'Fraction("\1")/\2', e)  # a/b fraction literal
    e = re.sub(r'(?<![\w."])(\d+\.\d+)(?![\w."])', r'Fraction("\1")', e)
    e = re.sub(r'(?<![\w."(])(\d+)(?![\w."(,)])', r'Fraction(\1)', e)
    try:
        return eval(e, {'Fraction': Fraction})
    except Exception:
        return None

problems = 0
seen = {}
total = 0
checked = 0
for path in sorted(glob.glob('hard/*.txt')):
    g = os.path.splitext(os.path.basename(path))[0]
    unit = 0
    for ln, line in enumerate(open(path, encoding='utf-8').read().splitlines(), 1):
        if line.startswith('##'):
            unit = int(line[2:]); continue
        f = line.split('|')
        if len(f) < 6: continue
        total += 1
        q = f[1]
        key = q + '|' + '|'.join(f[2:6] if f[0] == 'C' else [])
        if key in seen:
            problems += 1; print(f'重複題 {g} u{unit} L{ln}  與 {seen[key]}: {q[:30]}')
        seen[key] = f'{g} u{unit} L{ln}'
        m = re.fullmatch(r'([\d.＋－×÷()（）/ 　又]+)＝(?:？|___)(?:（最簡分數）)?', q.strip())
        if not m:
            continue
        val = evaluate(m[1])
        if val is None:
            continue
        checked += 1
        if f[0] == 'C':
            opts = dict(zip('ABCD', f[2:6])); ans = f[6]
            vals = {k: parse_num(v) for k, v in opts.items()}
            hits = [k for k, v in vals.items() if v is not None and v == val]
            if hits != [ans]:
                problems += 1; print(f'選擇 {g} u{unit} L{ln}  {q}  算得 {val}  標答 {ans}={opts[ans]} 命中 {hits}')
        else:
            pa = parse_num(f[3])
            if pa is not None and pa != val:
                problems += 1; print(f'填充 {g} u{unit} L{ln}  {q}  算得 {val}  標答 {f[3]}')
print('總題數', total, '自動驗算', checked, '問題', problems)
