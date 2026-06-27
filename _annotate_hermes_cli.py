#!/usr/bin/env python3
"""Batch annotate hermes_cli Python files with 产品经理理解要点 docstring blocks."""

import re
from pathlib import Path

annotations = {
    '__init__.py': ('Hermes CLI 包', 'Hermes Agent 的命令行界面主包，提供 hermes 命令的所有子命令和交互功能。', '- 核心职责：作为 CLI 入口点，暴露版本号和包元数据\n- 系统定位：用户入口层，hermes 命令 → 本包 → 各功能模块'),
    '_parser.py': ('CLI 参数解析', '定义 Hermes CLI 的顶层参数解析器，处理全局选项如 --version、--debug 等。', '- 核心职责：构建 argparse 顶层解析器，注册全局标志\n- 系统定位：命令解析层，用户输入 → 参数解析 → 路由到子命令'),
    '_subprocess_compat.py': ('子进程兼容层', '提供跨平台的子进程创建兼容函数，处理 Windows/POSIX 差异。', '- 核心职责：封装 subprocess 调用，统一处理 stdin 继承和平台差异\n- 系统定位：基础设施层，所有子进程调用的统一入口'),
    'active_sessions.py': ('活跃会话管理', '追踪和管理当前正在运行的 Hermes Agent 会话，支持会话列表/恢复/切换。', '- 核心职责：枚举活跃会话，提供会话恢复和切换能力\n- 关键概念：会话持久化在 state.db，可跨进程恢复\n- 系统定位：会话管理层'),
    'auth.py': ('认证模块', '处理用户认证流程，包括 API Key 验证、OAuth 登录、Token 刷新等。', '- 核心职责：管理认证状态，执行登录/注销流程，刷新过期 Token\n- 关键概念：支持多种认证方式（API Key、OAuth、浏览器登录）\n- 系统定位：安全认证层'),
    'auth_commands.py': ('认证命令', '实现 auth 相关子命令（login、logout、status 等）的命令行处理。', '- 核心职责：注册和执行认证子命令\n- 系统定位：命令实现层'),
    'azure_detect.py': ('Azure 环境检测', '自动检测 Azure/Entra ID 认证环境，配置对应的认证方式。', '- 核心职责：探测 Azure Foundry/Entra ID 环境，自动切换认证模式\n- 系统定位：环境适配层'),
    'backup.py': ('备份与恢复', '实现 Hermes 配置和会话数据的备份/恢复功能。', '- 核心职责：打包 ~/.hermes 目录，支持增量备份和全量恢复\n- 系统定位：数据运维层'),
    'banner.py': ('启动横幅', '显示 Hermes CLI 启动时的欢迎横幅和版本信息。', '- 核心职责：渲染启动 Logo、版本号、模型信息\n- 系统定位：UI 展示层'),
    'blueprint_cmd.py': ('蓝图命令', '实现自动化蓝图（定时任务模板）的管理命令。', '- 核心职责：列出/应用/创建自动化蓝图\n- 关键概念：蓝图是预定义的自动化任务模板，如每日摘要、代码审查\n- 系统定位：自动化管理层'),
    'browser_connect.py': ('浏览器连接', '管理与 Chrome/Chromium 的 CDP 连接，支持浏览器自动化操作。', '- 核心职责：启动/发现浏览器实例，建立调试协议连接\n- 关键概念：通过 Chrome DevTools Protocol 控制浏览器\n- 系统定位：浏览器自动化基础设施层'),
    'build_info.py': ('构建信息', '收集和暴露 Hermes 的构建元数据（版本、Git 提交、构建时间等）。', '- 核心职责：在运行时提供构建版本信息，支持 --version 输出\n- 系统定位：元数据层'),
    'bundles.py': ('资源包管理', '管理 Hermes 的资源包（模型配置、技能定义等）的下载和更新。', '- 核心职责：下载/验证/更新资源包\n- 系统定位：资源管理层'),
    'callbacks.py': ('回调处理器', '定义 Agent 运行时的各类回调函数，处理工具调用、思考过程、流式输出等事件。', '- 核心职责：注册 Agent 回调，将内部事件转换为用户可见的输出\n- 关键概念：流式输出、工具调用展示、思考过程展示\n- 系统定位：事件处理层'),
    'checkpoints.py': ('检查点管理', '管理对话检查点，支持回滚到历史对话状态。', '- 核心职责：创建/列出/恢复对话检查点\n- 关键概念：检查点是对话状态的快照，用于安全回滚\n- 系统定位：状态管理层'),
    'claw.py': ('Claw 安全扫描', '集成 Claw 安全扫描能力，对代码和配置进行安全审计。', '- 核心职责：执行安全扫描并生成报告\n- 系统定位：安全审计层'),
    'cli_agent_setup_mixin.py': ('Agent 设置混入', 'HermesCLI 的混入类，提供 Agent 初始化和配置设置的共享逻辑。', '- 核心职责：抽取 Agent 设置相关的公共方法，减少主类代码量\n- 系统定位：代码复用层（Mixin 模式）'),
    'cli_commands_mixin.py': ('命令混入', 'HermesCLI 的混入类，提供各子命令的注册和执行逻辑。', '- 核心职责：注册斜杠命令和子命令处理函数\n- 系统定位：命令路由层（Mixin 模式）'),
    'cli_output.py': ('CLI 输出格式化', '统一 CLI 的输出格式，包括颜色、缩进、进度条等。', '- 核心职责：格式化各类输出（错误、警告、表格、进度）\n- 系统定位：UI 格式化层'),
    'clipboard.py': ('剪贴板操作', '跨平台剪贴板读写，支持将 Agent 输出复制到系统剪贴板。', '- 核心职责：检测可用的剪贴板工具，执行复制操作\n- 系统定位：系统集成层'),
    'codex_models.py': ('Codex 模型配置', '定义 OpenAI Codex 系列模型的特殊配置和兼容处理。', '- 核心职责：适配 Codex 模型的 API 差异（参数名、响应格式等）\n- 系统定位：模型适配层'),
    'codex_runtime_plugin_migration.py': ('Codex 运行时迁移', '从旧版 Codex 运行时插件迁移配置到新格式。', '- 核心职责：检测旧配置格式，自动迁移到新格式\n- 系统定位：兼容迁移层'),
    'codex_runtime_switch.py': ('Codex 运行时切换', '在 Codex 和标准 OpenAI 运行时之间切换。', '- 核心职责：根据模型类型选择合适的运行时\n- 系统定位：运行时选择层'),
    'colors.py': ('颜色主题', '定义 CLI 输出的颜色方案，支持明暗主题和终端能力检测。', '- 核心职责：根据终端能力（真彩色/256色/无颜色）选择颜色方案\n- 系统定位：UI 主题层'),
    'commands.py': ('命令注册', '定义和注册所有斜杠命令（/help、/model、/clear 等）。', '- 核心职责：维护命令注册表，处理命令补全和执行\n- 关键概念：斜杠命令是用户在对话中输入的 / 前缀快捷命令\n- 系统定位：命令管理层'),
    'completion.py': ('Tab 补全', '实现命令和文件路径的 Tab 补全功能。', '- 核心职责：提供补全候选项，支持子命令、模型名、文件路径补全\n- 系统定位：交互增强层'),
    'config.py': ('配置管理', '管理 ~/.hermes/ 下的所有配置文件，支持版本化迁移和验证。', '- 核心职责：读写配置文件，执行格式迁移，验证配置合法性\n- 关键概念：配置文件有版本号，升级时自动迁移\n- 系统定位：配置基础设施层'),
    'container_boot.py': ('容器启动', 'Docker 容器首次启动时的初始化逻辑（配置迁移、目录创建等）。', '- 核心职责：检测并执行首次启动初始化步骤\n- 系统定位：运维层，Docker 部署专用'),
    'copilot_auth.py': ('Copilot 认证', '处理 GitHub Copilot 的认证流程，复用 Copilot Token。', '- 核心职责：获取和刷新 Copilot 的 OAuth Token\n- 系统定位：第三方认证集成层'),
    'cron.py': ('定时任务', '管理和调度定时任务（cron jobs），支持自然语言描述调度。', '- 核心职责：创建/列出/删除/暂停定时任务，调度执行\n- 关键概念：支持 cron 表达式和自然语言调度（每天/每周）\n- 系统定位：自动化调度层'),
    'curator.py': ('数据策展', '管理训练数据的策展流程——筛选、标注、导出高质量对话轨迹。', '- 核心职责：策展对话数据用于模型微调\n- 系统定位：数据工程层'),
    'curses_ui.py': ('Curses 界面', '基于 curses 的终端 UI 实现（备用界面，非主要 TUI）。', '- 核心职责：提供基本的终端对话界面\n- 系统定位：备用 UI 层'),
    'dashboard_auth/__init__.py': ('Dashboard 认证', 'Dashboard Web 界面的认证系统，保护管理端点。', '- 核心职责：协调各认证组件\n- 系统定位：Web 认证层'),
    'dashboard_auth/audit.py': ('认证审计', '记录认证事件的审计日志（登录、注销、Token 刷新等）。', '- 核心职责：记录和查询认证审计事件\n- 系统定位：安全审计层'),
    'dashboard_auth/base.py': ('认证基类', '定义 Dashboard 认证策略的基类和接口。', '- 核心职责：声明认证策略接口\n- 系统定位：接口定义层'),
    'dashboard_auth/cookies.py': ('Cookie 认证', '基于 Cookie 的会话认证实现。', '- 核心职责：签发/验证/刷新会话 Cookie\n- 系统定位：Cookie 认证实现层'),
    'dashboard_auth/login_page.py': ('登录页面', '渲染 Dashboard 的登录页面 HTML。', '- 核心职责：生成登录表单 HTML\n- 系统定位：Web UI 层'),
    'dashboard_auth/middleware.py': ('认证中间件', 'FastAPI 中间件，拦截请求执行认证检查。', '- 核心职责：在请求处理前验证身份，未认证则重定向到登录页\n- 系统定位：Web 中间件层'),
    'dashboard_auth/prefix.py': ('路径前缀认证', '基于 URL 路径前缀的认证规则。', '- 核心职责：定义哪些路径需要认证\n- 系统定位：路由安全层'),
    'dashboard_auth/public_paths.py': ('公开路径', '定义不需要认证的公开路径列表。', '- 核心职责：维护白名单路径\n- 系统定位：安全配置层'),
    'dashboard_auth/registry.py': ('认证注册', '注册和查找可用的认证策略。', '- 核心职责：维护认证策略注册表\n- 系统定位：策略管理层'),
    'dashboard_auth/routes.py': ('认证路由', '定义认证相关的 HTTP 路由。', '- 核心职责：注册认证端点\n- 系统定位：Web 路由层'),
    'dashboard_auth/ws_tickets.py': ('WS 门票', '为 WebSocket 连接签发一次性认证门票。', '- 核心职责：生成/验证 WebSocket 认证门票\n- 系统定位：WebSocket 安全层'),
    'dashboard_register.py': ('Dashboard 注册', '将 Hermes 实例注册到 Dashboard。', '- 核心职责：向 Dashboard 注册 Agent 实例信息\n- 系统定位：服务发现层'),
    'debug.py': ('调试工具', '提供运行时调试能力。', '- 核心职责：收集和展示调试信息\n- 系统定位：开发调试层'),
    'default_soul.py': ('默认灵魂', '定义 Hermes Agent 的默认系统提示词。', '- 核心职责：加载和组装默认的 Agent 人格和行为指令\n- 关键概念：灵魂是 Agent 的核心身份定义\n- 系统定位：Agent 人格层'),
    'dep_ensure.py': ('依赖确保', '检查并安装 Hermes 运行所需的外部依赖。', '- 核心职责：探测缺失依赖，提示安装或自动安装\n- 系统定位：环境准备层'),
    'dingtalk_auth.py': ('钉钉认证', '处理钉钉平台的 OAuth 认证集成。', '- 核心职责：实现钉钉 OAuth 登录流程\n- 系统定位：第三方集成层'),
    'doctor.py': ('环境诊断', '执行 Hermes 运行环境的健康检查。', '- 核心职责：逐项检查环境依赖、配置、网络连通性\n- 系统定位：用户支持层'),
    'dump.py': ('状态转储', '将 Agent 内部状态转储为可读的调试文件。', '- 核心职责：序列化 Agent 状态到文件\n- 系统定位：调试导出层'),
    'env_loader.py': ('环境变量加载', '从 .env 文件加载环境变量到进程环境。', '- 核心职责：按优先级加载 .env 文件\n- 系统定位：配置基础设施层'),
    'fallback_cmd.py': ('降级命令', '当子命令无法执行时提供降级处理。', '- 核心职责：捕获命令执行异常，提供可操作的修复建议\n- 系统定位：容错层'),
    'fallback_config.py': ('降级配置', '当主配置不可用时提供合理的默认配置降级。', '- 核心职责：生成降级配置\n- 系统定位：容错层'),
    'gateway.py': ('API 网关', 'Hermes HTTP/WebSocket 网关服务器。', '- 核心职责：启动 FastAPI 服务，提供 REST + WebSocket 端点\n- 关键概念：支持多会话、流式输出、认证中间件\n- 系统定位：API 服务层'),
    'gateway_enroll.py': ('网关注册', '将本地网关注册到服务发现系统。', '- 核心职责：向注册中心报告网关地址和能力\n- 系统定位：服务发现层'),
    'gateway_windows.py': ('Windows 网关', 'Windows 平台上的网关特殊处理。', '- 核心职责：适配 Windows 的网关启动和管理\n- 系统定位：平台适配层'),
    'goals.py': ('目标追踪', '追踪和管理用户设定的对话目标/任务列表。', '- 核心职责：创建/更新/完成对话目标\n- 系统定位：任务管理层'),
    'gui_uninstall.py': ('GUI 卸载', '处理 GUI 桌面应用的卸载流程。', '- 核心职责：清理 GUI 安装文件和注册表项\n- 系统定位：运维层'),
    'hooks.py': ('钩子系统', '管理事件钩子，在特定事件触发时执行自定义脚本。', '- 核心职责：注册/触发/管理事件钩子\n- 关键概念：钩子如 on_message、on_tool_call\n- 系统定位：扩展机制层'),
    'inventory.py': ('资源清单', '收集和展示 Hermes 可用的全部资源。', '- 核心职责：汇总 Agent 的能力清单\n- 系统定位：信息展示层'),
    'kanban.py': ('看板管理', '实现看板式任务管理。', '- 核心职责：管理看板面板和卡片\n- 关键概念：看板是任务可视化管理工具\n- 系统定位：任务管理层'),
    'kanban_db.py': ('看板数据库', '看板数据的持久化存储层。', '- 核心职责：读写看板数据\n- 系统定位：数据持久化层'),
    'kanban_decompose.py': ('看板任务分解', '将大任务自动分解为子任务。', '- 核心职责：调用 LLM 将任务拆解为可执行的子任务\n- 关键概念：任务分解是 Agent 辅助规划的核心能力\n- 系统定位：AI 辅助规划层'),
    'kanban_diagnostics.py': ('看板诊断', '诊断看板数据的一致性问题并修复。', '- 核心职责：检测和修复看板数据异常\n- 系统定位：数据维护层'),
    'kanban_specify.py': ('看板规格化', '将自然语言任务描述规格化为结构化看板卡片。', '- 核心职责：用 LLM 将模糊描述转为精确的任务规格\n- 系统定位：AI 辅助层'),
    'kanban_swarm.py': ('看板集群', '多 Agent 协作执行看板任务的调度器。', '- 核心职责：分配看板任务给多个 Agent 并行执行\n- 关键概念：Swarm 模式——多 Agent 分工协作\n- 系统定位：多 Agent 调度层'),
    'logs.py': ('日志管理', '管理 Hermes 运行日志的查看、搜索和导出。', '- 核心职责：读取/过滤/展示日志文件\n- 系统定位：可观测性层'),
    'main.py': ('CLI 主入口', 'Hermes CLI 的主入口函数。', '- 核心职责：顶层命令分发\n- 系统定位：应用入口层'),
    'managed_scope.py': ('受管作用域', '管理 Agent 的受管作用域——限制可访问范围。', '- 核心职责：定义和执行 Agent 的权限边界\n- 关键概念：作用域控制 Agent 可读写哪些目录\n- 系统定位：安全隔离层'),
    'managed_uv.py': ('UV 包管理', '封装 uv 包管理器的调用。', '- 核心职责：确保 uv 可用，通过 uv 安装/更新依赖\n- 系统定位：环境管理层'),
    'mcp_catalog.py': ('MCP 目录', '发现和列出可用的 MCP 服务器。', '- 核心职责：扫描已配置的 MCP 服务器\n- 关键概念：MCP 是 Agent 调用外部工具的标准协议\n- 系统定位：工具发现层'),
    'mcp_config.py': ('MCP 配置', '管理 MCP 服务器的配置。', '- 核心职责：读写 MCP 服务器配置\n- 系统定位：工具配置层'),
    'mcp_picker.py': ('MCP 选择器', '交互式选择要启用的 MCP 服务器。', '- 核心职责：展示 MCP 目录并让用户选择\n- 系统定位：交互配置层'),
    'mcp_security.py': ('MCP 安全', 'MCP 服务器连接的安全策略。', '- 核心职责：执行 MCP 服务器的安全沙箱策略\n- 系统定位：安全隔离层'),
    'mcp_startup.py': ('MCP 启动', '启动和管理 MCP 服务器子进程的生命周期。', '- 核心职责：spawn MCP 服务器进程，监控健康状态\n- 系统定位：进程管理层'),
    'memory_providers.py': ('记忆提供方', '管理长期记忆的存储提供方。', '- 核心职责：注册/选择记忆存储后端\n- 系统定位：记忆基础设施层'),
    'memory_setup.py': ('记忆设置', '引导用户配置长期记忆系统。', '- 核心职责：交互式设置记忆存储方式和参数\n- 系统定位：配置引导层'),
    'middleware.py': ('中间件', 'CLI 模式下的请求/响应中间件。', '- 核心职责：在请求处理链中插入横切关注点\n- 系统定位：横切基础设施层'),
    'migrate.py': ('数据迁移', '执行 Hermes 数据格式的版本间迁移。', '- 核心职责：检测数据版本，执行迁移脚本\n- 系统定位：数据兼容层'),
    'model_catalog.py': ('模型目录', '维护可用模型列表，支持远程拉取和本地缓存。', '- 核心职责：获取模型列表（远程>本地缓存>硬编码）\n- 关键概念：模型信息包括名称、上下文窗口、价格\n- 系统定位：模型发现层'),
    'model_cost_guard.py': ('模型成本控制', '监控和限制 API 调用成本。', '- 核心职责：追踪 Token 消耗，计算费用，超阈值告警\n- 关键概念：按模型定价计算费用\n- 系统定位：成本治理层'),
    'model_normalize.py': ('模型名称规范化', '将用户输入的模型名称规范化为内部标准名称。', '- 核心职责：处理模型名别名、大小写等变体\n- 系统定位：数据标准化层'),
    'model_setup_flows.py': ('模型设置流程', '引导用户选择和配置 AI 模型的交互式流程。', '- 核心职责：展示模型目录，引导选择，配置 API Key\n- 系统定位：用户引导层'),
    'model_switch.py': ('模型切换', '在对话中动态切换使用的 AI 模型。', '- 核心职责：验证模型可用性，切换当前模型\n- 系统定位：运行时配置层'),
    'models.py': ('模型定义', '定义所有支持的 AI 模型的元数据和配置。', '- 核心职责：硬编码模型列表、能力标签、上下文窗口\n- 系统定位：模型元数据层'),
    'nous_account.py': ('Nous 账户', 'Nous Research 平台的账户管理。', '- 核心职责：查询账户信息、余额\n- 系统定位：第三方平台集成层'),
    'nous_billing.py': ('Nous 计费', 'Nous Research 平台的计费查询。', '- 核心职责：查询账单明细和用量\n- 系统定位：计费查询层'),
    'nous_subscription.py': ('Nous 订阅', 'Nous Research 平台的订阅管理。', '- 核心职责：查询/变更订阅计划和配额\n- 系统定位：订阅管理层'),
    'oneshot.py': ('单次执行', '非交互式单次执行模式。', '- 核心职责：执行单条指令并输出结果\n- 关键概念：与交互式 REPL 模式对应\n- 系统定位：非交互执行层'),
    'pairing.py': ('设备配对', '处理新设备的配对流程。', '- 核心职责：生成/验证设备配对码\n- 系统定位：设备管理层'),
    'partial_compress.py': ('部分压缩', '对超长对话进行部分压缩。', '- 核心职责：选择性压缩对话历史，控制 Token 预算\n- 关键概念：压缩策略保留最近对话+摘要历史\n- 系统定位：Token 预算管理层'),
    'platforms.py': ('平台检测', '检测和抽象运行平台特性。', '- 核心职责：识别 OS、终端、Shell 类型\n- 系统定位：平台抽象层'),
    'plugins.py': ('插件系统', '管理 Hermes 插件的发现、加载和生命周期。', '- 核心职责：扫描/加载/启用/禁用插件\n- 关键概念：插件扩展 Agent 能力\n- 系统定位：扩展机制层'),
    'plugins_cmd.py': ('插件命令', '实现 plugins 子命令。', '- 核心职责：处理插件管理的命令行操作\n- 系统定位：命令实现层'),
    'portal_cli.py': ('Portal CLI', 'Nous Portal 的命令行管理工具。', '- 核心职责：与 Nous Portal API 交互\n- 系统定位：远程管理层'),
    'profile_describer.py': ('档案描述', '生成 Agent 配置档案的人类可读描述。', '- 核心职责：将配置文件转为自然语言描述\n- 系统定位：信息展示层'),
    'profile_distribution.py': ('档案分发', '将 Agent 配置档案分发到目标环境。', '- 核心职责：打包和部署配置档案\n- 系统定位：部署层'),
    'profiles.py': ('配置档案', '管理 Agent 配置档案——预设的模型/工具/技能组合。', '- 核心职责：创建/列出/切换配置档案\n- 关键概念：档案是预配置的 Agent 人格+能力组合\n- 系统定位：配置管理层'),
    'prompt_size.py': ('提示大小', '计算和管理发送给模型的提示 Token 数量。', '- 核心职责：估算 Token 数，处理超长提示\n- 系统定位：Token 预算层'),
    'provider_catalog.py': ('提供方目录', '管理和展示可用的模型推理提供方。', '- 核心职责：聚合所有提供方信息\n- 系统定位：提供方发现层'),
    'providers.py': ('提供方管理', '运行时提供方管理。', '- 核心职责：解析提供方配置，构建 API 客户端\n- 系统定位：提供方运行时层'),
    'proxy/__init__.py': ('代理模块', 'HTTP 代理模块。', '- 核心职责：作为透明代理转发 API 请求\n- 系统定位：网络代理层'),
    'proxy/adapters/__init__.py': ('代理适配器', '代理适配器子包。', '- 核心职责：注册和发现适配器\n- 系统定位：适配器管理层'),
    'proxy/adapters/base.py': ('适配器基类', '定义代理适配器的基类接口。', '- 核心职责：声明请求/响应转换接口\n- 系统定位：接口定义层'),
    'proxy/adapters/nous_portal.py': ('Nous Portal 适配器', '适配 Nous Portal 的 API 格式。', '- 核心职责：转换请求/响应以匹配 Portal 协议\n- 系统定位：协议适配层'),
    'proxy/adapters/xai.py': ('xAI 适配器', '适配 xAI（Grok）的 API 格式差异。', '- 核心职责：处理 xAI 特有的请求/响应格式\n- 系统定位：协议适配层'),
    'proxy/cli.py': ('代理 CLI', '代理服务的命令行启动入口。', '- 核心职责：解析代理启动参数\n- 系统定位：命令入口层'),
    'proxy/server.py': ('代理服务器', 'HTTP 代理服务器实现。', '- 核心职责：监听 HTTP 请求，路由到适配器\n- 系统定位：网络服务层'),
    'psutil_android.py': ('Android 系统监控', '在 Android/Termux 上提供系统资源监控。', '- 核心职责：Android 上替代 psutil\n- 系统定位：平台适配层'),
    'pt_input_extras.py': ('输入增强', 'prompt_toolkit 输入的增强功能。', '- 核心职责：增强终端输入体验\n- 系统定位：UI 增强层'),
    'pty_bridge.py': ('PTY 桥接', '伪终端桥接。', '- 核心职责：创建/管理 PTY 连接\n- 系统定位：终端基础设施层'),
    'relaunch.py': ('进程重启', '安全重启 Hermes 进程。', '- 核心职责：保存状态，exec 新进程\n- 系统定位：生命周期管理层'),
    'runtime_provider.py': ('运行时提供方', '解析当前运行时应使用的模型提供方。', '- 核心职责：根据配置确定活跃的提供方\n- 系统定位：运行时决策层'),
    'secret_prompt.py': ('密钥输入', '安全地从终端读取密钥。', '- 核心职责：隐藏输入内容，防止密钥泄露\n- 系统定位：安全输入层'),
    'secrets_cli.py': ('密钥管理', '管理 API Key 等密钥。', '- 核心职责：安全存储/列出/删除密钥\n- 系统定位：密钥管理层'),
    'security_advisories.py': ('安全公告', '检查和展示已知的安全漏洞公告。', '- 核心职责：拉取安全公告，提示升级\n- 系统定位：安全通知层'),
    'security_audit.py': ('安全审计', '执行安全审计检查。', '- 核心职责：检查常见安全配置问题\n- 系统定位：安全审计层'),
    'send_cmd.py': ('发送命令', '实现 /send 斜杠命令。', '- 核心职责：处理对话中的消息发送\n- 系统定位：命令实现层'),
    'service_manager.py': ('服务管理', '管理 Hermes 作为系统服务的生命周期。', '- 核心职责：安装/启动/停止/卸载系统服务\n- 系统定位：服务管理层'),
    'session_listing.py': ('会话列表', '列出和展示历史会话记录。', '- 核心职责：从数据库查询会话列表\n- 系统定位：信息展示层'),
    'session_recap.py': ('会话回顾', '生成会话的摘要回顾。', '- 核心职责：用 LLM 生成会话摘要\n- 系统定位：AI 辅助层'),
    'setup.py': ('安装设置', 'Hermes 首次安装的交互式设置引导。', '- 核心职责：引导用户完成首次配置\n- 系统定位：用户引导层'),
    'setup_whatsapp_cloud.py': ('WhatsApp 配置', '配置 WhatsApp Cloud API 集成。', '- 核心职责：引导设置 WhatsApp Business API 凭证\n- 系统定位：第三方集成配置层'),
    'skills_config.py': ('技能配置', '管理技能的配置和启用状态。', '- 核心职责：读写技能配置，控制技能开关\n- 系统定位：技能管理层'),
    'skills_hub.py': ('技能市场', '与 Skills Hub 交互——搜索、安装、更新技能。', '- 核心职责：从多个技能源搜索和安装技能\n- 关键概念：技能源包括 skills.sh、GitHub、ClawHub 等\n- 系统定位：技能市场客户端层'),
    'skin_engine.py': ('皮肤引擎', '管理 CLI 的视觉皮肤/主题切换。', '- 核心职责：加载/切换皮肤配置\n- 系统定位：UI 主题层'),
    'slack_cli.py': ('Slack 集成', 'Hermes 与 Slack 的集成。', '- 核心职责：启动 Slack Bot，处理消息事件\n- 系统定位：第三方平台集成层'),
    'status.py': ('状态查询', '查询和展示 Hermes 的运行状态。', '- 核心职责：收集运行状态信息并格式化输出\n- 系统定位：信息展示层'),
    'stdio.py': ('标准 IO', '标准输入输出模式下的消息处理。', '- 核心职责：从 stdin 读取输入，向 stdout 写入输出\n- 系统定位：I/O 层'),
    'subcommands/__init__.py': ('子命令包', '子命令注册包。', '- 核心职责：子命令模块的统一入口\n- 系统定位：命令组织层'),
    'subcommands/_shared.py': ('子命令共享', '子命令间的共享工具函数。', '- 核心职责：抽取子命令的公共逻辑\n- 系统定位：代码复用层'),
    'subcommands/acp.py': ('ACP 子命令', 'hermes acp 子命令。', '- 核心职责：启动 ACP 服务\n- 系统定位：命令实现层'),
    'subcommands/auth.py': ('认证子命令', 'hermes auth 子命令。', '- 核心职责：login/logout/status 子命令\n- 系统定位：命令实现层'),
    'subcommands/backup.py': ('备份子命令', 'hermes backup 子命令。', '- 核心职责：创建/恢复备份\n- 系统定位：命令实现层'),
    'subcommands/claw.py': ('Claw 子命令', 'hermes claw 子命令。', '- 核心职责：启动 Claw 安全扫描\n- 系统定位：命令实现层'),
    'subcommands/config.py': ('配置子命令', 'hermes config 子命令。', '- 核心职责：get/set/list 配置项\n- 系统定位：命令实现层'),
    'subcommands/cron.py': ('定时任务子命令', 'hermes cron 子命令。', '- 核心职责：管理定时任务\n- 系统定位：命令实现层'),
    'subcommands/dashboard.py': ('Dashboard 子命令', 'hermes dashboard 子命令。', '- 核心职责：启动 Dashboard Web 服务\n- 系统定位：命令实现层'),
    'subcommands/debug.py': ('调试子命令', 'hermes debug 子命令。', '- 核心职责：启动调试模式\n- 系统定位：命令实现层'),
    'subcommands/doctor.py': ('诊断子命令', 'hermes doctor 子命令。', '- 核心职责：运行诊断检查\n- 系统定位：命令实现层'),
    'subcommands/dump.py': ('转储子命令', 'hermes dump 子命令。', '- 核心职责：导出 Agent 状态\n- 系统定位：命令实现层'),
    'subcommands/gateway.py': ('网关子命令', 'hermes gateway 子命令。', '- 核心职责：启动 HTTP/WebSocket 网关服务\n- 系统定位：命令实现层'),
    'subcommands/gui.py': ('GUI 子命令', 'hermes gui 子命令。', '- 核心职责：启动图形界面\n- 系统定位：命令实现层'),
    'subcommands/hooks.py': ('钩子子命令', 'hermes hooks 子命令。', '- 核心职责：管理事件钩子\n- 系统定位：命令实现层'),
    'subcommands/import_cmd.py': ('导入子命令', 'hermes import 子命令。', '- 核心职责：从外部源导入配置\n- 系统定位：命令实现层'),
    'subcommands/insights.py': ('洞察子命令', 'hermes insights 子命令。', '- 核心职责：展示使用统计和分析\n- 系统定位：命令实现层'),
    'subcommands/login.py': ('登录子命令', 'hermes login 子命令。', '- 核心职责：执行登录流程\n- 系统定位：命令实现层'),
    'subcommands/logout.py': ('注销子命令', 'hermes logout 子命令。', '- 核心职责：清除认证状态\n- 系统定位：命令实现层'),
    'subcommands/logs.py': ('日志子命令', 'hermes logs 子命令。', '- 核心职责：展示运行日志\n- 系统定位：命令实现层'),
    'subcommands/mcp.py': ('MCP 子命令', 'hermes mcp 子命令。', '- 核心职责：管理 MCP 服务器\n- 系统定位：命令实现层'),
    'subcommands/memory.py': ('记忆子命令', 'hermes memory 子命令。', '- 核心职责：管理长期记忆\n- 系统定位：命令实现层'),
    'subcommands/model.py': ('模型子命令', 'hermes model 子命令。', '- 核心职责：管理模型配置\n- 系统定位：命令实现层'),
    'subcommands/pairing.py': ('配对子命令', 'hermes pairing 子命令。', '- 核心职责：管理设备配对\n- 系统定位：命令实现层'),
    'subcommands/plugins.py': ('插件子命令', 'hermes plugins 子命令。', '- 核心职责：管理插件\n- 系统定位：命令实现层'),
    'subcommands/postinstall.py': ('安装后子命令', 'hermes postinstall 子命令。', '- 核心职责：执行安装后的设置步骤\n- 系统定位：运维层'),
    'subcommands/profile.py': ('档案子命令', 'hermes profile 子命令。', '- 核心职责：管理配置档案\n- 系统定位：命令实现层'),
    'subcommands/prompt_size.py': ('提示大小子命令', 'hermes prompt-size 子命令。', '- 核心职责：计算提示大小\n- 系统定位：命令实现层'),
    'subcommands/security.py': ('安全子命令', 'hermes security 子命令。', '- 核心职责：运行安全检查\n- 系统定位：命令实现层'),
    'subcommands/setup.py': ('设置子命令', 'hermes setup 子命令。', '- 核心职责：交互式设置\n- 系统定位：命令实现层'),
    'subcommands/skills.py': ('技能子命令', 'hermes skills 子命令。', '- 核心职责：管理技能\n- 系统定位：命令实现层'),
    'subcommands/slack.py': ('Slack 子命令', 'hermes slack 子命令。', '- 核心职责：管理 Slack 集成\n- 系统定位：命令实现层'),
    'subcommands/status.py': ('状态子命令', 'hermes status 子命令。', '- 核心职责：展示运行状态\n- 系统定位：命令实现层'),
    'subcommands/tools.py': ('工具子命令', 'hermes tools 子命令。', '- 核心职责：管理工具\n- 系统定位：命令实现层'),
    'subcommands/uninstall.py': ('卸载子命令', 'hermes uninstall 子命令。', '- 核心职责：卸载 Hermes\n- 系统定位：运维层'),
    'subcommands/update.py': ('更新子命令', 'hermes update 子命令。', '- 核心职责：检查并安装新版本\n- 系统定位：自更新层'),
    'subcommands/version.py': ('版本子命令', 'hermes version 子命令。', '- 核心职责：输出版本号\n- 系统定位：命令实现层'),
    'subcommands/webhook.py': ('Webhook 子命令', 'hermes webhook 子命令。', '- 核心职责：管理 Webhook\n- 系统定位：命令实现层'),
    'subcommands/whatsapp.py': ('WhatsApp 子命令', 'hermes whatsapp 子命令。', '- 核心职责：配置 WhatsApp Bot\n- 系统定位：命令实现层'),
    'suggestions_cmd.py': ('建议命令', '实现 /suggest 斜杠命令。', '- 核心职责：用 LLM 生成操作建议\n- 系统定位：AI 辅助层'),
    'telegram_managed_bot.py': ('Telegram Bot', 'Hermes 的 Telegram Bot 集成。', '- 核心职责：启动 Telegram Bot，处理消息\n- 系统定位：第三方平台集成层'),
    'timeouts.py': ('超时配置', '定义各操作的超时时间。', '- 核心职责：集中管理超时参数\n- 系统定位：配置层'),
    'tips.py': ('提示小贴士', '展示使用提示和小贴士。', '- 核心职责：选择和展示上下文相关的提示\n- 系统定位：用户引导层'),
    'tools_config.py': ('工具配置', '管理内置工具的配置和启用状态。', '- 核心职责：读写工具配置，控制工具开关\n- 系统定位：工具管理层'),
    'uninstall.py': ('卸载逻辑', 'Hermes 的卸载逻辑。', '- 核心职责：递归清理安装目录和配置文件\n- 系统定位：运维层'),
    'voice.py': ('语音模式', '语音输入/输出模式。', '- 核心职责：管理麦克风录音、STT/TTS 调用\n- 关键概念：支持实时语音对话模式\n- 系统定位：多模态交互层'),
    'web_server.py': ('Web 服务器', 'Hermes Dashboard 的 Web 服务器实现。', '- 核心职责：启动 FastAPI 服务\n- 系统定位：Web 服务层'),
    'webhook.py': ('Webhook 处理', '接收和处理外部 Webhook 事件。', '- 核心职责：验证签名，分发事件\n- 系统定位：事件集成层'),
    'win_pty_bridge.py': ('Windows PTY 桥接', 'Windows 平台上的 PTY 桥接实现。', '- 核心职责：适配 Windows 伪终端\n- 系统定位：平台适配层'),
    'write_approval_commands.py': ('写入审批命令', '实现文件写入审批的斜杠命令。', '- 核心职责：处理 Agent 写文件的审批请求\n- 系统定位：安全交互层'),
    'xai_retirement.py': ('xAI 退役', '处理 xAI 提供方的退役/迁移逻辑。', '- 核心职责：将旧版 xAI 配置迁移到新格式\n- 系统定位：兼容迁移层'),
}

