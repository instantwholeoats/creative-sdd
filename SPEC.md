# CreativeSDD v0.1 実装仕様書

## 1. 概要

CreativeSDDは、AIエージェントを利用した創作・執筆のための軽量なSpec-Driven Writingフレームワークである。

初期の主要実行環境は **Codex CLI** とする。

CreativeSDDは文章生成アプリ、文章エディタ、単なるテンプレート集ではない。

CreativeSDDが管理するのは、以下の創作ライフサイクルである。

```text
人間の曖昧な創作意図
    ↓
AIとのDiscovery
    ↓
Creative Spec
    ↓
Plan
    ↓
Draft
    ↓
Review
    ↓
Revise
    ↓
Reconcile
    ↓
次のDraft
```

中心となる設計思想は以下である。

> 人間に仕様書を書かせない。
>
> 人間とAIの対話によって創作上の仕様を発見する。
>
> AIがspecを提案し、人間が重要な境界で承認する。

CreativeSDD v0.1は意図的に小さく保つ。

以下は作らない。

- Webアプリ
- GUI
- データベース
- Vector DB
- Embedding / RAG基盤
- 独自LLMクライアント
- 独自エージェントランタイム
- daemon
- background service
- 複雑なオーケストレーションシステム

v0.1は主として以下から構成する。

- Codex Agent Skills
- Markdownテンプレート
- ファイルシステム上のプロジェクト規約
- 小規模な決定論的検証スクリプト
- Git互換のプレーンテキスト状態管理

CreativeSDDを削除しても、ユーザーの作品そのものは通常のMarkdownとして利用できなければならない。

---

# 2. 主要目的

CreativeSDD v0.1では、ユーザーが例えば以下のような曖昧な入力だけで開始できること。

> 近未来の東京を舞台に、AIによって仕事を失った元エンジニアの話を書きたい。細かいところはまだ何も決めていない。

ユーザー自身に以下を書かせてはならない。

- `characters.md`
- `world.md`
- `outline.md`
- `brief.md`
- `spec.md`

AIが以下を判断する。

1. すでに決定していること
2. 暗黙に示されていること
3. 未決定のこと
4. 矛盾していること
5. 今決める必要があること
6. 後から決めればよいこと
7. したがって今ユーザーに質問すべきこと

Discoveryは固定フォーム形式にしてはならない。

質問は既存の情報に応じて適応的に生成すること。

---

# 3. 非目標

v0.1では以下を目標としない。

- Markdownエディタの代替
- 長編小説全体の一括自動生成
- 文学的品質の保証
- CMS連携
- 出版ワークフロー
- 高度なsemantic search
- 外部知識DB
- グラフィカルなプロジェクト管理
- あらゆる創作ジャンルへの対応
- あらゆるAIエージェントへの対応

Codex CLIをリファレンス実装とする。

将来の移植可能性は考慮するが、そのためにv0.1を複雑化してはならない。

---

# 4. 基本思想

## 4.1 対話駆動の仕様策定

CreativeSDDは、

```text
人間がspecを書く
↓
AIが実行する
```

というモデルを採用しない。

代わりに、

```text
人間がやりたいことを話す
↓
AIが意図を理解する
↓
不足事項を特定する
↓
必要なことだけ質問する
↓
AIがspecを提案する
↓
人間が確認・修正・承認する
↓
AIがspecに基づいて執筆する
```

とする。

Creative Specは入力フォームではない。

**人間とAIが共同で発見した創作上の契約**である。

---

# 5. Adaptive Discovery

DiscoveryはCreativeSDDの中核機能である。

未解決事項は概念的に以下へ分類する。

```text
BLOCKING
IMPORTANT
DEFERRABLE
IRRELEVANT
```

## BLOCKING

次の工程へ進むために解決が必要。

例：

ブログを書きたいと言われたが、何について書くのか全く分からない。

## IMPORTANT

作品へ大きな影響を与えるが、暫定判断でも進行可能。

例：

文学寄りの作品なのか、エンターテインメント寄りなのか。

## DEFERRABLE

後から決めても問題ない。

例：

第14章に一度だけ登場する店の内装。

## IRRELEVANT

そもそも仕様化する必要がない。

例：

物語に関係しない主人公の好きな色。

原則としてBLOCKINGを優先する。

