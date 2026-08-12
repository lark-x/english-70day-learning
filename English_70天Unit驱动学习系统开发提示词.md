# 英语 70 天 Unit 驱动学习系统——开发计划与编码模型提示词

## 1. 项目目标

请从零开发一个简洁、稳定、数据驱动的个人英语学习 Web 应用。

项目只保留三条核心链路：

```text
新内容学习
上一学习日完整复习
错题管理
```

课程内容全部来自用户提供的 Unit / 教材数据。系统不自行编造教材知识，不自动补充不存在的单词、翻译、语法、句子、练习或作文。

整体流程：

```text
用户提供数据源
↓
分析与标准化
↓
生成固定 70 天学习计划
↓
上一学习日完整复习
↓
今日新内容
↓
练习 / 作文
↓
错题记录
↓
保存 StudySnapshot
↓
下一学习日继续
```

---

## 2. 70 天固定计划

项目必须固定为：

```text
70 个 Learning Day
```

这里的 Day 是“学习日”，不是自然日。

例如：

```text
8 月 1 日完成 Day 10
8 月 2~4 日没有学习
8 月 5 日重新打开
```

此时应：

```text
复习 Day 10
↓
学习 Day 11
```

不得自动跳到 Day 14。

因此：

```text
Learning Day ≠ Calendar Day
```

学习进度只根据实际完成的 Day 计算。

---

## 3. 每日新单词硬上限

必须定义全局唯一配置：

```ts
export const COURSE_CONFIG = {
  planDays: 70,
  maxNewWordsPerDay: 35,
};
```

硬规则：

```text
每天新单词 <= 35
```

如果数据源足够，目标是让每天尽量接近：

```text
35 个新单词
```

但绝对不能为了凑 35 个而生成不存在的单词。

如果数据不足：

```text
允许某些天 < 35
```

如果数据过多：

```text
优先选择核心词汇
其余保留为 extension vocabulary
```

理论最大首次新词容量：

```text
70 × 35 = 2450
```

---

## 4. 用户提供数据后必须先分析

收到真实数据源后，不要直接写页面，也不要直接按 Unit 数量平均拆分。

第一阶段必须做：

```text
数据分析
```

输出 Content Analysis Report，至少包含：

- Unit 数量
- 原始单词数量
- 去重后单词数量
- 词组数量
- 语法点数量
- 句子数量
- 练习数量
- 作文数量
- 缺失中文翻译数量
- 缺失音标数量
- 缺失关系数量
- 每个 Unit 的内容规模
- 数据是否足够支持 70 天
- 预计每天新词数量
- 哪些 Unit 需要拆成多个学习日
- 哪些 Unit 内容较少，可与相邻内容组合

必须先完成分析，再生成 70 天计划。

---

## 5. 内容预处理 Pipeline

建议独立于 Web：

```text
scripts/content/
  analyze-source.ts
  normalize-source.ts
  score-vocabulary.ts
  build-70-day-plan.ts
  validate-plan.ts
```

执行顺序：

```text
Raw Source
↓
Analyze
↓
Normalize
↓
Vocabulary Scoring
↓
Build 70-Day Plan
↓
Validate
↓
Generated Course Data
```

Web UI 只消费生成后的标准数据，不负责 OCR、PDF 解析或复杂课程拆分。

---

## 6. 标准 Unit 模型

```ts
interface Unit {
  id: string;
  order: number;
  title: string;
  subtitle?: string;

  words: WordItem[];
  phrases: PhraseItem[];
  grammar: GrammarItem[];
  sentences: SentenceItem[];
  exercises: ExerciseItem[];

  composition?: CompositionItem;
}
```

Unit 顺序由 `order` 决定，不依赖文件名。

---

## 7. 单词模型

```ts
interface WordItem {
  id: string;
  word: string;

  phonetic?: {
    uk?: string;
    us?: string;
  };

  audio?: {
    uk?: string;
    us?: string;
  };

  meanings: Array<{
    partOfSpeech?: string;
    translation: string;
  }>;

  phraseIds?: string[];
  grammarIds?: string[];
  sentenceIds?: string[];

  sourceUnitId: string;

  coreScore?: number;
  priority?: "core" | "important" | "extension";

  notes?: string;
}
```