SEP = "─" * 65
base = Path('hermes_cli')
count = 0
errors = []

for rel, (title, summary, details) in annotations.items():
    fpath = base / rel
    if not fpath.exists():
        errors.append(f'NOT FOUND: {fpath}')
        continue
    text = fpath.read_text()
    if '【产品经理理解要点】' in text:
        continue

    chinese_block = f"""{title}

【产品经理理解要点】
{summary}
{details}

{SEP}"""

    # Strategy 1: File has existing docstring
    # Find the first triple-quoted docstring
    docstring_match = re.search(r'(""")(.*?)(""")', text, re.DOTALL)
    if docstring_match:
        start, end = docstring_match.start(), docstring_match.end()
        old_docstring_content = docstring_match.group(2)
        # Prepend Chinese block before existing content
        new_docstring_content = chinese_block + "\n" + old_docstring_content.lstrip('\n')
        new_docstring = f'"""{new_docstring_content}"""'
        text = text[:start] + new_docstring + text[end:]
        count += 1
        fpath.write_text(text)
        continue

    # Strategy 2: No docstring - add one
    # After from __future__ import annotations if present, or after shebang+imports
    lines = text.split('\n')

    # Find insertion point
    insert_idx = 0
    if lines and lines[0].startswith('#!'):
        insert_idx = 1

    # Skip from __future__ import
    for i in range(insert_idx, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('from __future__'):
            insert_idx = i + 1
            break
        elif stripped == '' or stripped.startswith('#') or stripped.startswith('import') or stripped.startswith('from'):
            insert_idx = i + 1
        else:
            break

    # Find first non-blank, non-comment, non-import line after initial imports
    # Actually, just insert after from __future__ or after shebang
    # Re-find: insert after from __future__ if present, otherwise after shebang
    insert_idx = 0
    if lines and lines[0].startswith('#!'):
        insert_idx = 1
    for i in range(insert_idx, len(lines)):
        if lines[i].strip().startswith('from __future__ import annotations'):
            insert_idx = i + 1
            break

    new_doc = f'"""{chinese_block}\n"""'
    lines.insert(insert_idx, new_doc)
    fpath.write_text('\n'.join(lines))
    count += 1

print(f'Annotated {count} files')
if errors:
    print('Errors:')
    for e in errors:
        print(f'  {e}')