IMPORTANTは必要なものだけ質問する。

DEFERRABLEについては原則質問しない。

IRRELEVANTは仕様へ追加しない。

---

# 6. 質問ポリシー

Discoveryでは毎回以下を行う。

1. 現在のプロジェクト状態を読む
2. ユーザーが明言したことを抽出する
3. 事実とAIの推測を分離する
4. 未決定事項を特定する
5. 矛盾を検出する
6. 未決定事項の影響度を評価する
7. 今必要な質問だけを選ぶ

一度に行う質問は原則として **1〜3問** とする。

固定された長大な質問票をユーザーへ提示してはならない。

ユーザーの回答によって複数の事項が同時に解決した場合、それらについて再質問してはならない。

十分な情報が得られた場合、空欄を埋める目的だけでDiscoveryを続けてはならない。

---

# 7. 判断状態

重要な判断は概念的に以下へ分類する。

```text
CONFIRMED
INFERRED
PROVISIONAL
OPEN
```

## CONFIRMED

ユーザー自身が明言した、または明示的に承認した。

## INFERRED

既存情報から強く推定でき、誤解の可能性が低い。

## PROVISIONAL

作業を進めるためAIが暫定的に選択した。

後から変更可能。

## OPEN

意図的に未決定として残している。

CreativeSDDは、AIによる推測を勝手に確定事項へ昇格させてはならない。

---

# 8. ワークフロー

基本フェーズは以下とする。

```text
DISCOVERY
    ↓
SPEC
    ↓
PLAN
    ↓
DRAFT
    ↓
REVIEW
    ↓
REVISE
    ↓
RECONCILE
    ↘
      次のDRAFT
```

ユーザーがすべての内部フェーズを明示的に操作する必要はない。

---

# 9. v0.1のSkills

以下のCodex Agent Skillsを実装する。

```text
creative-discovery
creative-spec
creative-plan
creative-draft
creative-review
creative-revise
creative-status
```

v0.1では原則としてこれ以上増やさない。

---

# 10. creative-discovery

## 目的

ユーザーの曖昧な創作意図から、Creative Specを作成できるだけの理解を得る。

CreativeSDDの推奨エントリーポイントとする。

例：

```text
$creative-discovery

AI時代の働き方について、自分の経験をベースにブログを書きたい。
```

## 責務

1. CreativeSDDプロジェクト状態を確認する
2. 新規作品か既存作品か判断する
3. 明示された意図を抽出する
4. 曖昧さを検出する
5. 矛盾を検出する
6. 未決定事項を分類する
7. 必要な質問だけ行う
8. Discovery状態を保存する
9. 現在の理解をユーザーへ提示する
10. spec化する前に重要事項の確認を行う

## 出力

```text
.creative/work/brief.md
```

推奨構造：

```markdown
# Creative Brief

## 作品種別

## 現在の構想

## 目的

## 想定読者

## 読者に与えたい体験

## 制約

## 確定事項

## 暫定事項

## 意図的な未決定事項

## 解決が必要な事項

## 参考資料

## 現在の理解
```

すべての項目を埋めることを目的としてはならない。

---

# 11. Discovery終了条件

以下を満たしたらDiscoveryを終了できる。

- BLOCKINGな不明点がない
- IMPORTANTな事項が解決済み、または暫定扱いになっている
- 有用なCreative Specを作れるだけの情報がある
- AIの理解をユーザーが確認できる

終了時には、簡潔に以下を提示する。

```text
現在、作品について以下のように理解しています。

- ...
- ...
- ...

意図的に未決定としているもの：

- ...
- ...

この状態でCreative Specを作成できます。
```

Discoveryを無限に続けてはならない。

---

# 12. creative-spec

## 目的

Discoveryで得られた理解を、持続的なCreative Contractへ変換する。

出力：

```text
.creative/work/spec.md
```

---

# 13. Fiction Spec

小説では概ね以下を扱う。

```markdown
# Creative Spec

## 基本情報
- 仮題
- 種別
- ジャンル

## 作品の意図
- コアとなる構想
- テーマ
- 読者体験

## 創作方針
- トーン
- 視点
- 文体
- ナラティブ距離

## 物語上の契約
- 中心的な問い
- 主な対立
- Stakes
- 解決の方向性

## キャラクター
- 主要人物
- 動機
- 重要な関係

## 世界
- 舞台
- 物語へ影響する世界のルール

## 制約
- 必須要素
- 避ける要素

## 意図的な創作余白

## 判断記録
```

