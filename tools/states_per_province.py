import numpy as np, re, glob, os, shutil, collections, json
from PIL import Image
from scipy import ndimage as ndi
SRC='/home/claude/work/stage12'; DST='/home/claude/work/stage13'
if os.path.exists(DST): shutil.rmtree(DST)
shutil.copytree(SRC,DST)
M=DST+'/mortaly_world'; S=SRC+'/mortaly_world'
rng=np.random.default_rng(77)
# ---- province geometry
a=np.array(Image.open(S+'/map/provinces.bmp').convert('RGB')).astype(np.int64); H,W=a.shape[:2]
lut={}; typ={}
for l in open(S+'/map/definition.csv'):
    p=l.strip().split(';')
    if p[0]=='0': continue
    lut[int(p[1])*65536+int(p[2])*256+int(p[3])]=int(p[0]); typ[int(p[0])]=p[4]
code=a[...,0]*65536+a[...,1]*256+a[...,2]
u,inv=np.unique(code.ravel(),return_inverse=True); new=np.array([lut[x] for x in u])[inv].reshape(H,W)
NT=len(typ); NL=sum(1 for v in typ.values() if v=='land')
sl=ndi.find_objects(new)
def mask_of(k):
    s=sl[k-1]; m=np.zeros((H,W),bool); m[s]=(new[s]==k); return m
poles={}; radius={}
for k in range(1,NT+1):
    s=sl[k-1]; sub=(new[s]==k); dt=ndi.distance_transform_edt(np.pad(sub,1))[1:-1,1:-1]
    i=np.unravel_index(dt.argmax(),dt.shape); poles[k]=(i[0]+s[0].start,i[1]+s[1].start); radius[k]=float(dt.max())
adj=collections.defaultdict(collections.Counter)
for dy,dx in [(0,1),(1,0)]:
    A=new[:H-dy,:W-dx]; B=new[dy:,dx:]; m=A!=B
    for x,y in zip(A[m].tolist(),B[m].tolist()): adj[x][y]+=1; adj[y][x]+=1
coastal={k:any(q>NL for q in adj[k]) for k in range(1,NL+1)}
# ---- parse old states (stage 12)
old={}
for f in glob.glob(S+'/history/states/*.txt'):
    t=open(f,encoding='utf-8').read(); sid=int(re.search(r'\bid\s*=\s*(\d+)',t).group(1))
    provs=[int(x) for x in re.search(r'provinces\s*=\s*\{([^}]*)\}',t).group(1).split()]
    vp=re.search(r'victory_points\s*=\s*\{\s*(\d+)\s+(\d+)',t)
    bl=dict((k,int(v)) for k,v in re.findall(r'(\w+)\s*=\s*(\d+)',re.search(r'buildings\s*=\s*\{([^}]*)\}',t).group(1)))
    old[sid]=dict(owner=re.search(r'owner\s*=\s*(\w+)',t).group(1),manpower=int(re.search(r'manpower\s*=\s*(\d+)',t).group(1)),
        cat=re.search(r'state_category\s*=\s*(\w+)',t).group(1),provs=provs,vp=(int(vp.group(1)),int(vp.group(2))),bld=bl,
        name=re.search(r'name\s*=\s*"([^"]+)"',t).group(1))
# country display names (ru/en) from existing loc
def loc(path):
    d={}
    for l in open(path,encoding='utf-8-sig'):
        m=re.match(r'\s*([A-Za-z0-9_.]+):\d+\s+"(.*)"\s*$',l)
        if m: d[m.group(1)]=m.group(2)
    return d
ru=loc(S+'/localisation/russian/mortaly_world_l_russian.yml'); en=loc(S+'/localisation/english/mortaly_world_l_english.yml')
slug={'YOZ':'Yozh_Empire','VMP':'Vampire_Kingdom','WWF':'Werewolfs_Forest','CRL':'Cruel_Land','PCL':'Peace_Land','BLI':'Blue_Isles','ORD':'Order_Empire','FOX':'Fox_Island','HMS':'Hippomotoswamp','SVB':'Severobaikalsk','DLD':'Dead_Land','OVS':'Overshadoweds'}
# ---- new states: one per province (state id == province id)
for f in glob.glob(M+'/history/states/*.txt'): os.remove(f)
newst={}; p2old={}; counter=collections.Counter()
for sid in sorted(old):
    o=old[sid]
    for p in o['provs']: p2old[p]=sid
