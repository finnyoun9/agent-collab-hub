# 飞书接入

[English](FEISHU.md) | 简体中文

飞书负责入口和通知，Hermes 负责常驻调度，GitHub 保存需要持久化的任务状态。

```text
飞书命令
  -> Hermes / Coordinator
  -> 选择主执行 Agent
  -> 调用本机 CLI 或通知远端 Agent
  -> 汇总结果并回传飞书
```

建议命令：

```text
/task <目标>                创建待分流任务
/quick <目标>               创建并分配给 bench-opencode
/queue                      查看任务队列
/assign <issue> <agent-id>  指定主执行 Agent
/handoff <issue>            查看最新结果
```

普通任务不强制 PR、独立审查或完整测试。高风险任务才进入受控模式。
`FEISHU_WEBHOOK_URL` 等密钥只能通过环境变量提供，不能写入 Issue、文件、
Git 日志或 Agent 消息。
