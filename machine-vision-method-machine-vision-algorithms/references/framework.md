# 《Machine Vision Algorithms and Applications》可执行方法论

对象：Carsten Steger, Markus Ulrich, Christian Wiedemann, *Machine Vision Algorithms and Applications*, 2nd Edition, Wiley-VCH, 2018  
适配行业：机器视觉软件和算法工程师  
提炼目标：把书中的机器视觉工程方法转化为可执行判断框架，而不是读书笔记。  
调研日期：2026-08-28

## 来源清单

1. Wiley-VCH 官方书页：确认书名、作者、版本、出版信息、章节结构、第二版扩展范围，以及“理论基础 + 应用重点 + HALCON 13 示例”的定位。  
   URL: https://www.wiley-vch.de/en/areas-interest/natural-sciences/physics-11ph/optics-photonics-11ph4/machine-vision-algorithms-and-applications-978-3-527-41365-2
2. Wiley-VCH 官方目录 PDF：用于章节级追溯。目录显示第 2 章为图像采集，第 3 章为机器视觉算法，第 4 章为应用案例。  
   URL: https://application.wiley-vch.de/books/sample/3527413650_ftoc.pdf
3. Wiley-VCH 官方样章第 1 章 Introduction：用于确认机器视觉典型任务、系统组成、多学科边界，以及本书关注“从图像中提取相关信息”的范围。  
   URL: https://application.wiley-vch.de/books/sample/3527413650_c01.pdf
4. MVTec Research & Teaching / Publications：确认该书是 MVTec 公开宣称的机器视觉专业知识载体，并提供书中应用示例程序下载入口。  
   URL: https://www.mvtec.com/research-teaching/publications
5. MVTec HALCON 产品页：用于补充工业级实现取向，包括图像采集到深度学习的工具覆盖、并行/GPU、亚像素测量、标定与世界坐标测量。  
   URL: https://www.mvtec.com/products/halcon
6. MVTec HALCON Features & Tools：用于验证 HALCON 面向可靠工业检测、测量、识别、3D 与部署工作流。  
   URL: https://www.mvtec.com/products/halcon/features-tools
7. MVTec Machine Vision Applications：用于归纳工业应用场景：质量检测、识别、测量、3D Matching、目标识别。  
   URL: https://www.mvtec.com/application-areas/applications
8. MVTec HALCON Documentation：用于定位 Reference Manual、Solution Guides、Programmer Manuals、Technical Notes 等工程资料源。  
   URL: https://www.mvtec.com/products/halcon/documentation
9. HALCON Image Source Operator Reference：用于现代图像采集抽象、设备/接口/流参数、触发与缓冲元数据等工程规则。  
   URL: https://www.mvtec.com/doc/halcon/2511/en/toc_imagesource.html
10. HALCON `find_shape_model` Operator Reference：用于 ROI/domain 决定搜索空间、边界模型、亚像素参数、金字塔层级与贪婪度等匹配规则。  
    URL: https://docs.mvtec.com/hdevelopevo/25.05.0.2-preview/content/reference/operators/find_shape_model.html
11. HALCON Filters Operator Reference：用于 reduced domain 下滤波边界、未定义像素、连续滤波误差传播等实现风险。  
    URL: https://www.mvtec.com/doc/halcon/1911/en/toc_filters.html
12. HALCON Region Morphology Operator Reference：用于形态学连接/分离、开闭运算、结构元素选择等规则。  
    URL: https://www.mvtec.com/doc/halcon/2211/en/toc_morphology_region.html
13. MVTec Measuring Technology：用于补充 1D/2D/3D 亚像素测量、边缘、轮廓拟合、灰度标定与 3D 重建的公开说明。  
    URL: https://www.mvtec.com/knowledge-base/technologies/measuring

## 核心框架

### 框架 1：成像优先的机器视觉闭环

来源：第 1 章 Introduction；第 2 章 Image Acquisition；第 3 章 Machine Vision Algorithms；第 4 章 Machine Vision Applications；HALCON Image Source 文档。

适用场景：新建检测/测量/识别/定位项目，或算法在实验图上可行但上线不稳定。

