#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple LESSONS -> candidate Guard/XCheck/Skill promoter."""
from __future__ import annotations
import argparse, json, re
from datetime import date
from pathlib import Path
ROOT = Path.cwd()

ROW_RE = re.compile(r"\|\s*(L\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def parse_rows(text: str):
    out=[]
    for m in ROW_RE.finditer(text):
        lid,title,tags,prio,status=[x.strip() for x in m.groups()]
        if lid == '#': continue
        tag_list=[t.strip() for t in re.sub(r"[\[\]]", "", tags).split(',') if t.strip()]
        out.append({"id":lid,"title":title,"tags":tag_list,"priority":prio,"status":status})
    return out


def target_for(tags, title):
    blob = " ".join(tags + [title]).lower()
    if any(k in blob for k in ["security","token","secret","api","hook","manifest","发布","权限"]):
        return "guard"
    if any(k in blob for k in ["xcheck","report","测试","验证","抽样","评测"]):
        return "xcheck"
    if any(k in blob for k in ["skill","workflow","流程","discovery","bootstrap"]):
        return "skill"
    return "guard"


def score(row):
    s = 0
    if row['priority'].upper() == 'P1': s += 8
    if row['status'] == 'Pinned': s += 8
    if 'Rule' in row['tags'] or 'Guard' in row['tags']: s += 5
    if 'Memory' in row['tags'] or 'Legacy' in row['tags']: s += 5
    return s


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args=ap.parse_args()
    lessons_path=ROOT/'docs/LESSONS.md'
    if not lessons_path.exists():
        print('No docs/LESSONS.md found')
        return 0
    rows=parse_rows(lessons_path.read_text(encoding='utf-8'))
    candidates=[]
    for r in rows:
        r['promotion_score']=score(r)
        r['promotion_target']=target_for(r['tags'], r['title'])
        r['promotion_status']='candidate' if r['promotion_score']>=10 else 'watch'
        if r['promotion_status']=='candidate': candidates.append(r)
    data={"version":"v5.1","updated_at":str(date.today()),"lessons":rows}
    if args.write:
        (ROOT/'evolution').mkdir(exist_ok=True)
        (ROOT/'evolution/lesson-index.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        (ROOT/'evolution/candidates').mkdir(parents=True, exist_ok=True)
        for c in candidates:
            p=ROOT/'evolution/candidates'/f"{c['id']}-{c['promotion_target']}.md"
            p.write_text(f"# Candidate: {c['id']} {c['title']}\n\n- Target: {c['promotion_target']}\n- Score: {c['promotion_score']}\n- Status: {c['promotion_status']}\n\n## Suggested rule\n\nTODO: convert this lesson into a concrete {c['promotion_target']} rule.\n", encoding='utf-8')
        with (ROOT/'evolution/promotion-log.md').open('a', encoding='utf-8') as f:
            f.write(f"\n## {date.today()} evolve run\n\n")
            for c in candidates:
                f.write(f"- {c['id']} -> {c['promotion_target']} ({c['promotion_score']})\n")
    print(json.dumps({"candidate_count":len(candidates),"candidates":candidates}, ensure_ascii=False, indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