---

## 8. 新词全局去重

一个单词第一次进入正式学习日时：

```text
isNew = true
```

以后即使它再次出现在：

- 新 Unit
- 词组
- 语法
- 句子
- 练习
- 作文

都不能再次占用“每日 35 个新词”的额度。

需要维护全局首次曝光集合：

```ts
introducedWordIds: Set<string>
```

同一个词只能有一次首次新词曝光。

---

## 9. 核心词汇筛选

如果某个 Unit 或某个计划日存在超过 35 个候选新词，不能简单 `slice(0, 35)`。

需要计算 `coreScore`。

建议权重：

```text
用户明确标注重点词       +100
练习题直接涉及           +40
作文要求涉及             +35
关联语法                 +25
关联词组                 +20
Unit 中高频出现           +1~20
跨多个 Unit 出现          +10~30
标题 / 核心段落关键词     +20
已在以前作为新词学过      不再作为新词
```

排序规则必须稳定、可重复：

```text
coreScore DESC
sourceUnitOrder ASC
sourceIndex ASC
word ASC
```

不要使用随机数。

词汇优先级：

```text
core
important
extension
```

其中：

- `core`：优先进入 70 天计划
- `important`：有容量时进入
- `extension`：保留在资料库和点击查词中，但不一定进入首次 70 天新词计划

---

## 10. 70 天计划不能机械按 Unit 拆

不要：

```text
Unit 1 = Day 1
Unit 2 = Day 2
```

应根据每个 Unit 的真实内容规模拆分。

例如：

```text
Unit 1
  Day 1
  Day 2
  Day 3

Unit 2
  Day 4
  Day 5
```

也允许一个内容很少的 Unit 与下一个 Unit 的部分内容组合。

但每个学习日都必须保留：

```text
sourceUnitIds
```

用于追踪来源。

---

## 11. 每日新内容组成

每天新学习内容固定围绕：

```text
单词
词组
相关语法
相关句子
相关练习
相关作文
```

重点是“相关”。

不能生成：

```text
35 个随机单词
+
无关语法
+
无关句子
```

应该围绕相同 Unit 或相同主题组织。

例如：

```text
Day 12
来源：Unit 4 Part A

新单词：
work
blessing
career
opportunity
...

词组：
take an opportunity
make progress

语法：
动名词作主语

句子：
来自 Unit 4 的相关原句

练习：
围绕上述词汇、语法、句子

作文：
围绕 Unit 4 主题
```

---

## 12. DayPlan 数据模型

```ts
interface DayPlan {
  day: number;

  sourceUnitIds: string[];

  title: string;

  newWordIds: string[];
  phraseIds: string[];
  grammarIds: string[];
  sentenceIds: string[];
  exerciseIds: string[];

  compositionId?: string;
}
```

必须满足：

```text
day ∈ 1..70
newWordIds.length <= 35
```

---

## 13. 推荐生成的数据结构

```text
public/data/

  course/
    units/
      unit-01.json
      unit-02.json

    words.json
    phrases.json
    grammar.json
    sentences.json
    exercises.json
    compositions.json

  plan/
    manifest.json
    day-01.json
    day-02.json
    ...
    day-70.json
```

---

## 14. 70 天 Manifest

```json
{
  "schemaVersion": 1,
  "planDays": 70,
  "maxNewWordsPerDay": 35,
  "days": [
    {
      "day": 1,
      "file": "day-01.json"
    }
  ]
}
```

---

## 15. 70 天计划验证器

必须实现：

```text
validate-plan.ts
```

至少验证：

1. 必须恰好存在 Day 1~Day 70。
2. 每天 `newWordIds.length <= 35`。
3. 一个单词不能在两个 Day 中都被标记为首次新词。
4. 所有 ID 必须存在于课程数据中。
5. 不能存在 Day 0 或 Day 71。
6. 所有完整英文句子必须存在中文翻译。
7. 所有计划必须可追溯到至少一个 Unit。
8. 不允许引用不存在的词组、语法、句子、练习或作文。

---

## 16. 数据不足时

如果数据不足以支撑 70 天高密度学习：

不要生成假内容。

应生成报告：

```text
DATA_INSUFFICIENT
```

例如：

