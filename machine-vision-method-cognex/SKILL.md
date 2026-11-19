---
name: machine-vision-method-cognex
description: |
  Cognex 产品与应用资料方法论。面向 In-Sight、VisionPro、ViDi/Deep Learning、DataMan、Verifier、
  读码、智能相机、产线集成、误检漏检管理和应用选型。
  触发词：「Cognex」「In-Sight」「VisionPro」「DataMan」「ViDi」「读码率」「智能相机选型」。
---

# Cognex 工业视觉商业化落地方法论

## 什么时候用我

- 读码、智能相机、PC 视觉、Cognex 产品选型和现场集成。
- no-read、误剔、漏检、触发丢结果、PLC 通信、验收争议。

## 核心框架

### 1. 从图像到动作的闭环工程链

先定义业务动作：放行、剔除、分拣、追溯、报警、停线、机器人取放。再定义物理事实、成像、工具链、判定逻辑、产线接口和记录闭环。

### 2. 应用选型矩阵

- 读码/DPM：DataMan。
- 单相机规则清晰：In-Sight EasyBuilder。
- 复杂逻辑：In-Sight Spreadsheet。
- 多相机/高速/定制 UI：VisionPro。
- 外观复杂且样本足够：ViDi/Deep Learning。
- 码质量合规：Verifier。

### 3. 误检/漏检样本闭环

区分 no-read、misread、false reject、false accept、trigger miss、buffer overflow、PLC 未读结果。保存证据图和版本，用固定样本库 A/B 回放。

## 决策规则

1. 图像没有稳定突出目标特征时，先调 FOV、焦点、曝光、光源和遮光。
2. 输出真实尺寸或机器人坐标时必须标定，硬件变化后重标定。
3. 工件姿态变化时，先定位/fixture，再测量或检测。
4. 读 1D/2D/DPM 码，默认从 DataMan/ID 专用能力开始。
5. 码质量合规不能只看读码率，要做验证和可追溯报告。
6. 单相机简单任务优先 EasyBuilder，复杂逻辑再升级 Spreadsheet 或 VisionPro。
7. 多相机、高速、复杂 UI 或数据库集成优先 VisionPro。
8. AI 缺陷检测必须有足够样本和独立测试集。
9. 调参不能只看一两张样图。
10. PLC 触发与结果读取必须验证握手和超时。

## 检查清单

- [ ] 业务动作和误判代价明确。
- [ ] FOV、工作距离、镜头、焦点、曝光和光源方案明确。
- [ ] 样本覆盖良品、不良、边界、班次、产线、批次。
- [ ] 选型理由明确：DataMan/In-Sight/VisionPro/ViDi/Verifier。
- [ ] 节拍包含采集、处理、通信和剔除动作。
- [ ] read rate、no-read、decode time、trigger overrun、buffer overflow 有监控。
- [ ] 失败图像和参数版本可回放。

## 反模式

- 先写算法，后补光学。
- 用读码率替代码质量。
- 把 Trigger Ack 当作拍照完成。
- 用几张好图验收 AI 缺陷检测。
- 把智能相机当万能上位机。

## 边界

具体型号、FOV、协议字段、授权、报价和售后承诺以 Cognex 当前官方资料为准。详细提炼见 `references/framework.md`。

