# HALCON 工业机器视觉项目方法论

调研时间：2026-08-28

对象：HALCON 官方文档、MVTec Solution Guides、HALCON Operator Reference、MVTec 官方示例与产品说明。

适用角色：机器视觉软件工程师、算法工程师、视觉应用工程师、产线视觉调试工程师。

## 来源清单

优先级 A：MVTec 官方一手资料

- MVTec HALCON Documentation：官方文档入口，包含 Reference Manual、HALCON Basics、Solution Guides、Programmer's Guide、Technical Notes、Release Notes。https://www.mvtec.com/products/halcon/documentation
- HALCON Operator Reference 26.05：官方算子参考，覆盖 1D Measuring、2D Metrology、Matching、OCR、Inspection、Calibration、3D Matching、3D Reconstruction、Deep Learning、Image Source、System 等章节。https://www.mvtec.com/doc/halcon/2605/en/
- Solution Guide I - Basics：HALCON 基础概念、图像/区域/XLD/坐标/开发流程。
- Solution Guide II-A - Image Acquisition：相机采集、接口、触发、参数、图像源。
- Solution Guide II-B - Matching：shape-based、NCC、descriptor、deformable 等匹配路线。
- Solution Guide II-D - Classification：分类、纹理检测、缺陷分类与传统/深度学习分类路线。
- Solution Guide III-A - 1D Measuring：边缘剖面、亚像素测量、测量矩形/圆弧、边缘对。
- Solution Guide III-B - 2D Measuring：2D metrology 模型、几何对象、拟合与结果评估。
- Solution Guide III-C - 3D Vision：标定、3D 重建、3D 对象模型、3D matching、机器人相关坐标关系。
- Programmer's Guide：应用集成、语言接口、HDevEngine、部署结构。
- Technical Note - Surface-Based Matching：surface model 的匹配步骤、参数与调试。
- Technical Note - Parallel Programming：并行化、线程安全、性能诊断。
- Technical Note - Memory Management：对象/handle 生命周期、内存使用和长期运行风险。
- HDevelop 官方介绍：HDevelop 用于交互式开发、视觉逻辑验证、profiling、代码导出与 HDevEngine 集成。https://www.mvtec.com/products/halcon/features-tools/development-tools-programming/hdevelop
- HALCON 26.05 Release Notes：自动轮廓优化 for shape matching、advanced object detection、增强数据增强、Deep OCR 更新等版本变化。https://www.mvtec.com/products/halcon/documentation/release-notes-2605-0

优先级 B：官方算子页与示例片段

- `find_shape_models` / `find_generic_shape_model`：多模板 shape matching、金字塔层数、`MinScore`、`MaxOverlap`、`SubPixel`、`Greediness` 等参数。
- `find_ncc_models`：NCC 多模型匹配；当 NCC 找不到合适匹配或分数过低时，应考虑其他匹配方法。
- `create_metrology_model` / `apply_metrology_model`：2D metrology 容器、几何对象、测量区域、边缘定位、RANSAC 拟合。
- `measure_pos` / `fuzzy_measure_pos`：1D 测量剖面、边缘候选、contrast/position/distance 等 fuzzy 选择。
- `create_variation_model` / `train_variation_model` / `compare_variation_model`：基于好品波动模型的图像差异检测。
- Texture Inspection：使用无缺陷纹理图训练 GMM-based 模型，基于图像金字塔分析多频段纹理缺陷。
- Deep Learning / Anomaly Detection / Object Detection / Segmentation：深度学习模型、样本字典、预处理、batch、训练/推理差异。
- Deep OCR / `get_deep_ocr_param` / `apply_dl_model`：词级文本检测与识别、默认/compact 组件、置信度与候选字符。
- Calibration / `find_calib_object` / `calibrate_cameras`：标定数据模型、相机参数、标定板提取、重投影/世界坐标基础。
- `find_surface_model`：3D surface matching 的 approximate matching、sparse refinement、dense refinement；点云法线、采样、score 与 result handle 调试。
- Image Source / `create_image_source`：图像源 handle、插件/设备、配置文件、采集参数持久化。

排除来源：知乎、微信公众号、百度百科、论坛摘抄、未标明 HALCON 版本的二手教程。它们可用于理解中文实践语境，但不作为本方法论证据。

## 核心框架一：HALCON 项目四层闭环

