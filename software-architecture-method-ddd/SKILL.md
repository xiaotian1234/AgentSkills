---
name: software-architecture-method-ddd
description: |
  《Domain-Driven Design》方法论，把统一语言、核心领域、限界上下文、上下文映射、聚合与防腐层转化为软件边界设计流程。
  适用于复杂业务建模、模块或服务拆分、遗留系统隔离和事务边界评审。触发词包括「DDD」「Domain-Driven Design」
  「领域驱动设计」「限界上下文」「聚合设计」「上下文映射」「防腐层」。
---

# 《Domain-Driven Design》：让代码边界服从领域语言

## 什么时候用

- 业务术语和代码命名反复错位：统一语言与知识消化。
- 拆模块、服务或团队边界：战略设计与上下文映射。
- 设计领域对象和事务边界：模型驱动设计与聚合。
- 遗留系统污染新模型：防腐层或 Bubble Context。
- 简单 CRUD、纯算法或基础设施选型不必完整采用 DDD。

普通分析不加载资料文件；仅在用户要求完整章节、作者后续修正、来源审计或争议核验时，读取 [references/framework.md](references/framework.md)。

## 框架一：知识消化与统一语言

来源：第 1-3 章。

1. 与领域专家围绕真实案例和异常场景建模。
2. 形成 Ubiquitous Language，消除一词多义与同义多词。
3. 让语言进入对话、测试、代码和文档。
4. 发现矛盾时修改模型，而不是维护业务词典与技术词典两套真相。

输出：术语表、业务场景、模型草图和可执行示例。

## 框架二：战略设计

来源：第 14-16 章。

1. 识别 Core Domain、Supporting Subdomain 和 Generic Subdomain。
2. 将不同模型放入明确 Bounded Context。
3. 绘制 Context Map。
4. 为上下文关系选择 Shared Kernel、Customer/Supplier、Conformist、Anticorruption Layer、Open Host Service 或 Published Language。
5. 把最强设计能力投入核心领域。

输出：领域分区、上下文图、关系模式和集成契约。

## 框架三：模型驱动设计

来源：第 4-7、9-13 章。

隔离 Domain Layer；区分 Entity、Value Object、Domain Service；用 Aggregate 定义不变量和事务边界；通过 Factory 创建复杂对象，通过 Repository 访问聚合；持续重构到更深概念。

## 决策规则

1. 如果同一术语在不同团队含义不同，先划分上下文，不做全局统一模型。（第 14 章）
2. 如果业务价值集中在少数规则，把最好的人投入 Core Domain。（第 15 章）
3. 如果外部模型污染核心模型，建立 Anticorruption Layer。（第 14 章）
4. 如果对象由属性值定义且无持续身份，建模为不可变 Value Object。（第 5-6 章）
5. 如果操作不自然属于 Entity 或 Value Object，使用无状态 Domain Service。（第 5 章）
6. 如果对象必须共同维护不变量，定义 Aggregate Root，外部只引用根。（第 6 章）
7. 如果事务跨多个聚合，重新检查是否真的需要同步一致。（第 6、14 章及作者后续演讲）
8. 如果命名不能与领域专家直接讨论，统一语言尚未形成。（第 2-3 章）
9. 如果模型只是数据库表或 UI 表单，回到行为与约束重新建模。（第 4-5、9 章）
10. 如果要替换大型遗留系统，优先建立渐进边界，不做大爆炸重写。（作者 2011 演讲）

## 上下文与聚合清单

- [ ] 核心、支撑和通用子域已区分。
- [ ] 每个 Bounded Context 有明确语言、模型、代码和数据边界。
- [ ] Context Map 标明上下游关系和集成模式。
- [ ] 外部或遗留模型是否需要 ACL 已评估。
- [ ] Entity 身份和 Value Object 值语义清楚。
- [ ] 每个 Aggregate 的不变量、根和事务边界明确。
- [ ] Repository 只面向确需持久化访问的聚合根。
- [ ] 模型能用真实业务案例和测试表达。

## 反模式

- 一个企业一个统一模型。（第 14 章）
- 贫血领域模型，规则散落在应用服务。（第 4-5 章）
- 用数据库表结构代替领域建模。（第 4、9 章）
- 巨型聚合，把对象图误作一致性边界。（第 6 章）
- 对所有子域同等投入。（第 15 章）

## 工作流

先判断问题属于语言、战略边界还是战术模型；收集业务实例和不变量；按相应框架产生模型；用清单复核。输出必须区分 Bounded Context、部署单元和数据库边界，不能默认三者相等。

## 边界

- DDD 对规则复杂系统价值最高，简单 CRUD 不宜过度建模。
- 原书战术示例带有早期 Java 时代痕迹，实现方式需要现代化。
- Bounded Context 是语义边界，不自动等于微服务。
- DDD 不直接解决性能、可用性、视觉算法和实时控制。

> 本 Skill 由 career-skill-factory 生成，仅供个人学习，版权归原作者。
