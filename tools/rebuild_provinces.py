import numpy as np, re, glob, os, shutil, collections, math, sys, json
from PIL import Image
from scipy import ndimage as ndi
from scipy.cluster.vq import kmeans2

SRC='/home/claude/work/stage3'; DST='/home/claude/work/stage12'
MAJOR={'YOZ','VMP','WWF','CRL','ORD'}; FACTOR_MAJ=int(sys.argv[1]) if len(sys.argv)>1 else 16; FACTOR_MIN=int(sys.argv[2]) if len(sys.argv)>2 else 4
rng=np.random.default_rng(2026)
if os.path.exists(DST): shutil.rmtree(DST)
shutil.copytree(SRC,DST)
M=DST+'/mortaly_world'; S=SRC+'/mortaly_world'

# ---------- load old map
a=np.array(Image.open(S+'/map/provinces.bmp').convert('RGB')).astype(np.int64)
H,W=a.shape[:2]
lut={}; otype={}; oterr={}
for l in open(S+'/map/definition.csv'):
    p=l.strip().split(';')
    if p[0]=='0': continue
    lut[int(p[1])*65536+int(p[2])*256+int(p[3])]=int(p[0]); otype[int(p[0])]=p[4]; oterr[int(p[0])]=p[6]
code=a[...,0]*65536+a[...,1]*256+a[...,2]
u,inv=np.unique(code.ravel(),return_inverse=True); old=np.array([lut[x] for x in u])[inv].reshape(H,W)
old_land=sorted(k for k,v in otype.items() if v=='land'); old_sea=sorted(k for k,v in otype.items() if v=='sea')
# old states
st_files={}; o2s={}; st_owner={}
for f in glob.glob(S+'/history/states/*.txt'):
    t=open(f,encoding='utf-8').read(); sid=int(re.search(r'\bid\s*=\s*(\d+)',t).group(1))
    st_files[sid]=f; st_owner[sid]=re.search(r'owner\s*=\s*(\w+)',t).group(1)
    for x in re.search(r'provinces\s*=\s*\{([^}]*)\}',t).group(1).split(): o2s[int(x)]=sid
owner_of={p:st_owner[o2s[p]] for p in old_land}
area={p:int((old==p).sum()) for p in old_land}

# ---------- children counts
nchild={}
by_c=collections.defaultdict(list)
for p in old_land: by_c[owner_of[p]].append(p)
for c,ps in by_c.items():
    f=FACTOR_MAJ if c in MAJOR else FACTOR_MIN
    if c=='BLI':  # islands of very different size: distribute by area
        total=f*len(ps); tot_a=sum(area[p] for p in ps)
        raw={p:total*area[p]/tot_a for p in ps}; n={p:max(1,int(raw[p])) for p in ps}
        while sum(n.values())<total:
            q=max(ps,key=lambda p:raw[p]-n[p]); n[q]+=1
        while sum(n.values())>total:
            q=min([p for p in ps if n[p]>1],key=lambda p:raw[p]-n[p]); n[q]-=1
        nchild.update(n)
    else:
        for p in ps: nchild[p]=f
print('children total',sum(nchild.values()),{c:sum(nchild[p] for p in ps) for c,ps in by_c.items()})

# ---------- split provinces
new=np.zeros((H,W),np.int64); parent={}; nid=0
def comps_ok(lab,n):
    for k in range(n):
        if ndi.label(lab==k)[1]!=1: return False
    return True