specは作品全体を事前に書いてしまうためのものではない。

**創作上守るべき境界を定義するもの**とする。

---

# 14. Blog Spec

ブログ・記事では概ね以下を扱う。

```markdown
# Creative Spec

## 基本情報
- 形式
- 想定文字数

## 目的

## 想定読者

## 中心的な主張

## 読了後に期待する状態

## 主要な論点

## 根拠として必要なもの

## トーン

## 構成上の制約

## 調査が必要な事項

## 扱わない事項

## 未決定事項
```

SEOは必要な場合のみ扱う。

標準ではSEO記事を前提としない。

---

# 15. Human Approval Gate

`spec.md`には機械的に判定できる状態を持たせる。

例：

```yaml
---
status: draft
work_type: fiction
language: ja
---
```

承認後：

```yaml
---
status: approved
work_type: fiction
language: ja
---
```

以下のような自然言語による承認を認識してよい。

- これでいいです
- これで進めてください
- 承認します
- OKです
- Looks good
- Use this

specが存在するだけでは承認済みとして扱わない。

重大な変更が行われた場合は承認状態を再検討する。

---

# 16. creative-plan

## 目的

承認済みCreative Specを、実際に執筆できる計画へ変換する。

出力：

```text
.creative/work/design.md
.creative/work/outline.md
.creative/work/tasks.md
```

必要以上に詳細化しない。

---

# 17. design.md

`spec.md`はCreative Contractである。

`design.md`は、その契約をどう実現するかという現在の設計である。

小説では例えば：

- narrative architecture
- POV strategy
- pacing
- character arc
- reveal strategy
- timeline strategy
- continuity risk

ブログでは例えば：

- 論理構造
- argument architecture
- 根拠の配置
- 章構成
- 具体例
- rhetorical progression

specの単なる複製にしない。

---

# 18. outline.md

outlineは**未来の予定**である。

Canonical Factではない。

各単位は概ね以下を持てる。

```markdown
## Unit 03

### 目的

### 開始時点の状態

### 主な展開

### 終了時点の状態

### 必要な情報

### 任意のアイデア
```

小説では：

- scene
- chapter
- sequence

記事では：

- section
- subsection

などを単位とできる。

---

# 19. tasks.md

実際に実行可能な執筆単位へ分割する。

例：

```markdown
# Tasks

- [ ] 1. 導入を書く
  - Goal: 問題提起を行う
  - Boundary: 導入部分のみ

- [ ] 2. AIによる実装作業の変化を書く
  - Depends: 1

- [ ] 3. 要求定義の重要性を書く
  - Depends: 2
```

長編小説では：

```markdown
- [ ] 12. Chapter 12を書く
  - Goal: ...
  - Required state: ...
  - Expected resulting state: ...
```

原則として一度に一つの意味のあるWriting Unitを扱う。

---

# 20. creative-draft

## 目的

一つのWriting Taskを執筆する。

処理：

1. 対象taskを特定
2. 最小限必要なcontextを読む
3. specを確認
4. designを確認
5. outlineの対象範囲を確認
6. continuityを確認
7. 必要なcanonを確認
8. 必要に応じて過去summaryを確認
9. 対象単位を書く
10. 無関係な原稿を変更しない
11. 成功した場合のみtaskを完了扱いにする

原稿：

```text
manuscript/
```

例：

```text
manuscript/001.md
manuscript/002.md
```

ブログの場合：

```text
manuscript/article.md
```

---

# 21. Context Economy

すべての操作で全作品を読み込まない。

基本：

```text
global spec
+
current task
+
relevant design
+
current continuity
+
必要なcanon
+
必要な過去原稿
```

必要なら `rg` 等によるfilesystem searchを使用する。

v0.1ではEmbedding / Vector DB / RAGを導入しない。

---

# 22. Fiction Canon

長編小説では必要に応じて以下を持つ。

```text
.creative/work/canon/
    characters.md
    world.md
    timeline.md
    terminology.md
```

必要なファイルのみ作成する。

空ファイルを大量に作らない。

Canonでは少なくとも概念的に以下を区別する。

