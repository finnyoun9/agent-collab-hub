# 飞书接入

[English](FEISHU.md) | 简体中文

飞书负责入口和通知，GitHub 负责保存唯一可信状态：

```text
飞书指令/卡片
  -> 现有 bot 或 metabot
  -> GitHub Issue API
  -> Agent 在原生客户端领取并执行
  -> HANDOFF / PR 事件
  -> GitHub Action 或 bot
  -> 飞书卡片通知
```

建议指令：

```text
/task <目标>                创建待分流 Issue
/quick <目标>               创建低风险任务并分配给 bench-workbuddy
/queue                      查看 ready、claimed、blocked 任务
/assign <issue> <agent-id>  指定负责人
/handoff <issue>            查看最新交接
/decision <issue> <内容>    把人工决定写回 GitHub
```

飞书通知默认使用中文。设置 GitHub Actions variable `COLLAB_LANG=en` 可切换为英文；`zh` 为中文。

仓库 secret `FEISHU_WEBHOOK_URL` 只通过环境变量传给通知脚本，不能写入 Issue、文件、Git 日志或 Agent 消息。

当前 bench 长连接实现和启动方式见 [../coordinator/README.zh-CN.md](../coordinator/README.zh-CN.md)。它不需要公网 Gateway；目前通过文本命令创建和分配任务，WorkBuddy 仍需人工打开客户端执行。
