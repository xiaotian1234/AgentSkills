# 《Domain-Driven Design》方法论存档

- 作者：Eric Evans
- 版本基线：Addison-Wesley，2003/2004；以作者公开 DDD Reference 和后续演讲校准重点
- 调研截止：2026-09-17

## 核心框架

### 1. 知识消化与统一语言（第 1-3 章）

适用：需求频繁误解、业务术语与代码命名脱节、规则散落在 UI 和条件分支中。

步骤：与领域专家围绕真实案例建模；形成 Ubiquitous Language；让语言进入对话、测试、代码和文档；发现矛盾时修改模型与语言，而不是维护双重词典。

输出：术语表、关键业务场景、模型草图、可执行示例。

### 2. 战略设计：核心领域、限界上下文和上下文映射（第 14-16 章）

适用：大型系统拆分、团队边界、遗留系统共存、服务或模块划分。

步骤：识别 Core Domain；将不同模型放入明确 Bounded Context；画 Context Map；为上下文关系选择 Shared Kernel、Customer/Supplier、Conformist、Anticorruption Layer、Open Host Service 或 Published Language；把最好人才投入核心领域。

输出：领域分区、上下文图、关系模式、集成契约和投资优先级。

### 3. 模型驱动设计与聚合一致性边界（第 4-7、9-13 章）

适用：领域对象、状态机、事务边界和复杂规则设计。

步骤：隔离 Domain Layer；区分 Entity、Value Object、Service；用 Aggregate 定义不变量和事务边界；通过 Factory 创建复杂对象，通过 Repository 提供集合式访问；持续重构到更深的业务概念。

输出：领域模型、聚合边界、不变量、仓储接口、领域服务和测试示例。

## 决策规则

1. 如果同一术语在不同团队含义不同，则先划分上下文，不要强行建立全局模型。（第 14 章）
2. 如果业务价值主要集中在少数规则，则把最强设计能力投入 Core Domain。（第 15 章）
3. 如果外部或遗留模型会污染核心模型，则建立 Anticorruption Layer。（第 14 章）
4. 如果对象由属性值定义且无持续身份，则建模为不可变 Value Object。（第 5-6 章）
5. 如果操作不自然属于 Entity 或 Value Object，则使用无状态 Domain Service。（第 5 章）
6. 如果一组对象必须共同维护不变量，则定义 Aggregate Root，并限制外部只引用根。（第 6 章）
7. 如果事务跨越多个聚合，则重新检查一致性是否真的需要同步完成。（第 6、14 章及后续作者演讲）
8. 如果代码命名无法与领域专家直接讨论，则模型尚未形成统一语言。（第 2-3 章）
9. 如果模型只反映数据库表或 UI 表单，则回到领域行为和约束重新建模。（第 4-5、9 章）
10. 如果要替换大型遗留系统，则优先建立 Bubble Context 等渐进边界，不做大爆炸重写。（作者 2011 遗留系统演讲）

## 上下文与聚合检查清单

- [ ] 核心领域、支撑子域和通用子域已区分。
- [ ] 每个 Bounded Context 有明确语言、模型、代码和数据边界。
- [ ] Context Map 标明上下游关系和集成模式。
- [ ] 外部模型是否需要 ACL 已评估。
- [ ] Entity 身份、Value Object 值语义和 Service 职责清楚。
- [ ] 每个 Aggregate 的不变量、根和事务边界明确。
- [ ] Repository 只面向需要持久化访问的聚合根。
- [ ] 模型能用真实业务案例和测试表达。

## 反模式

1. 一个企业一个统一模型：忽略语境差异，制造巨大共享模型。（第 14 章）
2. 贫血领域模型：对象只有数据，规则散落在应用服务。（第 4-5 章）
3. 数据库驱动建模：把表结构当成领域真相。（第 4、9 章）
4. 巨型聚合：把便利的对象图误作事务一致性边界。（第 6 章）
5. 对所有子域同等投入：在通用能力上消耗核心团队。（第 15 章）

## 边界

- DDD 适合业务规则复杂、语言和模型能创造价值的系统；简单 CRUD 不必完整采用。
- 原书战术示例具有早期 Java/面向对象时代痕迹，原则可迁移，实现方式需现代化。
- Bounded Context 是模型语义边界，不自动等于微服务、进程或数据库。
- DDD 不直接解决性能、可用性、视觉算法或实时设备控制，需要其他方法交叉评审。

## 来源

- https://www.domainlanguage.com/ddd/reference/
- https://domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
- https://www.dddcommunity.org/uncategorized/what-ive-learned-about-ddd-book-talk-eric-evans/
- https://www.dddcommunity.org/library/evans_2009_2/
- https://www.dddcommunity.org/news/eric-evans-talk-what-i-learned-about-ddd-book-qcon-2009-published-infoq/
- https://www.dddcommunity.org/news/index-html-2/?nb=1&share=twitter
- https://www.dddcommunity.org/library/evans_2011_2/
- https://www.dddcommunity.org/uncategorized/ch1_2/
- https://www.dddcommunity.org/uncategorized/foreword_martin_fowler/

