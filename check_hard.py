"""粗略檢查 hard/*.txt：驗算說明中的算式，並比對答案。只報告可疑處，供人工複查。"""
import glob, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
EQ = re.compile(r'(\d+(?:\.\d+)?(?:\s*[＋－×÷]\s*\d+(?:\.\d+)?)+)\s*＝\s*(\d+(?:\.\d+)?)')
def ev(e):
    e = e.replace('＋', '+').replace('－', '-').replace('×', '*').replace('÷', '/')
    try:
        return eval(e, {}, {})
    except Exception:
        return None
bad = 0
for path in sorted(glob.glob('hard/*.txt')):
    g = os.path.splitext(os.path.basename(path))[0]
    unit = 0
    for ln, line in enumerate(open(path, encoding='utf-8').read().splitlines(), 1):
        if line.startswith('##'):
            unit = int(line[2:]); continue
        f = line.split('|')
        if len(f) < 6: continue
        exp = f[7] if f[0] == 'C' else f[4]
        for m in EQ.finditer(exp):
            v = ev(m.group(1))
            if v is None or abs(v - float(m.group(2))) > 1e-9:
                bad += 1; print(f'{g} u{unit} L{ln} 算式不成立: {m.group(0)}')
        nums = EQ.findall(exp)
        if f[0] == 'C':
            opts = {k: t for k, t in zip('ABCD', f[2:6])}
            ans = f[6]
            if nums:
                last = nums[-1][1]
                if last not in re.findall(r'\d+(?:\.\d+)?', opts[ans]) and any(last in re.findall(r'\d+(?:\.\d+)?', t) for k, t in opts.items() if k != ans):
                    bad += 1; print(f'{g} u{unit} L{ln} 正解選項不含算式結果 {last}: 答{ans} {opts[ans]} | {f[1][:30]}')
            if len(set(opts.values())) < 4: bad += 1; print(f'{g} u{unit} L{ln} 選項重複')
        else:
            if nums:
                last = nums[-1][1]
                an = re.findall(r'\d+(?:\.\d+)?', f[3])
                if an and last not in an and f[3].replace(' ', '') != last:
                    bad += 1; print(f'{g} u{unit} L{ln} 答案 {f[3]} 與算式結果 {last} 不同: {f[1][:30]}')
print('flags', bad)
