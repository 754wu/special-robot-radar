#!/usr/bin/env python3
"""Metadata-level per-record review; suggestions are NOT automatic relabels."""
import csv,json,re
from collections import Counter
from pathlib import Path
data=json.loads(Path("docs/items.json").read_text(encoding="utf-8"))
if isinstance(data,dict):data=list(data.values())
def hit(s,p):return bool(re.search(p,s,re.I))
issues=[]; groups=Counter();cats=Counter(); examples={}
for i,x in enumerate(data):
 t=str(x.get("title") or "");a=str(x.get("description") or "");txt=t+" "+a;c=x.get("category","未分类");cats[c]+=1
 findings=[]
 def flag(code,suggest,why):findings.append((code,suggest,why))
 if c=="硬件与防爆" and hit(t,r"reinforcement.learning|locomotion.policy|navigation|slam") and not hit(t,r"mechanical.design|structural.design|actuator.design|gearbox|flameproof|explosion.proof"):flag("HW_ALGORITHM","小脑与运动控制/感知建图与导航","题名主贡献可能是算法")
 if c=="硬件与防爆" and not hit(txt,r"mechanical|actuat|motor|joint|linkage|transmission|hardware|battery|explosion.proof|flameproof|chassis|gearbox|mechanism|structural|kinematic|dimensional.synthesis|topology.size|adaptive.foot|drivetrain|piezoelectric|track.design|cable.management|visuo.tactile|tactile.sensor|sensor.design|结构|机构|电机|防爆|传动"):flag("HW_NO_EVIDENCE","待复核","缺少明确硬件设计证据")
 if c=="感知建图与导航" and hit(txt,r"skill.calling|tool.calling|skill.selection|task.decomposition|llm.based.task.planning|reflection.and.replanning") and hit(txt,r"llm|vlm|language.model|agentic|embodied.agent"):flag("NAV_AGENT","大脑与具身智能","存在高层Agent技能编排特征")
 if c=="小脑与运动控制" and hit(txt,r"skill.calling|tool.calling|task.decomposition|llm.based.task.planning") and hit(txt,r"llm|vlm|language.model|agentic"):flag("CTRL_AGENT","大脑与具身智能","存在高层Agent决策特征")
 if c=="大脑与具身智能" and hit(t,r"locomotion|gait|whole.body.control|torque.control|trajectory.tracking") and not hit(txt,r"llm|vlm|vla|vision.language|task.planning|skill.calling|tool.calling|high.level|agentic"):flag("BRAIN_CONTROL","小脑与运动控制","可能是低层控制贡献")
 if c=="基础软件与系统" and hit(t,r"slam|navigation|reinforcement.learning|locomotion|object.detection") and not hit(t,r"dataset|benchmark|simulation.framework|software|middleware|digital.twin|simulator|platform"):flag("SOFT_ALGORITHM","感知导航/小脑","软件类题名疑似算法贡献")
 if c=="特种应用与产品" and hit(t,r"algorithm|deep.learning|reinforcement.learning|slam|visual.localization|path.planning") and not hit(t,r"system.integration|deployment|robot.prototype|robot.system|field.validation"):flag("APP_ALGORITHM","具体算法主类","应用系统类别可能混入算法论文")
 if hit(t,r"(?:^|/)awesome[-_ ]|reading[-_ ]list|curated[-_ ]list"):flag("RESOURCE_COLLECTION","资源索引","非原创研究合集")
 if x.get("source")=="GitHub" and hit(t,r"^([\w.-]+)/\1$"):flag("PROFILE","排除候选","GitHub个人简介仓库")
 if c=="感知建图与导航" and hit(txt,r"hierarchical.reasoning|long.horizon.planning|memory.guided.exploration|subgoal.selection|active.perception|replanning|reflection|multi.step.reasoning") and hit(txt,r"vision.language|vln|llm|vlm|embodied.agent"):
  flag("NAV_AGENT_REVIEW","大脑与具身智能（待复核）","可能为高层Agent，但普通导航也可能使用同类机制")
 if c=="大脑与具身智能" and hit(t,r"human.motion.priors|robot.centric.terrain|locomotion|gait|whole.body.control") and not hit(txt,r"task.decomposition|skill.calling|tool.calling|language.model.planning"):
  flag("BRAIN_POLICY_REVIEW","小脑与运动控制（待复核）","具身基础模型与低层动作策略存在边界")
 if len(a.strip())<50:flag("THIN_ABSTRACT","待复核","摘要证据不足")
 if x.get("needs_review"):flag("EXISTING_REVIEW","待复核","分类器已标记低可信度")
 record={"index":i,"title":t,"category":c,"suggested_category":"；".join(dict.fromkeys(q[1] for q in findings)),"issue_codes":"；".join(q[0] for q in findings),"reasons":"；".join(q[2] for q in findings),"url":x.get("url",""),"source":x.get("source",""),"abstract_excerpt":a[:220],"current_reason":x.get("classification_reason",""),"needs_review":bool(x.get("needs_review"))}
 issues.append(record)
 for code,_,_ in findings:groups[code]+=1;examples.setdefault(code,[]).append(record)
Path("docs").mkdir(exist_ok=True)
cols=list(issues[0]) if issues else []
with Path("docs/classification_audit.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(issues)
lines=["# 全库逐条分类元数据审计","","本表对每条已入库资源扫描标题、摘要及现有分类；疑点不等于确证错分。","",f"总资源：{len(data)}；出现一项或以上疑点：{sum(bool(x['issue_codes']) for x in issues)}。","","## 分类数量",""]
lines += [f"- {k}: {v}" for k,v in cats.most_common()]
lines += ["","## 疑点分布",""]
lines += [f"- {k}: {v}" for k,v in groups.most_common()]
lines += ["","## 重点疑点逐篇示例",""]
for k,ls in sorted(examples.items(),key=lambda z:-len(z[1])):
 lines.append(f"### {k}（{len(ls)} 条）")
 for x in ls[:12]:
  lines.append(f"- {x['title']} | 当前：{x['category']} | 建议：{x['suggested_category']} | {x['url']}")
Path("docs/classification_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Audited",len(data),"items with",len(groups),"issue types")
