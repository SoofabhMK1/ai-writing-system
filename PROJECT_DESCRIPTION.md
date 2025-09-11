### **项目概览 (Project Overview)**
*   **项目名称**: ai-writing-system
*   **核心目标**: 一个AI辅助写作系统，提供从项目创建、大纲编辑、角色管理到AI生成内容的全流程支持。
*   **技术栈**: 
    *   **后端**: Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, Uvicorn, OpenAI API
    *   **前端**: Vue.js 3, Vite, Vue Router, Pinia, Axios
    *   **容器化**: Docker, Docker Compose, Nginx
*   **项目架构**: 前后端分离架构。前端是Vue.js单页应用（SPA），后端是FastAPI提供RESTful API。通过Docker Compose统一编排和部署，其中Nginx作为前端静态文件的Web服务器和后端的反向代理。

### **核心工作流程 (Core Workflows)**

#### **AI 对话与内容生成**
1.  **前端 (`OutlineEditor.vue`)**: 用户在 AI 配置面板 (`GenerationConfigPanel.vue`) 中选择配置，并点击“生成大纲”按钮。
2.  **前端 (`OutlineEditor.vue`)**: 调用 `aiGenerationService` 获取初始提示词，然后导航到独立的对话页面 (`ConversationView.vue`)，并将提示词暂存。
3.  **前端 (`ConversationView.vue`)**: 这是一个支持多轮对话的独立页面。
    *   左侧的 `ConversationSidebar.vue` 显示历史对话列表，并提供“使用初始 Prompt”的按钮。
    *   用户点击按钮，初始 Prompt 被填充到 `ChatInput.vue` 中。
4.  **前端 (`ChatInput.vue`)**: 用户确认或修改后，点击发送。
5.  **前端 (`conversation.js` Pinia Store)**: `sendMessage` action 被调用。
    *   **发送前预览**: 如果用户在 `ConversationSidebar.vue` 中勾选了“发送前预览”，`conversation.js` 会调用 `modal.js` store 来弹出一个 `PreviewSendModal.vue` 模态框，显示即将发送的完整内容。
    *   **发送请求**: 用户在预览后点击“继续”，或如果未开启预览，`sendMessage` action 会通过 `fetch` API 向后端的流式端点 `/api/v1/ai/chat-stream` 发起 `POST` 请求，请求体中包含**完整的消息历史**。
