# EmbodiedCAD 软件使用指南

本文面向初级操作者，目标是让第一次接触本项目的用户能够完成软件启动、项目创建、模型预览、参数修改、诊断检查和 CAD 文件导出。本文默认你已经拿到了 EmbodiedCAD 压缩包，并已经把它解压到电脑上的某个文件夹。

## 1. 软件是做什么的

EmbodiedCAD 是一个面向无人机、机械臂和具身智能设备的轻量级 CAD 设计工作台。它不是传统的大型 CAD 软件，而是把参数化模型、组件化装配、三维预览、工程诊断和导出流程集中在一个本地网页工作台中。

用户可以通过界面创建项目，选择无人机、机械臂或单个 CAD 零件工作区，修改部件参数，重新生成模型，并导出 STEP、STL、GLB 和 manifest 文件。

本项目中有两个容易混淆的界面：

- EmbodiedCAD Platform：主要操作平台，用于无人机、机械臂、CAD 组件项目设计，默认地址是 `http://127.0.0.1:5173`。
- CAD Explorer：通用 CAD 浏览器，用于查看 `models/` 下的 STEP、STL、DXF、URDF 文件，默认地址是 `http://127.0.0.1:4178`。

如果你是进行 EmbodiedCAD 项目演示、创建无人机或机械臂方案，主要使用 EmbodiedCAD Platform。

## 2. 解压后的最快启动方式

如果你只是想运行软件，不想手动输入命令，按下面步骤操作：

1. 解压压缩包。
2. 打开解压后的文件夹。
3. 双击 `启动_EmbodiedCAD.bat`。如果中文文件名在对方电脑上显示异常，也可以双击 `start_embodiedcad.bat`。
4. 首次运行时，脚本会自动创建 `.venv`、安装 Python 依赖和前端依赖，这一步可能需要几分钟。
5. 等待浏览器自动打开 `http://127.0.0.1:5173`。
6. 页面打开后，不要关闭自动弹出的 API 服务窗口和前端服务窗口。

如果 Windows 提示脚本被拦截，可以右键 `start_embodiedcad.ps1`，选择“使用 PowerShell 运行”。如果仍然无法运行，请参考下面的手动启动方式。

## 3. 使用前准备

### 3.1 需要的软件环境

电脑需要安装：

- Python 3.11 或兼容版本
- Node.js 和 npm
- 浏览器，推荐 Chrome 或 Edge

项目已经包含本地 Python 虚拟环境时，可以优先使用项目里的 `.venv`。

### 3.2 手动安装 Python 依赖

在 PowerShell 中进入解压后的文件夹。例如，如果你把压缩包解压到了桌面，可以进入类似这样的目录：

```powershell
cd "$env:USERPROFILE\Desktop\EmbodiedCAD_可运行版"
```

安装 CAD 和 API 依赖：

```powershell
.\.venv\Scripts\python -m pip install -r requirements-cad.txt
.\.venv\Scripts\python -m pip install -r cad_module\requirements-api.txt
```

如果 `.venv` 不存在，可以先创建虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-cad.txt
.\.venv\Scripts\python -m pip install -r cad_module\requirements-api.txt
```

### 3.3 手动安装前端依赖

进入 EmbodiedCAD 前端目录：

```powershell
cd "解压后的文件夹\cad_module\web_viewer"
npm install
```

安装完成后回到项目根目录也可以：

```powershell
cd "解压后的文件夹"
```

## 4. 手动启动软件

EmbodiedCAD 需要同时启动 API 服务和前端页面。建议打开两个 PowerShell 窗口。

### 4.1 启动 API 服务

第一个 PowerShell 窗口执行：

```powershell
cd "解压后的文件夹"
.\.venv\Scripts\python -m cad_module.server
```

正常启动后，API 服务地址一般是：

```text
http://127.0.0.1:8000
```

不要关闭这个窗口。关闭后，前端页面将无法创建项目、保存项目或生成模型。

### 4.2 启动前端页面

第二个 PowerShell 窗口执行：

```powershell
cd "解压后的文件夹\cad_module\web_viewer"
npm run dev
```

正常启动后，浏览器打开：

```text
http://127.0.0.1:5173
```

看到 EmbodiedCAD Platform 页面后，就可以开始操作。

## 5. 页面区域说明

EmbodiedCAD 的主界面是三栏工程工作台：

- 顶部栏：显示软件名称、当前项目状态、主题切换、构建或演示相关入口。
- 左侧栏：用于选择工作区、创建项目、加载示例项目、查看组件库和装配树。
- 中间区域：3D 工作区，用来查看生成的 GLB 模型，可以旋转、缩放、观察整体结构。
- 右侧栏：Inspector 面板，包含 Edit、Analyze、Guidance、Export、Assistant 等标签页。

常见标签页含义：

- Edit：编辑当前选中组件的参数、位置或连接关系。
- Analyze：查看检查结果、诊断信息和工程问题。
- Guidance：查看设计目标、质量、续航、推力、机械臂 reach 等工程建议。
- Export：查看和下载生成的 STEP、STL、GLB、manifest 等文件。
- Assistant：输入自然语言设计意图，先预览操作，再确认应用。

## 6. 推荐入门流程：加载示例项目

第一次使用时，建议先不要从空项目开始，而是加载示例项目。

### 5.1 加载无人机示例

1. 打开 `http://127.0.0.1:5173`。
2. 在首页选择 Drone Workspace。
3. 点击 Load Demo Drone。
4. 等待页面提示模型加载完成。
5. 查看中间 3D 区域是否出现无人机结构。
6. 在左侧 Assembly Tree 中点击不同组件，例如 body、battery、arm、motor mount、payload。
7. 观察右侧 Edit 面板中参数随选中组件变化。

