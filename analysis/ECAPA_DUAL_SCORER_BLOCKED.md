# ECAPA 双评分器——阻塞分析（2026-10-11 13:33，abandoned-with-reason）

目标：对既有 clone run 用 CAM++＋ECAPA 双评分器消 SIM 同源偏置（AGENTS 可解释性③）。
现象：CAM++（`iic/speech_campplus_sv_zh-cn_16k-common`）在 paraformer 环境加载/推理正常（主评测已用）。
ECAPA（`iic/speech_ecapa-tdnn_sv_zh-cn_3dspeaker_16k`）经 funasr AutoModel 注册即失败：
`funasr.models.xvector.e2e_sv → No module named 'funasr.layers'`、`funasr.models.sond.sv_decoder → 'funasr.models.decoder'`——
pip 安装的 funasr 1.4.16 不含该 3dspeaker 模型族所需的模块（模型卡要求源码安装 funasr 或更新版本）。
补装 openai-whisper 无效（非同一缺项）。

处置：不为本工具引入源码 funasr（会破坏环境钉死纪律）。候选后续：
①独立小环境源码装 funasr 仅评测用；②换 modelscope pipeline（speaker_pipeline）评测；③保持单评分器＋在结论里降档表述（现状）。
**当前所有 SIM 结论维持"CAM++ 单源、相对排序可信、绝对值有同源偏置风险"的既定口径声明。**
