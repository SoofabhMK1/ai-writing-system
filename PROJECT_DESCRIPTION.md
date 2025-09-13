### **项目概览 (Project Overview)**
*   **项目名称**: ai-writing-system
*   **核心目标**: 一个AI辅助写作系统，提供从项目创建、大纲编辑、角色管理到AI生成内容的全流程支持。
*   **技术栈**: 
    *   **后端**: Python, FastAPI, SQLAlchemy (Async), PostgreSQL, Alembic, Pydantic V2, Uvicorn, OpenAI API
    *   **前端**: Vue.js 3, Vite, Vue Router, Pinia, Axios
    *   **容器化**: Docker, Docker Compose, Nginx
*   **项目架构**: 前后端分离架构。前端是Vue.js单页应用（SPA），后端是FastAPI提供RESTful API。通过Docker Compose统一编排和部署，其中Nginx作为前端静态文件的Web服务器和后端的反向代理。

### **核心工作流程 (Core Workflows)**

#### **AI 对话与内容生成**
1.  **访问**: 用户通过顶部导航栏的“对话”链接，进入独立的对话页面 (`ConversationView.vue`)。
2.  **配置对话**: 在 `ConversationSidebar.vue` 中，用户可以：
    *   选择要使用的 **AI 模型**。
    *   选择一个“**对话预设 (Prompt Preset)**”。一个预设封装了固定的系统提示、COT指导和其他指令。
    *   开启或关闭“**发送前预览**”功能。
    *   浏览、加载或删除**历史对话**。
3.  **发送消息**:
    *   用户在 `ChatInput.vue` 中输入消息并点击发送。
    *   `conversation.js` Pinia store 的 `sendMessage` action 被调用。
4.  **结构化消息构建**:
    *   `utils/messageBuilder.js` 工具函数被调用，它会执行以下核心操作：
        *   获取当前选中的“对话预设”。
        *   将当前对话内容拆分为“历史信息”和“用户当次输入”。
        *   过滤掉历史信息中所有AI回复的“思考过程”部分。
        *   按照预设，构建一个结构化的、由多条消息组成的数组。
    *   **消息结构**:
        ```json
        [
          { "role": "system", "content": "..." },
          { "role": "system", "content": "..." },
          { 
            "role": "user", 
            "content": "<history>...</history>\n<user_input>...</user_input>" 
          },
          { "role": "system", "content": "..." }
        ]
        ```
    *   **价值**: 这种结构通过标签明确告知AI各部分的角色，使COT指导能够精确引用上下文，极大地提升了AI回复的可控性和质量。
5.  **请求与响应**:
    *   `sendMessage` action 通过 `fetch` API 向后端的流式端点 `/api/v1/ai/chat-stream` 发起 `POST` 请求。
    *   后端通过 `StreamingResponse` 以**服务器发送事件 (SSE)** 的格式实时返回AI的思考过程 (`event: reasoning`) 和最终答案 (`event: content`)。
    *   `ChatInterface.vue` 组件负责展示这些流式数据，包括可折叠的思考过程。
6.  **保存对话**: 用户可以保存当前对话，所有消息（包括思考过程）都会被存入数据库。

#### **角色库管理**
1.  **访问**: 用户通过顶部导航栏的“角色库”链接，进入 `CharacterLibraryView.vue` 页面。
2.  **创建角色**:
    *   用户点击左侧的“创建新角色”按钮，会弹出一个 `CreateCharacterModal.vue` 模态框。
    *   用户在模态框的文本域中输入或粘贴 JSON 格式的角色数据，点击保存。
    *   前端通过 `characterService` 向后端的 `POST /api/v1/characters/` 发送请求。
3.  **查看与删除**:
    *   `CharacterList.vue` 以卡片形式展示所有角色。
    *   点击任意角色卡片，会弹出 `CharacterDetailModal.vue`，其中使用 Tab 布局展示角色的详细信息。
    *   在详情模态框中，用户可以点击“删除”按钮，并通过一个二次确认弹窗 (`ConfirmationModal.vue`) 来最终删除角色。
4.  **更新角色**:
    *   在详情模态框中，用户点击“更新”按钮，界面会切换到“编辑模式”。
    *   在编辑模式下，所有字段都变为可编辑状态，包括可以动态增删键值对的 JSON 字段。
    *   保存后，前端通过 `characterService` 向后端的 `PUT /api/v1/characters/{id}` 发送请求。

### **架构亮点与设计模式**

