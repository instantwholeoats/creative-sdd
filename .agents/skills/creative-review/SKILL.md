---
name: creative-review
description: 原稿を変更せずEditorとしてMechanical、Creative Contract、Continuity、Structural、Editorialの観点から一つのUnitをレビューし、指摘の承認状態を管理する。DraftまたはRevisionのレビュー、Review artifact作成、指摘の承認・却下を行うときに使う。
---

# Creative Review

一つの原稿を独立性の高いEditor視点で評価し、`.creative/work/reviews/NNN.md`へ記録する。原稿は変更しない。

## 出力と境界

- 新規Reviewは`../../../templates/review.md`を基礎にする。
- Review作成時は対応するReview artifactだけを作成または更新する。
- 指摘の承認・却下時は、明示された指摘の`status`だけを更新する。
- manuscript、Spec、Plan、task、Acceptance、continuity、summary、canonを変更しない。
- ReviewとRevisionを同時に行わない。Review中に修正文を原稿へ適用しない。
- 主観的な好みを客観的エラーとして扱わない。

## ワークフロー

### 1. 対象とcontextを確認する

1. `AGENTS.md`、対象原稿、`.creative/work/spec.md`、対応task、対応Outline Unitを読む。
2. 関連するDesign、continuity、必要なcanon、関連Summaryだけを読む。
3. 既存ReviewとGit差分があれば、今回の原稿範囲を特定するために読む。
4. `spec.md`の`status`が`approved`であることを確認する。
5. 対象原稿がない、対応taskを特定できない、taskが未完了、またはSpecが未承認ならReviewを作らない。

執筆時の会話や自己説明を評価根拠にせず、保存済みartifactと現在の原稿を根拠にする。Planがdrift reconciliationで`draft`へ戻っていても、既に存在する原稿はレビューできる。

### 2. Mechanical検査を先に行う

`scripts/creative_lint.py`が存在すれば、次を実行して対象に関係する結果をReviewへ反映する。

```bash
python3 scripts/creative_lint.py --root .
```

ファイル名、Markdown heading、frontmatter、ID重複、taskとmanuscriptの対応など、機械検査できる事項をLLMだけで再判定しない。lint失敗そのものを原稿の文学的欠陥と呼ばない。

### 3. Editorとしてレビューする

必要な観点だけを使う。

- Mechanical: lint結果、文字数やheadingなど明示的制約
- Contract Compliance: Spec、明示制約、読者、POV、tense、tone
- Continuity: timeline、location、knowledge、possessions、relationships、world rules
- Structural: Unit目的、progression、causality、pacing、transition
- Editorial: redundancy、exposition、不明瞭さ、specificity、voice、反復

矛盾の可能性がある場合は、嘘、unreliable narrator、flashback、人物の誤認、mystery、意図的例外を考慮する。確証がなければ断定せず、severityを上げすぎない。

### 4. Review artifactを作る

- ファイル名は原稿の3桁番号を使う。番号がなければ対応する数値task IDを3桁にゼロ埋めする。
- frontmatterの`manuscript_sha256`へ現在の原稿のSHA-256を記録する。
- `verdict`は、修正が必要なBLOCKER、MAJOR、MINORがあれば`revise`、なければ`pass`にする。OPTIONALだけで`revise`にしない。
- `revision_status`は`verdict: pass`なら`not_required`、`verdict: revise`なら`pending`から始める。
- 指摘ごとに安定した`RV-NNN` ID、severity、`status: proposed`、location、issue、evidence、recommendationを記録する。
- 指摘がない区分へダミー項目を作らない。
- Recommended Revision Scopeは必要最小限の範囲を示し、全体改稿を既定にしない。

Reviewを作成してもtaskのチェック、`Acceptance`、Review artifact外の状態は変更しない。

### 5. 指摘の承認を処理する

ユーザーが現在のReviewを確認したうえで、特定の指摘を明示的に承認または却下した場合だけ対象IDの`status`を変更する。

- 承認: `proposed`から`approved`
- 却下: `proposed`または`approved`から`rejected`
- 文脈のない「OK」や対象Reviewを提示済みか不明な場合は変更しない。
- 「必須指摘をすべて承認」はBLOCKER、MAJOR、MINORだけを承認し、OPTIONALは明示されない限り承認しない。
- `resolved`はcreative-reviseだけが設定する。
- 承認操作で`verdict`や`revision_status`を変更しない。

### 6. 応答する

対象、verdict、severity別件数、主要な根拠、推奨Revision範囲、Review保存先を簡潔に伝える。Review作成時は原稿を変更していないことを明示する。承認処理時は変更した指摘IDだけを伝える。
