---
name: creative-draft
description: 承認済みCreative Specと承認済みPlanに従って一つのWriting TaskをMarkdown原稿として執筆し、受け入れ済み原稿からcontinuity、Unit Summary、必要なfiction canonを更新してNarrative Driftをreconcileする。小説の一章・一場面やブログの一節を書くとき、原稿を受理して状態を確定するときに使う。
---

# Creative Draft

一つのWriting Taskに必要なcontextだけを読み、対象範囲だけを原稿として書く。原稿が明示的に受け入れられた後は、その原稿を現実として状態を更新する。

## 出力と境界

- 執筆時は`manuscript/`配下の対象原稿と、`.creative/work/tasks.md`の対応するチェックボックスおよび`Acceptance`だけを作成または更新する。
- 原稿受理時は対象taskの`Acceptance`、`.creative/work/continuity.md`、対応する`.creative/work/summaries/NNN.md`、必要な`.creative/work/canon/*.md`、将来Unitの`outline.md`と未完了task、および再承認が必要な場合の`design.md`の`status`だけを更新できる。
- `spec.md`、`brief.md`、受け入れ済み原稿を変更しない。
- 一度に複数taskを執筆しない。
- 対象外の原稿や、同一ファイル内の対象外Sectionを変更しない。
- Review artifactやRevision状態をこのSkillで作成・更新しない。P4のREADME、tests、fixtures、example project、インストール機能を作成しない。
- 外部DB、RAG、Embeddingを使用しない。Markdown artifactと必要に応じたfilesystem searchだけを使う。

## ワークフロー

### 1. 入力状態を確認する

1. `AGENTS.md`を読む。
2. `.creative/work/spec.md`を全文読む。
3. `.creative/work/design.md`を読む。
4. `.creative/work/tasks.md`を全文読む。
5. 対象taskに対応する`.creative/work/outline.md`のUnitだけを読む。
6. `.creative/work/continuity.md`があれば読む。
7. 対象taskに必要な`.creative/work/canon/`のファイルと過去のUnit Summaryだけを読む。
8. Specの`work_type`に対応する`../../../profiles/fiction.md`または`../../../profiles/blog.md`を読み、対象taskに関係する観点だけを参照する。
9. 最新のユーザー指示を既存artifactより優先する。

`spec.md`がない、Specの`status`が`approved`でない、Plan artifactが不足している、または`design.md`のfrontmatterにあるPlanの`status`が`approved`でない場合は執筆しない。必要なSpec承認、Plan作成、またはPlan承認を案内する。`design.md`に`status`がない場合は未承認の`draft`として扱う。

現在のSpecとDesign・Outline・Tasksを比較し、中心的な意図または主張、想定読者、約束する読者体験、主要人物、中心的対立、POV、トーン、必須要素、避ける要素、TaskのBoundaryやOutputなどに重大な不整合がないことを確認する。

重大な不整合がある、または現在のPlanが古いSpecに基づく疑いを解消できない場合は執筆しない。不整合の要点を示し、`creative-plan`でPlanを更新して再承認するよう案内する。原稿やPlanをその場で自動修正しない。

### 2. 対象taskを決める

- ユーザーがtask IDを指定した場合はそのtaskだけを選ぶ。
- 指定がなく、依存関係を満たす未完了taskが一つだけ明確ならそれを選ぶ。
- 複数候補があり選択で内容や順序が変わる場合は、執筆前にtask IDの指定を求める。
- 依存taskが未完了なら実行しない。
- 完了済みtaskは、ユーザーが明示的に再執筆または修正を依頼しない限り選ばない。受理済み原稿を再執筆する場合は、変更した時点で対応taskの`Acceptance`を`pending`へ戻す。
- `Output`が`manuscript/`配下でないtaskは実行しない。

### 3. 必要最小限のcontextを集める

対象taskの`Goal`、`Boundary`、`Output`、対応するOutline Unit、関連するDesignとSpecの制約を特定する。

Contextの優先順位を次の順にする。

1. ユーザーの明示的な現在の指示
2. 受け入れられた原稿上の現実
3. 成立済みCanon
4. 承認済みSpec
5. Design
6. Outline
7. AIの暫定案

`continuity.md`は現在状態、Unit Summaryは過去原稿の圧縮表現、canonは長期的な確定事項として使う。Character KnowledgeとReader Knowledgeを混同しない。既存原稿が必要な場合も対象ファイルと直接必要な過去原稿だけを読み、作品全体や全canonを一律に読み込まない。情報が競合する場合は上の優先順位で判断し、OutlineをCanonical Factとして扱わない。

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

成功した場合だけ、`tasks.md`の対応する一行を`- [ ]`から`- [x]`へ変更する。原稿を新規作成または変更した場合は、対応する`Acceptance`を`pending`にする。失敗、不足、判断待ちの場合は未完了のままにする。次のtaskを自動実行しない。

