# text-to-cad 架构理解报告

## A. 项目核心目标

这是一个**以编程 AI 代理（如 Codex、Claude Code）为核心驱动的 CAD 生成 harness（脚手架）**。

核心目标：
- 让 AI 代理通过修改 Python 源文件来生成/编辑三维 CAD 几何体
- 提供本地 Web 浏览器（CAD Explorer），无需后端即可实时预览生成的模型
- 通过 `@cad[...]` 引用系统让 AI 能精确定位模型中的面/边/角，做几何感知的精细编辑
- 全部资产都纳入 git 版本管理（源文件 + 生成物一起提交）

**不是**：端对端的在线平台，不提供云端 LLM 调用，也不持有任何 AI 推理服务。

---

## B. 完整用户流程（文本输入 → CAD 文件 → 浏览模型）

```
用户用自然语言描述零件
        │
        ▼
AI 代理（Codex/Claude Code）在 models/ 下
编写或修改 Python 生成器 source.py
（包含 gen_step() 函数，使用 build123d 构建几何体）
        │
        ▼
AI 代理调用 Python CLI 脚本：
  .venv/bin/python skills/cad/scripts/gen_step_part models/xxx/source.py
        │
        ▼
Python 脚本执行：
  1. 导入 source.py，调用 gen_step()
  2. 通过 build123d / OCP (OpenCascade) 生成几何体
  3. 导出 STEP 文件（models/xxx/part.step）
  4. 把 STEP 转换为 GLB（Three.js 可消费的网格）
  5. 提取拓扑数据（topology.json / topology.bin，包含面/边/角索引）
  6. 以上 GLB + topology 存入 models/xxx/.part.step/ 隐藏目录
        │
        ▼
Vite dev server（npm run dev，端口 4178）监听文件系统变化
检测到新 .step / .glb / topology 文件变化后
通过 WebSocket 推送 cad-catalog:changed 事件给浏览器
        │
        ▼
浏览器中的 React 应用重新拉取 /__cad/catalog
（Vite 中间件扫描 models/ 目录，返回所有 CAD 条目清单）
        │
        ▼
用户在 CAD Explorer 中看到模型，
可以旋转/拾取面/复制 @cad[...] 引用
供下一轮 AI 精细编辑使用
```

---

## C. Python 部分负责什么

Python 层是**唯一的 CAD 生产引擎**，完全在用户本地运行。

| 模块 | 职责 |
|------|------|
| `source.py`（用户/AI 编写） | 定义 `gen_step()` → 调用 build123d API 构建 Shape |
| `build123d` + `OCP` | 实际几何内核（OpenCascade 的 Python 绑定），处理布尔运算、挤出、倒角等 |
| `gen_step_part` / `gen_step_assembly` | 调用生成器 → 导出 STEP → 调用 GLB/topology 管线 |
| `common/generation.py`（40KB） | 生成主流程：执行器、STEP 导出、GLB 转换、拓扑提取、元数据写入 |
| `common/step_scene.py`（72KB） | STEP 文件解析、场景图构建、面/边/角拓扑编号（是 cadref 和 picking 的基础） |
| `common/assembly_composition.py`（48KB） | 装配体的组合逻辑（递归 children 树 → STEP 组装） |
| `common/catalog.py` | 元数据目录写入 |
| `cadref` | 从 STEP 文件解析并查询 `@cad[...]` refs（面积、法向量、坐标等几何事实） |
| `snapshot` | 用 OCP 渲染等距/俯视/透视截图 PNG（供 AI 快速验证） |
| `gen_dxf` | 从 `gen_dxf()` 生成 DXF 平面图 |
| `gen_urdf`（URDF skill） | 从 `gen_urdf()` 生成机器人 URDF 描述文件 |

> Python 层**不依赖 viewer**，可以独立运行。

---

## D. React/Vite/Three.js viewer 负责什么

Viewer 是**只读的本地 CAD 浏览器**，不修改任何文件。

| 层 | 技术 | 职责 |
|----|------|------|
| 构建/服务 | Vite 7 | 开发服务器 + HMR + 自定义中间件（`/__cad/catalog` API、静态 CAD 文件服务） |
| UI 框架 | React 18 | 组件树：工作台 / 侧边栏 / 3D 视图 / DXF 视图 / URDF 视图 |
| 3D 渲染 | Three.js 0.160 | 加载 GLB，渲染 STEP 模型（含拾取代理几何） |
| 目录扫描 | `cadDirectoryScanner.mjs` | 扫描 `.step/.stl/.dxf/.urdf` 文件 → 构建 CAD 条目列表（JSON） |
| HMR 感知 | `vite.config.mjs` 中的 `cadCatalogPlugin` | 监听文件变化 → WS 推送 → 前端重新拉取目录 |
| 选择器 / Picking | `lib/selectors/` + `components/viewer/hooks/useViewerPicking` | 处理面/边/角拾取，生成 `@cad[...]` 剪贴板内容 |
| DXF 浏览 | `components/DxfViewer.js` | 解析并渲染 DXF 平面图 |
| URDF 浏览 | `lib/urdf/` | 解析 URDF XML，Joint Slider 动画，正运动学 |
| 持久化 | `lib/workbench/persistence.js` | `localStorage` / `sessionStorage` 存储工作台状态 |
| 装配体视图 | `lib/assembly/` | 从 topology.json 中的 `assembly.root` 重建装配树，分层加载 GLB |

