#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate/update lesson promotion candidates.

This is intentionally conservative. It proposes candidates but does not create new
skills automatically unless --write is passed.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path.cwd()
LESSONS = ROOT / "docs" / "LESSONS.md"
INDEX = ROOT / "evolution" / "lesson-index.json"
PROMOTION_LOG = ROOT / "evolution" / "promotion-log.md"
CANDIDATES = ROOT / "evolution" / "candidates"

KEYWORDS = {
    "guard": ["风险", "token", "密钥", "删除", "发布", "manifest", "权限", "schema", "API"],
    "xcheck": ["验证", "测试", "报表", "输出", "抽样", "字段", "summary", "smoke"],
    "skill": ["重复", "流程", "自动", "工具", "hook", "memory", "经验"],
}

GENERATED_STATUSES = {"candidate", "keep_as_lesson", ""}


def parse_index(text: str):
    rows = []
    in_index = False
    header = []
    for line in text.splitlines():
        if line.strip() == "## 索引":
            in_index = True
            continue
        if in_index and line.startswith("## "):
            break
        if not in_index or not line.startswith("|") or "---" in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if cols and cols[0] == "#":
            header = cols
            continue
        if len(cols) >= 5 and re.fullmatch(r"L\d+", cols[0]):
            row = {
                "id": cols[0],
                "title": "",
                "type": "",
                "maturity": "",
                "tags": "",
                "priority": "",
                "status": "",
            }
            if header and len(header) == len(cols):
                for name, value in zip(header, cols):
                    if name == "标题":
                        row["title"] = value
                    elif name == "类型":
                        row["type"] = value
                    elif name == "成熟度":
                        row["maturity"] = value
                    elif name == "标签":
                        row["tags"] = value
                    elif name == "优先级":
                        row["priority"] = value
                    elif name == "状态":
                        row["status"] = value
            elif len(cols) >= 7:
                row.update({
                    "title": cols[1],
                    "type": cols[2],
                    "maturity": cols[3],
                    "tags": cols[4],
                    "priority": cols[5],
                    "status": cols[6],
                })
            else:
                row.update({
                    "title": cols[1],
                    "tags": cols[2],
                    "priority": cols[3],
                    "status": cols[4],
                })
            rows.append(row)
    return rows


def score(row):
    text = " ".join(row.values())
    base = 0
    if row.get("priority") == "P1": base += 6
    if row.get("status") == "Pinned": base += 4
    if any(k in text for k in KEYWORDS["guard"]): base += 5
    if any(k in text for k in KEYWORDS["xcheck"]): base += 4
    if any(k in text for k in KEYWORDS["skill"]): base += 4
    return base


def target(row):
    text = " ".join(row.values())
    if any(k in text for k in KEYWORDS["guard"]): return "guard"
    if any(k in text for k in KEYWORDS["xcheck"]): return "xcheck"
    if any(k in text for k in KEYWORDS["skill"]): return "skill"
    return "lesson"


def load_existing_index():
    if not INDEX.exists():
        return {"schema_version": "v5.6", "lessons": []}, {}
    data = json.loads(INDEX.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        return {"schema_version": "v5.6", "lessons": []}, {}
    lessons = data.get("lessons", [])
    if not isinstance(lessons, list):
        lessons = []
    by_id = {
        item.get("id"): item
        for item in lessons
        if isinstance(item, dict) and item.get("id")
    }
    return data, by_id


def generated_status(score_value, target_value):
    if score_value >= 10 and target_value != "lesson":
        return "candidate"
    return "keep_as_lesson"


def merge_item(row, existing):
    s = score(row)
    t = target(row)
    item = dict(existing or {})
    previous_status = str(item.get("promotion_status", ""))
    previous_target = str(item.get("promotion_target", ""))
    preserve_promotion = previous_status and previous_status not in {"keep_as_lesson", ""}

    item.update({
        "id": row["id"],
        "title": row["title"],
        "tags": row["tags"],
        "priority": row["priority"],
        "status": row["status"],
        "promotion_score": s,
        "source": "docs/LESSONS.md",
    })
    # type/maturity belong to the lesson schema. Preserve existing values to
    # avoid clobbering v5.2+ metadata; seed them only for brand-new rows.
    if not item.get("type"):
        item["type"] = row.get("type", "")
    if not item.get("maturity"):
        item["maturity"] = row.get("maturity", "")

    if preserve_promotion and previous_target:
        item["promotion_target"] = previous_target
    else:
        item["promotion_target"] = t

    if previous_status and previous_status not in GENERATED_STATUSES:
        item["promotion_status"] = previous_status
    elif previous_status == "candidate":
        item["promotion_status"] = previous_status
    else:
        item["promotion_status"] = generated_status(s, t)
    return item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not LESSONS.exists():
        raise SystemExit("docs/LESSONS.md not found")

    rows = parse_index(LESSONS.read_text(encoding="utf-8-sig"))
    existing_data, existing_by_id = load_existing_index()
    data = dict(existing_data)
    data["schema_version"] = existing_data.get("schema_version", "v5.6")
    data["updated_at"] = str(date.today())
    data["lessons"] = []
    candidates = []
    seen_ids = set()
    for row in rows:
        item = merge_item(row, existing_by_id.get(row["id"], {}))
        data["lessons"].append(item)
        seen_ids.add(row["id"])
        if item["promotion_status"] == "candidate":
            candidates.append(item)
    for old in existing_data.get("lessons", []):
        if isinstance(old, dict) and old.get("id") not in seen_ids:
            data["lessons"].append(old)

    if args.write:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        CANDIDATES.mkdir(parents=True, exist_ok=True)
        for item in candidates:
            slug = f"{item['id']}-{item['promotion_target']}-candidate.md"
            (CANDIDATES / slug).write_text(
                f"# {item['promotion_target'].upper()} Candidate: {item['id']} {item['title']}\n\n"
                f"- 来源：docs/LESSONS.md#{item['id']}\n"
                f"- 分数：{item['promotion_score']}\n"
                f"- 建议目标：{item['promotion_target']}\n\n"
                f"## 建议\n\n请人工审查后迁入 vibe-{item['promotion_target']} 或保留为 lesson。\n",
                encoding="utf-8"
            )
        with PROMOTION_LOG.open("a", encoding="utf-8") as f:
            f.write(
                f"\n## [{date.today()}] promote | lesson promotion candidates\n"
                f"- Generated {len(candidates)} promotion candidates.\n"
            )
    print(json.dumps({"candidates": candidates, "count": len(candidates)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