```text
原稿ですでに成立した事実
ユーザーが明示的に確定した事実
未来の予定に過ぎない情報
```

予定を自動的にCanon化してはならない。

---

# 23. continuity.md

長編作品では以下を管理できる。

```text
.creative/work/continuity.md
```

例：

```markdown
# Continuity State

## 現在の物語時刻

## 現在地

## キャラクター状態

### 葵
- location:
- physical_state:
- emotional_state:
- possessions:
- current_goal:

## キャラクターが知っていること

### 葵
- ...

## キャラクターが知らないこと

### 葵
- ...

## 読者が知っていること

## 未解決のThread

## 最近変更された事実
```

特に、

```text
Character Knowledge
```

と

```text
Reader Knowledge
```

を混同してはならない。

これはミステリー、サスペンス、dramatic irony等で重要である。

---

# 24. Unit Summary

長編では以下を作成できる。

```text
.creative/work/summaries/
    001.md
    002.md
```

例：

```markdown
# Unit 001 Summary

## 起きた出来事

## 状態変化

## 新しく成立したCanon

## Character Knowledgeの変化

## Reader Knowledgeの変化

## 未解決Thread

## 伏線
```

Summaryの主目的はcontext cost削減である。

---

# 25. Narrative Drift

CreativeSDDは **Narrative Drift** を第一級の概念として扱う。

例：

outline：

> Chapter 12で葵は東京へ帰る。

実際のdraft：

> 葵は横浜に残ることを選択した。

この場合、outlineへ合わせるために原稿を自動修正してはならない。

優先度：

```text
ユーザーの明示的な現在の指示
        ↓
受け入れられた原稿上の現実
        ↓
成立済みCanon
        ↓
承認済みSpec
        ↓
Design
        ↓
Outline
        ↓
AIの暫定案
```

Driftを検出した場合：

1. 差異を検出する
2. 意図的か事故か評価する
3. 上位制約違反でなければ原稿を尊重する
4. continuityを更新する
5. 将来outlineとのreconciliationを行う
6. Creative Contractそのものへ影響する場合だけユーザーへ確認する

---

# 26. creative-review

## 目的

WriterではなくEditorとしてレビューする。

可能であれば執筆時とは独立性の高いcontextで行う。

レビュー観点：

### Mechanical

可能な限りdeterministic toolingを使用する。

- ファイル名
- Markdown構造
- 文字数
- 禁止語
- heading
- frontmatter
- ID重複

### Contract Compliance

- spec
- 明示制約
- 想定読者
- POV
- tense
- tone

### Continuity

- timeline
- location
- character knowledge
- possessions
- relationships
- world rules

### Structural

- unitの目的
- progression
- causality
- pacing
- transition

### Editorial

- redundancy
- exposition過多
- 不明瞭な表現
- specificity不足
- voice不整合
- AI的な反復パターン

指摘は以下に分類する。

```text
BLOCKER
MAJOR
MINOR
OPTIONAL
```

主観的な好みを客観的エラーとして扱わない。

---

# 27. Review Artifact

出力：

```text
.creative/work/reviews/<unit>.md
```

例：

```markdown
# Review: Unit 012

## Verdict
pass | revise

## Blockers

## Major Findings

## Minor Findings

## Optional Editorial Suggestions

## Continuity Findings

## Spec Compliance

## Recommended Revision Scope
```

---

# 28. creative-revise

## 目的

Review指摘を必要最小限の変更で反映する。

1. 原稿を読む
2. Reviewを読む
3. 対応対象を特定
4. 必要な範囲だけ変更
5. 無関係な文章を維持
6. 新たなcontinuity regressionがないか確認

AIが「もっと良くできる」という理由だけで章全体を書き直してはならない。

---

# 29. Reconciliation

DraftまたはRevisionが受け入れられた後：

```text
manuscript
    ↓
state change抽出
    ↓
continuity更新
    ↓
summary更新
    ↓
narrative drift検出
    ↓
future outline reconcile
```

小さな下流変更は自動反映してよい。

作品構造を変えるような変更はユーザーへ提示する。

---

# 30. creative-status

プロジェクトの現在地を簡潔に表示する。

例：

