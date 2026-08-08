---
name: creative-draft
description: 承認済みCreative Specと承認済みのDesign・Outline・Tasksに従い、指定された一つのWriting TaskをMarkdown原稿として執筆する。小説の一章・一場面やブログの一節を書き、成功したtaskだけを完了するときに使う。
---

# Creative Draft

一つのWriting Taskに必要なcontextだけを読み、対象範囲だけを原稿として書く。

## 出力と境界

- `manuscript/`配下の対象原稿と、`.creative/work/tasks.md`の対応するチェックボックスだけを作成または更新する。
- `spec.md`、`design.md`、`outline.md`を変更しない。
- 一度に複数taskを執筆しない。
- 対象外の原稿や、同一ファイル内の対象外Sectionを変更しない。
- continuity、summaries、canon、narrative drift、review、reviseなどP2以降のartifactを作成・更新しない。

## ワークフロー

### 1. 入力状態を確認する

1. `AGENTS.md`を読む。
2. `.creative/work/spec.md`を全文読む。
3. `.creative/work/design.md`を読む。
4. `.creative/work/tasks.md`を全文読む。
5. 対象taskに対応する`.creative/work/outline.md`のUnitだけを読む。
6. 最新のユーザー指示を既存artifactより優先する。

`spec.md`がない、Specの`status`が`approved`でない、Plan artifactが不足している、または`design.md`のfrontmatterにあるPlanの`status`が`approved`でない場合は執筆しない。必要なSpec承認、Plan作成、またはPlan承認を案内する。`design.md`に`status`がない場合は未承認の`draft`として扱う。

現在のSpecとDesign・Outline・Tasksを比較し、中心的な意図または主張、想定読者、約束する読者体験、主要人物、中心的対立、POV、トーン、必須要素、避ける要素、TaskのBoundaryやOutputなどに重大な不整合がないことを確認する。

重大な不整合がある、または現在のPlanが古いSpecに基づく疑いを解消できない場合は執筆しない。不整合の要点を示し、`creative-plan`でPlanを更新して再承認するよう案内する。原稿やPlanをその場で自動修正しない。

### 2. 対象taskを決める

- ユーザーがtask IDを指定した場合はそのtaskだけを選ぶ。
- 指定がなく、依存関係を満たす未完了taskが一つだけ明確ならそれを選ぶ。
- 複数候補があり選択で内容や順序が変わる場合は、執筆前にtask IDの指定を求める。
- 依存taskが未完了なら実行しない。
- 完了済みtaskは、ユーザーが明示的に再執筆または修正を依頼しない限り選ばない。
- `Output`が`manuscript/`配下でないtaskは実行しない。

### 3. 必要最小限のcontextを集める

対象taskの`Goal`、`Boundary`、`Output`、対応するOutline Unit、関連するDesignとSpecの制約を特定する。

既存原稿が必要な場合は、対象ファイルと直接必要な過去原稿だけを読む。作品全体を一律に読み込まない。P1ではcontinuity、summaries、canonを前提にせず、新規作成もしない。

### 4. 一つのUnitを書く

- `Goal`を達成し、`Boundary`を越えないMarkdown原稿を書く。
- 小説はtaskの`Output`で指定された3桁連番ファイルへ保存する。
- ブログは原則として`manuscript/article.md`へ保存する。既存記事を扱う場合はtaskで指定されたSectionだけを追加または更新する。
- 既存ファイルを扱う場合は対象外の文章を保持する。
- Specの必須要素、避ける要素、読者体験、トーンを守る。
- Outlineを予定として参照し、ユーザーの最新指示や承認済みSpecより優先しない。
- task外の続きを先回りして書かない。

### 5. 完了を記録する

原稿を読み直し、対象taskのGoalとBoundary、Specの明示制約を満たし、対象外を変更していないことを確認する。

成功した場合だけ、`tasks.md`の対応する一行を`- [ ]`から`- [x]`へ変更する。失敗、不足、判断待ちの場合は未完了のままにする。次のtaskを自動実行しない。

### 6. 応答する

完了したtask ID、原稿の保存先、執筆した範囲を簡潔に伝える。未完了のままなら、その理由と次に必要な判断だけを伝える。