一句话：HALCON 项目不是“找一个神奇算子”，而是把成像、坐标、算法、工程化四层同时闭环。

### 1. 成像层：先让信息存在

目标：让目标特征在图像/点云中稳定、可分、可重复。

步骤：

1. 明确被检测特征：轮廓、灰度差、纹理异常、字符、码、尺寸边缘、3D 几何、位姿。
2. 选择照明和光学方案：优先通过光源、镜头、滤光、曝光、触发降低算法负担。
3. 固定采集条件：曝光、增益、触发时序、焦距、工作距离、产品姿态、背景。
4. 用 HDevelop 快速检查：灰度直方图、ROI、轮廓、XLD、局部剖面、点云密度。
5. 建立样本集：好品、坏品、边界样本、脏污样本、换批样本、不同班次/温度/光照样本。

输出：

- 成像约束表：光源、镜头、相机、分辨率、景深、触发、曝光。
- 特征可见性判断：目标特征是否在原始图像中可被稳定区分。
- 不可算法化风险：缺陷/字符/边缘在成像上不可见或与正常变化混淆。

### 2. 坐标层：把像素变成可解释的量

目标：把“图上看起来对”变成“机械、测量、机器人都能复用的坐标”。

步骤：

1. 区分任务坐标需求：像素定位、亚像素测量、世界坐标测量、机器人抓取、3D 位姿。
2. 像素级定位任务：记录 ROI、模板原点、匹配坐标、旋转角。
3. 尺寸测量任务：使用标定或比例尺，不把像素距离直接当成工程尺寸。
4. 机器人/多相机任务：建立相机内参、外参、手眼或多视角坐标链。
5. 3D 任务：检查点云单位、法线方向、坐标系定义、CAD/传感器坐标是否一致。

输出：

- 坐标链说明：Image -> Camera -> World -> Robot/Part。
- 标定策略：单相机、多相机、手眼、3D 传感器或结构光。
- 精度预算：成像分辨率、标定误差、重复定位误差、机械误差。

### 3. 算法层：按特征类型选算子族

目标：用 HALCON 的“算子族”匹配问题结构，而不是凭习惯堆 threshold/morphology。

步骤：

1. 目标是“有形状的已知对象”：优先 shape-based matching 或 generic shape model。
2. 目标是“灰度外观稳定的小模板”：可试 NCC，但一旦亮度/形变/遮挡/边界导致 score 不稳，切换 shape/deformable/descriptor。
3. 目标是“边缘位置/尺寸”：使用 1D Measuring 或 2D Metrology。
4. 目标是“字符/词”：优先 Deep OCR；字符被严格分割且字体稳定时才考虑传统 OCR 分类器。
5. 目标是“与好品差异”：固定姿态可用 variation model；纹理表面用 texture inspection；复杂语义缺陷用 anomaly detection/segmentation/object detection。
6. 目标是“3D 位姿”：点云/CAD 对齐用 surface-based matching；多视角 CAD 目标可评估 Deep 3D Matching；抓取点用 3D gripping point detection。

输出：

- 算子路线图：主路线、备选路线、触发切换条件。
- 参数实验表：每轮只改 1-2 个关键参数，记录精度、漏检、误检、耗时。
- 可视化证据：中间 region/XLD/contour/result handle/score image。

### 4. 工程层：从 HDevelop 证明到产线可维护

目标：把交互式脚本变成长期运行、可诊断、可部署的软件。

步骤：

1. 在 HDevelop 中快速原型：使用 Assistant、单步、变量窗口、graphics window、profiler。
2. 固化接口：输入图像/点云、输出 OK/NG、坐标、角度、尺寸、置信度、缺陷区域、错误码。
3. 封装 procedure 或导出代码：C/C++/C#/.NET/Python 或 HDevEngine，避免业务系统直接拼散乱算子。
4. 管理 handle 生命周期：模板、metrology model、variation model、texture model、DL model、surface model 明确初始化、复用、释放。
5. 做产线诊断包：保存原图、参数快照、中间结果、最终结果、耗时、版本、光源/相机配置。
6. 做版本兼容检查：HALCON Progress/Steady、授权模块、GPU/CUDA/OpenVINO/TensorRT、OS、driver、第三方库。

输出：

