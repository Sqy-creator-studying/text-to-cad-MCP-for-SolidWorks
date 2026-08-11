# CAD MCP Servers Package

**让Claude通过自然语言直接控制CATIA和SolidWorks！**

## 📦 这是什么？

这是一个独立的MCP服务器包，可以让Claude Code或Claude Desktop通过自然语言直接控制你的CAD软件创建3D模型。

## 🎯 快速体验

```
你: "在CATIA中创建一个直径50mm、高度100mm的圆柱体"
Claude: [自动控制CATIA创建模型] ✨
```

## 📁 包含内容

```
MCP服务器/
├── cad_module/mcp_servers/
│   └── catia_mcp.py           # CATIA MCP服务器
├── mcp_servers/
│   └── solidworks_mcp.py      # SolidWorks MCP服务器
├── test_catia_connection.py   # CATIA连接测试
├── catia_cylinder_demo.py     # CATIA演示脚本
├── README_CATIA_MCP.md        # CATIA完整文档
└── README_MCP.md              # SolidWorks完整文档
```

## 🚀 3步安装

### 1. 安装依赖
```bash
pip install pywin32 mcp
```

### 2. 配置MCP服务器

创建或编辑 `~/.claude/mcp.json`：

**CATIA配置：**
```json
{
  "mcpServers": {
    "catia": {
      "command": "python",
      "args": ["完整路径/cad_module/mcp_servers/catia_mcp.py"]
    }
  }
}
```

**SolidWorks配置：**
```json
{
  "mcpServers": {
    "solidworks": {
      "command": "python",
      "args": ["完整路径/mcp_servers/solidworks_mcp.py"]
    }
  }
}
```

**两者都用：**
```json
{
  "mcpServers": {
    "catia": {
      "command": "python",
      "args": ["完整路径/cad_module/mcp_servers/catia_mcp.py"]
    },
    "solidworks": {
      "command": "python",
      "args": ["完整路径/mcp_servers/solidworks_mcp.py"]
    }
  }
}
```

### 3. 测试连接

**测试CATIA：**
```bash
python test_catia_connection.py
```

## ✅ 验证安装

1. 打开CATIA或SolidWorks
2. 重启Claude Code
3. 对Claude说："在CATIA中创建一个圆柱体"
4. 看模型自动生成！

## 🛠️ 可用工具

### CATIA工具（8个）

| 工具 | 功能 | 单位 |
|------|------|------|
| catia_new_part | 创建新零件 | - |
| catia_create_sketch | 创建草图 | - |
| catia_draw_circle | 绘制圆 | 毫米 |
| catia_draw_rectangle | 绘制矩形 | 毫米 |
| catia_pad | 拉伸 | 毫米 |
| catia_pocket | 挖槽/切除 | 毫米 |
| catia_update | 更新零件 | - |
| catia_fit_all | 适配视图 | - |

### SolidWorks工具（13个）

| 工具 | 功能 |
|------|------|
| sw_new_part | 创建新零件 |
| sw_select_plane | 选择参考平面 |
| sw_create_sketch | 创建草图 |
| sw_draw_circle | 绘制圆 |
| sw_draw_center_rect | 绘制矩形 |
| sw_extrude | 拉伸 |
| sw_cut_extrude | 切除拉伸 |
| 等等... | 查看完整文档 |

## 💡 使用示例

### 示例1: 圆柱体
```
"创建一个直径50mm、高度100mm的圆柱体"
```

### 示例2: 带孔的盒子
```
"做一个100x100x50mm的盒子，中心有一个直径30mm的通孔"
```

### 示例3: 电机支架
```
"设计一个80x60mm的电机安装板，厚度10mm，四角有M4螺丝孔"
```

### 示例4: L型支架
```
"创建一个L型支架：底板60x40mm，立板高50mm，厚度3mm"
```

## 📚 完整文档

- **CATIA**: [README_CATIA_MCP.md](README_CATIA_MCP.md)
- **SolidWorks**: [README_MCP.md](README_MCP.md)
- **验证报告**: [CATIA_MCP_验证报告.md](CATIA_MCP_验证报告.md)

## 🔍 故障排除

### "Cannot connect to CATIA/SolidWorks"

1. ✅ 确保CAD软件正在运行
2. ✅ 以管理员身份运行Python
3. ✅ 检查COM自动化是否启用

### "No active sketch"

先用 `create_sketch` 创建草图，再绘制几何图形

### 几何体不可见

调用 `update()` 更新零件，然后 `fit_all()` 适配视图

## 📋 系统要求

- **操作系统**: Windows（COM自动化需要）
- **Python**: 3.8+
- **CAD软件**: CATIA V5/V6 或 SolidWorks 2020+
- **Claude**: Claude Code 或 Claude Desktop

## 🎁 额外工具

### 测试脚本
```bash
python test_catia_connection.py
```
检查CATIA连接和配置

### 演示脚本
```bash
python catia_cylinder_demo.py
```
自动创建一个圆柱体作为演示

## 📦 如何分享

### 方式1: GitHub Release

1. 创建release分支
2. 只保留必要文件
3. 创建release包

### 方式2: 单独仓库

创建一个新仓库只包含MCP服务器：
```
cad-mcp-servers/
├── catia/
│   ├── catia_mcp.py
│   ├── test_connection.py
│   └── demo.py
├── solidworks/
│   ├── solidworks_mcp.py
│   └── ...
├── README.md
└── requirements.txt
```

### 方式3: Python包

打包成pip可安装的包：
```bash
pip install cad-mcp-servers
```

## 🤝 贡献

欢迎提交：
- Bug报告
- 新功能建议
- 更多CAD软件支持
- 文档改进

## 📄 许可证

MIT License

## 🔗 相关链接

- **原项目**: [EmbodiedCAD](https://github.com/earthtojake/text-to-cad)
- **你的仓库**: [text-to-cad-MCP-for-SolidWorks](https://github.com/Sqy-creator-studying/text-to-cad-MCP-for-SolidWorks)
- **MCP协议**: [Model Context Protocol](https://modelcontextprotocol.io)

## ⭐ 如果有帮助，请给个星标！

---

**Made with ❤️ by [Sqy-creator-studying](https://github.com/Sqy-creator-studying)**
