#!/usr/bin/env python3
"""
批量添加中文注释脚本 v2 — 针对 hermes-agent 最新版本
为缺少【产品经理理解要点】的 Python 文件自动添加中文模块概要和关键函数注释
"""

import os
import re
import ast
import sys

# 需要添加注释的核心文件及其业务概要
FILE_SUMMARIES = {
    # ===== gateway 核心运行时 =====
    "gateway/run.py": "Gateway 主运行入口，负责启动、关闭、信号处理和主循环，是整个 Hermes 后台服务的心脏",
    "gateway/config.py": "Gateway 配置加载与校验，管理所有运行时参数（模型、平台、安全策略等）",
    "gateway/session.py": "会话生命周期管理，负责创建、切换、销毁对话会话，以及会话状态持久化",
    "gateway/slash_commands.py": "斜杠命令处理（/help, /model, /compress 等），用户通过命令控制智能体行为",
    "gateway/status.py": "系统状态面板，展示当前会话、模型、配额等运行信息",
    "gateway/stream_consumer.py": "流式消息消费器，从 LLM 接收 SSE 流式响应并分发给各平台适配器",
    
    # ===== gateway 平台 API =====
    "gateway/platforms/api_server.py": "HTTP API 服务端，提供 REST 接口供外部系统调用 Hermes 智能体",
    "gateway/platforms/base.py": "平台适配器基类，定义所有平台（Discord/Telegram/Slack 等）的统一接口规范",
    "gateway/platforms/yuanbao.py": "腾讯元宝平台适配器，接入腾讯元宝用户的消息收发",
    
    # ===== gateway 平台插件 =====
    "plugins/platforms/telegram/adapter.py": "Telegram 平台适配器，处理 Bot 消息收发、群组管理、内联键盘交互",
    "plugins/platforms/slack/adapter.py": "Slack 平台适配器，处理工作空间消息、线程回复、App Home 交互",
    "plugins/platforms/feishu/adapter.py": "飞书平台适配器，处理飞书机器人消息、卡片交互、事件订阅",
    "plugins/platforms/matrix/adapter.py": "Matrix 协议适配器，支持去中心化即时通讯 Matrix 协议",
    "plugins/platforms/qqbot/adapter.py": "QQ 机器人平台适配器，接入 QQ 频道和群聊消息",
    "plugins/platforms/weixin.py": "微信公众号适配器，处理微信消息、菜单和模板消息",
    "plugins/platforms/whatsapp_cloud.py": "WhatsApp Cloud API 适配器，处理商业账号消息收发",
    "plugins/platforms/whatsapp/adapter.py": "WhatsApp 桥接适配器，通过本地桥接处理 WhatsApp 消息",
    "plugins/platforms/wecom/adapter.py": "企业微信适配器，处理企业微信应用消息和回调",
    "plugins/platforms/dingtalk/adapter.py": "钉钉适配器，处理钉钉机器人消息和事件回调",
    "plugins/platforms/signal.py": "Signal 私密通讯适配器，通过 signal-cli 桥接处理消息",
    
    # ===== gateway relay =====
    "gateway/relay/adapter.py": "Relay 中继适配器，支持多实例 Gateway 之间的消息转发和负载均衡",
    
    # ===== tools 工具集 =====
    "tools/mcp_tool.py": "MCP 工具执行器，调用外部 MCP 服务器提供的工具能力（文件操作、搜索等）",
    "tools/browser_tool.py": "浏览器操控工具，支持网页浏览、截图、点击等自动化操作",
    "tools/approval.py": "审批工具，对敏感操作（文件写入、命令执行等）进行人工审批确认",
    "tools/delegate_tool.py": "子智能体委派工具，将子任务分配给子智能体执行并收集结果",
    "tools/terminal_tool.py": "终端工具，在沙箱环境中执行 shell 命令并返回输出",
    "tools/file_operations.py": "文件操作工具集，提供读、写、搜索、编辑文件的能力",
    "tools/file_tools.py": "文件工具扩展，支持批量文件操作和文件安全校验",
    "tools/code_execution_tool.py": "代码执行工具，在隔离环境中运行用户提交的代码片段",
    "tools/checkpoint_manager.py": "检查点管理器，保存和恢复会话快照，支持回退到历史状态",
    "tools/kanban_tools.py": "看板工具，管理任务卡片的状态流转和看板视图",
    "tools/send_message_tool.py": "消息发送工具，让智能体主动向用户发送消息和通知",
    "tools/skills_sync_client.py": "技能同步客户端，从远程仓库同步和更新技能包",
    "tools/skills_tool.py": "技能管理工具，动态加载、执行和卸载技能模块",
    "tools/skill_manager_tool.py": "技能管理器扩展，支持技能的注册、发现和生命周期管理",
    "tools/image_generation_tool.py": "图像生成工具，调用 AI 模型生成图片",
    "tools/computer_use/cua_backend.py": "Computer Use 后端，实现浏览器和桌面的自动化操控协议",
    "tools/environments/docker.py": "Docker 执行环境，在容器中隔离运行代码和命令",
    "tools/environments/local.py": "本地执行环境，直接在宿主机上运行命令（受安全策略约束）",
    
    # ===== cron 定时任务 =====
    "cron/scheduler.py": "定时任务调度器，按 cron 表达式触发预设任务（日报生成、定时提醒等）",
    "cron/jobs.py": "定时任务定义，包含预设的自动化任务模板和执行逻辑",
    
    # ===== hermes_cli 核心补充 =====
    "hermes_cli/update_cmd.py": "更新命令，检查并安装 Hermes 新版本，支持自动升级",
    "hermes_cli/config_defaults.py": "配置默认值定义，列出所有可配置项及其默认值和校验规则",
    "hermes_cli/console_engine.py": "控制台渲染引擎，管理 TUI 终端界面的布局、主题和交互",
    "hermes_cli/cli_billing_mixin.py": "计费混入模块，在 CLI 中展示用量和账单信息",
    
    # ===== tui_gateway =====
    "tui_gateway/methods_session.py": "TUI 会话方法，处理终端界面中的会话创建、恢复、切换",
    "tui_gateway/methods_tools.py": "TUI 工具方法，在终端界面中展示工具调用结果和审批交互",
    
    # ===== agent 补充 =====
    "agent/moa_loop.py": "MoA（混合智能体）循环，编排多个专业子智能体协同完成任务",
    "agent/proxy_sources/iron_proxy.py": "Iron 代理源，管理多个 API Key 的轮换和负载均衡，提升服务可用性",
    
    # ===== 根目录关键文件 =====
    "hermes_state_search.py": "会话状态搜索引擎，支持全文检索历史会话和对话内容",
    "setup.py": "Python 包安装配置，定义依赖、入口点和打包元数据",
}


