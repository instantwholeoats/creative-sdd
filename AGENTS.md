# CreativeSDD 開発ガイド

## 仕様とスコープ

- `SPEC.md` をCreativeSDDの製品仕様の正本とする。設計や実装が競合する場合は`SPEC.md`を優先する。
- 現在の実装フェーズはP3 — Qualityである。ユーザーから次フェーズ開始の指示があるまでP4以降へ着手しない。
- 現在指定されている実装フェーズの範囲だけを変更する。将来フェーズの機能を先回りして追加しない。
- 将来の拡張だけを理由に抽象化、設定、依存関係、常駐処理を増やさない。Markdown、filesystem convention、Codex Agent Skillなど、要件を満たす最も単純な方法を優先する。

## 言語と命名

- 人間が読む自然言語は、原則として日本語で記述する。
- ファイル名、ディレクトリ名、YAML key、enum、コード上の識別子など、機械が扱う名前は英語にする。

## プロダクト原則

- CreativeSDDの中心はConversation-Driven Specificationである。人間の曖昧な創作意図から、AIとの対話を通じて必要十分なCreative Specを発見する。
- ユーザーに`brief.md`や`spec.md`などの仕様ファイルを書かせない。AIが対話から提案・更新し、重要な境界で人間の承認を得る。
- Discoveryを固定質問票にしない。既知事項、未決定事項、矛盾、影響度を毎回評価し、今必要な1〜3問だけを選ぶ。
- ユーザーの明示事項、AIの推測、暫定判断、意図的な未決定事項を混同しない。

## 原稿規約

- 原稿はリポジトリ直下の`manuscript/`へ、通常のMarkdownとして保存する。`.creative/`配下へ原稿を置かない。
- 小説は原則として一つのWriting Unitを一つのファイルにし、`manuscript/001.md`のような3桁の連番を使う。
- ブログは原則として`manuscript/article.md`へ保存する。複数taskで同じファイルを扱う場合は、各taskの`Boundary`で担当する見出しまたは範囲を明確にする。
- `tasks.md`の各taskには`Output`を記録し、出力先は必ず`manuscript/`配下にする。
- 一度に執筆するのは一つのWriting Taskだけとし、対象外の原稿や同一ファイル内の対象外範囲を変更しない。
- 原稿の作成または更新に成功した場合だけ、対応するtaskを完了扱いにする。
- `outline.md`は未来の予定であり、原稿で成立した事実として扱わない。

## 状態管理規約

- 原稿がユーザーに受け入れられた後だけ、原稿から状態変化を抽出し、`continuity.md`、Unit Summary、必要なfiction canon、将来のOutlineをreconcileする。
- `tasks.md`ではチェックボックスの完了と原稿受理を分け、`Acceptance: pending | accepted`で管理する。この項目がない旧形式のtaskは`pending`とみなす。
- `Acceptance`は必要な状態同期がすべて完了した最後にだけ`accepted`にする。すでに`accepted`で受理後に変更されていない原稿は再同期せず、同じ受理操作を冪等に扱う。原稿を変更した場合は`pending`へ戻す。
- 優先順位は、ユーザーの明示的な現在の指示、受け入れられた原稿上の現実、成立済みCanon、承認済みSpec、Design、Outline、AIの暫定案の順とする。
- Narrative Driftを検出しても、原稿をOutlineへ合わせるために自動修正しない。上位制約に反しない受け入れ済み原稿を尊重し、将来の計画側を調整する。
- OutlineとTaskの`Expected resulting state`は未来の予定であり、Canonical Factとして扱わない。
- `continuity.md`ではCharacter KnowledgeとReader Knowledgeを別の見出しで管理し、推測で同一視しない。
- Fiction Canonは長期的な整合性に必要なファイルだけを作る。原稿で成立した事実、ユーザーが明示的に確定した事実、未来の予定を区別し、予定をCanon化しない。
- Unit Summaryは受け入れ済み原稿の圧縮された参照情報として扱い、原稿にない出来事や状態を追加しない。
- P4のREADME、tests、fixtures、example project、インストール機能を作成しない。
- 状態管理はMarkdownとfilesystem searchで行い、外部DB、RAG、Embeddingを追加しない。

## 品質管理規約

- ReviewはEditorとして行い、原稿を変更しない。Review artifactの`verdict`と各指摘の`status`を、task完了や原稿受理と混同しない。
- ReviewとRevisionは承認済みSpecをCreative Contractとして行う。Planがdrift reconciliationで`draft`へ戻っていても既存原稿には実行できるが、Specが未承認なら実行しない。
- Review指摘は安定したID、`severity: BLOCKER | MAJOR | MINOR | OPTIONAL`、`status: proposed | approved | rejected | resolved`で管理する。
- Revisionは`approved`な指摘だけを必要最小限の範囲で反映し、対象外の文章を維持する。主観的な改善だけを理由に全体を書き直さない。
- `verdict: pass`でも、ユーザーがOPTIONAL指摘を明示的に承認した場合はRevisionできる。未適用のapproved指摘が残る間は`revision_status: applied`にしない。
- Revision後は対応taskの`Acceptance`を`pending`にする。承認済み指摘をすべて適用できた場合だけReview artifactの`revision_status`を`applied`にし、Revisionを原稿受理とみなさない。
- `revision_status`は`not_required | pending | applied | accepted`とし、Reviewの`verdict: pass | revise`とは別に管理する。
- Revisionが明示的に受け入れられた後だけ、P2の状態同期を実行し、最後に`Acceptance: accepted`と`revision_status: accepted`を記録する。
- lintはfrontmatter、heading、ID、path、artifact間の状態整合など決定論的な構造だけを検査する。文学的品質、面白さ、声、創造性を機械判定しない。
- statusは既存のMarkdown artifactとlint結果を読み取り、現在状態と次に可能な操作を提示するだけで、創作内容や状態を変更しない。
