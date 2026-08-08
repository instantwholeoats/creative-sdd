---
name: creative-revise
description: Review artifactで明示的にapprovedとなった指摘だけを、対象原稿の必要最小限の範囲へ反映し、Revisionの受理後にP2 stateをreconcileする。レビュー指摘に基づく修正、Revision状態の更新、修正版原稿の受理を行うときに使う。
---

# Creative Revise

ReviewとRevisionを分離し、承認済み指摘だけを原稿へ最小限反映する。修正完了を原稿受理とみなさない。

## 出力と境界

- Revision時は対象原稿、対応taskの`Acceptance`、対象Review artifactだけを更新する。
- Revision受理時はP2 reconciliationに必要なcontinuity、summary、必要なcanon、future outline、未完了task、必要ならPlan statusを更新できる。
- Spec、brief、対象外原稿、対象外Section、未承認指摘を変更しない。
- 新しいReviewを作らず、未承認の改善を便乗させない。
- P4 artifact、外部DB、RAG、Embedding、独自runtimeを追加しない。

## ワークフロー

### 1. 対象Reviewを検証する

1. `AGENTS.md`、対象原稿、対応Review、Spec、taskを読む。
2. `spec.md`の`status`が`approved`であることを確認する。
3. Reviewの`manuscript`が対象原稿と一致し、`manuscript_sha256`が現在の原稿hashと一致することを確認する。
4. `status: approved`の未解決指摘が一件以上あることを確認する。`verdict: pass`でも、ユーザーがOPTIONAL指摘を明示的に承認した場合はRevisionできる。
5. Specが未承認、Reviewが古い、対象が曖昧、または承認済み指摘がない場合は原稿を変更せず、Spec承認、再Review、または指摘承認を案内する。

`proposed`、`rejected`、`resolved`な指摘はRevision対象にしない。

### 2. 修正範囲を固定する

各approved指摘について、location、issue、evidence、recommendationとRecommended Revision Scopeから必要最小限の変更範囲を特定する。

- 対象外の文章、見出し、順序、voiceを維持する。
- 「もっと良くできる」だけを理由に章や記事全体を書き直さない。
- 一つの局所修正で複数指摘を解決できても、未承認指摘を暗黙に解決扱いにしない。
- 承認指摘がCreative Contract変更を要求する場合は修正せず、Spec側の判断が必要であることを伝える。

### 3. Revisionを適用する

1. approved指摘だけを原稿へ反映する。
2. 差分を読み、対象外を変更していないことを確認する。
3. continuity regression、POV、tense、明示制約を再確認する。
4. `scripts/creative_lint.py`があれば実行する。新しいlint errorが出た場合は完了扱いにしない。
5. 正常に反映した指摘だけを`status: resolved`へ変更する。
6. Reviewの`manuscript_sha256`を修正後原稿のhashへ更新する。未適用のapproved指摘がなければ`revision_status: applied`にし、残っていれば`pending`のままにする。
7. 対応taskのチェック状態は変えず、`Acceptance: pending`へ変更する。

一部だけ成功した場合は成功した指摘だけをresolvedにし、未適用のapproved指摘と理由を残す。`revision_status`を`applied`にしない。Revision後にcontinuity、summary、canon、Outlineを更新しない。

### 4. Revision受理を処理する

ユーザーが対象となる修正版原稿を現在の会話で確認し、明示的に受け入れた場合だけ実行する。文脈のない「OK」や対象が不明な承認では受理しない。

1. Reviewのhashと現在の原稿hashが一致することを確認する。taskが`Acceptance: accepted`かつReviewが`revision_status: accepted`なら、同じhashを再同期せず終了する。
2. 未処理のBLOCKER、MAJOR、MINOR指摘がないことを確認する。`proposed`は承認または却下を求め、`approved`はRevision完了を求める。
3. まだ受理されていない場合は、Reviewの`revision_status`が`applied`で、taskの`Acceptance`が`pending`であることを確認する。
4. `../creative-draft/SKILL.md`の「受け入れ済み原稿をreconcileする」に従い、原稿から状態変化を抽出する。
5. continuity、対応Summary、必要なfiction canonを更新する。
6. Narrative Driftを検出し、小さな変更だけをfuture outlineと未完了taskへ反映する。原稿をOutlineへ戻さない。
7. 意味のあるPlan変更なら`design.md`を`draft`へ戻す。Creative Contractまたは構造へ影響する場合は自動反映せず確認する。
8. 状態同期がすべて正常に完了した最後にだけ、taskを`Acceptance: accepted`、Reviewを`revision_status: accepted`にする。

同期が途中で失敗した場合は両方を未受理状態に保ち、原稿は変更しない。

### 5. 応答する

Revision時は変更した指摘ID、原稿範囲、lint結果、未適用指摘、`Acceptance: pending`であることを伝える。受理時は更新したstate、Drift、Plan再承認の要否、Acceptanceとrevision_statusを伝える。