def add_module_summary(filepath: str, summary: str) -> bool:
    """在文件顶部 docstring 后添加【产品经理理解要点】"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 已经有注释就跳过
    if "产品经理理解要点" in content:
        return False
    
    annotation = f"\n# 【产品经理理解要点】{summary}\n"
    
    # 尝试在文件开头 docstring 后插入
    # 情况1: 文件以 #! 或 coding 声明开头
    lines = content.split("\n")
    insert_pos = 0
    
    # 跳过 shebang 和 encoding 声明
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped.startswith("#!"):
            insert_pos = i + 1
            continue
        if stripped.startswith("# -*- coding") or stripped.startswith("# coding"):
            insert_pos = i + 1
            continue
        if stripped == "" or stripped.startswith("#"):
            if insert_pos == i:
                insert_pos = i + 1
            continue
        break
    
    # 检查是否有 docstring
    rest = "\n".join(lines[insert_pos:])
    if rest.strip().startswith('"""') or rest.strip().startswith("'''"):
        quote = '"""' if rest.strip().startswith('"""') else "'''"
        # 找到 docstring 结束位置
        doc_start = content.find(quote)
        doc_end = content.find(quote, doc_start + 3)
        if doc_end != -1:
            # 在 docstring 结束后插入
            insert_pos = content[:doc_end + 3].count("\n")
    
    lines.insert(insert_pos, annotation)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


def add_function_annotations(filepath: str) -> int:
    """为关键函数/类添加中文注释"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 如果已经有很多注释，跳过
    if content.count("产品经理理解要点") > 5:
        return 0
    
    # 关键函数名 -> 中文说明映射（通用规则）
    KEY_FUNCTIONS = {
        "run": "主运行入口",
        "main": "主入口函数",
        "start": "启动服务",
        "stop": "停止服务",
        "handle_message": "处理收到的消息",
        "send_message": "发送消息",
        "on_message": "消息回调处理",
        "process_message": "消息处理逻辑",
        "execute": "执行操作",
        "connect": "建立连接",
        "disconnect": "断开连接",
        "setup": "初始化配置",
        "load_config": "加载配置",
        "save_config": "保存配置",
        "create_session": "创建会话",
        "delete_session": "删除会话",
        "get_session": "获取会话信息",
        "list_sessions": "列出所有会话",
        "compress": "压缩上下文",
        "truncate": "截断消息",
        "approve": "审批确认",
        "reject": "拒绝操作",
        "schedule": "调度任务",
        "run_job": "执行定时任务",
        "health_check": "健康检查",
        "authenticate": "认证鉴权",
    }
    
    count = 0
    lines = content.split("\n")
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        stripped = line.strip()
        
        # 检测函数/类定义
        for func_name, desc in KEY_FUNCTIONS.items():
            # 匹配 def func_name 或 async def func_name 或 class ClassName
            patterns = [
                rf"^(\s*)(async\s+)?def\s+{func_name}\s*\(",
            ]
            for pattern in patterns:
                if re.match(pattern, stripped):
                    indent = re.match(r"(\s*)", stripped).group(1)
                    # 检查下一行是否已有注释
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    if not next_line.startswith("#") and not next_line.startswith('"""') and not next_line.startswith("'''"):
                        new_lines.append(f"{indent}# {desc}")
                        count += 1
                    break
    
    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
    
    return count


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    total_files = 0
    total_annotations = 0
    
    for rel_path, summary in FILE_SUMMARIES.items():
        filepath = os.path.join(root, rel_path)
        if not os.path.exists(filepath):
            print(f"  跳过（不存在）: {rel_path}")
            continue
        
        added = add_module_summary(filepath, summary)
        func_count = add_function_annotations(filepath)
        
        if added or func_count > 0:
            total_files += 1
            total_annotations += 1 + func_count
            print(f"  + {rel_path}: 模块概要={added}, 函数注释={func_count}")
        else:
            print(f"  = {rel_path}: 已有注释，跳过")
    
    print(f"\n完成！共处理 {total_files} 个文件，新增 {total_annotations} 条中文注释")


if __name__ == "__main__":
    main()