```text
当前唯一词汇：1100
理论最大计划容量：2450
预计平均每日新词：15.7
缺少作文：23 天
缺少练习：12 天
```

仍可把已有内容合理铺到 70 天，但允许某些天：

```text
新词 < 35
```

禁止为了凑数自动生成教材内容。

---

## 17. 数据过多时

如果唯一候选新词超过：

```text
2450
```

则：

```text
核心词优先
↓
重要词次之
↓
extension 保留
```

未进入 70 天首次学习计划的词不能删除。

它们仍可：

- 出现在资料页
- 出现在相关句子中
- 出现在 Word Drawer
- 作为扩展词查看

---

## 18. 上一学习日完整复习

复习与 70 天排课是两套独立逻辑。

计划负责：

```text
今天学什么
```

复习负责：

```text
上一次学过什么
```

完成 Day N 后，下一次开始学习时必须首先复习 Day N 的全部学习内容。

例如 Day 10：

```text
35 单词
8 词组
2 语法
10 句子
12 练习
1 作文
```

下一学习日必须完整包含：

```text
35 单词复习
8 词组复习
2 语法复习
10 句子复习
12 练习复习
1 作文复习
```

禁止：

- 只复习错题
- 只复习单词
- 随机抽样
- 根据算法跳过部分内容

第一版只实行：

```text
上一学习日全量复习
```

不做复杂 SM-2、D+3、D+7。

---

## 19. StudySnapshot

完成当天学习时创建：

```ts
interface StudySnapshot {
  id: string;

  day: number;
  date: string;

  newWordIds: string[];
  phraseIds: string[];
  grammarIds: string[];
  sentenceIds: string[];
  exerciseIds: string[];

  compositionId?: string;

  completedAt: string;
}
```

Snapshot 只保存 ID。

不要复制整份教材正文。

下一次学习通过 ID 读取最新课程数据。

---

## 20. 今日学习页面

顶部显示：

```text
70 天进度：Day 12 / 70
上一学习日：Day 11
今日新内容：Day 12
```

页面结构：

```text
上一学习日完整复习

────────────────

今日新内容
```

第一天没有上一学习日，只显示 Day 1 新内容。

---

## 21. 今日新内容顺序

固定：

```text
1. 单词
2. 词组
3. 语法
4. 句子
5. 练习
6. 作文
```

可以使用 Stepper：

```text
1 / 6 单词
2 / 6 词组
3 / 6 语法
4 / 6 句子
5 / 6 练习
6 / 6 作文
```

---

## 22. 双语句子是硬约束

统一：

```ts
interface BilingualSentence {
  en: string;
  zh: string;
}
```

所有完整英文句子必须：

```text
英文一行
中文下一行
```

例如：

```text
You need a clear plan to achieve your goal.
你需要一个清晰的计划来实现自己的目标。
```

以下全部必须双语：

- 词组例句
- 语法例句
- 句子模块
- 练习题中的完整英文句子
- 练习解析中的例句
- 作文参考内容
- Word Drawer 相关句子

如果数据缺翻译：

```text
标记为资料缺失
```

不要自动编造。

---

## 23. 词组模型

```ts
interface PhraseItem {
  id: string;
  phrase: string;
  translation: string;

  explanation?: string;

  examples?: BilingualSentence[];

  relatedWordIds?: string[];

  sourceUnitId: string;
}
```

---

## 24. 语法模型

```ts
interface GrammarItem {
  id: string;

  title: string;
  explanation: string;
  structure?: string;

  examples: BilingualSentence[];

  relatedWordIds?: string[];
  relatedPhraseIds?: string[];

  sourceUnitId: string;
}
```

---

## 25. 句子模型

```ts
interface SentenceItem {
  id: string;

  en: string;
  zh: string;

  explanation?: string;

  relatedWordIds?: string[];
  relatedPhraseIds?: string[];
  relatedGrammarIds?: string[];

  sourceUnitId: string;
}
```

---

## 26. 练习

第一版支持：

```text
choice
fill
translation
ordering
short-answer
```

回答错误后：

```text
自动进入错题本
```

提交后立即显示：

```text
是否正确
正确答案
解析
```

如果解析包含完整英文句子，也必须显示中文翻译。