- `init / process / debug / dispose` 四段式接口。
- 参数文件与模型文件清单。
- 回放测试集与性能基线。
- 现场调试 SOP。

## 核心框架二：算子选择决策树

### A. 定位与模板匹配

1. 轮廓稳定、纹理/亮度不稳定：选 shape-based matching。
2. 有多个模板或多目标类别：选 `find_shape_models` 或 generic shape model，管理 `ModelIDs`、`MaxOverlap`、`NumMatches`。
3. 只需外观相关性且灰度稳定：可选 NCC；但 NCC score 低或不稳定时，不应继续强行降阈值，应评估 shape/deformable/descriptor。
4. 局部形变明显：评估 deformable matching。
5. 平面纹理/特征点丰富、对象不适合轮廓模板：评估 descriptor-based matching。
6. 需要 3D pose：2D matching 只能给图像位姿；要输出空间位姿时必须接标定、PnP/投影链或直接用 3D matching。

关键参数：

- `AngleStart / AngleExtent`：不要给无限大搜索范围，先用机械约束收窄。
- `MinScore`：先用代表性样本统计 score 分布，再定生产阈值。
- `NumLevels`：自动金字塔层数可能漏掉细小或弱特征；漏检时优先检查层数，而不是单纯降低 `MinScore`。
- `Greediness`：速度和完整性权衡；上线前用边界样本验证。
- `SubPixel`：测量/装配定位任务应明确启用并验证亚像素策略。

### B. 测量

1. 单条边、边缘对、宽度、间距：先用 1D Measuring。
2. 圆、椭圆、矩形、直线等几何对象：使用 2D Metrology。
3. 目标位置会变化：先匹配定位，再通过 alignment 更新测量对象位置。
4. 边缘候选多、毛刺多：使用 polarity、contrast、position、pair distance 或 fuzzy measure 控制候选选择。
5. 要工程尺寸：必须标定或做像素-世界转换；只在纯相对比较中接受像素单位。

关键参数：

- `Sigma`：边缘平滑尺度；过小抗噪差，过大吞掉细边。
- `Threshold`：边缘幅值门槛；必须按现场噪声和对比度统计。
- `Transition`：正负边缘方向；由物理明暗关系决定。
- measure region 长宽/间距：覆盖边缘波动，但不要引入邻近干扰边。
- RANSAC/拟合结果：看残差、边缘数量、异常点，而不是只看最终尺寸。

### C. OCR / OCV / 读码

1. 读词、自然场景文字、字符连在一起：优先 Deep OCR。
2. 单字符被稳定分割、字体有限、字符集受控：可用传统 OCR MLP/SVM/KNN。
3. 需要验证印字是否正确、清晰、缺笔：区分 OCR（读内容）与 OCV（验证外观质量）。
4. 需要码制识别：不要用 OCR 读 Data Matrix/QR/Barcode，应使用 Identification 算子族。
5. Deep OCR 上线前必须记录检测框、识别结果、候选字符、置信度分布和拒识策略。

关键参数：

- 检测组件与识别组件：默认模型准确，compact 模型更快但可能较低精度。
- 图像预处理：尺寸、通道、灰度/real 类型、方向、对比度与文字高度。
- 字符集/lexicon：能用业务词表约束时不要浪费模型自由度。
- 置信度：不要把最高候选当真值；设置复核/拒识/二次采图逻辑。

### D. 缺陷检测

1. 姿态固定、好品可对齐、缺陷表现为局部差异：variation model。
2. 纹理表面、正常纹理本身有随机变化：texture inspection。
3. 好品样本足够、缺陷类型未知或稀少：deep anomaly detection。
4. 缺陷类别明确且有标注：classification / object detection / segmentation。
5. 需要缺陷面积、位置、形态计量：优先 segmentation 或传统阈值+形态学/XLD 后处理。
6. 缺陷不可见或与正常波动重叠：回到成像层，不要指望模型凭空分辨。

关键判断：

- 好品变化范围是否覆盖真实生产波动。
- 坏品是否混入好品训练集。
- 缺陷是像素级异常、结构异常、语义异常还是测量超差。
- 检测结果是否能被质量工程接受：位置、面积、严重度、可追溯图。

### E. 标定与 3D

