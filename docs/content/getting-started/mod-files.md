# Modファイル構造

最小構成テンプレートのファイルを解説します。

``` yaml
src
└─main
    ├─java/com/example/examplemod
    │   └─ExampleMod.java
    │
    └─resources
        └─META-INF
            └─mods.toml

gradle.properties
build.gradle
settings.gradle
.gitignore
```

## gradle.properties

`build.gradle`等で使用する設定値を定義するファイルです。

テンプレートではModIDやModの名前を定義しています。

```properties title="gradle.properties"
minecraft_version=1.20.1
forge_version=47.4.10

...

mod_id=examplemod
mod_name=Example Mod
mod_license=All Rights Reserved
mod_version=1.0.0
```

使用箇所(例)

```gradle title="build.gradle" 
dependencies {
    minecraft "net.minecraftforge:forge:${minecraft_version}-${forge_version}"
}
```

## build.gradle

ビルド処理の内容を定義するファイルです。

[#Gradle](../advanced/gradle.md) で詳しく解説しています。

### settings.gradle

プロジェクト全体の設定を定義するファイルです。


## ExampleMod.java

Modの起点となるメインクラスです。

<!-- NOTE: Modクラス解説を追加 -->

## mods.toml

Modの情報をローダーに伝えるためのファイルです。

[Forge Wiki](https://docs.minecraftforge.net/en/1.20.1/gettingstarted/modfiles/) にフォーマットや詳しい情報があります。

ここにも `${...}` となっている部分がありますが、これは `gradle.properties` で定義した値を参照しています。

## .gitignore

Git が管理対象から除外するファイルを定義するファイルです。

例えば、リポジトリには不要な `run` ディレクトリは管理対象から除外する必要があります。
Gradleプラグインのリポジトリなどを記述します。