---

## 27. 错题模型

```ts
interface MistakeRecord {
  id: string;

  exerciseId: string;
  unitId: string;

  userAnswer: unknown;
  correctAnswer: unknown;

  wrongCount: number;
  reviewCount: number;

  firstWrongAt: string;
  lastWrongAt: string;

  status:
    | "unresolved"
    | "reviewing"
    | "resolved";
}
```

同一道题重复答错时更新记录，不无限创建重复项。

---

## 28. 作文

```ts
interface CompositionItem {
  id: string;

  title: string;

  prompt: string;
  promptTranslation?: string;

  requirements?: string[];

  suggestedWordIds?: string[];
  suggestedPhraseIds?: string[];
  suggestedGrammarIds?: string[];

  reference?: Array<{
    en: string;
    zh: string;
  }>;

  sourceUnitId: string;
}
```

参考作文采用：

```text
英文段落
中文段落

英文段落
中文段落
```

---

## 29. 全局单词点击

任何学习区域中的英文单词都必须可以点击：

- 单词
- 词组
- 语法例句
- 句子
- 练习
- 解析
- 作文
- 参考作文

统一使用：

```text
InteractiveEnglishText
```

点击后打开：

```text
Word Drawer
```

不要让每个模块单独实现点击逻辑。

---

## 30. Word Drawer

桌面端右侧显示，移动端使用 Bottom Sheet。

固定展示：

```text
单词

UK / US 发音

UK / US 音标

中文释义

相关词组

相关语法

相关句子

来源 Unit
```

例如：

```text
achieve

UK 🔊
/əˈtʃiːv/

US 🔊
/əˈtʃiːv/

v.
实现；达到；取得

相关词组
achieve a goal
实现目标

相关句子
You need a clear plan to achieve your goal.
你需要一个清晰的计划来实现自己的目标。
```

优先播放数据中提供的音频。

没有音频时使用浏览器 `SpeechSynthesis` fallback。

---

## 31. 资料页

资料页用于：

- 按 Unit 浏览
- 查看全部单词
- 查看全部词组
- 查看语法
- 查看句子

资料页只用于浏览：

```text
不得改变 70 天学习进度
```

---

## 32. 课程数据与学习状态分离

课程数据只读：

```text
Unit
Word
Phrase
Grammar
Sentence
Exercise
Composition
70-Day Plan
```

学习状态存 IndexedDB：

```text
currentDay
completedDays
StudySnapshot
ExerciseAttempt
CompositionAttempt
ReviewRecord
MistakeRecord
```

UI 不允许直接访问 IndexedDB。

统一经过 `StudyStorage`。

---

## 33. 推荐技术栈

如果没有其他限制：

```text
Vue 3
TypeScript
Vite
Vue Router
Pinia
Dexie / IndexedDB
Zod
Vitest
```

纯 Web、Local First。

第一版不需要后端。

---

## 34. 推荐目录

```text
src/

  domain/
    course/
    plan/
    study/
    review/
    mistakes/

  features/
    today/
    learning/
    review/
    mistakes/
    dictionary/
    materials/

  components/
    bilingual/

  services/
    storage/
    speech/

  stores/
  router/

scripts/
  content/
    analyze-source.ts
    normalize-source.ts
    score-vocabulary.ts
    build-70-day-plan.ts
    validate-plan.ts
```

---

## 35. Review Builder 必须是纯函数

```ts
buildPreviousReview(
  snapshot,
  courseData,
)
```

不得：

- 访问 Vue
- 访问 IndexedDB
- 修改 Store

输入学习快照和课程数据，返回：

```ts
interface ReviewSession {
  day: number;

  words: WordItem[];
  phrases: PhraseItem[];
  grammar: GrammarItem[];
  sentences: SentenceItem[];
  exercises: ExerciseItem[];

  composition?: CompositionItem;
}
```

---

## 36. 70 天生成报告

计划生成时同时生成：

```text
content-plan-report.json
```

至少：

```json
{
  "planDays": 70,
  "maxNewWordsPerDay": 35,

  "uniqueWords": 0,
  "scheduledNewWords": 0,
  "extensionWords": 0,

  "daysWith35Words": 0,
  "minWordsPerDay": 0,
  "maxWordsPerDay": 35,

  "units": 0,

  "missingTranslations": 0,
  "missingPhonetics": 0,

  "warnings": []
}
```