1. 需要尺寸或空间 pose：先设计标定，不要后补。
2. 单相机平面测量：相机标定 + 平面世界坐标映射。
3. 多相机/立体：multi-view 或 binocular calibration，统一坐标系。
4. 相机配机器人：hand-eye calibration，明确 eye-in-hand / eye-to-hand。
5. CAD/点云匹配：surface-based matching；检查采样、法线、遮挡、噪声、score。
6. 多视角 2D 图像推 3D pose：评估 Deep 3D Matching，但要满足多视角标定与模型要求。
7. 点云重建：根据传感器和任务选 stereo、structured light、sheet of light、photometric stereo、depth from focus 等路线。

关键参数/对象：

- `create_calib_data`、`set_calib_data_cam_param`、`set_calib_data_calib_object`、`find_calib_object`、`calibrate_cameras`。
- 标定板质量、拍摄姿态覆盖、finder pattern 可见性、重投影误差。
- `create_surface_model`、`find_surface_model`、`ReturnResultHandle='true'`、`get_surface_matching_result`。
- 点云点密度、法线方向、法线计算方法、CAD 采样、坐标单位。

## 核心框架三：调试闭环

一句话：每一个 NG/漏检/误检都必须能回放、解释、定位到层级。

### 1. 回放

保存以下内容：

- 原图或原始点云，不只保存截图。
- 相机曝光、增益、触发时间、光源状态、镜头/工位编号。
- HALCON 版本、授权模块、运行平台、GPU/driver。
- 参数文件、模型文件、标定文件、模板文件、DL 模型文件。
- 中间结果：ROI、region、XLD、matching result、metrology contour、score image、DL heatmap/region。

### 2. 归因

按顺序排查：

1. 成像问题：过曝、欠曝、反光、污渍、虚焦、运动模糊、产品姿态漂移。
2. 坐标问题：ROI 未跟随、模板 origin 错、标定文件错、世界坐标链错。
3. 算法问题：阈值、金字塔层数、候选边选择、训练样本污染、score 分布漂移。
4. 工程问题：handle 复用错误、线程共享状态、内存泄漏、版本/授权/路径问题。
5. 产线问题：换批、夹具磨损、物料供应商差异、环境温度、光源衰减。

### 3. 改动

每次只改少量参数，并保存：

- 改动原因。
- 受影响样本。
- 漏检/误检变化。
- 单张耗时和吞吐。
- 是否需要重新标定、重新训练、重新验证。

## 决策规则

1. 如果目标特征在原图中不可稳定区分，先改光学/照明/机构，不先调算法。
2. 如果任务输出是尺寸、空间 pose 或机器人坐标，先完成标定与坐标链设计，再写检测逻辑。
3. 如果对象轮廓稳定但灰度变化大，优先 shape-based matching；如果灰度外观稳定且变化小，才考虑 NCC。
4. 如果匹配漏检发生在细小模板或弱轮廓上，先检查 `NumLevels`、ROI、模型轮廓和角度范围，再下调 `MinScore`。
5. 如果测量对象位置会随工件姿态变化，先用 matching 定位，再对 metrology/measure ROI 做 alignment。
6. 如果边缘候选有多条，必须用 transition、contrast、position、distance/fuzzy 规则约束候选；不要靠取第一个结果。
7. 如果字符是词级或未可靠分割，优先 Deep OCR；如果字符分割稳定、字符集很小、字体固定，传统 OCR 仍可更轻量。
8. 如果缺陷类别未知且坏样本少，用 anomaly/variation/texture 路线；如果缺陷类别明确且标注足够，用 detection/segmentation/classification。
9. 如果做 3D surface matching，必须验证点云法线、采样密度、遮挡比例、score 子项和 result handle；不要只看 pose 是否“看起来对”。
10. 如果要部署到产线，必须在 HDevelop 原型之外建立模型/参数/标定文件版本、回放集、异常日志、耗时基线和释放策略。

## 检查清单一：方案设计评审