for p in old_land:
    n=nchild[p]; m=old==p; ys,xs=np.nonzero(m); pts=np.c_[xs,ys].astype(float)
    if n==1: lab=np.zeros(len(pts),int)
    else:
        best=None
        for t in range(40):
            c,_=kmeans2(pts[::max(1,len(pts)//4000)],n,minit='++',seed=int(rng.integers(1<<30)))
            d=((pts[:,None,:]-c[None])**2).sum(2); l=d.argmin(1); sz=np.bincount(l,minlength=n)
            if (sz==0).any(): continue
            img=np.full((H,W),-1); img[ys,xs]=l
            conn=all(ndi.label(img==k)[1]==1 for k in range(n))
            score=(0 if conn else 10)+sz.std()/sz.mean()
            if sz.min()<60: score+=5
            if best is None or score<best[0]: best=(score,l)
            if conn and score<0.35: break
        lab=best[1]
        if best[0]>=5: print('WARN province',p,'score',best[0])
    for k in range(n):
        nid+=1; sel=lab==k; new[ys[sel],xs[sel]]=nid; parent[nid]=p
NL=nid
# sea ids follow
sea_map={}
for s in old_sea:
    NL_s=NL+1+old_sea.index(s); sea_map[s]=NL_s; new[old==s]=NL_s
NT=NL+len(old_sea)
print('land',NL,'sea',len(old_sea),'total',NT)

# ---------- fix 4-way crossings
def crossings(ids):
    A,B,C,D=ids[:-1,:-1],ids[:-1,1:],ids[1:,:-1],ids[1:,1:]
    s=np.sort(np.stack([A,B,C,D]),0)
    return np.argwhere((s[1:]!=s[:-1]).sum(0)==3)
isl=lambda v: v<=NL
for it in range(50):
    cr=crossings(new)
    if len(cr)==0: break
    for y,x in cr:
        A,B,C,D=new[y,x],new[y,x+1],new[y+1,x],new[y+1,x+1]
        if len({A,B,C,D})<4: continue
        # change D to a neighbour of same kind (land/sea), else any
        for cand in (B,C,A):
            if isl(cand)==isl(D): new[y+1,x+1]=cand; break
        else: new[y+1,x+1]=B
print('crossings left',len(crossings(new)))
# connectivity of children after fixes
disc=[k for k in range(1,NL+1) if ndi.label(new==k)[1]!=1]
print('disconnected land children',disc[:10],len(disc))
sizes=np.bincount(new.ravel(),minlength=NT+1)
print('min child size',sizes[1:NL+1].min(),'median',int(np.median(sizes[1:NL+1])))
np.save('/home/claude/work/rebuild/new_ids.npy',new); json.dump({str(k):v for k,v in parent.items()},open('/home/claude/work/rebuild/parent.json','w'))
json.dump({'NL':NL,'NT':NT},open('/home/claude/work/rebuild/meta.json','w'))
# ======================= PART 2: write files =======================
sl=ndi.find_objects(new)
def mask_of(k): 
    s=sl[k-1]; m=np.zeros((H,W),bool); m[s]=(new[s]==k); return m
poles={}; radius={}
for k in range(1,NT+1):
    s=sl[k-1]; sub=(new[s]==k); dt=ndi.distance_transform_edt(np.pad(sub,1))[1:-1,1:-1]
    i=np.unravel_index(dt.argmax(),dt.shape); poles[k]=(i[0]+s[0].start,i[1]+s[1].start); radius[k]=float(dt.max())
# old provinces -> main child
main_child={}
for p in old_land:
    m=old==p; s=ndi.find_objects(m.astype(int))[0]; sub=m[s]
    dt=ndi.distance_transform_edt(np.pad(sub,1))[1:-1,1:-1]; i=np.unravel_index(dt.argmax(),dt.shape)
    main_child[p]=int(new[i[0]+s[0].start,i[1]+s[1].start])
    assert parent[main_child[p]]==p
children=collections.defaultdict(list)
for k,p in parent.items(): children[p].append(k)
# adjacency + border lengths
adj=collections.defaultdict(collections.Counter)
for dy,dx in [(0,1),(1,0)]:
    A=new[:H-dy,:W-dx]; B=new[dy:,dx:]; m=A!=B
    for x,y in zip(A[m].tolist(),B[m].tolist()): adj[x][y]+=1; adj[y][x]+=1
land_ids=list(range(1,NL+1)); sea_ids=list(range(NL+1,NT+1))
coastal={k:any(q>NL for q in adj[k]) for k in land_ids}
# ---------- provinces.bmp + definition.csv
used={(0,0,0)}; cols={}
for k in range(1,NT+1):
    while True:
        c=tuple(int(v) for v in rng.integers(1,255,3))
        if c not in used: used.add(c); break
    cols[k]=c
img=np.zeros((H,W,3),np.uint8)
lutc=np.zeros((NT+1,3),np.uint8)
for k,c in cols.items(): lutc[k]=c
img=lutc[new]
Image.fromarray(img,'RGB').save(M+'/map/provinces.bmp',format='BMP')
rows=['0;0;0;0;land;false;unknown;0']
for k in range(1,NT+1):
    r,g,b=cols[k]
    if k<=NL: rows.append(f'{k};{r};{g};{b};land;{str(coastal[k]).lower()};{oterr[parent[k]]};1')
    else: rows.append(f'{k};{r};{g};{b};sea;false;ocean;0')
open(M+'/map/definition.csv','w').write('\n'.join(rows)+'\n')
# ---------- states
state_new_provs={}
def wrap(ids,indent):
    ids=sorted(ids); lines=[' '.join(map(str,ids[i:i+20])) for i in range(0,len(ids),20)]
    return ('\n'+indent).join(lines)
for sid,f in st_files.items():
    t=open(f,encoding='utf-8').read()
    olds=[int(x) for x in re.search(r'provinces\s*=\s*\{([^}]*)\}',t).group(1).split()]
    nps=[c for p in olds for c in children[p]]; state_new_provs[sid]=nps
    t=re.sub(r'provinces\s*=\s*\{[^}]*\}','provinces = {\n\t\t'+wrap(nps,'\t\t')+'\n\t}',t,count=1)
    def vp(mm):
        body=mm.group(1)
        body=re.sub(r'(\d+)(\s+\d+)',lambda q:str(main_child[int(q.group(1))])+q.group(2),body)
        return 'victory_points = {'+body+'}'
    t=re.sub(r'victory_points\s*=\s*\{([^}]*)\}',vp,t)
    open(M+'/history/states/'+os.path.basename(f),'w',encoding='utf-8',newline='\n').write(t)
# ---------- strategic regions
for f in glob.glob(M+'/map/strategicregions/*.txt'):
    t=open(f,encoding='utf-8').read()
    olds=[int(x) for x in re.search(r'provinces\s*=\s*\{([^}]*)\}',t).group(1).split()]
    nps=[]
    for p in olds: nps+= children[p] if p in children else [sea_map[p]]
    t=re.sub(r'provinces\s*=\s*\{[^}]*\}','provinces = {\n\t\t'+wrap(nps,'\t\t')+'\n\t}',t,count=1)
    open(f,'w',encoding='utf-8',newline='\n').write(t)
# ---------- supply nodes / airports / rocketsites
out=[]
for l in open(S+'/map/supply_nodes.txt'):
    q=l.split()
    if q: out.append(f'{q[0]} {main_child[int(q[1])]}')
open(M+'/map/supply_nodes.txt','w').write('\n'.join(out)+'\n')
for nm in ('airports','rocketsites'):
    out=[]
    for l in open(S+f'/map/{nm}.txt'):
        q=l.strip().split(';')
        if len(q)==2: out.append(f'{q[0]};{main_child[int(q[1])]}')
    open(M+f'/map/{nm}.txt','w').write('\n'.join(out)+'\n')
# ---------- railways
def path(a,b):
    allowed=set(children[parent_of_old(a)]) if False else None
def bfs(src,dst,allowed):
    prev={src:None}; q=collections.deque([src])
    while q:
        x=q.popleft()
        if x==dst: break
        for y in adj[x]:
            if y in allowed and y not in prev: prev[y]=x; q.append(y)
    if dst not in prev: return None
    p=[]; x=dst
    while x is not None: p.append(x); x=prev[x]
    return p[::-1]
out=[]
for l in open(S+'/map/railways.txt'):
    q=list(map(int,l.split()))
    if not q: continue
    lvl,n,olds=q[0],q[1],q[2:]
    full=[main_child[olds[0]]]
    for a,b in zip(olds,olds[1:]):
        allowed=set(children[a])|set(children[b])
        pth=bfs(main_child[a],main_child[b],allowed)
        assert pth,(a,b)
        full+=pth[1:]
    out.append(f'{lvl} {len(full)} '+' '.join(map(str,full)))
open(M+'/map/railways.txt','w').write('\n'.join(out)+'\n')
print('railways',len(out),'max len',max(len(x.split())-2 for x in out))
# ---------- unitstacks
offs=[(0,0),(-17.5,-10),(0,-12.5),(15,3),(-12.5,7.5),(5,17.5),(-13.5,0),(13.5,0)]
types_a=[0,1,2,3,4,5,9,10]; types_b=[21,22,23,24,25,26,38]
def to_xz(row,col): return col+0.5, (H-1-row)+0.5
lines=[]
masks_cache={}
for k in range(1,NT+1):
    if k>NL:
        continue
    pr,pc=poles[k]; r=radius[k]; sc=min(1.0,max(0.12,0.75*r/20.0))
    m=mask_of(k); pts=[]
    for (dx,dy) in offs:
        col=int(round(pc+dx*sc)); row=int(round(pr-dy*sc))
        col=min(max(col,0),W-1); row=min(max(row,0),H-1)
        if not m[row,col]:
            col,row=pc,pr
        pts.append((row,col))
    for ti,t in enumerate(types_a+types_b):
        row,col=pts[ti%8] if ti<8 else pts[(ti-8)%8]
        x,z=to_xz(row,col); lines.append((k,t,x,z))
# sea: copy old lines with remapped ids
sea_lines=[]
for l in open(S+'/map/unitstacks.txt'):
    q=l.strip().split(';')
    if len(q)<7: continue
    if int(q[0]) in sea_map: sea_lines.append(f'{sea_map[int(q[0])]};'+';'.join(q[1:]))
with open(M+'/map/unitstacks.txt','w') as fo:
    for k,t,x,z in lines: fo.write(f'{k};{t};{x:.2f};10.40;{z:.2f};0.00;1.07\n')
    for s in sorted(sea_lines,key=lambda s:int(s.split(';')[0])): fo.write(s+'\n')
# ---------- buildings
rot=lambda: round(float(rng.uniform(-3.14,6.28)),2)
bl=[]
land_state_pix={}
prov2state={k:sid for sid,ps in state_new_provs.items() for k in ps}
state_arr=np.zeros(NT+1,int)
for k,s in prov2state.items(): state_arr[k]=s
smask=state_arr[new]  # per pixel state id
STATE_TYPES=[('arms_factory',6),('industrial_complex',6),('anti_air_building',3),('air_base',1),('synthetic_refinery',1),('nuclear_reactor_spawn',1),('rocket_site_spawn',1),('radar_station',1),('fuel_silo',1),('stronghold_network',1)]
for sid in sorted(state_new_provs):
    ps=state_new_provs[sid]; sm=smask==sid
    ys,xs=np.nonzero(sm); 
    sub=sm[ys.min():ys.max()+1,xs.min():xs.max()+1]; dt=ndi.distance_transform_edt(np.pad(sub,1))[1:-1,1:-1]
    i=np.unravel_index(dt.argmax(),dt.shape); cr,cc=i[0]+ys.min(),i[1]+xs.min()
    # candidate pixels
    chosen=[]; R=14
    total=sum(n for _,n in STATE_TYPES)
    while len(chosen)<total and R<200:
        cand=np.argwhere(sm[max(0,cr-R):cr+R+1,max(0,cc-R):cc+R+1])+[max(0,cr-R),max(0,cc-R)]
        order=rng.permutation(len(cand)); chosen=[]
        for j in order:
            r_,c_=cand[j]
            if all((r_-a)**2+(c_-b)**2>=9 for a,b in chosen): chosen.append((r_,c_))
            if len(chosen)==total: break
        R+=8
    if len(chosen)<total: 
        chosen=chosen+[chosen[i%len(chosen)] for i in range(total-len(chosen))]
    n=0
    for tname,cnt in STATE_TYPES:
        for _ in range(cnt):
            r_,c_=chosen[n]; n+=1; x,z=to_xz(r_,c_); bl.append((sid,f'{sid};{tname};{x:.2f};10.40;{z:.2f};{rot()};0'))
    first_coastal=None
    for k in sorted(ps):
        pr,pc=poles[k]; x,z=to_xz(pr,pc)
        bl.append((sid,f'{sid};bunker;{x:.2f};10.40;{z:.2f};{rot()};0'))
        bl.append((sid,f'{sid};supply_node;{x:.2f};10.40;{z:.2f};{rot()};0'))
        px,pz=x+(1 if radius[k]>3 else 0),z
        bl.append((sid,f'{sid};special_project_facility_spawn;{px:.2f};10.40;{pz:.2f};{rot()};0'))
    for k in sorted(ps):
        if not coastal[k]: continue
        sea=max((q for q in adj[k] if q>NL),key=lambda q:adj[k][q])
        pm=mask_of(k); band=ndi.binary_dilation(mask_of(sea),iterations=3)&pm
        cand=np.argwhere(band)
        pr,pc=poles[k]; d=((cand-[pr,pc])**2).sum(1); r1,c1=cand[d.argmin()]
        x,z=to_xz(r1,c1)
        if first_coastal is None:
            first_coastal=(x,z); bl.append((sid,f'{sid};dockyard;{x:.2f};9.70;{z:.2f};{rot()};0'))
        bl.append((sid,f'{sid};coastal_bunker;{x:.2f};9.70;{z:.2f};{rot()};0'))
        bl.append((sid,f'{sid};naval_base_spawn;{x:.2f};9.70;{z:.2f};{rot()};{sea}'))
        band2=ndi.binary_dilation(mask_of(sea),iterations=12)&pm; cand2=np.argwhere(band2)
        j=rng.permutation(len(cand2))[:2]
        for idx,tname in zip(j,('naval_headquarters','naval_supply_hub')):
            r2,c2=cand2[idx]; x2,z2=to_xz(r2,c2); bl.append((sid,f'{sid};{tname};{x2:.2f};10.00;{z2:.2f};{rot()};0'))
        if len(j)<2:
            for tname in ('naval_headquarters','naval_supply_hub')[len(j):]: bl.append((sid,f'{sid};{tname};{x:.2f};10.00;{z:.2f};{rot()};0'))
        bl.append((sid,f'{sid};floating_harbor;{x:.2f};9.70;{z:.2f};{rot()};{sea}'))
with open(M+'/map/buildings.txt','w') as fo:
    for s,l in bl: fo.write(l+'\n')
print('buildings lines',len(bl))
json.dump({'poles':{str(k):[int(v[0]),int(v[1])] for k,v in poles.items()}},open('/home/claude/work/rebuild/poles.json','w'))
print('DONE')
