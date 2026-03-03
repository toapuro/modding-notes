# Git のセットアップ

バージョン管理は Mod 開発において必須ではありませんが、変更履歴の追跡やバックアップとして非常に役立ちます。
ここでは Git の初期設定から GitHub へのプッシュまでの基本的な流れを説明します。

!!! note
    このセクションでは、マウスによる GUI 操作ではなく、コマンドラインを用いた CLI 操作が主体となります。
    Windows の場合は **Windows Terminal** 、 macOS の場合は **ターミナル** の使用を推奨します。

## Git のインストール

=== "Windows"

    PowerShell やコマンドプロンプトから、 Winget 経由でインストールします。

    ```shell
    winget install --id Git.Git -e --source winget
    ```

    あるいは、 [Git for Windows](https://github.com/git-for-windows/git/releases/latest) から直接入手することもできます。

=== "macOS"

    [Homebrew](https://brew.sh/ja/) をセットアップ後、以下のコマンドをターミナルで実行してインストールします。

    ```shell
    brew install git
    ```

    その他のインストール方法については [git-scm](https://git-scm.com/install/mac) を参照してください。

=== "Linux"

    各パッケージマネージャを使ってインストールします。

    ```shell
    # Ubuntu / Debian
    sudo apt update && sudo apt install git

    # Fedora
    sudo dnf install git
    ```

    その他のディストリビューションについては [git-scm](https://git-scm.com/install/linux) を参照してください。

### 初期設定

インストール後、まずユーザー情報を設定します。コミットにこの情報が記録されます。

```shell
git config --global user.name "名前"
git config --global user.email "メールアドレス"
```

!!! danger "Danger: メールアドレスの流出に注意"
    ここで設定した名前及びメールアドレスは、公開リポジトリにプッシュしたコミットから**誰でも確認できます**。
    個人のメールアドレスを使用する代わりに、GitHub から提供されている `noreply` アドレスを使うことを推奨します。
    詳しくは [#メールアドレスを公開しない](#メールアドレスを公開しない) を参照してください。

設定が反映されているか確認するには、以下のコマンドを使います。

```shell
git config user.name
git config user.email
```

## GitHub CLI のインストール

**GitHub CLI (`gh`)** を使うと、手間のかかる GitHub 認証を簡単に済ませたり、 GitHub 関連の操作をコマンドラインから直接行ったりすることができます。

=== "Windows"

    Winget 経由でインストールします。

    ```shell
    winget install --id GitHub.cli
    ```

    あるいは、 [リリースページ](https://github.com/cli/cli/releases/latest) から直接入手してください。

=== "macOS"

    Homebrew 経由でインストールします。

    ```shell
    brew install gh
    ```

    あるいは、 [リリースページ](https://github.com/cli/cli/releases/latest) から直接入手してください。

=== "Linux"

    ディストリビューションによって手順が異なります。

    ```shell
    # Ubuntu / Debian
    (type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
        && sudo mkdir -p -m 755 /etc/apt/keyrings \
        && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
        && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
        && sudo mkdir -p -m 755 /etc/apt/sources.list.d \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
        && sudo apt update \
        && sudo apt install gh -y

    # Fedora (DNF5)
    sudo dnf install dnf5-plugins
    sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
    sudo dnf install gh --repo gh-cli
    ```

    詳細は [GitHub CLI のドキュメント](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) を参照してください。

インストール後、 `gh auth login` を実行してログインします。

```
$ gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: XXXX-XXXX
Press Enter to open https://github.com/login/device in your browser...
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
! Authentication credentials saved in plain text
✓ Logged in as <username>
```

## Git の基本操作

### リポジトリのクローン

GitHub などで公開されているパブリックリポジトリは、誰でもクローンしてローカルで作業を始めることができます。

```shell
# カレントディレクトリにリポジトリをクローン
git clone https://github.com/<ユーザー名>/<リポジトリ名>

# GitHub CLI でも同様に操作できます
gh repo clone <ユーザー名>/<リポジトリ名>
```

プライベートリポジトリについては、 GitHub CLI 等での認証が済んでいれば、同様にクローンできます。

一般に、GitHub側のリポジトリを **リモートリポジトリ** 、クローンした手元のリポジトリを **ローカルリポジトリ** と呼びます。

### リポジトリへの変更

ローカルで変更を加えても、そのままでは GitHub へ反映できません。

Git リポジトリ上で変更は **コミット** という単位で管理されます。

変更は、まず **ステージング** してからコミットする必要があります。

```shell
# 変更をステージング
git add <ファイル>

# カレントディレクトリ配下の変更をすべてステージング
git add .
```

```shell
# ステージングした変更をコミット
git commit -m "コミットメッセージ"
```

これでコミットがローカルの Git リポジトリに記録されました。

リモートに反映するには、プッシュします。

```shell
# 現在のブランチをリモートにプッシュ
git push

# または
git push origin <ブランチ名>
```

GitHub 上のリモートリポジトリにコミットをプッシュできるのは、そのリポジトリの所有者とコラボレーターだけです。
他人のリポジトリに変更を提案するときは、 GitHub 上でフォークしたリポジトリへ変更を加え、プルリクエストを送信するのが一般的です。

### リポジトリの更新

リモートリポジトリの最新の履歴を取得するには、フェッチします。これはローカルの作業ブランチには影響しません。

```shell
# リモートの変更を取得
git fetch
```

変更を取得して現在のブランチに統合するには、プルします。

```shell
# 変更をフェッチしてマージ
git pull
```

特に共同開発においては、 `git pull` で他の人との整合性を取ってから変更を加えることが重要です。

### 基本的なワークフロー

日常的によく使うコマンドをまとめます。

| コマンド | 内容 |
| --- | --- |
| `git status` | 変更のあるファイルを確認 |
| `git diff` | 変更内容の差分を確認 |
| `git log --graph --oneline --all` | コミット履歴を確認 |
| `git add .` | カレントディレクトリ配下の変更をステージング |
| `git commit -m "コメント"` | ステージングした変更をコミット |
| `git pull` | リモートの変更を取得 |
| `git push` | リモートにプッシュ |

!!! tip
    IntelliJ IDEA には Git の GUI クライアントが内蔵されています。
    視覚的にコミット・プッシュ・差分確認などの操作ができるため、ぜひ活用してください。

### .gitignore の設定

`.gitignore` に記載したパターンのファイルは Git の追跡対象から除外されます。
ビルド成果物や IDE の設定ファイルなど、リポジトリに含めたくないものを指定しておきましょう。

Forge / NeoForge などのテンプレートを使っている場合はあらかじめ `.gitignore` が用意されています。

!!! note
    コミット済みのファイルは、後から `.gitignore` を書き換えても追跡され続けます。

## メールアドレスを公開しない

Git の設定に使ったメールアドレスはコミットに埋め込まれ、 `git log` などで参照できます。
公開リポジトリにプッシュすると、コミット履歴から誰でも確認できる状態になってしまいます。

### noreply アドレスを使う（推奨）

GitHub はプライバシー保護のために **noreply アドレス** を提供しています。

1. GitHub の [**Settings > Emails**](https://github.com/settings/emails) を開く
2. **Keep my email addresses private** にチェックを入れる
3. \[任意\] **Block command line pushes that expose my email** にチェックを入れる
  - 有効にすると、 GitHub に登録済みのアドレスでコミットした場合にプッシュが拒否されるようになります
4. 表示される `xxxxxxxxxx+username@users.noreply.github.com` 形式のアドレスをコピーする

```shell
git config --global user.email "xxxxxxxxxx+username@users.noreply.github.com"
```

これで今後のコミットには実際のアドレスが含まれなくなります。

### リポジトリごとに設定を使い分ける

用途によってアドレスを分けたい場合は、リポジトリのルートで `--global` なしでコマンドを実行します。
ローカル設定はグローバル設定より優先されます。

```shell
git config user.email "work@example.com"
```

### すでに流出してしまった場合

!!! warning "Warning: force-push では解決しない"
    GitHub はプッシュされたコミットをほぼすべて保持しています。
    `git push --force` で履歴を書き換えても、コミットハッシュがわかれば元のコミットは参照可能な場合があります。

すでに公開してしまったメールアドレスを確実に消し去る方法は、**リポジトリを削除・再作成**することです。
そうならないよう、くれぐれも注意してください。

いずれの場合も、まず **今後のコミットに正しいアドレスが使われるよう設定を直す** ことが最優先となります。