- [ ] 目标输出是否明确：OK/NG、坐标、角度、尺寸、字符、缺陷区域、3D pose、抓取点。
- [ ] 原图/点云是否包含足够信息，而不是依赖后处理“猜”。
- [ ] 是否有好品、坏品、边界样本、不同批次、不同班次、现场干扰样本。
- [ ] 是否明确像素坐标、相机坐标、世界坐标、机器人坐标之间的转换关系。
- [ ] 是否需要标定；若需要，标定板、拍摄姿态、重投影误差和标定文件版本是否受控。
- [ ] 算子族是否匹配问题结构：matching、measuring、OCR、inspection、DL、3D。
- [ ] 是否有主路线和备选路线，以及切换条件。
- [ ] 是否定义验收指标：漏检率、误检率、重复精度、GRR/MSA、节拍、内存、恢复时间。
- [ ] 是否有可解释中间结果，方便现场人员判断失败原因。
- [ ] 是否确认 HALCON 版本、授权模块、系统、GPU/driver、第三方依赖。

## 检查清单二：上线与现场调试

- [ ] HDevelop 原型已冻结，并导出 procedure/代码或通过 HDevEngine 集成。
- [ ] `init / process / debug / dispose` 生命周期清楚，handle 不在每帧重复创建。
- [ ] 模板、DL model、variation/texture/metrology/surface model、标定文件有版本号。
- [ ] 每帧记录必要日志：输入 ID、结果、score/confidence、耗时、异常码。
- [ ] NG、漏检、误检样本能回放，且能重现同样结果。
- [ ] 中间结果可按开关保存，不影响正常节拍。
- [ ] 多线程环境中确认 HALCON operator/handle 的线程安全和状态修改行为。
- [ ] 长时间运行做过内存和 handle 泄漏观察。
- [ ] 光源衰减、镜头污染、焦距变化、夹具磨损有巡检或报警逻辑。
- [ ] 更新 HALCON 版本、模型或参数后，跑固定回归样本集并保存对比报告。

## 反模式

1. 阈值炼丹：缺陷、字符、边缘不可稳定分离时，继续堆 `threshold`、`opening`、`closing`，而不回到照明和样本分布。
2. 低分放行：匹配不稳时只降低 `MinScore`，不检查金字塔层数、模型轮廓、极性、遮挡、ROI、角度范围。
3. 像素即尺寸：没有标定或比例验证，就把像素距离当作毫米输出。
4. 好品污染训练：variation/texture/anomaly 训练集中混入坏品或边界坏品，导致模型把缺陷学成正常。
5. 原型即产线：HDevelop 里跑通后直接上线，没有日志、回放、参数版本、异常处理和资源释放。

## 边界声明

- 本方法论基于 MVTec 官方公开文档与算子参考提炼，不替代具体 HALCON 版本的 Operator Reference。参数默认值、授权模块、深度学习支持、CUDA/driver 要以项目使用版本为准。
- HALCON 算子不能弥补成像物理缺失。目标特征没有进入图像/点云，或被正常波动完全覆盖时，应优先改硬件、工装和采集条件。
- 深度学习路线需要数据治理、标注质量、训练/验证集划分和现场漂移监控；不能把 pretrained model 当作免验证方案。
- 3D 与机器人项目的主要风险常在坐标链、标定、机械重复性和现场遮挡，不只在 `find_*` 算子。
- MVTec 示例程序适合学习算子组合与调参思路，但不能直接代表生产级异常处理、日志和工程架构。

## 适用场景

- 工业零件定位、姿态估计、抓取前定位、装配引导。
- 尺寸测量、边缘/孔径/轮廓/间距检测、几何拟合。
- 印字 OCR/OCV、标签字符识别、受控字符集读取。
- 表面缺陷、纹理缺陷、外观异常、缺陷分类与分割。
- 相机标定、手眼标定、多相机、3D 重建、点云/CAD matching。
- HALCON 原型从 HDevelop 走向 C++/C#/Python/.NET/HDevEngine 部署。

## 不适用场景

- 目标缺陷无法通过任何成像手段呈现的检测任务。
- 需要端到端业务系统设计、MES/PLC/运动控制完整架构，但没有视觉输入输出边界。
- 纯学术 CV 研究，不依赖 HALCON 算子体系或工业现场约束。
- 非受控自然场景、大规模开放世界识别，且没有稳定采集条件和闭环验证。
- 只要求写入门教程或语法速查，而不需要项目决策和上线方法论。

## 方法论压缩版

1. 先证明图像有信息。
2. 再证明坐标链成立。
3. 然后按特征类型选算子族。
4. 用代表性样本调参数，不用单张漂亮图调参数。
5. 保存中间结果，让每次失败可解释。
6. 部署前固化模型、参数、标定、版本、日志、回放和资源释放。

