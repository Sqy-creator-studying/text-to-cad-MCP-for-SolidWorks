<div align="center">

<img src="skills/cad/assets/text-to-cad-demo.gif" alt="Demo of the text-to-cad harness generating and previewing CAD geometry" width="100%">

<br>

# ⚙️ Text-to-CAD: 完整的AI驱动CAD建模平台 ⚙️

**首个无需CAD软件的AI建模平台 + 可选的专业CAD集成**

自然语言 → 3D模型（5秒内，浏览器直接查看）→ 可选导入专业CAD软件继续编辑

[![GitHub stars](https://img.shields.io/github/stars/Sqy-creator-studying/text-to-cad?style=for-the-badge&logo=github&label=Stars)](https://github.com/Sqy-creator-studying/text-to-cad/stargazers)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](requirements-cad.txt)
[![CATIA](https://img.shields.io/badge/CATIA-V5%2FV6-FF6B35?style=for-the-badge)](cad_module/mcp_servers/catia_mcp.py)
[![SolidWorks](https://img.shields.io/badge/SolidWorks-2025-DA291C?style=for-the-badge)](mcp_servers/solidworks_mcp.py)
[![MCP](https://img.shields.io/badge/MCP-Server-6B46C1?style=for-the-badge)](README_CATIA_MCP.md)
[![build123d](https://img.shields.io/badge/build123d-CAD-00A676?style=for-the-badge)](https://github.com/gumyr/build123d)

[English](#english) | [中文](#chinese)

</div>

---

## 🎯 为什么选择这个项目？

### 与其他CAD自动化工具的核心区别

| 特性 | 本项目 | 其他MCP工具 | 传统CAD |
|------|--------|-------------|---------|
| **需要CAD软件** | ❌ 可选 | ✅ 必须 | ✅ 必须 |
| **浏览器直接查看** | ✅ 内置 | ❌ 无 | ❌ 无 |
| **5秒快速原型** | ✅ 是 | ❌ 慢 | ❌ 很慢 |
| **中文深度优化** | ✅ 完整 | ⚠️ 部分 | ⚠️ 基础 |
| **垂直领域模板** | ✅ 专业 | ⚠️ 通用 | ❌ 无 |
| **专业CAD集成** | ✅ 可选 | ✅ 是 | - |
| **教育资源** | ✅ 丰富 | ⚠️ 基础 | ⚠️ 有限 |

---

## <a name="chinese"></a>🚀 三层架构设计（独一无二）

```
┌─────────────────────────────────────────────────────────┐
│  第1层: Web快速原型（无需CAD软件）                       │
│  ├─ 自然语言输入（中文/英文）                           │
│  ├─ AI解析 + 代码生成                                   │
│  ├─ 5秒内生成3D模型                                     │
│  └─ 浏览器直接查看 + 交互                               │
└─────────────────────────────────────────────────────────┘
                         ↓ 满意？点击"在CAD中打开"
┌─────────────────────────────────────────────────────────┐
│  第2层: 专业CAD增强（MCP集成）                          │
│  ├─ 自动在CATIA/SolidWorks中重建                       │
│  ├─ 继续专业编辑和标注                                 │
│  └─ 生成工程图纸                                        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  第3层: 制造生产                                        │
│  └─ 导出 STEP/STL/DXF → 直接制造                       │
└─────────────────────────────────────────────────────────┘
```

### 💡 实际使用场景

#### 场景A: 产品设计师（快速迭代）
```
"我想看看电机支架的大概样子"
→ 打开网页输入描述
→ 5秒后看到3D模型
→ 调整参数，立即重新生成
→ ❌ 不需要等待CAD软件启动
→ ❌ 不需要学习复杂的CAD操作
```

#### 场景B: 机械工程师（专业制造）
```
"我需要精确的工程图纸"
→ 在Web上快速原型
→ 满意后点击"在CATIA中打开"
→ MCP自动在CATIA中重建模型
→ 添加工程标注和尺寸
→ 导出生产图纸
```

#### 场景C: 学生和教育（学习CAD）
```
→ 使用完整教程和演示脚本
→ 理解自然语言如何转换为CAD
→ 测试脚本验证连接
→ 丰富的中文文档支持
```

---

## 🎁 核心优势

### 1️⃣ **完整的独立系统**（其他MCP工具没有）

```python
# 你输入
"创建一个直径50mm、高度100mm的圆柱体"

# 系统处理（完全自动）
自然语言解析 → 生成Python代码 → 执行build123d → 导出STEP/STL/GLB

# 结果
✅ 浏览器中看到3D模型（无需CAD软件）
✅ 可以旋转、缩放、测量
✅ 导出文件直接制造
```

### 2️⃣ **可选的专业CAD集成**（双CAD支持）

**CATIA MCP服务器**（8个工具）
- `catia_new_part` - 创建新零件
- `catia_create_sketch` - 创建草图
- `catia_draw_circle` - 绘制圆（毫米）
- `catia_draw_rectangle` - 绘制矩形（毫米）
- `catia_pad` - 拉伸（毫米）
- `catia_pocket` - 挖槽/切除（毫米）
- `catia_update` - 更新零件
- `catia_fit_all` - 适配视图

📚 [CATIA完整文档](README_CATIA_MCP.md)

**SolidWorks MCP服务器**（13个工具）
- VBA宏生成器
- 中文/日文/德文平面名称自动识别
- SolidWorks 2025 完整验证

📚 [SolidWorks完整文档](README_MCP.md)

### 3️⃣ **垂直领域优化模板库**

专为特定行业设计的模板：

| 行业 | 模板 | 参数 |
|------|------|------|
| **无人机** | `drone_arm` | 机臂长度、减重孔、安装孔 |
| **能源** | `battery_pack` | 电芯数量、布局、外壳 |
| **电机** | `motor_mount` | 安装板、螺栓孔、分度圆 |
| **机械** | `bracket_simple` | L型支架、安装孔 |
| **通用** | `generic_plate` | 安装板、孔位 |
| **标准件** | `bushing`, `flange` | 轴套、法兰 |

### 4️⃣ **深度中文优化**

- ✅ 完整的中文自然语言处理
- ✅ 中文技术文档和教程
- ✅ 中文参数别名（例如："外径"、"孔距圆"、"厚度"）
- ✅ 中文错误提示和帮助
- ✅ 中文模板关键词识别

```python
# 支持中文输入
"创建一个法兰盘：外径80mm，厚度10mm，中心孔直径20mm，分度圆60mm，4个M6螺栓孔"
```

### 5️⃣ **完整的教育资源**

- 📖 [CATIA MCP验证报告](CATIA_MCP_验证报告.md) - 完整的测试和验证
- 🧪 [连接测试脚本](test_catia_connection.py) - 验证CAD连接
- 🎯 [演示脚本](catia_cylinder_demo.py) - 自动创建圆柱体
- 📚 技术文档和故障排除指南
- 🎓 适合教学和学习

---

## 🆕 CATIA集成（NEW）

**首个开源的CATIA + Claude Code集成方案**

### 特点

- ✅ **CATIA V5/V6支持** - 完整的COM自动化
- ✅ **单位统一** - 全部使用毫米（CATIA原生单位）
- ✅ **实时预览** - 在CATIA中看到建模过程
- ✅ **完整验证** - 包含测试和演示脚本

### 快速开始 - CATIA

```bash
# 1. 安装依赖
pip install pywin32 mcp

# 2. 打开CATIA（必须运行）

# 3. 配置Claude Code (~/.claude/mcp.json)
{
  "mcpServers": {
    "catia": {
      "command": "python",
      "args": ["完整路径/cad_module/mcp_servers/catia_mcp.py"]
    }
  }
}

# 4. 重启Claude Code

# 5. 测试连接
python test_catia_connection.py

# 6. 运行演示（创建圆柱体）
python catia_cylinder_demo.py
```

### 使用示例

```
你: "在CATIA中创建一个直径50mm、高度100mm的圆柱体"

Claude会自动执行:
1. catia_new_part()              # 创建新零件
2. catia_create_sketch("xy")     # 在XY平面创建草图
3. catia_draw_circle(25)         # 绘制半径25mm的圆
4. catia_pad(100)                # 拉伸100mm
5. catia_fit_all()               # 适配视图

结果: 在CATIA中看到完整的圆柱体模型！
```

📚 **完整文档**: [CATIA MCP服务器指南](README_CATIA_MCP.md)

---

## 🔧 SolidWorks集成（Enhanced）

### 技术突破

| 挑战 | 解决方案 |
|------|---------|
| Python `None` → COM `VT_EMPTY` 类型不匹配 | 使用 `InvokeTypes` 显式传递 `VT_DISPATCH` 空指针 |
| SW 2025 API参数数量与文档不符 | 实验验证: `FeatureExtrusion2`=23参数, `FeatureCut`=20参数 |
| 中文SolidWorks平面名称本地化 | 自动扫描特征树，建立英文→本地化映射 |

### MCP工具

- `sw_get_version` - 获取SolidWorks版本
- `sw_new_part` - 创建新零件
- `sw_select_plane` - 选择参考平面（自动映射中文名称）
- `sw_create_sketch` - 创建2D草图
- `sw_draw_circle` - 绘制圆（米）
- `sw_draw_center_rect` - 绘制中心矩形
- `sw_extrude` - 盲孔拉伸（23参数，SW 2025）
- `sw_cut_extrude` - 切除拉伸（20参数，SW 2025）
- `sw_select_face` - 选择面
- `sw_clear_selection` - 清除选择
- `sw_zoom_fit` - 缩放适配
- `sw_get_plane_names` - 显示检测到的平面名称
- `sw_list_features` - 列出所有特征

### VBA宏导出

```python
from cad_module.exporters.sw_macro import generate_sw_macro

macro = generate_sw_macro('motor_mount', {
    'plate_diameter': 52,          # mm
    'thickness': 5,
    'center_hole_diameter': 12,
    'bolt_circle_diameter': 32,
    'bolt_hole_diameter': 3.2,
    'bolt_count': 4,
})

with open('MotorMount.bas', 'w', encoding='utf-8') as f:
    f.write(macro)
# 导入SW: Alt+F11 → 文件 → 导入文件 → 选择.bas → F5
```

**支持的模板**: `box`, `cylinder`, `generic_plate`, `motor_mount`, `bracket_simple`, `bushing`, `flange`

**支持的特征**: `hole`, `circular_user_hole_pattern`, `linear_hole_pattern`, `rectangular_pocket`, `obround_slot`, `fillet`, `chamfer`

📚 **完整文档**: [SolidWorks MCP服务器指南](README_MCP.md)

---

## <a name="english"></a>🌍 English

### What Makes This Project Unique?

**Text-to-CAD is the ONLY platform that offers:**

1. **CAD-software-free modeling** - Generate and view 3D models in your browser
2. **Optional professional CAD integration** - Export to CATIA/SolidWorks when needed
3. **Three-tier architecture** - Web prototype → Professional CAD → Manufacturing
4. **Chinese language optimization** - Deep support for Chinese users
5. **Vertical domain templates** - Specialized for drones, motors, batteries
6. **Complete educational resources** - Tutorials, tests, demos

### Quick Start - Web Platform

```bash
# Clone repository
git clone https://github.com/Sqy-creator-studying/text-to-cad.git
cd text-to-cad

# Install Python dependencies
python3.11 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements-cad.txt

# Install viewer dependencies
cd viewer
npm install

# Run local CAD Explorer
npm run dev
```

Then open [http://localhost:4178](http://localhost:4178)

### Features

- **Generate** - Create source-controlled CAD models with AI agents
- **Export** - Produce STEP, STL, DXF, GLB, topology data, and URDF
- **Browse** - Inspect geometry in local CAD Explorer viewer
- **Reference** - Use stable `@cad[...]` references for precise edits
- **Review** - Render quick snapshots for iteration
- **Reproduce** - Edit source files, regenerate targets
- **Local** - Run completely locally with no backend

---

## 📊 与其他项目对比

### 现有的CAD MCP项目

我们尊重并推荐以下优秀项目（按字母排序）：

**CATIA MCP服务器:**
- [daiemon12/catia-v5-mcp-server](https://github.com/daiemon12/catia-v5-mcp-server) - 首个CATIA V5 MCP服务器
- [scanzy/catia-mcp](https://github.com/scanzy/catia-mcp) - CATIA基础操作

**SolidWorks MCP服务器:**
- [alisamsam/solidworks-mcp](https://github.com/alisamsam/solidworks-mcp) - 22工具，生产级
- [eyfel/mcp-server-solidworks](https://github.com/eyfel/mcp-server-solidworks) - 通用AI桥接
- [tylerstoltz/SW_MCP](https://github.com/tylerstoltz/SW_MCP) - C# SDK实现

### 本项目的差异化

| 维度 | 本项目 | 其他MCP项目 |
|------|--------|-------------|
| **定位** | 完整的Text-to-CAD平台 | CAD软件控制工具 |
| **核心价值** | 无需CAD软件即可建模 | 自动化CAD工作流 |
| **目标用户** | 设计师、学生、快速原型 | 专业CAD工程师 |
| **使用场景** | Web原型 + 可选CAD | 必须有CAD软件 |
| **中文支持** | 深度优化 | 基础/部分 |
| **教育资源** | 丰富完整 | 基础文档 |

**我们的独特价值**: 提供从快速原型到专业制造的完整链路，而不仅仅是CAD软件的遥控器。

---

## 🧰 技术栈

- **前端**: React + Three.js + Vite
- **后端**: Python 3.11+ + Flask
- **CAD引擎**: build123d + OCP (OpenCascade)
- **CAD集成**: COM自动化 (pywin32)
- **协议**: Model Context Protocol (MCP)
- **导出格式**: STEP, STL, DXF, GLB, URDF

---

## 🔁 工作流程

1. **描述** - 用自然语言描述你想要的零件/组件
2. **生成** - AI自动生成CAD源代码
3. **预览** - 在Web查看器中查看3D模型
4. **调整** - 修改参数，实时重新生成
5. **导出** - 导出STEP/STL文件或导入CAD软件
6. **制造** - 直接用于3D打印或CNC加工

---

## 📦 发布包

独立的MCP工具包可供下载：

- 📥 [cad-mcp-servers-v1.0.zip](../../releases) - 包含CATIA和SolidWorks MCP服务器
- 📖 [MCP工具包README](MCP_PACKAGE_README.md) - 独立安装指南
- 🧪 [测试和演示脚本](test_catia_connection.py) - 验证工具

---

## 🤝 贡献

欢迎贡献！你可以：

- 🐛 报告bug
- 💡 建议新功能
- 🔧 提交pull request
- 📚 改进文档
- 🌐 添加更多CAD软件支持

---

## 📄 许可证

本项目采用 **Apache License 2.0** 许可 - 详见 [LICENSE](LICENSE)

**Apache 2.0 意味着:**

- ✅ 自由使用、修改、分发，商业用途也可以
- ✅ 明确授予专利权，不用担心专利诉讼
- ✅ 修改后的代码可以闭源，不需要强制开源
- ⚠️ 分发时必须保留版权声明和LICENSE文件
- ⚠️ 修改过的文件需要标注变更

部分代码衍生自 [text-to-cad](https://github.com/earthtojake/text-to-cad) by Thompson Labs，原为MIT许可。原始MIT声明保留在 [LICENSE](LICENSE) 中。

---

## 🙏 致谢

- 基于 [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) 项目
- 使用 [build123d](https://github.com/gumyr/build123d) CAD引擎
- 感谢 [Anthropic](https://www.anthropic.com/) 的Model Context Protocol
- 感谢所有贡献者和用户

---

<div align="center">

**作者**: [Sqy-creator-studying](https://github.com/Sqy-creator-studying)  
**基于**: [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)  
**版权**: © 2026 Sqy-creator-studying

⭐ **如果这个项目对你有帮助，请给个星标！** ⭐

[报告问题](https://github.com/Sqy-creator-studying/text-to-cad-MCP-for-SolidWorks/issues) · [功能请求](https://github.com/Sqy-creator-studying/text-to-cad-MCP-for-SolidWorks/issues) · [讨论](https://github.com/Sqy-creator-studying/text-to-cad-MCP-for-SolidWorks/discussions)

</div>