**Vite 在 dev 模式和 build 模式的区别：**
- `dev`：动态扫描、WebSocket 热更新、直接 serve 仓库文件
- `build`：静态打包，把 `CAD_DIR` 下所有 CAD 资产一起复制进 `dist/`

---

## E. skills/cad 里的脚本分别负责什么

```
skills/cad/scripts/
├── gen_step_part/          # 入口：生成单零件 STEP + GLB + topology
│   ├── cli.py              # 命令行参数解析
│   └── __main__.py         # python -m 入口
├── gen_step_assembly/      # 入口：生成装配体 STEP + GLB + topology
├── gen_dxf/                # 入口：生成 DXF 平面图
├── cadref/                 # 入口：解析/查询 @cad[...] refs
│   ├── cli.py（10KB）      # inspect / planes / diff 子命令
│   ├── analysis.py（16KB） # 几何分析（面积、法向量、包围盒）
│   ├── inspect.py（18KB）  # 拓扑检查、facts 输出
│   ├── lookup.py（9KB）    # ref 解析 → 拓扑条目查找
│   └── syntax.py（5KB）    # @cad[...] 语法解析器
├── snapshot/               # 入口：渲染 PNG 截图
│   └── cli.py（34KB）      # 等距/平行/透视视图渲染
└── common/                 # 所有脚本共享的核心库
    ├── generation.py（40KB）    # 主生成流程（执行器 + 导出协调）
    ├── step_scene.py（72KB）    # STEP 解析 + 拓扑编号（最重要的文件）
    ├── assembly_composition.py（48KB）  # 装配体组合
    ├── assembly_spec.py（16KB） # 装配体规范校验
    ├── catalog.py（22KB）       # 元数据目录
    ├── metadata.py（17KB）      # STEP 元数据
    ├── dxf.py（13KB）           # DXF 生成工具
    ├── glb.py                   # GLB 导出
    ├── stl.py                   # STL 导出
    ├── render.py                # 渲染工具
    └── validators.py            # 几何验证
```

> `step_scene.py` 是整个 Python 侧最关键的文件——它把 OCP/STEP 的几何对象转化为带编号的面/边/角拓扑结构，供 cadref 查询和 viewer picking 使用。

---

## F. models/ 文件夹在整个系统中扮演什么角色

`models/` 是**整个系统的共享数据层**，连接 Python 生成侧和 React 浏览侧。

```
models/
└── my_part/
    ├── source.py              ← 源文件（AI/用户编写，git 追踪）
    ├── part.step              ← 生成物（STEP 格式，git 追踪）
    ├── part.stl               ← 可选生成物
    ├── part.dxf               ← 可选生成物
    └── .part.step/            ← 隐藏的 viewer 消费目录（git 追踪）
        ├── model.glb          ← Three.js 加载的网格
        ├── topology.json      ← 面/边/角拓扑 + 装配树
        └── topology.bin       ← 二进制拓扑加速查找
```

**角色总结：**
- Python 脚本**写入** `models/`
- Viewer（Vite）**读取** `models/`，扫描条目、serve 文件
- 两侧通过**文件系统**解耦，没有 API、没有数据库
- 整个 `models/` 目录（含隐藏 `.step/` 目录）一起 git commit

---

## G. 文件分类：源文件 vs 生成物 vs 不可手动修改

| 类型 | 文件/目录 | 说明 |
|------|-----------|------|
| ✅ **源文件（可编辑）** | `models/**/source.py` | CAD 生成器，包含 `gen_step()` |
| ✅ **源文件（可编辑）** | `viewer/components/`, `viewer/lib/` | Viewer React 代码 |
| ✅ **源文件（可编辑）** | `skills/cad/scripts/` | Python CLI 工具 |
| ✅ **源文件（可编辑）** | `viewer/vite.config.mjs` | Vite 配置 |
| ⚠️ **生成物（git 追踪，但不要手改）** | `models/**/*.step` / `.stl` / `.dxf` | 从 Python 生成器生成 |
| ⚠️ **生成物（git 追踪，但不要手改）** | `models/**/.*.step/model.glb` | STEP → GLB 转换产物 |
| ⚠️ **生成物（git 追踪，但不要手改）** | `models/**/.*.step/topology.json/.bin` | 拓扑数据 |
| ❌ **不可手改，且通常不 git 追踪** | `viewer/dist/` | 生产构建输出 |
| ❌ **不可手改，且不 git 追踪** | `viewer/node_modules/` | npm 依赖 |
| ❌ **不可手改，且不 git 追踪** | `.venv/` | Python venv |
| ❌ **不可手改** | `/tmp/cad-renders/` | snapshot 临时审查图（不入 models/） |

