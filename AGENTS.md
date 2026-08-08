# CreativeSDD 開発ガイド

## 仕様とスコープ

- `SPEC.md` をCreativeSDDの製品仕様の正本とする。設計や実装が競合する場合は`SPEC.md`を優先する。
- 現在の実装フェーズはP2 — Stateである。ユーザーから次フェーズ開始の指示があるまでP3以降へ着手しない。
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
- P3のreview、revise、lint、status、およびP4のREADME、tests、fixtures、example projectを作成しない。
- 状態管理はMarkdownとfilesystem searchで行い、外部DB、RAG、Embeddingを追加しない。
