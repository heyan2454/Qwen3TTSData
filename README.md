# Qwen3TTSData

Qwen3-TTS（TTS 线）轻量数据仓：合成产物、prompt 登记、读数与结论。代码与环境在姊妹仓 `../Qwen3TTS`（GitHub 私有仓待建：heyan2454/Qwen3TTSData）。

## 结构

| 路径 | 内容 |
| --- | --- |
| `AGENTS.md` | 数据仓纪律 |
| `MANIFEST.csv` | 全仓逐件 sha256/bytes 清单 |
| `outputs/smoke_*/` | 冒烟合成（双口径 wav＋result.json） |
| `samples/prompts/` | 克隆 prompt（wav＋txt 成对） |
| `docs/sessions/` | 工作 session 结论 |
| `scripts/update_manifest.py` | 清单重扫工具 |

## 快速验证

```bash
cd /home/hyan/TTS/Qwen3TTS
python scripts/smoke_tts.py
cd /home/hyan/TTS/Qwen3TTSData && python scripts/update_manifest.py
```
