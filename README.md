# VincentLogan Skills

个人维护的可移植 AI Skills 仓库，面向支持 `SKILL.md` 的客户端使用。每个 Skill 都将提示规范、可选脚本和参考模板打包在同一目录中，以便导入、版本管理和复用。

## 当前 Skills

| Skill | 用途 | 目录 | 下载 |
|---|---|---|---|
| `courseware-study-notes` | 从 PPTX、旧版 PPT 或 PDF 课程讲义生成按原顺序组织、带证明讲解和复习材料的 Markdown 笔记。 | [进入目录](./courseware-study-notes/) | [下载 ZIP](./dist/courseware-study-notes.zip) |

## 安装

1. 下载对应的 ZIP，或克隆本仓库。
2. 在支持 Skills 的客户端中导入 `courseware-study-notes/` 目录或 ZIP。
3. 在目标环境安装脚本依赖：

   ```bash
   python -m pip install -r courseware-study-notes/requirements.txt
   ```

4. 调用 `$courseware-study-notes`，并提供课件路径及（可选）输出文件夹/文件名。

> 此 Skill 默认只在本地读取课件与写入 Markdown 笔记；它不需要 API Key，也不上传课件内容。

## 目录约定

```text
<skill-name>/
├── SKILL.md       # 给 Agent 的工作流规则
├── scripts/       # 可独立运行的确定性提取脚本（如有）
├── references/    # 按需读取的模板和规范（如有）
├── assets/        # 可选资源（如有）
└── agents/        # 支持的客户端 UI 元数据（如有）
```

## 版本与发布

每次稳定更新会同时提交源码与 `dist/` 中的 ZIP 包。GitHub 仓库创建并连接后，本 README 的相对链接会自动成为对应目录入口和下载入口。