---

## 37. 必须测试

### 70 天

```text
days.length === 70
```

Day 1~70 全部存在。

### 35 词上限

```ts
for (const day of plan.days) {
  expect(day.newWordIds.length)
    .toBeLessThanOrEqual(35);
}
```

### 新词唯一曝光

同一个词不能在两个学习日都作为新词。

### 上一学习日完整复习

假设 Day 1：

```text
35 words
5 phrases
2 grammar
8 sentences
10 exercises
1 composition
```

下一次学习必须得到完全相同数量的 ReviewSession。

### 跨自然日

```text
8 月 1 日完成 Day 10
8 月 5 日重新学习
```

必须：

```text
复习 Day 10
学习 Day 11
```

### 双语完整性

所有完整英文句子必须存在 `zh`。

### 错题

- 答错自动创建
- 重复答错更新 `wrongCount`
- 重新答对不删除历史错误

### Word Drawer

点击英文单词后能显示：

- 音标
- 中文释义
- 相关词组
- 相关语法
- 相关句子

---

## 38. 明确删除原复杂项目中的功能

不要实现：

```text
Stage 1~5 晋级系统
能力评分
考试大纲中心
考试覆盖率
Remedial Queue
复杂自适应排课
AI 自动生成教材
OCR 运行时解析
排行榜
积分
社交
复杂账户系统
复杂数据库
```

新项目核心只有：

```text
70 天内容计划
+
上一学习日完整复习
+
今日新内容
+
错题
+
全局单词查询
```

---

## 39. 开发顺序

### Phase 1
读取真实数据源，生成 Content Analysis Report。

### Phase 2
建立 Domain Types、Zod Schema、Normalizer。

### Phase 3
实现词汇去重、coreScore 和 70 天 Plan Builder。

### Phase 4
实现 70 天 Validator，验证 70 天、35 新词上限、ID、翻译完整性。

### Phase 5
实现双语组件、InteractiveEnglishText、WordDrawer、Speech。

### Phase 6
实现今日学习和六个学习模块。

### Phase 7
实现 StudySnapshot、上一学习日完整 Review。

### Phase 8
实现练习、错题和作文。

### Phase 9
实现 IndexedDB、状态恢复、70 天进度。

### Phase 10
完成响应式 UI、测试、Build 和清理。

每个 Phase 完成后必须运行：

```bash
npm run typecheck
npm run test
npm run build
```

内容数据还需：

```bash
npm run content:analyze
npm run content:build
npm run content:validate
```

---

## 40. 给编码模型的最终强制提示

```text
你正在开发一个 70 天 Unit 驱动英语学习器。

用户之后会提供真实 Unit / 教材数据。

收到真实数据后：
先分析数据，
再标准化，
再计算核心词汇，
再把全部内容拆成固定 70 个 Learning Day。

每日新单词最大 35 个。

如果数据足够：
尽量每天安排接近 35 个新词。

如果数据不足：
允许少于 35 个。

绝对禁止为了达到 35 个而生成不存在的单词。

如果候选词过多：
计算 coreScore，
优先安排 core / important，
其余作为 extension 保留。

同一个单词全局只能有一次“新词”曝光。

70 天不是自然日。
用户中断几天后继续时，不跳过 Learning Day。

每次开始新的 Learning Day 前，
必须完整复习上一次完成日的：
单词、词组、语法、句子、练习和作文。

昨日完整复习和错题本是两个独立系统。

今日新内容固定围绕：
单词、词组、语法、句子、练习、作文。

所有完整英文句子必须包含中文翻译，
UI 统一采用英文一行、中文下一行。

任何学习页面中的英文单词都可点击，
统一打开 Word Drawer，
显示：
发音、音标、中文释义、相关词组、相关语法、相关句子、来源 Unit。

不要实现阶段晋级、能力评分、考试大纲、复杂自适应算法、复杂后端或 AI 自动生成教材。

最终必须输出：
1. Content Analysis Report
2. 70-Day Plan
3. content-plan-report.json
4. Validation Result
5. Test Result
6. Data Gap / Warning List
```