步骤：

1. 定义视觉任务：把需求归类为对象识别、位置检测、完整性检查、形状/尺寸检测、表面检测之一；输出验收指标，如漏检率、误检率、定位误差、测量重复性、节拍。
2. 先设计成像链路：确定照明方向/光谱、镜头、景深、相机、触发、接口、曝光、增益、运动状态；输出一份采集配置表和风险项。
3. 约束图像域：定义 ROI/domain、坐标系、遮光/环境光控制、工件姿态范围；输出每个算法阶段使用的 domain。
4. 选择算法链：按“增强/变换 → 分割/边缘/形态学 → 特征/拟合/匹配/分类 → 决策”的顺序组合，而不是孤立挑一个算子。
5. 回到应用场景验证：用第 4 章式的案例拆解方法，把算法链映射为“定位基准 → 提取对象 → 测量/识别/检查 → 输出 OK/NG 或 pose”的流程。
6. 设计生产接口：触发、缓冲、时间戳、异常图保存、PLC/上位机结果字段必须在原型阶段定义。

输出物：视觉任务定义、采集配置表、ROI/domain 图、算法链路图、验收指标表、失败样本库。

### 框架 2：几何测量与定位的精度链

来源：第 2.2 节 Lenses；第 2.3 节 Cameras；第 3.7 节 Edge Extraction；第 3.8 节 Segmentation and Fitting of Geometric Primitives；第 3.9 节 Camera Calibration；第 3.10 节 3D Reconstruction；第 4.7 节 Measurement of Spark Plugs；第 4.10 节 3D Plane Reconstruction with Stereo；MVTec Measuring Technology。

适用场景：尺寸测量、几何公差检测、机器人定位、3D 平面/姿态重建。

步骤：

1. 把精度预算拆成硬件项和算法项：镜头畸变、景深、像元尺寸、噪声、运动模糊、照明对比度、标定误差、边缘定位误差、拟合残差。
2. 选择几何模型：普通面阵、远心、倾斜镜头、线扫、双目、结构光、光切、ToF；输出“为什么该模型足够”的假设清单。
3. 标定再测量：需要世界坐标或真实尺寸时，先做相机/系统标定，再使用亚像素边缘、轮廓或几何基元拟合。
4. 用鲁棒拟合处理污染：当轮廓含毛刺、遮挡、反光或局部缺陷时，优先考虑 robust line/circle/ellipse fitting，而不是让最小二乘吃下所有点。
5. 验证重复性与偏差：用标准件、重复采集、边缘方向变化、光照变化、姿态变化测量偏差；输出 Cg/Cgk、GRR 或项目内等价指标。

输出物：精度预算表、标定方案、测量算子链、重复性报告、残差/异常点可视化。

### 框架 3：应用模式到算法组合的路由表

来源：第 3 章各算法主题；第 4 章 Wafer Dicing、Reading of Serial Numbers、Saw Blades、Print Inspection、BGA、Surface Inspection、Molding Flash、Punched Sheets、Pose Verification、Non-Woven Classification、Surface Comparison、3D Pick-and-Place；MVTec Applications。

适用场景：面对一个视觉需求时，快速选择第一版方案并规划验证样本。

步骤：

1. 若目标是“有无/完整性/数量”：优先试 ROI + threshold/dynamic threshold/variation model + connection + morphology + region features。
2. 若目标是“尺寸/角度/位置”：优先试 edge extraction + subpixel contour + geometric primitive fitting + calibration/world coordinates。
3. 若目标是“已知零件定位/姿态”：优先试 template/shape-based matching；若为 3D pose，则路由到 shape-based 3D 或 surface-based 3D matching。
4. 若目标是“字符/码/序列号”：拆成 rectification/定位、character segmentation、feature extraction/classifier 或 OCR 模型。
5. 若目标是“纹理/材质/难定义缺陷”：优先建立正常样本模型或分类器，并把训练/验证/测试集分离。
6. 若目标是“机器人抓取/装配”：先解决手眼标定、pose 定义、坐标变换和抓取点，再谈检测算法。

