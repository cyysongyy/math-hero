"""檢查選擇題選項是否有「數值相等」的兩個選項（含帶分數、時間、長度、重量、容量換算）。"""
import glob, os, re, sys, io
from fractions import Fraction
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

UNITS = {  # 單位 -> (類別, 換成基本單位的倍數)
    '日': ('t', 1440), '天': ('t', 1440), '小時': ('t', 60), '時': ('t', 60), '分鐘': ('t', 1), '分': ('t', 1), '秒': ('t', Fraction(1, 60)),
    '公里': ('l', 1000000), '公尺': ('l', 1000), '公分': ('l', 10), '毫米': ('l', 1),
    '公斤': ('w', 1000), '公克': ('w', 1),
    '公升': ('v', 1000), '毫升': ('v', 1),
}
NUM = r'(\d+(?:\.\d+)?(?:/\d+)?)'

def val(tok):
    if '/' in tok:
        a, b = tok.split('/'); return Fraction(int(a), int(b))
    return Fraction(tok)

def parse(opt):
    s = opt.replace(' ', '').replace('，', '')
    # 帶分數：a又b/c
    m = re.fullmatch(r'(\d+)又(\d+)/(\d+)', s)
    if m: return ('n', Fraction(int(m[1])) + Fraction(int(m[2]), int(m[3])))
    m = re.fullmatch(NUM, s)
    if m: return ('n', val(m[1]))
    m = re.fullmatch(NUM + r'%', s)
    if m: return ('p', val(m[1]))
    # 複合單位 如 2小時45分、3公尺20公分
    parts = re.findall(NUM + r'(小時|分鐘|公里|公尺|公分|毫米|公斤|公克|公升|毫升|天|日|時|分|秒)', s)
    if parts and ''.join(a + b for a, b in parts) == s:
        cats = {UNITS[u][0] for _, u in parts}
        if len(cats) == 1:
            return (cats.pop(), sum(val(n) * UNITS[u][1] for n, u in parts))
    m = re.fullmatch(NUM + r'(個|人|元|顆|枝|公分|倍|度|張|本|桶|棵|輛|段|盒|袋|份|塊|平方公分|平方公尺|立方公分|公頃|平方公里)', s)
    if m: return ('u' + m[2], val(m[1]))
    return None

bad = 0
for path in sorted(glob.glob('hard/*.txt')):
    g = os.path.splitext(os.path.basename(path))[0]
    unit = 0
    for ln, line in enumerate(open(path, encoding='utf-8').read().splitlines(), 1):
        if line.startswith('##'):
            unit = int(line[2:]); continue
        f = line.split('|')
        if f[0] != 'C' or len(f) < 9: continue
        opts = f[2:6]
        ps = [parse(o) for o in opts]
        for i in range(4):
            for j in range(i + 1, 4):
                if ps[i] and ps[j] and ps[i] == ps[j]:
                    bad += 1
                    print(f'{g} u{unit} L{ln} 選項等值: {opts[i]} = {opts[j]} | {f[1][:30]}')
print('flags', bad)