这个示例适合演示项目的核心能力：组件化无人机、三维预览、参数编辑、诊断、导出。

### 5.2 加载机械臂示例

1. 在首页选择 Robot Arm Workspace。
2. 点击 Load Demo Robot Arm。
3. 等待 3D 模型生成。
4. 在装配树中查看 base、joint、link、gripper 等组件。
5. 切换到 Guidance 面板，查看关节数量、连杆数量、最大 reach 和载荷相关信息。

这个示例适合展示 EmbodiedCAD 对具身智能设备和机械结构的支持。

### 5.3 加载单零件示例

1. 在首页选择 CAD Component Workspace。
2. 点击 Load Demo CAD Component。
3. 查看生成的单个参数化零件，例如 energy module shell 或 motor mount。
4. 在 Edit 面板中修改尺寸、壁厚、孔径、通风口数量等参数。
5. 点击 Rebuild 或 Build 后查看模型变化。

这个示例适合学习单个 CAD 零件的参数化建模流程。

## 7. 创建新项目

### 6.1 新建无人机项目

1. 打开 EmbodiedCAD 首页。
2. 选择 Drone Workspace。
3. 点击 New Drone Project。
4. 系统创建空的无人机项目。
5. 可以使用初始化按钮或布局预设生成基础四旋翼结构。
6. 添加或调整组件，例如机身、电池、机臂、电机座、螺旋桨、载荷和起落架。
7. 点击 Build 或 Rebuild 生成 CAD 输出。

适合场景：设计无人机概念方案，比较紧凑型、续航型、载荷型布局。

### 6.2 新建机械臂项目

1. 选择 Robot Arm Workspace。
2. 点击 New Robot Arm Project。
3. 使用 3-DOF 初始化功能生成基础机械臂。
4. 查看组件树中的 base、revolute joint、link、end effector mount、gripper。
5. 修改连杆长度、关节位置或末端执行器相关参数。
6. 点击 Build 或 Rebuild 更新模型。
7. 在 Guidance 中查看 reach、joint/link count、payload capacity 等指标。

适合场景：快速建立桌面级机械臂概念结构。

### 6.3 新建 CAD 组件项目

1. 选择 CAD Component Workspace。
2. 点击 New CAD Component。
3. 选择组件模板，例如 box、cylinder、battery_pack、motor_mount、energy_module_shell、generic_plate、bracket_simple。
4. 在 Edit 面板调整数值参数。
5. 点击 Rebuild 重新生成模型。
6. 在 Export 面板下载结果。

适合场景：快速生成可复用的零件、壳体、支架、安装板等。

## 8. 修改模型参数

模型修改一般按下面流程进行：

1. 在左侧 Assembly Tree 中选择一个组件。
2. 在中间 3D 视图中确认选中对象。
3. 打开右侧 Edit 面板。
4. 修改尺寸、位置、角色、父组件、锚点或模板参数。
5. 修改后项目通常会显示 Rebuild needed。
6. 点击 Build 或 Rebuild。
7. 等待模型重新生成。
8. 检查 3D 预览是否符合预期。

