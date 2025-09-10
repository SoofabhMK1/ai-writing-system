---
### **项目概览 (Project Overview)**
*   **项目名称**: ai-writing-system
*   **核心目标**: 一个AI辅助写作系统，提供从项目创建、大纲编辑到AI生成内容的全流程支持。
*   **技术栈**: 
    *   **后端**: Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, Uvicorn, OpenAI API
    *   **前端**: Vue.js 3, Vite, Vue Router, Pinia, Axios
    *   **容器化**: Docker, Docker Compose, Nginx
*   **项目架构**: 前后端分离架构。前端是Vue.js单页应用（SPA），后端是FastAPI提供RESTful API。通过Docker Compose统一编排和部署，其中Nginx作为前端静态文件的Web服务器和后端的反向代理。

### **核心工作流程 (Core Workflow)**
以“生成大纲”功能为例，数据流如下：
1.  **前端 (`OutlineEditor.vue`)**: 用户在AI配置面板 (`GenerationConfigPanel.vue`) 中选择配置，并点击“生成大纲”按钮。
2.  **前端 (`OutlineEditor.vue`)**: 调用 `aiGenerationService` (从 `settingService.js` 导出) 获取初始提示词。
3.  **前端 (`AIGenerationModal.vue`)**: 弹出模态框，显示初始提示词。用户可修改后点击“确认并生成”。
4.  **前端 (`AIGenerationModal.vue`)**: 模态框自身通过 `fetch` API 向后端的流式端点 `/generate-outline-stream` 发起 `POST` 请求。
5.  **Nginx**: 作为反向代理，将请求无缝转发到 `backend` 服务。
6.  **后端 (`api/endpoints.py`)**: AI相关的路由接收到请求，并调用 `ai_service`。
7.  **后端 (`services/ai_service.py`)**: 该服务向AI模型发出流式请求。它被设计为可以处理支持独立“思维链”输出（`reasoning_content`）的先进模型。
8.  **前后端数据流**: 后端通过 `StreamingResponse` 以**服务器发送事件 (Server-Sent Events, SSE)** 的格式向前端推送数据。事件被明确标记为 `reasoning`（思维链）或 `content`（最终内容）。
9.  **前端 (`AIGenerationModal.vue`)**: 组件内的 `fetch` 逻辑会解析SSE流。`reasoning` 事件的数据被实时渲染到“AI 思维链”标签页，而 `content` 事件的数据则被渲染到“生成结果”标签页。
10. **前端 (`OutlineEditor.vue`)**: 用户在模态框中点击保存后，`AIGenerationModal` 会将纯净的JSON结果传递给 `OutlineEditor`，后者负责将其保存为一个新的“历史版本”。

### **文件结构与核心职责 (File Structure & Core Responsibilities)**
这是一个对大语言模型友好的项目文件结构树。在未来进行代码修改时，请务必参考此结构以理解各部分的功能和相互关系。

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
│       │   └── endpoints.py
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       ├── crud/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── crud_outline_node.py
│       │   ├── crud_project.py
│       │   └── crud_setting.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── outline_node.py
│       │   ├── project.py
│       │   └── setting.py
│       ├── schemas/
│       │   ├── __init__.py
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
        ├── components/
        │   ├── AIGenerationModal.vue
        │   ├── ConfirmationModal.vue
        │   ├── CreateProjectModal.vue
        │   ├── GenerationConfigPanel.vue
        │   ├── GenerationResultModal.vue
        │   ├── HistoryPanel.vue
        │   ├── NavBar.vue
        │   ├── Notification.vue
        │   ├── OutlineEditor.vue
        │   ├── OutlineNodeItem.vue
        │   ├── ProjectInfoPanel.vue
        │   ├── ProjectList.vue
        │   ├── PromptModal.vue
        │   └── settings/
        ├── router/
        │   └── index.js
        ├── services/
        │   ├── api.js
        │   ├── outlineNodeService.js
        │   ├── projectService.js
        │   └── settingService.js
        ├── store/
        │   ├── modal.js
        │   ├── notification.js
        │   └── prompt.js
        └── views/
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
        *   `api/`: 存放 API 路由层。
            *   `endpoints.py`: 定义所有 HTTP 端点 (Endpoints)，并将它们组织成 APIRouter。
        *   `core/`: 存放应用的核心配置和安全相关模块。
            *   `config.py`: 使用 Pydantic 的 `BaseSettings` 管理环境变量，是配置的唯一来源。
            *   `security.py`: 使用 `cryptography.fernet` 对敏感数据（如AI模型的API密钥）进行对称加密和解密。
        *   `crud/`: 包含所有数据库的 CRUD (Create, Read, Update, Delete) 操作逻辑。
            *   `base.py`: 定义了一个通用的 `CRUDBase` 类，封装了基本的数据库操作，以实现代码复用。
            *   `crud_*.py`: 继承自 `CRUDBase`，用于实现特定模型（如Project, OutlineNode）的数据库操作。
        *   `models/`: 定义 SQLAlchemy 的 ORM 数据模型，每个文件对应一个数据表。
            *   `__init__.py`: 作为 `models` 包的入口，负责导出所有模型类，以便其他模块可以统一从 `app.models` 导入。
            *   `base.py`: 声明所有模型都应继承的 `Base` 类。
            *   `project.py`, `outline_node.py`, `setting.py`: 分别定义项目、大纲节点和设置的数据表模型，并定义它们之间的关系（如级联删除）。
        *   `schemas/`: 定义 Pydantic 数据校验模型，用于API请求和响应的数据验证。
            *   `__init__.py`: 作为 `schemas` 包的入口，导出所有 Pydantic 模型。
            *   `project.py`, `outline_node.py`, `setting.py`: 分别定义与模型对应的Pydantic Schema。
        *   `services/`: 存放核心业务逻辑服务。
            *   `ai_service.py`: 封装与大语言模型 API 的交互逻辑。它以**服务器发送事件 (SSE)** 的格式处理流式响应，并能区分处理 `reasoning_content`（思维链）和 `content`（最终内容）两种数据，以支持更先进的模型。
            *   `prompt_service.py`: 负责动态构建发送给AI的结构化提示（Prompt）。目前，它会引导AI生成一个包含核心矛盾、主角任务、故事大纲等元素的“小说蓝图”，而不仅仅是章节列表。
        *   `database.py`: 初始化 SQLAlchemy 引擎和会话。
        *   `main.py`: FastAPI 应用的入口文件，负责组装路由、CORS 中间件等。
    *   `Dockerfile`: 用于构建后端服务 Docker 镜像的指令文件。
    *   `requirements.txt`: 定义了 Python 的所有依赖库。