```text
CreativeSDD Status

Work: Untitled Novel
Phase: Drafting
Spec: approved

Completed:
8 / 22 tasks

Current:
Chapter 9

Open major decisions:
- 結末
- 由衣の裏切りの正確な理由

Detected drift:
- Chapter 8の対決場所が東京から横浜へ変更された
- Chapters 9–10のoutline修正が必要

Next recommended action:
creative-draft 9
```

creative-statusは創作内容を変更しない。

---

# 31. Profiles

v0.1では以下だけ実装する。

```text
profiles/
    fiction.md
    blog.md
```

過度にgeneralizeしない。

---

# 32. Fiction Profile

主な観点：

- character consistency
- POV consistency
- world rules
- timeline
- scene purpose
- motivation
- causality
- information disclosure
- reader knowledge
- foreshadowing
- unresolved threads
- narrative voice

---

# 33. Blog Profile

主な観点：

- audience
- thesis
- claims
- evidence
- factual uncertainty
- logical flow
- source requirements
- repetition
- examples
- introduction
- conclusion

SEOはoptionalとする。

---

# 34. Author Steering

作品固有ではないユーザーの執筆方針を分離する。

```text
.creative/steering/
    author.md
    style.md
    principles.md
```

### author.md

- AIへ任せたい程度
- 執筆ワークフロー上の好み

### style.md

- 文体傾向
- 避けたい表現
- sentence density等

### principles.md

例：

- 論理矛盾は指摘する
- 自伝的事実をAIが創作しない
- sourced factとspeculationを区別する

長期的なAuthor Preferenceと、個別作品のCreative Specを混同しない。

---

# 35. 推奨Repository構造

CreativeSDD自体：

```text
creative-sdd/
├── AGENTS.md
├── SPEC.md
├── README.md
├── LICENSE
│
├── .agents/
│   └── skills/
│       ├── creative-discovery/
│       │   └── SKILL.md
│       ├── creative-spec/
│       │   └── SKILL.md
│       ├── creative-plan/
│       │   └── SKILL.md
│       ├── creative-draft/
│       │   └── SKILL.md
│       ├── creative-review/
│       │   └── SKILL.md
│       ├── creative-revise/
│       │   └── SKILL.md
│       └── creative-status/
│           └── SKILL.md
│
├── templates/
│   ├── brief.md
│   ├── spec-fiction.md
│   ├── spec-blog.md
│   ├── design.md
│   ├── outline.md
│   ├── tasks.md
│   ├── continuity.md
│   ├── summary.md
│   └── review.md
│
├── profiles/
│   ├── fiction.md
│   └── blog.md
│
├── steering/
│   ├── author.md
│   ├── style.md
│   └── principles.md
│
├── scripts/
│   └── creative_lint.py
│
└── tests/
```

CreativeSDDを導入した作品Repository：

```text
my-work/
├── AGENTS.md
│
├── .agents/
│   └── skills/
│
├── .creative/
│   ├── config.yaml
│   ├── steering/
│   ├── profiles/
│   └── work/
│       ├── brief.md
│       ├── spec.md
│       ├── design.md
│       ├── outline.md
│       ├── tasks.md
│       ├── continuity.md
│       ├── canon/
│       ├── summaries/
│       └── reviews/
│
└── manuscript/
```

---

# 36. 言語ポリシー

基本原則：

> 人間が読む自然言語は日本語。
> 機械が扱う識別子は英語。

日本語：

- AGENTS.md本文
- SKILL.md本文
- README
- templates本文
- brief/spec/design/outline本文

英語：

- directory name
- filename
- YAML key
- enum value
- Python identifier
- Skill name

例：

```yaml
---
status: approved
work_type: fiction
language: ja
---
```

---

# 37. Configuration

設定は最小限とする。

```yaml
version: 0.1

work:
  type: fiction
  language: ja

workflow:
  approval_required:
    spec: true
    plan: true

draft:
  unit: chapter

review:
  mechanical_lint: true
```

推測可能なものを設定項目にしない。

Convention over Configurationを優先する。

---

# 38. Deterministic Lint

```text
scripts/creative_lint.py
```

を実装する。

可能な限りPython標準ライブラリのみを使用する。

候補：

- target length
- heading
- frontmatter
- forbidden terms
- missing manuscript
- duplicate unit ID
- task/manuscript mismatch

単純な機械検査にLLM tokenを使用しない。

