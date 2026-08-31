---
name: machine-vision-method-halcon
description: |
  HALCON 官方文档与 Solution Guide 方法论。面向 HALCON 算子选择、模板匹配、测量、OCR、缺陷检测、
  标定、3D、HDevelop 原型、HDevEngine 部署和现场调试。
  触发词：「HALCON」「HDevelop」「HDevEngine」「find_shape_model」「metrology」「HALCON 方案评审」。
---

# HALCON 工业机器视觉方法论

## 什么时候用我

- HALCON 项目方案设计、算子选型、HDevelop 原型和上线调试。
- shape matching、NCC、metrology、OCR、variation model、texture inspection、calibration、3D。

## 核心框架

### 1. HALCON 四层闭环

1. 成像层：先让目标信息稳定存在。
2. 坐标层：标定、畸变、pose、ROI 和 domain。
3. 算法层：按特征类型选择算子族。
4. 工程层：HDevelop 证明后，用 HDevEngine 或目标语言封装、测试、部署。

### 2. 算子选择决策树

- 定位：shape model、NCC、descriptor、surface model。
- 测量：metrology model、边缘、亚像素、标定单位。
- OCR/OCV/读码：专用 OCR、Deep OCR、barcode/data code。
- 缺陷：variation model、texture inspection、anomaly/deep learning。
- 3D：calibration、surface matching、shape-based 3D。

### 3. 调试闭环

回放失败图像，分层归因，每次只改一个假设，用固定样本库比较新旧版本。

## 决策规则

1. 图像质量不稳时，先修光学和采集，不先换算子。
2. ROI/domain 要作为算法契约管理，不能随意裁掉必要上下文。
3. shape matching 适合边缘/轮廓稳定对象，纹理或强反光对象需谨慎。
4. metrology 必须结合标定和亚像素边缘质量评估。
5. OCR/读码优先用专用能力，不要从零拼普通分类器。
6. variation model 依赖稳定正常样本和稳定成像。
7. 深度学习要有独立测试集、版本和标注规范。
8. 3D 算子必须报告坐标系、标定、点云质量和遮挡边界。
9. HDevelop 原型上线前要拆清输入输出、异常、日志和性能。
10. 每次参数改动必须能回放验证。

## 检查清单

- [ ] 样张覆盖良品、不良、边界、换型和现场波动。
- [ ] 算子族选择和目标特征类型匹配。
- [ ] ROI/domain、坐标变换和标定链可解释。
- [ ] 关键参数有版本记录和回放结果。
- [ ] 处理时间满足 P95/P99 节拍。
- [ ] 失败图像自动保存。

## 反模式

- HDevelop 里跑通就直接交付。
- 固定 ROI 硬扛定位变化。
- 过度依赖魔法参数，不记录原因。
- reduced domain 裁掉上下文后误判。
- 只看少数 OK 图，不测边界和 NG 图。

## 边界

HALCON 版本、算子行为、授权和最佳实践会变化，具体项目应查当前 MVTec 官方文档。详细提炼见 `references/framework.md`。

