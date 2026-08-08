# CreativeSDD

CreativeSDDは、あなたが何を書きたいのかをAIとの対話で整理し、それをCreative Specとして保ちながら、小さな単位で執筆・レビュー・修正するための軽量なフレームワークです。

仕様書を自分で書く必要はありません。最初にすることは、ディレクトリを設計することでも、フォームを埋めることでもありません。まずCodexへ、書きたいものを普通の言葉で話してください。

```text
$creative-discovery を使って、近未来の東京で、人間とAIの関係について小説を書きたい。
細かいところはまだ決めていません。
```

CreativeSDDは、すでに分かっていることと未決定事項を分け、今必要な1〜3問だけを選びます。AIの推測を確定事項にせず、結末などを意図的に未決定のまま進めることもできます。

作品種別が分かった後は`profiles/fiction.md`または`profiles/blog.md`を参照します。Profileは小説とブログで見るべき観点を切り替えるためのもので、固定質問票としてすべてを尋ねるものではありません。

## まず使ってみる

動作する小さなプロジェクトを試すには、このRepositoryを取得したディレクトリで次を実行します。Python 3以外の外部依存はありません。

```bash
python3 scripts/creative_lint.py --root examples/fiction-mini
python3 -m unittest discover -s tests -v
```

`examples/fiction-mini`は、承認済みSpecとPlan、未着手の1 Taskだけを持つ例です。完成作品を大量生成するexampleではありません。

Codexを`examples/fiction-mini`で開き、次のように話せます。

```text
$creative-status を使って現在地を確認してください。
```

このexampleはすでにPlan承認まで進んでいるため、次は`$creative-draft`です。自分の作品は`$creative-discovery`から始めてください。

## 創作ワークフロー

1. `$creative-discovery`: 書きたいものを会話で伝えます。Codexが必要な確認だけを行い、`.creative/work/brief.md`へ現在の理解を保存します。
2. `$creative-spec`: 確認済みの理解からCreative Spec案を作ります。案を読んで明示的に承認するまで`status: draft`です。
3. `$creative-plan`: 承認済みSpecからDesign、Outline、Writing Taskを提案します。Plan全体を読んで明示的に承認するまでDraftへ進みません。
4. `$creative-draft`: 承認済みPlanの実行可能なTaskを一つだけ執筆します。原稿は`manuscript/`に保存されますが、この時点の`Acceptance`は`pending`です。
5. 原稿受理: 原稿を確認し、対象を明確にして受け入れます。受理後にだけcontinuity、Unit Summary、必要なcanon、将来のOutlineが原稿上の現実へReconcileされ、最後に`Acceptance: accepted`になります。
6. `$creative-review`: 原稿を変更せず、Creative Contract、continuity、構造、編集面をレビューします。指摘は`proposed`から始まり、修正対象にする指摘を人間が承認します。
7. `$creative-revise`: `approved`な指摘だけを必要最小限の範囲へ反映します。Revision適用は受理ではなく、`Acceptance`は再び`pending`になります。
8. Revision受理: 修正版を明示的に受け入れた後だけReconciliationを再実行し、`Acceptance: accepted`と`revision_status: accepted`を最後に記録します。
9. `$creative-status`: Spec、Plan、Task完了、原稿受理、Review、Revision、lintを混同せず、現在地と次に可能な操作を表示します。状態は変更しません。

Narrative Driftが起きた場合、たとえばOutlineでは「東京へ戻る」予定でも、受け入れた原稿で「横浜に残る」と成立したなら、原稿を予定へ戻しません。上位のCreative Contractに反しない限り原稿を尊重し、continuityと将来計画を調整します。

## Codexへ導入する