この時点では、原稿に書かれた事実をcontinuity、summary、canonへまだ反映しない。taskの完了は原稿の受け入れを意味しない。対象taskの`Acceptance`は`pending`のままにする。この項目がない旧形式のtaskは`pending`とみなす。

### 6. 原稿受理を確認する

ユーザーが特定の原稿またはUnitを明示して、その原稿を受け入れる意思を示した場合だけ、次のreconciliationへ進む。

- 対象原稿が存在し、対応taskが完了していることを確認する。
- 最新のユーザー発言が、質問への同意やPlan承認ではなく、対象原稿そのものへの明確な受理であることを確認する。
- 対象原稿を現在の会話で提示済みか確認できない場合や、文脈のない「OK」だけの場合は状態を更新しない。対象と要点を提示し、改めて明確な受理を求める。
- 受理後の処理中は原稿本文を変更しない。Outlineとの差異を理由に原稿を修正しない。
- 対象原稿のReviewに`revision_status: applied`がある場合は、このSkillで受理しない。`creative-revise`でRevision受理とP2状態同期を一体で行うよう案内する。
- 対象原稿のReviewに未処理のBLOCKER、MAJOR、MINOR指摘がある場合は受理しない。`proposed`は承認または却下、`approved`はRevisionを先に行うよう案内する。すべて`rejected`なら、原稿を変更せずこのSkillで受理できる。
- 対象taskの`Acceptance`がすでに`accepted`で、受理後に原稿が変更されていないなら、同じ原稿の状態同期を繰り返さない。同期済みであることを伝え、状態artifactと計画を変更せず終了する。受理後の変更が明示されている場合は`pending`へ戻し、現在の原稿について改めて明確な受理を確認する。

### 7. 受け入れ済み原稿をreconcileする

一つの受け入れ済み原稿について、次の順で処理する。

1. 原稿に実際に書かれた出来事、人物状態、所持品、物語時刻、場所、未解決Thread、Character Knowledgeの変化、Reader Knowledgeの変化を抽出する。
2. fictionの複数Unit作品で継続状態が必要なら、`../../../templates/continuity.md`を基礎に`.creative/work/continuity.md`を作成または更新する。Character Knowledge、Character Unknowns、Reader Knowledgeは必ず別の見出しに保つ。
3. 後続Unitのcontext削減に有用なら、`../../../templates/summary.md`を基礎に対応する`.creative/work/summaries/NNN.md`を作成または更新する。原稿名に3桁番号があればそれを使い、番号がなければ対応する数値task IDを3桁にゼロ埋めする。受け入れ済み原稿にない情報を追加しない。
4. fictionで長期的な整合性に必要な確定事項が生じた場合だけ、`characters.md`、`world.md`、`timeline.md`、`terminology.md`のうち必要なファイルを`.creative/work/canon/`へ作成または更新する。それぞれ対応する`../../../templates/canon-*.md`を基礎にする。空ファイルや無関係なcanonファイルを一括作成しない。
5. 対応するOutline Unitと原稿を比較し、Narrative Driftの有無、意図的か事故か、上位制約への影響を評価する。
6. 上位制約に反しない差異は受け入れ済み原稿を優先し、小さな下流変更だけを将来のOutline Unitと未完了taskのRequired stateまたはExpected resulting stateへ反映する。完了済みtaskを変更しない。
7. 将来の計画内容を意味的に変更した場合は、Plan全体を再確認できるよう`design.md`の`status`だけを`draft`へ戻す。次の執筆前に`creative-plan`で提示・再承認するよう案内する。
8. 必要な状態同期がすべて正常に完了した最後にだけ、対象taskの`Acceptance`を`accepted`へ更新する。項目がない旧形式のtaskにはこの時点で追加する。途中で更新できなかった項目があれば`pending`のままにし、未完了の内容をユーザーへ伝える。

Canonでは、原稿で成立した事実、ユーザーが明示的に確定した事実、未来の予定を見出しで分離する。Outline、Design、taskのExpected state、AIの案は未来の予定であり、それだけを根拠にCanonへ移さない。

Creative Contractを変える可能性がある差異、意図性を判断できない重大な差異、または作品構造を変えるreconciliationは自動反映しない。原稿を保持したまま影響と選択肢だけをユーザーへ提示する。確認が必要なのはCreative Contractまたは構造へ影響するときに限る。

### 8. 応答する

執筆時は、完了したtask ID、原稿の保存先、執筆した範囲を簡潔に伝え、原稿は未受理でstate未更新であることを明示する。未完了のままなら、その理由と次に必要な判断だけを伝える。

原稿受理時は、受理した原稿、更新したcontinuity・summary・canon、検出したDrift、future outlineへの反映、Plan再承認の要否を簡潔に伝える。作らなかったcanonファイルを作ったように報告しない。
