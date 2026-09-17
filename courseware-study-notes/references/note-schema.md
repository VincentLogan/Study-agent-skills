# Courseware note schema

Use this schema for the final Markdown file. Adapt headings to the source, but preserve the main-body order and keep all appendices after it.

```md
# <课程名>：<讲义或课件标题>

> 来源：`<文件名>`
> 课件范围：<S1–Sxx 或 P1–Pxx；长文件列出每一连续处理范围>
> 笔记按原课件讲授顺序整理。

## 本讲路线图

- <前置概念> → <核心机制> → <证明/算法> → <结论或应用>

## 1. <章节或小节标题> [S1–S4 / P1–P4]

**重要性：A · 必须掌握**

### 这一节要解决什么

<问题、动机、目标。>

### 核心概念

<定义、条件、符号和公式。>

### 核心原理解析

<结论是什么、为何可能成立、准备走哪条证明/解题路线，以及一句可记忆的结论。>

### 详细证明 / 推导 / 机制

1. <前提与记号>
2. <步骤及其依据>
3. <结论>

### 原课件例子

<该例子的输入/条件、所说明的规则或结论、可迁移的理解。不要复刻无关动画步骤。>

### 易错点

- <直接来自课件或其定义/推导的易错点。>

> 来源：[S1–S4 / P1–P4]

## 本讲总结

- <3–8 条最应该记住的结论，各附来源。>

## 复杂度与适用条件速查

| 结构 / 算法 | 操作 / 结论 | 时间复杂度 | 空间复杂度 | 条件 | 来源 |
|---|---|---:|---:|---|---|

## 复习自测

1. <问题>（来源：[...]）

## 术语速查

| 术语 | 一句话解释 | 来源 |
|---|---|---|

## 待核对

- [待核对 Pn/Sn] <无法可靠恢复的内容、原因、可行的人工确认方式。>
```

Use `$...$` for inline math and `$$...$$` for standalone expressions. HTML/CSS is a nonessential enhancement only: do not hide source facts, proof steps, or warnings inside a renderer-specific feature.