Codexは、Repository rootから現在の作業ディレクトリまでにある`.agents/skills`を読み込みます。また、ユーザー共通Skillは`$HOME/.agents/skills`から読み込みます。Skillは`$creative-discovery`のように明示でき、`/skills`でも確認できます。詳細は[公式OpenAIドキュメント](https://developers.openai.com/codex/skills)を参照してください。

### プロジェクト単位で使う（推奨）

新しい作品Repositoryへ、CreativeSDDのSkill、テンプレート、lintをコピーします。`/path/to/creative-sdd`と`/path/to/my-work`は実際の絶対パスへ置き換えてください。以下はCreativeSDDをまだ導入していないRepository向けです。既存の`.agents/skills`、`templates`、`profiles`、`scripts`がある場合は、同名ファイルを確認してから統合してください。

```bash
mkdir -p /path/to/my-work/.agents /path/to/my-work/scripts
cp -R /path/to/creative-sdd/.agents/skills /path/to/my-work/.agents/
cp -R /path/to/creative-sdd/templates /path/to/my-work/
cp -R /path/to/creative-sdd/profiles /path/to/my-work/
cp /path/to/creative-sdd/scripts/creative_lint.py /path/to/my-work/scripts/
```

作品Repositoryに`AGENTS.md`がない場合だけ、作品用の最小ガイドをコピーします。

```bash
test -e /path/to/my-work/AGENTS.md || cp /path/to/creative-sdd/examples/fiction-mini/AGENTS.md /path/to/my-work/AGENTS.md
```

既存の`AGENTS.md`がある場合、このコマンドは上書きしません。CreativeSDDの規約を既存ファイルへ手動で統合してください。コピー後、そのRepositoryをCodexで開きます。

```bash
cd /path/to/my-work
codex
```

最初のプロンプトは次の形で十分です。

```text
$creative-discovery を使って、AIでエンジニアは不要になるという議論への違和感をブログにしたい。
```

Codexが`.creative/work/`と`manuscript/`を必要になった時点で作るため、利用者が`brief.md`や`spec.md`を手書きする必要はありません。

### ユーザー共通Skillとして使う

複数Repositoryで同じSkillを使う場合は、安定した場所に置いたCreativeSDD checkoutからユーザーSkillへsymlinkできます。CodexはsymlinkされたSkill directoryをサポートします。

```bash
mkdir -p "$HOME/.agents/skills"
ln -s /path/to/creative-sdd/.agents/skills/creative-discovery "$HOME/.agents/skills/creative-discovery"
ln -s /path/to/creative-sdd/.agents/skills/creative-spec "$HOME/.agents/skills/creative-spec"
ln -s /path/to/creative-sdd/.agents/skills/creative-plan "$HOME/.agents/skills/creative-plan"
ln -s /path/to/creative-sdd/.agents/skills/creative-draft "$HOME/.agents/skills/creative-draft"
ln -s /path/to/creative-sdd/.agents/skills/creative-review "$HOME/.agents/skills/creative-review"
ln -s /path/to/creative-sdd/.agents/skills/creative-revise "$HOME/.agents/skills/creative-revise"
ln -s /path/to/creative-sdd/.agents/skills/creative-status "$HOME/.agents/skills/creative-status"
```

Skillは自動検出されます。表示されない場合はCodexを再起動してください。作品Repositoryには引き続き`AGENTS.md`と`scripts/creative_lint.py`が必要です。テンプレートとprofileもプロジェクトへコピーしておくと、プロジェクト固有の変更をGitで管理できます。

## 保存されるもの

会話から得たCreative Brief、承認状態、計画、continuity、Reviewは`.creative/work/`に保存されます。作品本文は常に通常のMarkdownとして`manuscript/`へ保存されます。CreativeSDDを外しても、原稿はそのまま読めます。

主要な構成は次のとおりです。

```text
my-work/
├── AGENTS.md
├── .agents/skills/
├── .creative/work/
│   ├── brief.md
│   ├── spec.md
│   ├── design.md
│   ├── outline.md
│   ├── tasks.md
│   ├── continuity.md
│   ├── canon/
│   ├── summaries/
│   └── reviews/
├── manuscript/
└── scripts/creative_lint.py
```

すべてのファイルを最初から作るわけではありません。作品に必要なartifactだけを段階的に作ります。

## 検証と開発

全テスト:

```bash
python3 -m unittest discover -s tests -v
```

lintの正常系:

```bash
python3 scripts/creative_lint.py --root tests/fixtures/fiction-minimal
python3 scripts/creative_lint.py --root tests/fixtures/blog-minimal
```

lintの異常系はテストが一時コピーを壊して、非0終了とerror codeを検証します。fixture自体は再利用可能な正常状態に保ちます。

全Skillの形式、必須テンプレートとprofile、READMEに記載したパス、P0〜P3の承認ゲート、Narrative Drift、Review、Revision受理後のReconciliationも同じテストスイートで検証します。

CreativeSDDはPython標準ライブラリ、Markdown、filesystem conventionだけで動作します。外部DB、RAG、Embedding、独自エージェントランタイム、Webアプリ、公開・配布基盤は含みません。