複雑なplugin systemは作らない。

---

# 39. Git

Gitは推奨するが必須ではない。

利用可能な場合：

- recent changes取得
- review範囲限定
- modified files特定
- human rollback

などに使用する。

レビュー時は可能なら：

```bash
git diff
```

を利用する。

ユーザー指示なしに自動commitしてはならない。

---

# 40. Source of Truth

## Creative Intent

```text
現在の明示的User Instruction
>
Approved Spec
>
過去のAssumption
```

## Story Reality

```text
Accepted Manuscript
>
Established Canon
>
Outline
```

## Planned Future

```text
Approved Spec
>
Design
>
Outline
>
Provisional Agent Idea
```

Outlineを理由に成立済み原稿を書き換えてはならない。

---

# 41. Contradiction Detection

例：

```text
characters.md:
葵は31歳

Chapter 4:
「先月29歳になった」
```

または：

```text
spec:
一人称

draft:
三人称全知視点
```

矛盾は概念的に以下へ分類する。

```text
hard contradiction
possible contradiction
intentional exception
```

以下の可能性を考慮する。

- 嘘
- unreliable narrator
- flashback
- character mistake
- mystery
- intentional exception

単純一致だけで自動修正してはならない。

---

# 42. UX原則

CreativeSDDはユーザーの認知負荷を減らす。

例えば：

> 主人公が会社を辞めた理由だけ、今決める必要があります。
>
> 1. AIによる人員削減
> 2. 自発的な退職
> 3. 現時点では曖昧にする
>
> 別案でも構いません。

のような質問はよい。

一方：

> 以下18項目をすべて入力してください。

は禁止する。

ただし自由回答が適する場合に強制的に選択式にしない。

---

# 43. Progressive Specification

完全な仕様を作ってから書き始める必要はない。

CreativeSDDは **Just Enough Specification** を採用する。

長編小説でも最初は：

- premise
- protagonist
- broad conflict
- tonal direction

だけで開始できる。

Chapter 17の詳細をChapter 1を書く前に決める必要はない。

必要になる直前にDiscoveryしてよい。

---

# 44. Creative Autonomy

概念的に以下の3モードを想定する。

```text
conservative
collaborative
exploratory
```

## conservative

重要な創作判断をユーザーへ確認する。

## collaborative

AIが合理的な提案をし、重要な境界だけ確認する。

## exploratory

AIが積極的に暫定案を作り、後からreconcileする。

デフォルト：

```text
collaborative
```

v0.1では複雑な権限システムを作らない。

---

# 45. Fast Path

すべてのWriting TaskにSDDを適用しない。

例えば：

- 1段落だけ直す
- 文法修正
- タイトル候補
- 短文作成

などではPersistent Spec不要と判断できる。

SDDそのものを目的化しない。

---

# 46. v0.1 Acceptance Criteria

## Scenario A: 曖昧な小説

入力：

> 近未来の東京で、人間とAIの関係について小説を書きたい。

期待：

1. 不足している高影響事項を特定
2. 一度に少数だけ質問
3. 自然言語で回答可能
4. brief.md更新
5. coherentな理解を提案
6. ユーザー承認
7. spec.md生成
8. plan生成
9. 1 unitをdraft
10. continuity/summary更新
11. review可能

---

## Scenario B: 詳細な構想

ユーザーが最初から以下を提示：

- premise
- characters
- setting
- ending
- POV
- tone

期待：

すでに回答済みの質問をしない。

速やかにspec提案へ進む。

---

## Scenario C: 意図的未決定

ユーザー：

> 結末は書きながら決めたい。

期待：

結末をOPENとして保存。

Discoveryで繰り返し質問しない。

---

## Scenario D: 変更

最初：

> 主人公は30歳。

後：

> 28歳にしたい。

期待：

最新の明示指示を優先する。

影響するartifactを特定する。

---

## Scenario E: Narrative Drift

Outline：

> 東京へ戻る。

Draft：

> 横浜に残る。

期待：

原稿を自動的に東京へ戻さない。

Driftとして認識する。

continuityとfuture planへの影響を処理する。

---

## Scenario F: Blog

ユーザー：

> 「AIでエンジニアは不要になる」という議論に違和感があるのでブログにしたい。

Discoveryでは：

