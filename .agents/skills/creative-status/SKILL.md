---
name: creative-status
description: 既存のCreativeSDD Markdown artifactと決定論的lint結果を読み、Spec・Plan・task完了・原稿受理・Review verdict・Revision statusを分離して現在地と次に可能な操作を表示する。プロジェクト状況、進捗、blocker、次の推奨操作を確認するときに使う。
---

# Creative Status

保存済みartifactだけから現在状態を読み取り、創作内容や状態を一切変更せず表示する。

## 出力と境界

- `AGENTS.md`、`.creative/work/`、`manuscript/`、必要ならGit差分を読む。
- `scripts/creative_lint.py`があれば実行し、結果を表示へ含める。
- artifact、原稿、チェックボックス、承認状態を作成・更新しない。
- 不明な状態を推測でapproved、accepted、resolvedにしない。

## 状態の読み分け

次を別々に表示する。

- Spec: `spec.md`の`status`
- Plan: `design.md`の`status`
- Task completion: `tasks.md`のチェックボックス
- Manuscript acceptance: taskの`Acceptance`。欠落は`pending`
- Review result: Reviewの`verdict`
- Finding approval: 各指摘の`status`
- Revision state: Reviewの`revision_status`
- Review currency: Reviewの`manuscript_sha256`と現在の原稿hashの一致

一つの状態から別の状態を推測しない。例えばtaskが完了でもacceptedとは限らず、`verdict: pass`でもacceptedとは限らない。

## 現在Phaseを判断する

最初に該当する状態を使う。

1. lint errorあり: `blocked`
2. Specなし: `discovery`
3. Specがdraft: `spec_approval`
4. Planなし: `planning`
5. Planがdraft: `plan_approval`
6. 完了原稿にReviewなし、またはReviewがstale: `review`
7. BLOCKER、MAJOR、MINORの`proposed`指摘あり: `finding_approval`
8. `approved`の未解決指摘あり: `revision`
9. `revision_status: applied`かつAcceptance pending: `revision_acceptance`
10. `verdict: pass`、または必須指摘がすべて`rejected`で、Acceptance pending: `manuscript_acceptance`
11. 実行可能な未完了taskあり: `drafting`
12. 全task完了・accepted: `complete`

Planがdraftでも、既存原稿のReviewやRevisionは可能である。次の新規DraftにはPlan再承認が必要であることを別途示す。

## 次に可能な操作を判断する

- Reviewなしまたはstale: `creative-review <task-id>`
- proposed指摘あり: Review指摘を確認・承認または却下。必須指摘をすべて却下した場合は、元の原稿を受理するか再Reviewする
- approved指摘あり: `creative-revise <task-id>`
- Revision applied: 修正版原稿を確認し、明示的に受理
- Review passでAcceptance pending: 原稿を確認し、明示的に受理
- Plan draft: `creative-plan`で提示・再承認
- 承認済みPlanに実行可能taskあり: `creative-draft <task-id>`
- lint error: 対応する構造エラーを解消

依存関係を満たさないtaskを実行可能と表示しない。複数候補がある場合は一つを断定せず候補を列挙する。

## 応答形式

日本語で簡潔に次を表示する。

```text
CreativeSDD Status

作品:
Phase:
Spec:
Plan:
Task完了:
原稿受理:
Review:
Revision:
Lint:
未解決事項:
次に可能な操作:
```

存在しない情報は「不明」または「なし」と明示する。表示のためにartifactを補完しない。