初级操作者需要注意：

- 数值单位通常是 mm 或 g，具体看界面字段。
- 修改尺寸后一定要重新构建，否则 3D 模型和导出文件可能还是旧版本。
- 如果组件位置异常，优先检查 parent、anchor、position 这类连接和放置参数。
- 如果模型看不见，先确认是否已经 Build，再检查 3D 视图是否缩放过远。

## 9. 使用设计目标和预设

无人机工作区支持一些设计目标和配置预设，用来快速切换方案风格。

常见设计目标：

- Compact：偏小型、紧凑布局。
- Balanced：默认平衡方案。
- Endurance：偏长续航，通常会使用更大的电池或更适合续航的螺旋桨配置。
- Payload：偏载荷能力，适合挂载传感器或较重任务载荷。

一般操作方式：

1. 打开 Drone Workspace 项目。
2. 在右侧 Guidance 或相关设计面板中选择目标。
3. 点击 Apply。
4. 系统更新相关组件参数或配置。
5. 点击 Rebuild。
6. 查看质量、续航、推重比、载荷余量等指标变化。

## 10. 查看诊断和修复建议

诊断功能用于发现设计中的潜在问题，例如组件未连接、布局冲突、推进配置不合理、电池配置不匹配等。

操作步骤：

1. 打开右侧 Analyze 面板。
2. 点击检查或刷新诊断。
3. 阅读每条诊断结果。
4. 如果界面提供 Fix 或 Batch Fix，可以先选择安全修复项。
5. 应用修复后重新 Build。
6. 再次查看诊断结果是否改善。

建议初级操作者优先使用系统提供的安全修复，不要一次性做过多手动参数变化。每次修改后重新构建并检查，可以更容易发现问题来源。

## 11. 使用 Assistant

Assistant 用于把自然语言请求转换为受控操作。它不是直接执行任意代码，而是先生成可检查的操作预览。

推荐流程：

1. 打开右侧 Assistant 面板。
2. 输入简短明确的需求，例如：
   - `make this an endurance drone`
   - `make the drone more compact`
   - `add payload capacity`
   - `explain diagnostics`
3. 点击 Preview。
4. 查看系统列出的操作、风险等级和说明。
5. 如果确认无误，再点击 Apply。
6. 应用后点击 Build 或 Rebuild。
7. 查看 3D 模型和 Guidance 指标是否变化。

注意事项：

- Assistant 应先 Preview，再 Apply。
- 不要把复杂需求一次性写得太长。
- 如果结果不符合预期，可以撤回到之前保存的项目，或重新调整参数。
- 当前 Assistant 是安全受控的操作映射，不是自由生成和执行 Python 代码。

## 12. 导入参考模型

参考模型通常是外部 GLB 或 GLTF，用来和当前生成模型做对比。它不是可编辑 CAD 组件。

操作步骤：

1. 先创建或打开一个项目。
2. 找到 Reference Model 或相关导入区域。
3. 选择本地 GLB/GLTF 文件，或输入模型 URL。
4. 导入后，在 3D 视图中查看参考模型叠加效果。
5. 调整 opacity、visible、lock 等显示选项。
6. 可以使用 Snap Origin 把参考模型移动到原点。
7. 可以使用 Scale to Generated BBox 让参考模型按生成模型包围盒缩放。
8. 需要说明部位时，可以添加 body、arm、motor、propeller、battery、payload、landing_gear 等手动标签。

注意：参考模型主要用于对齐、比较和标注，不会自动变成可编辑组件。

## 13. 构建和导出

### 13.1 什么时候需要 Build 或 Rebuild

以下情况需要重新构建：

- 新建项目后第一次生成模型。
- 修改了组件尺寸或参数。
- 添加、删除或复制组件。
- 应用了设计目标或布局预设。
- 使用 Assistant 应用了操作。
- 诊断修复后需要更新结果。

构建会生成或刷新：

- STEP：工程 CAD 交换格式。
- STL：常见 3D 打印或网格格式。
- GLB：网页 3D 预览格式。
- manifest.json：记录项目、组件、参数、导出文件和工程摘要。

### 13.2 导出文件

操作步骤：

1. 确认项目已经 Build 或 Rebuild 成功。
2. 打开右侧 Export 面板。
3. 查看可下载文件列表。
4. 根据用途下载：
   - 给 CAD 软件或工程交换使用：下载 STEP。
   - 给 3D 打印或网格查看使用：下载 STL。
   - 给网页展示或轻量预览使用：下载 GLB。
   - 给项目记录、复现或评审使用：下载 manifest。