#### **前端 (Frontend)**
*   `frontend/`: 前端应用的根目录，基于 Vue.js 3 和 Vite。
    *   `src/`: 前端应用的核心源代码目录。
        *   `components/`: 存放可复用的 Vue 组件。
            *   `OutlineEditor.vue`: **核心工作区组件**。当用户选择一个项目后，此组件作为主界面，整合了 `GenerationConfigPanel`（AI配置）, `ProjectInfoPanel`（项目信息）和 `HistoryPanel`（历史记录），并负责发起AI生成流程。
            *   `GenerationConfigPanel.vue`: 左侧的AI生成配置面板。
            *   `ProjectInfoPanel.vue`: 右上角的项目核心信息编辑面板。
            *   `HistoryPanel.vue`: 右下角的大纲历史版本列表面板。
            *   `ProjectList.vue`: 在项目列表页 (`ProjectListView`) 中，以卡片形式展示所有项目，并处理项目选择和删除的逻辑。
            *   `OutlineNodeItem.vue`: 用于在大纲树状图中展示单个节点。
            *   `NavBar.vue`: 应用顶部的导航栏。
            *   **模态框组件**:
                *   `AIGenerationModal.vue`: AI生成大纲的核心交互界面。它现在是一个功能完善的“智能”组件，内部自己处理 `fetch` 流式请求和SSE事件解析。其UI被重构为**标签页**形式，可分别展示“生成结果”、“AI思维链”和“Prompt”，极大地改善了用户体验。
                *   `ConfirmationModal.vue`: 通用的二次确认模态框。
                *   `CreateProjectModal.vue`: 创建新项目的模态框。
                *   `GenerationResultModal.vue`: 用于预览历史版本大纲的模态框。
                *   `PromptModal.vue`: 通用的、需要用户输入的提示框。
            *   **设置页面组件 (`settings/`)**:
                *   `AIModelSettings.vue`, `WorldviewSettings.vue`, `WritingStyleSettings.vue`, `PromptTemplates.vue`: 分别对应设置页面中的不同配置项的管理界面。
        *   `router/`: 存放 Vue Router 的配置，定义了应用的页面路由。
        *   `services/`: 存放与后端 API 通信的逻辑。
            *   `api.js`: 配置一个全局的 Axios 实例，设置了基础 URL (`/api/v1`)。
            *   `projectService.js`, `outlineNodeService.js`: 分别封装了与项目、大纲节点相关的API调用。
            *   `settingService.js`: 一个复合服务，导出了多个与设置相关的子服务，如 `worldviewService`, `writingStyleService`, `aiModelService` 以及发起AI生成请求的 `aiGenerationService`。
        *   `store/`: 存放 Pinia 的全局状态管理模块。
            *   `modal.js`, `notification.js`, `prompt.js`: 分别管理全局模态框、通知和输入提示框的状态和逻辑。
        *   `views/`: 存放页面级别的 Vue 组件。
            *   `ProjectListView.vue`: **项目列表页**。此页面是应用的主要入口和工作区，采用双栏布局，左侧是项目列表 (`ProjectList.vue`)，右侧是选中项目的工作区 (`OutlineEditor.vue`)。
            *   `ProjectDetailView.vue`: 用于展示项目详细信息或大纲的独立页面 (当前在主要流程中较少使用)。
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
---
