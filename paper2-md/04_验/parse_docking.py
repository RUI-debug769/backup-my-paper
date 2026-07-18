import pandas as pd, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

output_file = r'C:\Users\26404\AppData\Local\Temp\claude\C--Users-26404-Desktop-My-Paper\37a43c16-123f-478f-b7be-1d2a91be6507\tasks\byurfy9dl.output'
with open(output_file, 'rb') as f:
    raw = f.read().decode('utf-8', errors='replace')

p = re.compile(r'\s{3,4}1\s{6,7}(-\d+\.\d+)')
affs = [float(m) for m in p.findall(raw)]
print(f'提取到 {len(affs)} 个对接结果')

LIGS = ['1-octen-3-ol','hexanal','benzaldehyde','valeraldehyde','1-hexanol',
        'ethyl_3-methylbutanoate','ethyl_acetate','acetic_acid','2,5-dimethylpyrazine','3-carene']
PROTS = ['MBL_lectin','Tyrosinase','H_lectin']

rows = []
for i, dg in enumerate(affs):
    pi = i // 10; li = i % 10
    if pi < 3:
        rows.append({'protein':PROTS[pi],'ligand':LIGS[li],'dG_kcal_mol':dg})

df = pd.DataFrame(rows)
out = r'C:\Users\26404\Desktop\My Paper\2\04_验\docking_results\vina_docking_results.csv'
df.to_csv(out, index=False, encoding='utf-8-sig')
print(f'保存 {len(df)} 条结果')

ranked = df.sort_values('dG_kcal_mol')
print('\n对接结果排名:')
for i,(_,r) in enumerate(ranked.iterrows()):
    bar = '#' * min(12, int(abs(r['dG_kcal_mol'])*2))
    print(f'  {i+1:2d}. {r["protein"]:15s} x {r["ligand"]:28s} dG={r["dG_kcal_mol"]:+.1f} {bar}')

print('\n每蛋白 Top-3:')
for prot in PROTS:
    top = df[df.protein==prot].nsmallest(3,'dG_kcal_mol')
    print(f'  {prot}:')
    for _,r in top.iterrows():
        print(f'    {r["ligand"]:30s} dG={r["dG_kcal_mol"]:+.1f} kcal/mol')
print('\nDONE')