输出物：任务类型、推荐算法组合、最小样本集、必须验证的扰动条件、失败时的下一条路线。

## 决策规则

1. 如果图像中的目标差异不能稳定显现，则先改照明、镜头、曝光、遮光和机械定位，再调分割阈值。来源：第 1 章系统组成；第 2.1-2.4 节图像采集；样章强调成像组件对图像质量的影响。
2. 如果用户要求真实尺寸、角度或机器人坐标，则必须引入标定和坐标模型；不能只用像素距离给结论。来源：第 3.9 节 Camera Calibration；第 3.13 节 Hand-Eye Calibration；第 4.7、4.10、4.14 节应用。
3. 如果测量精度要求高于像素级，则使用亚像素边缘/轮廓和几何拟合，并记录边缘方向、滤波尺度、拟合残差。来源：第 3.7 节 Edge Extraction；第 3.8 节 Geometric Primitives；MVTec Measuring Technology。
4. 如果对象可以通过灰度或颜色与背景分离，则从 threshold/dynamic threshold/variation model 开始，再用 connection、morphology、region features 做结构化筛选。来源：第 3.4 节 Image Segmentation；第 3.5 节 Feature Extraction；第 3.6 节 Morphology；HALCON Region Morphology 文档。
5. 如果连通域被粘连或有小毛刺，则先选择结构元素并用 erosion/dilation/opening/closing 验证拓扑变化；不要直接靠面积阈值硬切。来源：第 3.6 节 Morphology；HALCON Region Morphology 文档关于连接/分离与开闭运算。
6. 如果使用 reduced domain 后还要连续滤波，则必须显式处理边界：扩大 ROI 后裁掉边缘、expand domain、full domain 或 crop domain；否则边界未定义像素会把误差传进后续滤波。来源：第 3.1-3.2 节数据结构与增强；HALCON Filters 文档。
7. 如果是已知形状的 2D 定位，且姿态范围可约束，则优先用 shape/template matching，并收窄 ROI、角度范围、尺度范围和 pyramid 层级以换取稳定性与速度。来源：第 3.11 节 Template Matching；HALCON `find_shape_model` 文档。
8. 如果模型可能贴近图像边界或 ROI 边界，则必须验证 border behavior；必要时扩大 domain 或启用对应边界模型参数，并接受运行时间上升。来源：HALCON `find_shape_model` 文档；第 3.11 节 Template Matching。
9. 如果需要 3D 信息，则先问“要测高度/平面、求 6D pose、还是做抓取”；不同目标分别路由到 stereo、sheet/structured light、3D matching 或 hand-eye calibration，而不是泛泛说“上 3D 相机”。来源：第 2.5 节 3D Image Acquisition Devices；第 3.10、3.12、3.13 节；第 4.10、4.14 节。
10. 如果使用分类、OCR 或深度学习相关方法，则必须拆分训练/验证/测试集，并把字符分割/特征抽取/分类边界写清楚；不能只报告训练集效果。来源：第 3.14 节 OCR；第 3.15 节 Classification，尤其 training/test/validation sets 与 novelty detection 主题。

## 检查清单

### 检查清单 1：视觉方案立项/原型评审

- [ ] 任务已归类：识别、定位、完整性、尺寸/形状、表面检测、3D/机器人之一。
- [ ] 已定义 OK/NG 或数值输出字段，并包含单位、坐标系、置信度或分数。
- [ ] 已列出节拍、漏检/误检、重复性、环境扰动、维护成本等验收指标。
- [ ] 已固定照明类型、方向、光谱、曝光、增益、镜头、焦距、工作距离、景深。
- [ ] 已说明相机接口、触发、频闪、缓冲、时间戳、丢帧处理、异常图保存策略。
- [ ] 已定义 ROI/domain，并说明每个滤波、分割、匹配、测量阶段是否改变 domain。
- [ ] 已准备覆盖良品、典型缺陷、边界缺陷、污染、姿态偏移、光照波动、批次差异的样本集。
- [ ] 已有失败样本复盘方式：保存原图、参数、版本、设备状态和最终判定。

### 检查清单 2：算法链上线前评审