#### **后端**
1.  **全异步数据库操作**:
    *   **位置**: `app/database.py`, `app/crud/base.py`
    *   **设计**: 项目的数据库层完全基于 `asyncio`。`database.py` 使用 `create_async_engine` 创建异步引擎，并提供一个 `get_db` 依赖项来分发 `AsyncSession`。`CRUDBase` 中的所有方法（`get`, `create`, `update` 等）都是 `async` 函数，确保了所有数据库交互都是非阻塞的。
    *   **价值**: 充分利用了FastAPI的异步特性，在高并发场景下能提供更高的性能。
2.  **智能化的 `CRUDBase`**:
    *   **位置**: `app/crud/base.py`
    *   **设计**: 通用的 `CRUDBase` 中的 `update` 方法被重构，使其能够**自动检测**目标列的类型。当更新一个 **JSONB** 类型的字段时，它会自动执行**合并（Merge）**操作，而不是简单地覆盖。
    *   **价值**: 极大地提升了代码的复用性。任何需要对 JSONB 字段进行部分更新的 CRUD 服务，都无需重写 `update` 方法，直接继承 `CRUDBase` 即可获得此能力。
2.  **声明式的 API 依赖项**:
    *   **位置**: `app/api/routers/characters.py`
    *   **设计**: 使用 FastAPI 的依赖注入系统，创建了 `get_character_or_404` 这样的可复用依赖项。
    *   **价值**: 将“根据 ID 获取对象，如果不存在则抛出 404 异常”的重复逻辑进行封装，使 API 路由函数更简洁、更具声明性，提升了代码的可读性和可维护性。

#### **前端**
1.  **单一职责的组件设计**:
    *   **示例**: 复杂的 `CharacterDetailModal.vue` 被拆分为 `CharacterDetailDisplay.vue` (只读显示) 和 `CharacterDetailEdit.vue` (编辑表单) 两个职责单一的子组件。
    *   **价值**: 遵循了“单一职责原则”，使得每个组件的代码都更少、更易于理解和维护。
2.  **全局滚动锁定机制**:
    *   **问题**: 解决了在显示模态框时，背景页面仍然可以滚动的“滚动穿透”问题。
    *   **设计**: 通过扩展 `store/modal.js` 增加一个全局模态框计数器，并在根组件 `App.vue` 中 `watch` 这个状态，动态地为 `<body>` 添加或移除一个 `overflow: hidden` 的 CSS 类。
    *   **价值**: 提供了一个优雅、集中且可扩展的全局 UI 问题解决方案。任何模态框（无论是全局还是局部），只需上报其状态给 `modalStore`，即可自动被纳入滚动锁定管理。
3.  **统一的 UI 规范 (Design System)**:
    *   **问题**: 项目初期缺乏统一的视觉和交互规范，导致组件样式不一致，维护困难。
    *   **设计**: 在 `frontend/src/style.css` 中建立了一套轻量级的设计规范。通过 CSS 自定义属性（变量）定义了全局的颜色、字体、间距、圆角和阴影 (Design Tokens)，并支持深色/浅色模式。
    *   **价值**: 确保了整个应用视觉风格的统一性（现代、简约），提高了开发效率（复用规范和通用样式类），并极大地简化了未来的 UI 维护和主题切换。所有核心组件和视图都已基于此规范进行了重构。
4.  **模块化的前端服务**:
    *   **问题**: 随着功能的增加，`conversation.js` Pinia store 变得越来越臃肿，混合了状态管理、API 调用和数据处理逻辑。
    *   **设计**: 对核心对话逻辑进行了重构，将不同的职责拆分到独立的模块中：
        *   `services/aiStreamService.js`: 专门负责处理从后端发来的 SSE（服务器发送事件）流。它能够解析标准的 SSE 格式，区分 `event: reasoning` 和 `content` 等不同的事件类型，并为每种事件类型调用相应的回调函数。
        *   `utils/messageBuilder.js`: 负责构建发送给 AI 的最终消息负载。它会根据用户选择的“对话预设”，将系统提示、COT指导、历史记录和用户当前输入整合成一个结构化的消息数组。
    *   **价值**: 这种关注点分离的设计使得 `conversation.js` store 的职责更加清晰（专注于状态管理），代码更易于维护和测试，并为未来扩展更复杂的消息处理逻辑（如动态插入上下文、摘要等）打下了坚实的基础。
5.  **可复用的布局与UI组件 (Reusable Layout & UI Components)**:
    *   **背景**: 为了解决多个视图中存在的布局重复和UI元素不一致的问题，我们创建了一系列高度可复用的基础组件。
    *   **设计**:
        *   **`WorkspaceLayout.vue`**: 提供了一个标准的双栏工作区布局（左侧固定宽度，右侧自适应），并被 `ProjectListView`, `CharacterLibraryView`, `ConversationView` 等核心视图所采用。
        *   **`StatusIndicator.vue`**: 一个用于处理异步数据状态（加载中、错误、空状态）的通用组件。它通过 `props` 接收状态，并显示相应的UI，从而统一了整个应用的数据加载反馈。
        *   **全局表单样式 (`.form-control`)**: 在 `style.css` 中定义了统一的表单控件样式，确保所有输入框、文本域都遵循统一的设计规范。
    *   **价值**: 这些组件的引入极大地减少了代码冗余，增强了UI的一致性，并为未来快速开发新功能页面提供了坚实的基础。

