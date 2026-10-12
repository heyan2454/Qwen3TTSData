#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""听样复验页生成器：音频 base64 内嵌自包含 HTML（含打分 UI＋JSON 导出）。"""
import base64, json, os, glob
OUT="/home/hyan/TTS/Qwen3TTSData/docs/listen/listen_review_20261012.html"
D="/home/hyan/TTS/Qwen3TTSData"
P="/home/hyan/ASR/ParaformerData"
def b64(p):
    return "data:audio/wav;base64,"+base64.b64encode(open(p,"rb").read()).decode()
def pick(pat):
    g=sorted(glob.glob(pat))
    return g[0] if g else None
items=[]
def add(sec,tid,path,desc,task,extra_audio=None):
    if not path or not os.path.exists(path):
        print("缺文件:",tid,path); return
    it={"sec":sec,"id":tid,"audio":b64(path),"desc":desc,"task":task,"size_kb":round(os.path.getsize(path)/1024)}
    if extra_audio:
        it["ab"]=it["audio"]; it["audio"]=b64(extra_audio)
    items.append(it)
# 一区：掉音
st=f"{D}/outputs/clone_stability_20261011_134458/wav"
_sib=pick(f"{st}/R2_t7_s2.wav") or pick(f"{st}/R2_t7_s42.wav")
add("1 掉音件","drop_R2_t7_s5",f"{st}/R2_t7_s5.wav","数字长句×seed5——自动检测出的真掉音(SIM 0.125,RMS 仅正常44%)","听：A(掉音)与B(同句正常seed)对比,音色是否明显跑偏？内容是否缺字/含混？",extra_audio=_sib)
add("1 掉音件","en_p1_durability",pick(f"{D}/outputs/endurance_Base_20261012_060540/wav/p00_en_p1.wav"),"耐久 2048 件长跑里退化超时批(en_p1..p4)的英文数字句,此为正常 pass 版本","听：连烧 2000+ 件后音质/完整性是否仍正常？")
# 二区：转写待定
add("2 转写待定","ref_en_5s",f"{D}/samples/prompts/ref_en_5s.wav","英文参考音频——其转写登记存疑被扣押","【重要】逐字写下你听到的英文句子(这解锁一批克隆实验)")
# 三区：九声线主观档
for spk in ["vivian","dylan","eric","uncle_fu","aiden","ryan","serena","sohee","ono_anna"]:
    d2=pick(f"{D}/outputs/cv_multispeaker_{spk}_11*/wav/*.wav")
    if d2: add("3 九声线主观",f"spk_{spk}",d2,f"CustomVoice 声线 {spk} 热词句","听:自然度/清晰度/像人吗(1-5分+一句印象)")
# 四区：字母数字词
v2=f"{P}/datasets/hotword_pilot_v2/wav"
rows_v2=[json.loads(l) for l in open(f"{P}/datasets/hotword_pilot_v2/manifest.jsonl",encoding="utf-8")]
al=[r for r in rows_v2 if r.get("group")=="with_target" and r.get("target_word") and not any("\u4e00"<=c<="\u9fff" for c in r["target_word"])]
for r in al[:5]:
    p2=os.path.join(v2, f'{r["id"]}.wav' if "id" in r else r["file"])
    if not os.path.exists(p2):
        cand=pick(f"{v2}/*{r['id']}*") or pick(f"{v2}/{r.get('file','').split('/')[-1]}")
        p2=cand
    if p2 and os.path.exists(p2): add("4 字母数字词",f"alnum_{r['target_word']}",p2,f"含[{r['target_word']}]的真句｜{r['text'][:44]}","听:字母词是 A-S-N 逐字母拼读还是被读成单词?")
print("alnum入页:",sum(1 for x in items if x['sec']=='4 字母数字词'))
# 五区:真实域含词句(AISHELL)
hits=json.load(open("/root/autodl-tmp/AISHELL-1/hot_speakers.json"))
import re as _re
tp="/root/autodl-tmp/AISHELL-1/data_aishell/transcript/aishell_transcript_v0.8.txt"
shown=0
for ln in open(tp,encoding="utf-8"):
    q=ln.strip().split(maxsplit=1)
    if len(q)!=2: continue
    ws=[w for w in hits.get("words_all",["周杰伦","海尔","联想"]) if w in q[1]]
    if not ws: 
        m=_re.search(r"S\d{4}",q[0])
        if m and m.group(0) in ("S0764","S0765") and any(w in q[1] for w in ["海尔","联想","华为","小米"]):
            pass
    if shown>=3: break
