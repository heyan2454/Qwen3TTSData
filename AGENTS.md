# AGENTS.md — Qwen3TTSData

Qwen3-TTS（TTS 线）的**轻量数据仓**：合成 wav、result.json、克隆 prompt 成对登记、结论与清单。纪律主文在代码仓 `../Qwen3TTS/AGENTS.md`，本仓遵守同一套。

## 进仓 / 不进仓

- **进仓**（单件建议 ≤25MB）：`outputs/smoke_*/`、`outputs/eval_*/`（wav＋result.json 成对）、`samples/prompts/`（prompt wav＋txt **必须成对**）、`docs/sessions/<YYYYMMDD_topic>/`、根 `MANIFEST.csv`。
- **不进仓**：模型权重（1.7B/0.6B/Tokenizer）、MODELSCOPE_CACHE、批量长音频集——留在数据盘 `/root/autodl-tmp/AST_storage/Speech/`，仓内只登记重取命令与校验值。禁止网盘与 autodl-fs。

## MANIFEST 纪律

任何文件进出本仓，同次重扫根目录 `MANIFEST.csv`：

```bash
python scripts/update_manifest.py
```

push 后复验 `git rev-list --count @{u}..HEAD` = 0。提交前缀：`data:`、`docs:`、`env:`。文档与提交信息用中文。GitHub 私有仓待建：本地提交先行，remote 建好后补挂。

## 口径

- `result.json` 是唯一数值来源（双口径 modes：custom_voice / voice_clone，各含 seconds、wall、rtf、speaker 或 ref 对路径），禁止手抄。
- 不同模式、不同 speaker、不同 prompt、不同 dtype 的读数不得混比。
- 主观听感记录写进 `docs/sessions/`，标注"主观，非指标"。
