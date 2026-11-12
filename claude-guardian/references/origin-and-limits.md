# 来源与限制

- 上游：[DUNHKpcc/Claude-Guardian](https://github.com/DUNHKpcc/Claude-Guardian)
- 参考提交：06fe998d753f697c47ae0b67be5fe91451532a1f
- 上游入口版本：0.2.0
- 本地变体：0.2.0-local-readonly.1
- 本地改编日期：2026-10-31
- 许可：GPL-3.0-only；完整许可见包内 LICENSE，原项目贡献者的权利不因本地改编而改变。

## 本地改动声明

入口指令重新编写，仅保留只读环境评估与订阅条件说明的用途。没有复制上游的修复/清理脚本、PDF、图片或其他运行资源。没有安装原版命令、后台服务、钩子或 MCP 服务。

本地版本去除了系统网络改动、账号清理、社区经验绝对化表达，以及将第三方检测评分视为订阅资格的判断。不得把原版未包含在此包中的功能视为本地已安装能力。

此版本从本地目录导入，不自动跟随上游 GitHub 更新。更新前应重新审查范围，不应将源直接切回上游并覆盖本地限制。

## 官方政策核对入口

以下是查阅入口，不表示这里已经核实其当前内容。回答现行资格或支付政策前，应读取当时的官方页面并确认生效时间；失效链接需从官方帮助中心继续查找。

- [Claude 可用地区](https://support.claude.com/en/articles/8461763-where-can-i-access-claude)
- [订阅 Claude Pro](https://support.claude.com/en/articles/8325609-how-do-i-sign-up-for-the-pro-plan)
- [银行卡被拒说明](https://support.claude.com/en/articles/9402418-why-was-my-card-declined)

## 证据边界

- 本机代理启用只证明配置标志，不证明代理正在运行。
- 单次网络可达只证明该目标在该时刻有响应。
- IP 归属、时区、语言、IPv6 或第三方评分均不能单独证明实际所在地、订阅资格或账户风险。
- 本技能没有服务方的风控数据，不能预测是否封号或保证支付成功。
- 安装本技能不授权未来的联网探测或账号/系统修改。

