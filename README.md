# Forge Modding Notes

主にMinecraft Forge 1.20.1のModdingについて解説したサイトです。

## セットアップ

パッケージ管理のため、[uvのインストール](https://docs.astral.sh/uv/getting-started/installation/)が必要です。

macOS/Linux:
```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```shell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

依存関係をインストールするには:
```shell
$ uv sync
```

## ビルド

HTMLにビルドする場合以下のコマンドを実行してください。
```shell
$ uv run mkdocs build
```

開発中のドキュメントを見る場合、以下のコマンドを実行します。
```shell
$ uv run mkdocs serve
```