for p in range(1,NL+1):
    o=old[p2old[p]]; main=(p==o['vp'][0]); own=o['owner']; counter[own]+=1; k=counter[own]
    n=len(o['provs']); mp=max(1000,round(o['manpower']/n/1000)*1000) if n else o['manpower']
    bld=dict(o['bld']) if main else {'infrastructure':2}
    cat=o['cat'] if main else 'rural'
    newst[p]=dict(owner=own,manpower=mp,cat=cat,bld=bld,vp=o['vp'][1] if main else None,k=k,oldsid=p2old[p],main=main)
    t='state = {\n\tid = %d\n\tname = "STATE_%d"\n\tmanpower = %d\n\tstate_category = %s\n\thistory = {\n\t\towner = %s\n\t\tadd_core_of = %s\n\t\tbuildings = {\n'%(p,p,mp,cat,own,own)
    for b,v in bld.items(): t+='\t\t\t%s = %d\n'%(b,v)
    t+='\t\t}\n'
    if main: t+='\t\tvictory_points = {\n\t\t\t%d %d\n\t\t}\n'%(p,o['vp'][1])
    t+='\t}\n\tprovinces = {\n\t\t%d\n\t}\n\tbuildings_max_level_factor = 1.0\n}\n'%p
    open(M+'/history/states/%d-%s_%d.txt'%(p,slug[own],k),'w',encoding='utf-8',newline='\n').write(t)
print('states',len(newst))
# ---- supply areas
for f in glob.glob(M+'/map/supplyareas/*.txt'):
    t=open(f,encoding='utf-8').read()
    olds=[int(x) for x in re.search(r'states\s*=\s*\{([^}]*)\}',t).group(1).split()]
    nst=sorted(p for p in newst if newst[p]['oldsid'] in olds)
    lines=[' '.join(map(str,nst[i:i+20])) for i in range(0,len(nst),20)]
    t=re.sub(r'states\s*=\s*\{[^}]*\}','states = {\n\t\t'+'\n\t\t'.join(lines)+'\n\t}',t,count=1)
    open(f,'w',encoding='utf-8',newline='\n').write(t)
# ---- airports / rocketsites (one per state)
for nm in ('airports','rocketsites'):
    open(M+f'/map/{nm}.txt','w').write('\n'.join(f'{p};{p}' for p in range(1,NL+1))+'\n')
# ---- capitals
for f in glob.glob(M+'/history/countries/*.txt'):
    t=open(f,encoding='utf-8').read(); m=re.match(r'capital\s*=\s*(\d+)',t)
    if m:
        o=old[int(m.group(1))]; newcap=o['vp'][0]
        t=re.sub(r'^capital\s*=\s*\d+',f'capital = {newcap}',t,count=1); open(f,'w',encoding='utf-8',newline='\n').write(t)
        print(os.path.basename(f),'capital',m.group(1),'->',newcap)
# ---- PCL split effect: all provinces-states of old states 10 and 11
split=[p for p in newst if newst[p]['oldsid'] in (10,11)]
eff='# Северная половина Жестокой земли (по площади) уходит Мирной земле.\n# TODO: вызвать из события/фокуса Жестокой земли, когда Scaf пришлёт условия гражданской войны.\nmortaly_cruel_land_split = {\n\tPCL = {\n'
for p in sorted(split): eff+=f'\t\ttransfer_state = {p}\n'
for p in sorted(split): eff+=f'\t\t{p} = {{ add_core_of = PCL }}\n'
eff+='\t}\n}\n'
open(M+'/common/scripted_effects/mortaly_effects.txt','w',encoding='utf-8',newline='\n').write(eff)
print('PCL split states',len(split))
# ---- localisation
def rewrite(path,names,vpn,src):
    out=[]
    for l in open(path,encoding='utf-8-sig'):
        if re.match(r'\s*(STATE_\d+|VICTORY_POINTS_\d+):',l): continue
        out.append(l.rstrip('\n'))
    for p in range(1,NL+1):
        out.append(f' STATE_{p}:0 "{names[p]}"')
        if newst[p]['main']: out.append(f' VICTORY_POINTS_{p}:0 "{names[p]}"')
    open(path,'w',encoding='utf-8-sig',newline='\n').write('\n'.join(out)+'\n')