- thesis
- audience
- reasoning
- evidence
- tone
- reader outcome

などを扱う。

小説向け質問をしない。

---

# 47. Tests

文学的品質をテストしない。

テスト対象：

- project structure
- template availability
- lint
- status parsing
- approval state
- profile resolution
- missing-file handling

fixture：

```text
tests/fixtures/
    fiction-minimal/
    blog-minimal/
```

生成文章そのもののbrittleなsnapshot testは避ける。

---

# 48. README

READMEの冒頭では仕組みではなくMental Modelを説明する。

例：

> CreativeSDDは、あなたが何を書きたいのかをAIとの対話によって整理し、
> それをCreative Specとして保持しながら、
> 長い作品を段階的に執筆・レビュー・修正するためのフレームワークです。
>
> 仕様書を自分で書く必要はありません。
> まず、作りたいものを普通の言葉で話してください。

最初の利用方法として `creative-discovery` を案内する。

ディレクトリ構造から説明を始めない。

---

# 49. 実装優先順位

## P0 — Core Discovery

1. repository structure
2. AGENTS.md
3. creative-discovery
4. brief template
5. creative-spec
6. fiction/blog spec templates
7. approval semantics

## P1 — Planning / Drafting

8. creative-plan
9. design template
10. outline template
11. tasks template
12. creative-draft
13. manuscript conventions

## P2 — State

14. continuity
15. summaries
16. canon
17. narrative drift

## P3 — Quality

18. creative-review
19. creative-revise
20. creative_lint.py
21. creative-status

## P4 — Documentation / Tests

22. fixtures
23. tests
24. README
25. example project

---

# 50. Premature Engineeringの禁止

以下の選択肢では原則として前者を選択する。

```text
Markdownの20行
>
Python abstraction layer
```

```text
filesystem convention
>
database schema
```

```text
Codex Agent Skill
>
custom agent runtime
```

明確に決定論的コードが有利な場合のみコードを書く。

v0.1の目的はInfrastructureの完成ではなくWriting Workflowの検証である。

---

# 51. 将来追加可能なもの

将来的には以下を追加できる。

```text
creative-research
creative-factcheck
creative-canon
creative-reconcile
creative-review-whole
creative-publish
creative-export
```

Profile：

```text
technical-writing
nonfiction-book
screenplay
memoir
academic
```

ただし将来のためだけにv0.1で実装しない。

---

# 52. CreativeSDDの本質

CreativeSDDの価値は、

> Markdownテンプレートを使ってAIが文章を書くこと

ではない。

CreativeSDDとは、

> 人間とAIが創作上の契約を徐々に発見し、
> 長期プロジェクトを通じてそれを保持し、
> 小さな単位で作品を作り、
> 実際に生まれた作品が計画と異なった場合にはその差異を検出し、
> 現実の作品に合わせて将来計画を再調整する仕組み

である。

最適化対象：

```text
低い導入コスト
+
高いcontinuity
+
明示的なdecision
+
不要な質問の最小化
+
context costの削減
+
重要な場面でのhuman control
```

---

# 53. 初期実装に対するCodexへの指示

この仕様に従ってCreativeSDD v0.1を実装すること。

ただし最初から全機能を実装しない。

まずP0を実装する。

実装開始前に：

1. この仕様書を最後まで読む
2. repositoryの状態を確認する
3. アーキテクチャへ重大な影響を与える曖昧さだけ特定する
4. 軽微な実装判断は最も単純な方法を自分で選択する
5. P0の実装計画を作る
6. P0だけ実装する
7. テスト・手動検証を行う
8. 実装結果と未実装項目を報告する

不要な外部依存を追加しない。

以下を優先する。

- Markdown
- Agent Skills
- filesystem state
- Python standard library
- Git

最重要ユースケースは：

```text
曖昧なユーザーの創作意図
    ↓
Adaptive Discovery
    ↓
必要最小限の質問
    ↓
Persistent Brief
    ↓
Creative Spec案
    ↓
Human Approval
```

である。

Discoveryを固定質問票として実装してはならない。

ユーザーにCreativeSDD用Markdownファイルを書かせてはならない。

AIの推測とユーザーが確定した事項を混同してはならない。

分からないことを無理に埋めず、必要に応じてOPENまたはPROVISIONALとして保持すること。

