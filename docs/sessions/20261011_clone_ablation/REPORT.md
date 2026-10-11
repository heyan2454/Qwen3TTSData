# REPORT — Qwen3-TTS-0.6B-Base 克隆双模式对照（项目 B 核心实验）

- run：`outputs/clone_abl_20261011_094500/`（wav×8＋meta.jsonl＋config_snapshot＋eval/）
- 日期：2026-10-11；环境：conda `qwen3-tts`（bf16＋sdpa，nice19 GPU 时片与 AST vocano 共存）；评测环境：conda `paraformer`（CPU）
- 设计（单变量）：同模型同参考语音（`samples/prompts/zero_shot_prompt.wav`＋其文本），臂一 `x_vector_only_mode=True`（仅说话人嵌入），臂二完整 ICL（ref_text＋语音 token）；目标文本 4 条（zh×2/en×1/数字混合×1）。Base 模型不做情感指令（选型合同红线）。

## 一、读数（唯一来源 eval/summary.json＋per_utt.jsonl）

| 臂 | mean CER | mean SIM(CAM++ cos) | 逐句 CER（zh1/zh2/en/num） | 逐句 SIM |
| --- | --- | --- | --- | --- |
| x_vector_only | 0.1496 | 0.643 | 0.0 / 0.0 / 0.0385 / 0.56* | .637/.672/.635/.627 |
| icl_full | 0.1496 | **0.711** | 0.0 / 0.0 / 0.0385 / 0.56* | .712/.739/.677/.718 |

*num 句 CER 为**口径虚高**（见 §三-2），两臂内容读数完全一致；SIM 逐句 4/4 同向 ICL>xvec。

## 二、结论线

1. **内容正确性对克隆模式不敏感**（两臂 CER 全等）：模式差异不改变"读对字"的概率，符合设计预期（LM 主干与语言建模同受文本条件驱动）。
2. **音色保真度 ICL 显著占优**（0.711 vs 0.643，均值差 +0.068，逐句同向）：与机制一致——x_vector_only 只给全局说话人嵌入，丢失参考语音的韵律/声学细节 token；SIM 指标（CAM++）对"仅嵌入模式"有系统性低估风险（同源度量），**相对排序可信，绝对值不可当 EER 类结论**。
3. **en_read 真实小错**：`reads→res/lady→lazy`——零样本参考是中文声线，跨语言音素保持失败属已知难点，两臂同现＝非模式问题。

## 三、口径与探针盲区（登记）

1. SIM 评分器（CAM++ 中文训练）与被测合成同源偏置：中文句合理，en 句 SIM 绝对值意义弱。
2. **回识别 CER 含 ITN 书写差虚高**：num 句模型朗读正确（"一百二十八点六元"），Paraformer 回识别大写数字≠原文"128.6"，norm 未做数字归一 → CER 0.56 不可当"读错"证据（与项目 A ASN 句同类，判 aux）。真正的字母串疑点：`ASN→识别成 asm`，发音 N/M 尾混淆待听样复验（wav 已入库可审）。
3. 样本量 4×2、单 seed：读数定性支撑机制叙事，不构成性能结论；扩充文本集（≥30 条分层）列为下一步。
4. RTF 基线修正：本次（系统忙、GPU 时片共享）连续 8 合成 RTF 1.5–2.0；2026-10-10 冒烟轮 RTF 20+ 为冷启动轮（首载首生、紧随安装事务），**引用 RTF 必须区分冷/热态**，AGENTS 慢路径结论由"flash-attn 缺失"修正为"flash-attn 缺失×冷启动放大"。

## 四、下一步（本线）

1. 文本集扩到 30+（zh/en/数字/专名分层），复跑双臂＋加 non_streaming_mode 敏感性臂。
2. SIM 双评分器对照（CAM++ vs 未来 ECAPA）消同源偏置。
3. 听样复验 `ASN→asm`（人工标注发音错误类别）。
4. 与项目 A 联动：合成语音回识别 CER 闭环表（已天然具备数据：本 run wav＋Paraformer 回识别）。