cn_ru={t:ru[t] for t in slug}; cn_en={t:en[t] for t in slug}
rewrite(M+'/localisation/russian/mortaly_world_l_russian.yml',{p:f"{cn_ru[newst[p]['owner']]} {newst[p]['k']}" for p in newst},None,ru)
rewrite(M+'/localisation/english/mortaly_world_l_english.yml',{p:f"{cn_en[newst[p]['owner']]} {newst[p]['k']}" for p in newst},None,en)
# ---- buildings.txt
def to_xz(row,col): return col+0.5,(H-1-row)+0.5
rot=lambda: round(float(rng.uniform(-3.14,6.28)),2)
STATE_TYPES=[('arms_factory',6),('industrial_complex',6),('anti_air_building',3),('air_base',1),('synthetic_refinery',1),('nuclear_reactor_spawn',1),('rocket_site_spawn',1),('radar_station',1),('fuel_silo',1),('stronghold_network',1)]
total=sum(n for _,n in STATE_TYPES); bl=[]
for p in range(1,NL+1):
    m=mask_of(p); cand=np.argwhere(m); order=rng.permutation(len(cand)); chosen=[]
    for mind2 in (6,4,2,1):
        chosen=[]
        for j in order:
            r_,c_=cand[j]
            if all((r_-x)**2+(c_-y)**2>=mind2 for x,y in chosen): chosen.append((r_,c_))
            if len(chosen)==total: break
        if len(chosen)==total: break
    while len(chosen)<total: chosen.append(chosen[len(chosen)%max(1,len(chosen))])
    n=0
    for tname,cnt in STATE_TYPES:
        for _ in range(cnt):
            r_,c_=chosen[n]; n+=1; x,z=to_xz(r_,c_); bl.append(f'{p};{tname};{x:.2f};10.40;{z:.2f};{rot()};0')
    pr,pc=poles[p]; x,z=to_xz(pr,pc)
    bl.append(f'{p};bunker;{x:.2f};10.40;{z:.2f};{rot()};0'); bl.append(f'{p};supply_node;{x:.2f};10.40;{z:.2f};{rot()};0')
    bl.append(f'{p};special_project_facility_spawn;{x+(1 if radius[p]>3 else 0):.2f};10.40;{z:.2f};{rot()};0')
    if coastal[p]:
        sea=max((q for q in adj[p] if q>NL),key=lambda q:adj[p][q])
        band=ndi.binary_dilation(mask_of(sea),iterations=3)&m; cd=np.argwhere(band)
        d=((cd-[pr,pc])**2).sum(1); r1,c1=cd[d.argmin()]; x,z=to_xz(r1,c1)
        bl.append(f'{p};dockyard;{x:.2f};9.70;{z:.2f};{rot()};0'); bl.append(f'{p};coastal_bunker;{x:.2f};9.70;{z:.2f};{rot()};0')
        bl.append(f'{p};naval_base_spawn;{x:.2f};9.70;{z:.2f};{rot()};{sea}')
        band2=ndi.binary_dilation(mask_of(sea),iterations=12)&m; c2=np.argwhere(band2); j=rng.permutation(len(c2))[:2]
        for idx,tname in zip(j,('naval_headquarters','naval_supply_hub')):
            r2,cc2=c2[idx]; x2,z2=to_xz(r2,cc2); bl.append(f'{p};{tname};{x2:.2f};10.00;{z2:.2f};{rot()};0')
        for tname in ('naval_headquarters','naval_supply_hub')[len(j):]: bl.append(f'{p};{tname};{x:.2f};10.00;{z:.2f};{rot()};0')
        bl.append(f'{p};floating_harbor;{x:.2f};9.70;{z:.2f};{rot()};{sea}')
open(M+'/map/buildings.txt','w').write('\n'.join(bl)+'\n'); print('buildings lines',len(bl))