A1="/root/autodl-tmp/AISHELL-1/data_aishell"
for ln in open(tp,encoding="utf-8"):
    q=ln.strip().split(maxsplit=1)
    if len(q)!=2: continue
    if shown>=3: break
    for w in ["海尔","联想","华为","小米","周杰伦"]:
        if w in q[1]:
            m=_re.search(r"S\d{4}",q[0])
            if not m: continue
            for base in (f"{A1}/wav/test/{m.group(0)}",f"{A1}/wav/train/{m.group(0)}"):
                pth=f"{base}/{q[0]}.wav"
                if os.path.exists(pth):
                    add("5 真实域含词句",f"real_{q[0]}",pth,f"AISHELL-1 真句,含热词[{w}]｜文本:{q[1].replace(' ','')}","听:该专有名词真人是否读对(对照组:我们全部热词结论的真域直觉)")
                    shown+=1; break
            break
print("入页件数:",len(items))
# HTML
sec_order=[]
for it in items:
    if it["sec"] not in sec_order: sec_order.append(it["sec"])
html='''<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>听样复验 · 2026-10-12</title>
<style>body{font-family:system-ui;max-width:860px;margin:24px auto;padding:0 16px;background:#0f1419;color:#dde}
h1{font-size:22px}h2{font-size:17px;color:#7fd;margin-top:32px;border-bottom:1px solid #234;padding-bottom:6px}
.card{background:#17222c;border:1px solid #2b3d4d;border-radius:10px;padding:14px;margin:12px 0}
audio{width:100%;margin:8px 0}.desc{color:#9ab;font-size:13px}.task{color:#fd8;font-size:14px;margin:6px 0}
input[type=range]{width:100%}textarea{width:100%;background:#0d1117;color:#cde;border:1px solid #2b3d4d;border-radius:6px;min-height:44px;font-size:14px}
.tag{display:inline-block;background:#234;color:#aed;border-radius:4px;padding:1px 8px;font-size:12px}
button{background:#2d6f4f;color:#fff;border:0;border-radius:6px;padding:8px 16px;font-size:14px;cursor:pointer;margin:6px 8px 30px 0}
progress{width:200px}</style></head><body>
<h1>听样复验页（2026-10-12 14:5x 生成 · 自包含可直接打开）</h1>
<p style="color:#9ab">进度:<progress id="pg"></progress> <span id="pgt"></span> ｜ 打分自动存在本地,最后点「导出结果JSON」贴回对话即可。<br>
每格:1-5 分滑条(主观档),文本框写任何批注(转写/印象/怀疑)。A-B 对比件先听 A(标记问题件)再听 B(对照)。</p>
<button onclick="exp()">导出结果 JSON</button><button onclick="clr()">清空重来</button>
'''
for sec in sec_order:
    html+=f"<h2>{sec}</h2>"
    for it in [x for x in items if x["sec"]==sec]:
        html+=f'''<div class="card"><div class="tag">{it["id"]}</div> <span style="color:#678;font-size:12px">{it["size_kb"]}KB</span>
<p class="desc">{it["desc"]}</p>'''
        if "ab" in it:
            html+=f'<p class="task">{it["task"]}</p><p>A(问题件):</p><audio controls preload=none src="{it["ab"]}"></audio><p>B(对照):</p><audio controls preload=none src="{it["audio"]}"></audio>'
        else:
            html+=f'<p class="task">{it["task"]}</p><audio controls preload=none src="{it["audio"]}"></audio>'
        html+=f'''<label>评分 1-5:</label><input type="range" min=1 max=5 value=3 id="r_{it["id"]}" oninput="save('{it["id"]}')">
<textarea id="n_{it["id"]}" placeholder="批注…" oninput="save('{it["id"]}')"></textarea></div>'''
html+='''<script>
const KEY="listen20261012";
function load(){try{return JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){return{}}}
function save(id){const d=load();d[id]={r:document.getElementById("r_"+id).value,n:document.getElementById("n_"+id).value};localStorage.setItem(KEY,JSON.stringify(d));prog()}
function prog(){const ids=window._ids;const d=load();const n=ids.filter(i=>d[i]&&(d[i].n||d[i].r!=3)).length;const p=document.getElementById("pg");p.max=ids.length;p.value=n;document.getElementById("pgt").textContent=n+"/"+ids.length}
function exp(){const d=load();const blob=new Blob([JSON.stringify(d,null,1)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="listen_results_20261012.json";a.click()}
function clr(){localStorage.removeItem(KEY);location.reload()}
window._ids='''+json.dumps([it["id"] for it in items])+''';prog();
</script></body></html>'''
os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,"w",encoding="utf-8").write(html)
print("[OK] 页面:",OUT,round(os.path.getsize(OUT)/1e6,1),"MB")