- [ ] 分割/边缘/匹配/分类的每一步都有可视化中间结果。
- [ ] 所有阈值都有来源：物理意义、统计分布、标定结果或验证集搜索，不是手感数字。
- [ ] 亚像素测量已验证重复性、偏差和异常点影响。
- [ ] 标定已验证重投影误差、工作平面/体积范围、焦距/光圈/姿态变化影响。
- [ ] ROI 边界、图像边界、reduced domain 滤波边界已做专门测试。
- [ ] 形态学结构元素大小与被检对象尺度相关，不是从示例程序复制。
- [ ] Matching 已测试遮挡、旋转、尺度、边界、相似干扰物、最小分数与重叠参数。
- [ ] 分类/OCR 已分离训练、验证、测试；测试集包含上线会遇到的难例。
- [ ] 性能已按目标硬件测试，包括最坏图像、最大 ROI、最大候选数和并发采集。
- [ ] 版本升级或 HALCON 算子参数变化有回归样本集兜底。

## 反模式

1. 算法先行，成像后补：在低对比、反光、阴影、运动模糊图像上堆阈值和滤波，会把问题从物理层拖到软件层，后期更难稳定。
2. ROI 当裁图，忽略 domain 语义：HALCON 中 domain 会影响滤波、匹配搜索空间和边界行为；把它当普通矩形裁剪容易造成漏检或边界伪影。
3. 用像素面积/像素距离交付测量项目：没有标定、畸变校正和精度预算时，像素指标很难对接真实公差。
4. 把形态学当“清理噪声按钮”：结构元素不绑定对象尺度和拓扑目标时，开闭运算会误删小缺陷、连错对象或改变测量边界。
5. 只在漂亮样本上调参：第 4 章应用案例的价值在组合验证；上线前不覆盖姿态、照明、缺陷边界和节拍压力，原型准确率没有工程意义。

## 边界声明

- 本提炼主要基于 Wiley 官方书页、目录、样章和 MVTec/HALCON 公开资料，未逐页访问完整商业版权文本；章节来源可追溯到公开目录，但细节规则应在正式 Skill 发布前用原书全文复核。
- 该书第二版出版于 2018 年，示例基于 HALCON 13；现代 HALCON 的 Image Source、深度学习、GPU、部署和文档结构已有更新，因此涉及当前 API 时应以现行 HALCON 文档为准。
- 本书核心强项是工业机器视觉的成像、几何、传统算法、标定、匹配和应用组合；不是深度学习模型训练、MLOps、主动学习、Transformer 检测器或生成式视觉的最新方法手册。
- 第 1 章明确本书聚焦到“从图像中提取相关信息”为止；PLC、现场总线、产线控制、MES/SCADA 集成、工装机械设计只作为接口边界，不应由本方法论单独覆盖。
- 该方法论假设工业场景中可控制照明、位置、触发或样本采集；开放世界、户外非受控视觉、消费级拍照识别需要引入其他计算机视觉/机器学习框架交叉验证。

## 适用场景

- 工业检测：表面缺陷、印刷检测、BGA/PCB/零件完整性、孔位/轮廓检查。
- 精密测量：1D/2D/3D 尺寸、角度、半径、平面高度、世界坐标测量。
- 识别与定位：序列号/OCR、条码前后处理、已知零件匹配、pose verification。
- 机器人视觉：手眼标定、3D pick-and-place、抓取点定义、姿态验证。
- HALCON 项目方案评审：算子链、domain、标定、性能、可维护性、上线风险。

## 不适用场景

- 主要依赖大规模标注数据训练的通用目标检测、语义分割、多模态模型评测。
- 完全不可控环境下的开放世界视觉，如自动驾驶全栈感知、街景理解、社交媒体图片理解。
- 纯相机/镜头硬件选型采购报告；本方法论能提出成像需求，但不能替代供应商实测。
- 产线电气、PLC、MES、网络安全、法规验证等非视觉算法主导的系统工程。
- 需要最新 HALCON 版本 API 精确参数时，应直接查当前 HALCON Operator Reference 和 Release Notes，而不是沿用 2018 书中示例。