### **文件结构与核心职责 (File Structure & Core Responsibilities)**

```plaintext
.
├── .env
├── .gitignore
├── backend/
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routers/
│       │       ├── ai_generation.py
│       │       ├── characters.py
│       │       ├── conversations.py
│       │       ├── outline_nodes.py
│       │       ├── projects.py
│       │       ├── prompt_presets.py
│       │       └── settings.py
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       ├── crud/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── crud_character.py
│       │   ├── crud_conversation.py
│       │   ├── crud_message.py
│       │   ├── crud_outline_node.py
│       │   ├── crud_project.py
│       │   ├── crud_prompt_preset.py
│       │   └── crud_setting.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── character.py
│       │   ├── conversation.py
│       │   ├── message.py
│       │   ├── outline_node.py
│       │   ├── project.py
│       │   ├── prompt_preset.py
│       │   └── setting.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── character.py
│       │   ├── conversation.py
│       │   ├── message.py
│       │   ├── outline_node.py
│       │   ├── project.py
│       │   ├── prompt_preset.py
│       │   └── setting.py
│       └── services/
│           ├── ai_service.py
│           └── prompt_service.py
├── docker-compose.yml
└── frontend/
    ├── Dockerfile
    ├── index.html
    ├── nginx.conf
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.vue
        ├── main.js
        ├── style.css
        ├── assets/
        │   └── vue.svg
        ├── components/
        │   ├── CharacterDetailDisplay.vue
        │   ├── CharacterDetailEdit.vue
        │   ├── CharacterDetailModal.vue
        │   ├── CharacterList.vue
        │   ├── ChatInput.vue
        │   ├── ChatInterface.vue
        │   ├── ConfirmationModal.vue
        │   ├── ConversationSidebar.vue
        │   ├── CreateCharacterModal.vue
        │   ├── CreateProjectModal.vue
        │   ├── DetailItem.vue
        │   ├── EditableField.vue
        │   ├── EditableJson.vue
        │   ├── GenerationConfigPanel.vue
        │   ├── GenerationResultModal.vue
        │   ├── HistoryPanel.vue
        │   ├── JsonViewer.vue
        │   ├── NavBar.vue
        │   ├── Notification.vue
        │   ├── OutlineEditor.vue
        │   ├── OutlineNodeItem.vue
        │   ├── PreviewSendModal.vue
        │   ├── ProjectInfoPanel.vue
        │   ├── ProjectList.vue
        │   ├── PromptModal.vue
        │   └── settings/
        │       ├── AIModelSettings.vue
        │       ├── PromptPresets.vue
        │       ├── PromptTemplates.vue
        │       ├── SettingsFormModal.vue
        │       ├── WorldviewSettings.vue
        │       └── WritingStyleSettings.vue
        ├── router/
        │   └── index.js
        ├── services/
        │   ├── aiStreamService.js
        │   ├── api.js
        │   ├── characterService.js
        │   ├── conversationService.js
        │   ├── outlineNodeService.js
        │   ├── projectService.js
        │   ├── promptPresetService.js
        │   └── settingService.js
        ├── store/
        │   ├── character.js
        │   ├── conversation.js
        │   ├── modal.js
        │   ├── notification.js
        │   ├── prompt.js
        │   └── promptPreset.js
        └── views/
            ├── CharacterLibraryView.vue
            ├── ConversationView.vue
            ├── ProjectDetailView.vue
            ├── ProjectListView.vue
            └── SettingsView.vue
```

