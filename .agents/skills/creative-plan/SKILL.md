---
name: creative-plan
description: 承認済みCreative Specを、現在の実現方針、未来のWriting Unit、実行可能なWriting Taskへ変換し、人間の承認を管理する。spec承認後に小説またはブログの執筆計画を新規作成・更新するとき、plan案を確認・承認するとき、design、outline、tasksが必要なときに使う。
---

# Creative Plan

承認済みCreative Specを、過剰に先回りしない実行可能な執筆計画へ変換する。

## 出力と境界

- `.creative/work/design.md`、`.creative/work/outline.md`、`.creative/work/tasks.md`だけを作成または更新する。
- 新規作成時はそれぞれ`../../../templates/design.md`、`../../../templates/outline.md`、`../../../templates/tasks.md`を基礎にする。
- `design.md`のfrontmatterにある`status`を、3つのartifactから成るPlan全体の承認状態として扱う。`outline.md`と`tasks.md`に重複した状態を持たせない。
- `spec.md`、`brief.md`、`manuscript/`を変更しない。
- continuity、summaries、canonは参照するだけで、このSkillでは作成・更新しない。
- review、revision、lint、status、tests、fixturesなどP3以降のartifactや機能を作成しない。
- Specの意図的な未決定事項を、計画の都合だけで確定しない。

## ワークフロー

### 1. 入力状態を確認する

1. `AGENTS.md`を読む。
2. `.creative/work/spec.md`を全文読む。
3. 既存の`design.md`、`outline.md`、`tasks.md`があれば全文を読む。
4. 既存原稿がある場合は、`.creative/work/continuity.md`、関連するUnit Summary、必要なcanon、対応する受け入れ済み原稿だけを読む。
5. 最新のユーザー指示を既存artifactより優先する。

`spec.md`がない、frontmatterの`status`が`approved`でない、または`work_type`が`fiction`か`blog`でない場合は計画を生成・更新しない。必要なDiscoveryまたはSpec承認へ戻るよう案内する。

新しいPlanは必ず次の状態から始める。既存の`design.md`に`status`がない場合も未承認の`draft`として扱う。

```yaml
---
status: draft
---
```

### 2. Designを作る

SpecをCreative Contractとして保ち、それをどう実現するかだけを書く。

- 小説では、物語構造、POV strategy、pacing、character arc、reveal strategyなど、現在の執筆に必要な設計を選ぶ。
- ブログでは、論理構造、argument architecture、根拠と具体例の配置、rhetorical progressionなど、現在の執筆に必要な設計を選ぶ。
- Spec本文の単なる複製にしない。
- Specにない設定、結論、根拠を確定事項として創作しない。
- 進行に必要なAIの判断は暫定であることを明記する。
- 空欄を埋めるためだけの設計を追加しない。

### 3. Outlineを作る

作品を意味のあるWriting Unitへ分ける。小説ではscene、chapter、sequence、ブログではsection、subsectionなど、作品に適した単位を選ぶ。

各Unitには必要な範囲で次を記録する。

- 目的
- 開始時点の状態
- 主な展開
- 終了時点の状態
- 必要な情報
- 任意のアイデア
- 対応するTask IDと`manuscript/`配下のOutput
- ブログで一つのファイルを分担する場合は対象Section

Outlineは未来の予定であり、成立済みの事実として書かない。SpecのOPENな結末などを、Outlineで暗黙に固定しない。長さに応じた必要十分な粒度に留める。

### 4. Tasksを作る

Outlineの各Unitを、原則として一対一の実行可能なWriting Taskへ変換する。

- 安定した連番IDと未完了チェックボックス`- [ ]`を使う。
- `Goal`、`Boundary`、`Output`、`Outline unit`、`Depends`を記録する。
- 新規taskには`Acceptance: pending`を記録する。`pending`は原稿の未受理、`accepted`は受理後の状態同期完了を表す。
- 小説で必要なら`Required state`と`Expected resulting state`も記録する。
- `Output`は必ず`manuscript/`配下にする。
- 小説は原則として`manuscript/001.md`のような3桁連番、ブログは原則として`manuscript/article.md`を使う。
- 一項目を一つの意味のあるWriting Unitにし、複数章や記事全体を曖昧な一taskへまとめない。
- 実行順が必要な場合だけ依存関係を付ける。

### 5. 既存計画を更新する

- 優先順位は、ユーザーの明示的な現在の指示、受け入れられた原稿上の現実、成立済みCanon、承認済みSpec、Design、Outline、AIの暫定案の順とする。
- 完了済みtaskのチェック状態と安定したIDを理由なく変更しない。
- 既存taskの`Acceptance`は、原稿が明示的に改稿され再受理待ちになった場合を除き変更しない。この項目がない旧形式のtaskは`pending`とみなす。
- 既存原稿を計画へ合わせるために変更しない。
- OutlineやtaskのExpected stateをCanonical Factとして扱わない。受け入れ済み原稿と競合する場合は原稿上の現実を優先する。
- continuityではCharacter KnowledgeとReader Knowledgeを別の状態として読み、片方の知識をもう片方へ推測で移さない。
- Narrative Driftを検出した場合は原稿を維持し、小さな下流変更を将来のOutline Unitと未完了taskへ反映する。Creative Contractまたは作品構造へ影響する変更は自動反映せず、影響をユーザーへ提示する。
- 完了済みtaskや受け入れ済み原稿の意味を変える計画変更は行わない。
- 承認済みPlanの実現方針、Unit、Task、境界、依存関係、Outputなど、執筆内容または順序へ影響する変更を行った場合は`status: draft`へ戻す。表記修正だけなら承認状態を維持してよい。

### 6. Plan案を提示する

新規作成または意味のある変更を行ったPlanは`status: draft`のまま、次をユーザーへ簡潔に提示する。

- Designの実現方針
- Unit数とTask数
- 各Unitの目的とOutput
- 主な依存関係
- 暫定判断とOPENな事項

提示後、修正点またはPlan全体への承認を求める。ユーザーがまだ見ていないPlanを暗黙に承認済みとしない。

### 7. Plan承認を処理する

次をすべて満たす場合だけ`design.md`の`status`を`approved`へ変更する。

1. `design.md`、`outline.md`、`tasks.md`がすべて存在する。
2. `design.md`の`status`が`draft`である。
3. 現在のSpecが`approved`である。
4. 承認対象となるPlanの内容が現在の会話でユーザーへ提示済みである。
5. ユーザーの最新発言がPlan全体への明確な承認である。
6. 現在のSpecとPlanに重大な不整合がない。

質問への同意や別の対象への「OK」をPlan承認と解釈しない。提示済みか確実に判断できない場合は、Planの要点を再提示して改めて承認を求め、ユーザーの次の明確な承認を待つ。

承認時はPlan本文を勝手に改善せず、`design.md`のfrontmatterにある`status`だけを変更する。承認を保存したことを明示する。

### 8. 応答する

作成・更新時はPlan案の要点と承認待ちであることを伝える。承認時は承認済みであることと、最初に実行可能なtaskを簡潔に伝える。暫定判断とOPENな事項があれば区別して示す。