---

## H. 做一个更小的类似平台最少需要保留哪些模块

**最小可行版本（文本 → 生成 STEP → 浏览器看 GLB）只需要：**

### Python 侧（必须）
- `build123d` + `OCP` — 几何内核
- `common/generation.py` 的核心路径（执行 `gen_step()` → 写 STEP → 写 GLB）
- `common/step_scene.py` 的基础部分（STEP → GLB 转换，可裁剪拓扑编号部分）
- `common/glb.py` — GLB 导出

### 前端侧（必须）
- `viewer/lib/cadDirectoryScanner.mjs` — 扫描目录
- `viewer/vite.config.mjs` 的 `cadCatalogPlugin` — dev server + HMR
- `components/CadViewer.js` 核心（Three.js GLB 加载 + OrbitControls）
- React + Three.js + Vite

### 最小数据流
```
source.py → gen_step() → .step → GLB → viewer 扫描 → 浏览器加载
```

**约 4-5 个 Python 文件 + 2-3 个前端文件就能跑通核心链路。**

---

## I. 可以优先删掉的功能

| 功能 | 涉及文件 | 删除风险 |
|------|----------|----------|
| **URDF 机器人描述** | `skills/urdf/` + `viewer/lib/urdf/` + `components/` URDF 视图 | 极低——完全独立，删了不影响 STEP/GLB 流程 |
| **DXF 平面图** | `skills/cad/scripts/gen_dxf/` + `viewer/lib/dxf/` + `components/DxfViewer.js` | 低——独立子流程 |
| **高级 @cad[...] refs 系统** | `skills/cad/scripts/cadref/`（含 analysis/inspect/lookup） + `viewer/lib/cadRefs.js` + picking hooks | 中——删后无法做几何感知编辑，但浏览不受影响 |
| **Topology / Picking（选面/边/角）** | `common/step_scene.py` 拓扑部分 + `viewer/lib/selectors/` + `topology.json/.bin` 生成 | 中——删后不能拾取，但 GLB 加载/旋转仍可用 |
| **Snapshot 截图** | `skills/cad/scripts/snapshot/` | 低——纯 AI 验证工具，不影响浏览器流程 |
| **装配体支持** | `common/assembly_*.py` + `viewer/lib/assembly/` | 中——如只做单零件可删 |
| **STL 导出** | `common/stl.py` + `gen_step_part` 中 `export_stl` 路径 | 低 |
| **LocalStorage 工作台持久化** | `viewer/lib/workbench/persistence.js` | 低——刷新页面会丢失选中状态，但功能不受影响 |
| **`build:app` / `test:node` 验证脚本** | `viewer/scripts/` + 所有 `.test.js` | 无——纯开发质量工具 |

---

## 总结图

```
┌──────────────────────────────────────────────────────┐
│                   用户 / AI 代理                       │
│  "给我生成一个 M8 螺栓"                                 │
└────────────────────┬─────────────────────────────────┘
                     │ 编写/修改
                     ▼
┌──────────────────────────────────────────────────────┐
│           models/bolt/source.py                       │
│           def gen_step(): ...  (build123d)            │
└────────────────────┬─────────────────────────────────┘
                     │ python skills/cad/scripts/gen_step_part
                     ▼
┌──────────────────────────────────────────────────────┐
│  Python 生成管线 (OCP / build123d)                     │
│  → bolt.step  → .bolt.step/model.glb                  │
│              → .bolt.step/topology.json               │
└────────────────────┬─────────────────────────────────┘
                     │ 文件系统写入 models/
                     ▼
┌──────────────────────────────────────────────────────┐
│  Vite dev server (port 4178)                          │
│  cadCatalogPlugin 检测文件变化                          │
│  → WS 推送 cad-catalog:changed                        │
└────────────────────┬─────────────────────────────────┘
                     │ HTTP / WS
                     ▼
┌──────────────────────────────────────────────────────┐
│  CAD Explorer (React + Three.js)                      │
│  → 加载 GLB → 渲染 → 支持 Picking → 复制 @cad[...]    │
└──────────────────────────────────────────────────────┘
```