#### **后端 (Backend)**
*   `backend/`: 后端应用的根目录，基于 Python FastAPI 框架。
    *   `alembic/`: 数据库迁移脚本目录，由 Alembic 管理。
    *   `app/`: FastAPI 应用的核心代码目录。
        *   `api/routers/`: 包含所有独立的路由模块，如 `projects.py`, `settings.py`, 以及 `prompt_presets.py`。
        *   `core/`: 存放应用的核心配置和安全相关模块。
        *   `crud/`: 包含所有数据库的 CRUD 操作逻辑。`base.py` 定义了通用的异步 `CRUDBase`，`crud_*.py` 文件实现了具体模型的数据库操作。
        *   `models/`: 定义 SQLAlchemy 的 ORM 数据模型。`__init__.py` 负责导出所有模型。
        *   `schemas/`: 定义 Pydantic 数据校验模型。`__init__.py` 负责导出所有 schemas。
        *   `services/`: 存放核心业务逻辑服务。
        *   `database.py`: 初始化 SQLAlchemy 异步引擎和会话，并定义了所有模型继承的 `Base` 类。
        *   `main.py`: FastAPI 应用的入口文件，聚合所有 API 路由。
        *   `services/`: 存放核心业务逻辑服务。
            *   `ai_service.py`: 封装与大语言模型 API 的交互逻辑。它现在包含一个 `generate_chat_completion` 方法，可以接收完整的消息历史，并以**服务器发送事件 (SSE)** 的格式处理流式响应。
            *   `prompt_service.py`: 负责动态构建发送给AI的结构化提示（Prompt）。目前，它会引导AI生成一个包含核心矛盾、主角任务、故事大纲等元素的“小说蓝图”，而不仅仅是章节列表。
        *   `database.py`: 初始化 SQLAlchemy 引擎和会话。
        *   `main.py`: FastAPI 应用的入口文件。其核心职责是初始化FastAPI应用，并从 `api/routers/` 目录中导入并聚合所有模块化的路由。
    *   `Dockerfile`: 用于构建后端服务 Docker 镜像的指令文件。
    *   `requirements.txt`: 定义了 Python 的所有依赖库。

#### **前端 (Frontend)**
*   `frontend/`: 前端应用的根目录，基于 Vue.js 3 和 Vite。
    *   `src/`: 前端应用的核心源代码目录。
        *   `components/`: 存放可复用的 Vue 组件。
            *   `ConversationSidebar.vue`: 对话页面的左侧边栏，包含AI模型和对话预设的选择。
            *   `settings/`: 包含所有设置页面的组件，如 `WorldviewSettings.vue` 和 `PromptPresets.vue`。
        *   `router/`: 存放 Vue Router 的配置。
        *   `services/`: 存放与后端 API 通信的逻辑，如 `projectService.js` 和 `promptPresetService.js`。
        *   `store/`: 存放 Pinia 的全局状态管理模块，如 `conversation.js` 和 `promptPreset.js`。
        *   `utils/`: 存放可复用的工具函数，如 `messageBuilder.js`。
        *   `views/`: 存放页面级别的 Vue 组件，如 `ConversationView.vue` 和 `SettingsView.vue`。
        *   `views/`: 存放页面级别的 Vue 组件。
            *   `ProjectListView.vue`: **项目列表页**。此页面是应用的主要入口，展示所有项目。
            *   `ProjectDetailView.vue`: **项目详情页**。当用户从列表页选择一个项目后进入此页面，采用双栏布局，左侧是项目列表 (`ProjectList.vue`)，右侧是选中项目的工作区 (`OutlineEditor.vue`)。
            *   `ConversationView.vue`: **独立的对话页面**。一个支持多轮对话的 AI 交互界面，包含功能丰富的侧边栏和主聊天窗口。
            *   `SettingsView.vue`: 应用的设置页面，允许用户管理AI模型、世界观、文风等。
        *   `App.vue`: Vue 应用的根组件，是所有页面的容器。
        *   `main.js`: 前端应用的入口文件，负责初始化Vue实例、Pinia和Vue Router。
    *   `index.html`: 单页应用的 HTML 入口文件。
    *   `vite.config.js`: Vite 构建工具的配置文件。核心配置是 `server.proxy`，它将开发环境中的 `/api/v1` 请求代理到后端服务，以解决跨域问题并与生产环境保持一致。
    *   `package.json`: 定义了项目信息、脚本命令和 Node.js 依赖。
    *   `nginx.conf`: Nginx 配置文件。在生产环境中，它负责两件事：1. 提供前端的静态文件（HTML, CSS, JS）。2. 作为反向代理，将所有 `/api/v1` 的请求转发到后端的 `backend:8001` 服务。
    *   `Dockerfile`: 使用多阶段构建（multi-stage build），先用 `node` 环境构建出静态文件，再用轻量级的 `nginx` 镜像来提供服务。

#### **根目录 (Root Directory)**
*   `.env`: 存储环境变量，如数据库连接信息、用于加密的 `SECRET_KEY` 等。**此文件不应提交到版本控制中。**
*   `docker-compose.yml`: Docker Compose 编排文件，定义并统一管理 `db` (PostgreSQL), `backend` (FastAPI), 和 `frontend` (Nginx) 三个服务，实现一键启动整个应用。
*   `.gitignore`: 定义了 Git 应忽略的文件和目录，如 `node_modules`, `__pycache__`, `.env` 等。