6.  **Nginx & 后端**: 请求通过 Nginx 转发到后端 `ai_generation.py` 路由，并调用 `ai_service.py`。
7.  **前后端数据流**: 后端通过 `StreamingResponse` 以**服务器发送事件 (SSE)** 的格式向前端实时推送 AI 的回复。
8.  **前端 (`conversation.js` Pinia Store)**: `sendMessage` action 解析 SSE 流，并持续更新 `ChatInterface.vue` 中显示的 AI 回复内容。
9.  **前端 (`ConversationSidebar.vue`)**: 用户可以点击“保存对话”按钮，将当前对话（包括所有消息）通过 `conversationService` 保存到后端数据库。

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
1.  **智能化的 `CRUDBase`**:
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
│       │   └── crud_setting.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── character.py
│       │   ├── conversation.py
│       │   ├── message.py
│       │   ├── outline_node.py
│       │   ├── project.py
│       │   └── setting.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── character.py
│       │   ├── conversation.py
│       │   ├── message.py
│       │   ├── outline_node.py
│       │   ├── project.py
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
        │       ├── PromptTemplates.vue
        │       ├── SettingsFormModal.vue
        │       ├── WorldviewSettings.vue
        │       └── WritingStyleSettings.vue
        ├── router/
        │   └── index.js
        ├── services/
        │   ├── api.js
        │   ├── characterService.js
        │   ├── conversationService.js
        │   ├── outlineNodeService.js
        │   ├── projectService.js
        │   └── settingService.js
        ├── store/
        │   ├── character.js
        │   ├── conversation.js
        │   ├── modal.js
        │   ├── notification.js
        │   └── prompt.js
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
        *   `env.py`: Alembic 的运行时环境配置。核心是设置 `target_metadata = Base.metadata`，并确保所有模型都被导入，以便 Alembic 能够自动检测模型变化。
        *   `versions/`: 存放具体的数据库版本脚本。
    *   `app/`: FastAPI 应用的核心代码目录。
        *   `api/`: 存放 API 路由层。该目录遵循模块化设计，将不同资源的路由拆分到独立的模块中。
            *   `routers/`: 包含所有独立的路由模块。
                *   `projects.py`: 负责所有与“项目”相关的CRUD操作。
                *   `outline_nodes.py`: 负责所有与“大纲节点”相关的CRUD操作。
                *   `settings.py`: 负责所有与“设置”相关的端点（世界观、文风、AI模型等），并使用工厂模式来减少重复代码。
                *   `ai_generation.py`: 负责所有与AI内容生成相关的端点，包括支持多轮对话历史的流式聊天端点。
                *   `conversations.py`: 负责对话历史的 CRUD 操作。
        *   `core/`: 存放应用的核心配置和安全相关模块。
            *   `config.py`: 使用 Pydantic 的 `BaseSettings` 管理环境变量，是配置的唯一来源。
            *   `security.py`: 使用 `cryptography.fernet` 对敏感数据（如AI模型的API密钥）进行对称加密和解密。
        *   `crud/`: 包含所有数据库的 CRUD (Create, Read, Update, Delete) 操作逻辑。
            *   `base.py`: 定义了一个通用的 `CRUDBase` 类，封装了基本的数据库操作，以实现代码复用。
            *   `crud_*.py`: 继承自 `CRUDBase`，用于实现特定模型（如Project, OutlineNode, Conversation）的数据库操作。
        *   `models/`: 定义 SQLAlchemy 的 ORM 数据模型，每个文件对应一个数据表。
            *   `__init__.py`: 作为 `models` 包的入口，负责导出所有模型类，以便其他模块可以统一从 `app.models` 导入。
            *   `base.py`: 声明所有模型都应继承的 `Base` 类。
            *   `project.py`, `outline_node.py`, `setting.py`: 分别定义项目、大纲节点和设置的数据表模型。
            *   `conversation.py`, `message.py`: 定义对话和消息的数据模型，支持存储多轮对话历史。
        *   `schemas/`: 定义 Pydantic 数据校验模型，用于API请求和响应的数据验证。
            *   `__init__.py`: 作为 `schemas` 包的入口，导出所有 Pydantic 模型。
            *   `project.py`, `outline_node.py`, `setting.py`: 分别定义与模型对应的Pydantic Schema。
            *   `conversation.py`, `message.py`: 为对话和消息定义 Pydantic Schemas。
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
            *   `OutlineEditor.vue`: **核心工作区组件**。当用户选择一个项目后，此组件作为主界面，整合了 `GenerationConfigPanel`（AI配置）, `ProjectInfoPanel`（项目信息）和 `HistoryPanel`（历史记录）。现在，它负责**发起 AI 对话**，将用户导航到独立的对话页面。
            *   **对话页面组件**:
                *   `ConversationSidebar.vue`: 对话页面的左侧边栏，用于管理和导航对话历史。现在还包含一个**“发送前预览”的切换开关**。
                *   `ChatInterface.vue`: 对话页面的核心区域，用于展示用户与 AI 之间的消息。
                *   `ChatInput.vue`: 对话页面的底部输入区域，包含文本输入框和发送按钮。
            *   `GenerationConfigPanel.vue`: 左侧的AI生成配置面板。
            *   `ProjectInfoPanel.vue`: 右上角的项目核心信息编辑面板。
            *   `HistoryPanel.vue`: 右下角的大纲历史版本列表面板。
            *   `ProjectList.vue`: 在项目列表页 (`ProjectListView`) 中，以卡片形式展示所有项目，并处理项目选择和删除的逻辑。
            *   `NavBar.vue`: 应用顶部的导航栏。
            *   **模态框组件**:
                *   `ConfirmationModal.vue`: 通用的二次确认模态框。
                *   `PreviewSendModal.vue`: 用于在发送前向用户展示完整请求内容的模态框。
                *   `CreateProjectModal.vue`: 创建新项目的模态框。
                *   `GenerationResultModal.vue`: 用于预览历史版本大纲的模态框。
                *   `PromptModal.vue`: 通用的、需要用户输入的提示框。
            *   **设置页面组件 (`settings/`)**:
                *   `AIModelSettings.vue`, `WorldviewSettings.vue`, `WritingStyleSettings.vue`, `PromptTemplates.vue`: 分别对应设置页面中的不同配置项的管理界面。
        *   `router/`: 存放 Vue Router 的配置，定义了应用的页面路由。
        *   `services/`: 存放与后端 API 通信的逻辑。
            *   `api.js`: 配置一个全局的 Axios 实例，设置了基础 URL (`/api/v1`)。
            *   `projectService.js`, `outlineNodeService.js`: 分别封装了与项目、大纲节点相关的API调用。
            *   `settingService.js`: 一个复合服务，导出了多个与设置相关的子服务。
            *   `conversationService.js`: 封装了与对话历史相关的 CRUD API 调用。
        *   `store/`: 存放 Pinia 的全局状态管理模块。
            *   `modal.js`: 管理全局模态框的状态和逻辑，现在支持**多种类型的模态框**（如 `ConfirmationModal` 和 `PreviewSendModal`）。
            *   `notification.js`, `prompt.js`: 分别管理通知和输入提示框的状态。
            *   `conversation.js`: 负责管理当前对话的状态，包括消息历史、加载状态，并处理与后端的流式通信。现在还包含**触发发送前预览的核心逻辑**。
        *   `views/`: 存放页面级别的 Vue 组件。
            *   `ProjectListView.vue`: **项目列表页**。此页面是应用的主要入口和工作区，采用双栏布局，左侧是项目列表 (`ProjectList.vue`)，右侧是选中项目的工作区 (`OutlineEditor.vue`)。
            *   `ConversationView.vue`: **对话页面**。一个独立的、支持多轮对话的 AI 交互界面，包含对话历史侧边栏和主聊天窗口。
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
