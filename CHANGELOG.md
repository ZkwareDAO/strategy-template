# CTA Strategy Core 变更日志

所有重要变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

## [1.0.0] — 开源初版

- 单体模式框架：每策略独立进程，直连 Binance 行情与下单
- 策略基类体系（`BaseStrategy` / `BaseStrategyCore` / `BaseState`）与两个参考实现
  （`example_ma_cross` 单周期、`example_mtf_trend` 多周期）
- 数据层：CSV 持久化 + WebSocket 实时 K 线 + 多时间框架聚合 + 技术指标
- backtrader 集成回测，与实盘共用策略代码和参数（三层配置模型）
- 信号 CSV 持久化与直连下单（`direct_trading`），仓位 JSON 持久化
- 完整文档：架构 / 脚本参考 / 信号格式 / 策略开发指南
