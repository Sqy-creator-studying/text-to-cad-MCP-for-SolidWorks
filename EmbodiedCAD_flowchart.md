# EmbodiedCAD 项目流程图

## 简版流程图

```mermaid
flowchart LR
    A["用户输入自然语言需求"] --> B["系统解析设计意图<br/>任务目标 / 参数 / 约束"]
    B --> C["生成或修改参数化 CAD 源文件<br/>Python + build123d"]
    C --> D["CAD 生成管线执行<br/>OpenCascade / STEP / STL / GLB / URDF"]
    D --> E["EmbodiedCAD / CAD Explorer 预览<br/>3D 工作区 / 装配树 / Inspector"]
    E --> F["结果检查与交互<br/>几何引用 / 参数编辑 / Assistant 预览"]
    F --> G{"满足需求?"}
    G -- "是" --> H["导出工程结果<br/>STEP / STL / GLB / manifest"]
    G -- "否" --> I["基于反馈继续迭代<br/>修改参数 / 结构 / 装配关系"]
    I --> C
```

## 申请材料可配说明

EmbodiedCAD 的核心流程是：将自然语言需求逐步转化为参数化建模结果，再通过工程工具链完成 CAD 生成、三维预览、结果检查和交互迭代。
它不是一次性“生成一个模型”，而是形成了“文本输入—模型生成—结果验证—继续修改”的闭环，更接近一个可持续交互和修正的智能体式工程设计系统。

## 若需要更技术化的版本

```mermaid
flowchart TD
    A["自然语言输入"] --> B["需求理解与任务拆解"]
    B --> C["参数 / 组件 / 约束映射"]
    C --> D["参数化 CAD 源文件"]
    D --> E["build123d / OpenCascade 几何建模"]
    E --> F["生成 STEP / STL / GLB / 拓扑数据"]
    F --> G["EmbodiedCAD 前端工作台"]
    G --> H["组件库 / 装配树 / 3D 工作区 / Inspector / Assistant"]
    H --> I["用户检查与交互反馈"]
    I --> J["参数调整 / 结构修改 / 装配优化"]
    J --> D
    F --> K["最终导出与展示"]
```