导出的文件通常保存在 `cad_module/outputs/` 或项目配置的输出目录中。

## 14. 保存、导入和继续编辑

### 14.1 保存项目

项目数据会保存在本地 JSON 中，通常位于：

```text
cad_module/projects/
```

操作时可以点击 Save Project 或相关保存按钮，确保当前组件参数、选择状态、参考模型信息和构建结果被记录。

### 14.2 导出项目 JSON

如果需要把项目交给别人继续编辑，可以导出项目 JSON。对方导入后可以恢复项目配置，再重新构建 CAD 输出。

### 14.3 导入项目 JSON

1. 点击 Import Project 或选择项目 JSON。
2. 等待系统导入。
3. 检查项目名称、组件树和参数是否正确。
4. 点击 Build 或 Rebuild 生成本机输出文件。

## 15. 演示建议流程

如果要向老师、评委或同学演示，推荐使用下面的顺序：

1. 打开 EmbodiedCAD Platform。
2. 点击 Load Demo Drone。
3. 展示三栏工作台：左侧组件库和装配树，中间 3D 预览，右侧 Inspector。
4. 点击无人机的 battery 或 payload 组件。
5. 修改一个简单参数，例如载荷大小或电池配置。
6. 展示 Rebuild needed 状态。
7. 点击 Rebuild，等待模型刷新。
8. 打开 Guidance，展示质量、续航、推力或载荷指标。
9. 打开 Analyze，展示诊断和 Fix。
10. 打开 Assistant，输入 `make this an endurance drone`，先 Preview，再 Apply。
11. 打开 Export，展示 STEP、STL、GLB、manifest 导出。

这个流程能够完整体现“文本意图 -> 参数化设计 -> 三维预览 -> 工程检查 -> 迭代修改 -> 导出”的闭环。

## 16. 常见问题

### 15.1 页面打不开

检查前端是否启动：

```powershell
cd "解压后的文件夹\cad_module\web_viewer"
npm run dev
```

然后打开：

```text
http://127.0.0.1:5173
```

### 15.2 页面打开了，但创建项目失败

通常是 API 服务没有启动。打开另一个 PowerShell：

```powershell
cd "解压后的文件夹"
.\.venv\Scripts\python -m cad_module.server
```

确认 `http://127.0.0.1:8000` 可用。

### 15.3 模型没有显示

可以按顺序检查：

1. 是否已经点击 Build 或 Rebuild。
2. API 服务是否仍在运行。
3. 页面右上或状态栏是否有错误提示。
4. 浏览器是否缩放到模型之外，可以尝试刷新页面或重新加载项目。
5. 是否导出的 GLB 文件生成失败。

### 15.4 修改参数后模型没变化

大多数情况是还没有重新构建。修改参数后请点击 Rebuild。右侧 Export 中的文件也需要重新构建后才是最新版本。

### 15.5 Assistant 没有效果

检查是否完成了 Preview 和 Apply 两步。Assistant 只是生成受控操作，Apply 后通常还需要 Rebuild 才能看到 CAD 输出变化。

### 15.6 端口被占用

如果 `8000` 或 `5173` 被占用，可以关闭之前的终端窗口，或检查是否已经有服务在运行。初级操作者建议优先关闭旧窗口后重新启动。

## 17. 附：通用 CAD Explorer 的使用

如果需要查看根项目 `models/` 下的 STEP、STL、DXF 或 URDF 文件，可以启动 CAD Explorer：

```powershell
cd "解压后的文件夹"
npm --prefix viewer run dev:ensure
```

打开：

```text
http://127.0.0.1:4178/?dir=models
```

CAD Explorer 主要用于浏览已有 CAD 文件，并支持复制 `@cad[...]` 引用，方便后续让 coding agent 精确修改某个面、边或组件。它不是 EmbodiedCAD Platform 的主要项目编辑界面。

## 18. 初级操作者记忆版流程

最简单的使用顺序可以记为：

```text
启动 API -> 启动前端 -> 加载 Demo 或新建项目 -> 选组件 -> 改参数 -> Rebuild -> 看诊断 -> 导出文件
```

只要记住“修改后要 Rebuild，导出前要确认 Build 成功”，就能避免大多数初学者常见问题。
