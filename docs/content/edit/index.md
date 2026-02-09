# Forge Modding Notes の編集方法

## 概要
Forge Modding Notes は、内容の更新、誤字脱字の修正、新しいページの追加など、あらゆる形態のコントリビュートを歓迎します。

このWikiでは、完全性や正確性よりも**共有できる知見**を残すことを目的としています。  
そのため、未完成の状態でも、Draft PR として送っていただければサポートができるかもしれません。

また、誤りがあった場合でも、レビュー時に確認を行うので問題ありません。

この Wiki は [MkDocs](https://www.mkdocs.org/) と [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) を使用して構築されており、GitHub 上で管理されています。

??? info "Git や Python をインストールしていない場合"
    MkDocs は Python で動作するため、実際のサイトでの表示上で確認するにはローカル環境に Python をインストールする必要がありますが、GitHub のウェブエディタを使用することで、ブラウザ上でも編集やプルリクエストの作成が可能です。

    1. 編集したいページの右上にある、鉛筆のアイコンをクリックします。
    2. 編集画面が開くので、初回のみ、緑色の「Fork this repository」ボタンをクリックし、自身のGitHubに**リポジトリをフォーク**します。  
    3. 編集画面がエディタに切り替わり、編集を行えるようになります。  
       この際、「Preview」タブで、Markdown の簡易的なレンダリング結果を確認できます。  
       アドモニションなどの MkDocs や Material for MkDocs に固有の機能は正しく表示されない場合があります。
    4. 編集が終わったら、緑色の 「Commit changes…」 から以下のローカルでの場合と同様に**コミットを作成**します。
    5. コミットの作成が完了すると、そのまま**プルリクエストの作成**画面へ進みます。

??? tip "ブラウザ上で完全なプレビュー環境を利用したい場合"
    GitHub の **Codespaces** を利用すると、ブラウザ上で VSCode と同様のエディタが起動し、Python などの環境構築を自分で行うことなく、本番同様のプレビュー（`mkdocs serve`）を実行できます。
    リポジトリのトップにある、緑色の「Code」ボタンから「Codespaces」タブを選択して作成してください。

---

## 編集の手順

### 1. リポジトリの準備

1.  GitHub の [toapuro/modding-notes](https://github.com/toapuro/modding-notes) をフォークします。
2.  フォークしたリポジトリをローカルにクローンします。
    ```bash title="Terminal"
    git clone https://github.com/<YOUR_USERNAME>/modding-notes.git
    cd modding-notes
    ```

### 2. 編集環境の構築

プレビューを確認するために、Python をインストールしている必要があります。

1.  必要なパッケージをインストールします。
    ```bash title="Terminal"
    pip install -r requirements.txt
    ```

### 3. 内容の編集

1.  **Markdown ファイルの作成・編集**:
    - ドキュメントの本体は `docs/content/` ディレクトリ内にあります。
    - 既存のページを更新するか、新しい `.md` ファイルを作成してください。
2.  **ナビゲーションの更新**:
    - 新しいページを追加した場合は、ルートディレクトリにある `mkdocs.yml` の `nav` セクションに、ナビゲーションに表示されるラベルと、それに対応するファイルパスを追記してください。

### 4. ローカルでのプレビュー

編集した内容をブラウザで確認します。

```bash title="Terminal"
mkdocs serve
```

実行後、 `http://127.0.0.1:8000/modding-notes/content/` にアクセスすると、リアルタイムでプレビューが表示されます。

??? info "リアルタイムプレビューが動作しない場合"
    2026年2月現在、[リアルタイムプレビューが動作しない不具合が報告](https://github.com/squidfunk/mkdocs-material/issues/8478)されています。

    この場合には、`--livereload`オプションを明示的に指定して実行することで、リアルタイムプレビューが動作する可能性があります。

    ```bash title="Terminal"
    mkdocs serve --livereload
    ```

### 5. コミットとプッシュ

変更が完了したら、コミットしてプッシュします。

**コミットメッセージの形式:**
以下のいずれかの形式を使用してください。

- `Add: <内容>` : ドキュメントの新規追加
- `Update: <内容>` : ドキュメントの更新
- `Fix: <内容>` : ドキュメントの誤字脱字や表現の修正、バグの修正
- `Ci: <内容>` : GitHub Actions などの CI 設定の変更

```bash title="Terminal"
git add .
git commit -m "Add: 編集方法のページを追加"
git push origin main
```

### 6. プルリクエストの作成

GitHub 上でオリジナルのリポジトリに対してプルリクエスト（PR）を作成してください。
未完成の状態でも、「Draft PR」として送っていただければサポートできる場合があります。

---

## 文法

原稿は、[Markdown](https://daringfireball.net/projects/markdown/)で記述してください。

基本的には一般的なMarkdownを使用しますが、以下に示すようないくつかの拡張記法が使用可能です。

### コードブロック

以下のように、使用するコンピュータ言語やファイル名を指定することで、シンタックスハイライトの表示や対応ファイルなどの情報を明示できます。

**使用例**

````markdown title="codeblock-example.md"
```java title="Main.java"
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
```
````

**結果**

```java title="Main.java"
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
```

詳細な説明は、 [Code blocks - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/) を参照してください。

### アドモニション

**使用例**

```markdown
!!! info "カスタムのタイトル"
    ここに内容を記述します。
```

**結果**

!!! info "カスタムのタイトル"
    ここに内容を記述します。

詳細な説明は、 [Admonitions - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) を参照してください。

### タブ

**使用例**

```markdown
=== "タブ1"
    タブ1の内容

=== "タブ2"
    タブ2の内容
```

**結果**

=== "タブ1"
    タブ1の内容

=== "タブ2"
    タブ2の内容

詳細な説明は、 [Content tabs - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/) を参照してください。

---

## スタイルガイド

!!! warning "要検討"

## 禁止事項

原稿には、以下の内容を含むことはできません。注意してください

- 他者の著作権を侵害する内容。
- Minecraft の EULA に違反する内容。
