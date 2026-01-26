# Gradle

Gradle とは、Javaビルドに使用されるツールです。

そして、そのGradleの設定ファイルを記述できるのがGroovy(もしくはKotlin DSL)です。

Groovyもプログラミング言語であるので、一つ一つ見ていくとブラックボックスではなくどれも意味があることがわかります。

1.20.1の Forge の [build.gradle](https://github.com/MinecraftForge/MinecraftForge/blob/1.20.1/mdk/build.gradle) を例に説明していきます。

コード中に出てくる `mod_id` や `minecraft_version` などの変数は、同階層にある `gradle.properties` ファイルで定義されている値を参照しています。

### プラグイン設定

```gradle title="build.gradle"
plugins {
    id 'eclipse' // Eclipse IDE
    id 'idea' // Intellij IDEA
    id 'maven-publish' // Maven公開用
    id 'net.minecraftforge.gradle' version '[6.0,6.2)' // ForgeGradle
}
```
Gradle プラグインという、Gradle を拡張するツールを記述する部分です。

マイクラの関連では ForgeGradle, MixinGradle 等があります。

例えば ForgeGradle では

- Minecaft のソースコードのダウンロード
- 難読化の解除(リマップ)
- 開発用クライアントの起動設定

などの作業を、Gradle が自動で行ってくれます。

```gradle title="build.gradle"
minecraft {
    mappings channel: mapping_channel, version: mapping_version
}
```
ここは開発環境のマッピングを指定しています。
[#マッピング](./mapping.md)で解説していますが、

クラス名やメソッド名、フィールド名等を読みやすくするための物です。

### 開発環境でのマイクラの設定

```gradle title="build.gradle"
minecraft {
    runs {
        configureEach {
            workingDirectory project.file('run')

            property 'forge.logging.markers', 'REGISTRIES'

            property 'forge.logging.console.level', 'debug'

            mods {
                "${mod_id}" {
                    source sourceSets.main
                }
            }
        }

        client {
            property 'forge.enabledGameTestNamespaces', mod_id
        }

        server {
            property 'forge.enabledGameTestNamespaces', mod_id
            args '--nogui'
        }

        gameTestServer {
            property 'forge.enabledGameTestNamespaces', mod_id
        }

        data {
            workingDirectory project.file('run-data')

            args '--mod', mod_id, '--all', '--output', file('src/generated/resources/'), '--existing', file('src/main/resources/')
        }
    }
}
```

ここは開発環境の実行の設定について書いてある部分です。

`client` なら `runClient` タスク、 `server` なら `runServer` タスクに対応します。他も同様です。

```gradle title="build.gradle"
sourceSets.main.resources { srcDir 'src/generated/resources' }
```

Datagen の生成結果をリソースとして追加する処理です。

```gradle title="build.gradle"
repositories {
    maven {
        url "https://cursemaven.com"
    }
}

dependencies {
    minecraft "net.minecraftforge:forge:${minecraft_version}-${forge_version}"

    implementation fg.deobf("curse.maven:jei-238222:7391695")
}
```

依存関係を設定する部分です。

`dependencies` に記述された依存関係は、`repositories`ブロックの中に記述されたレポジトリから参照してきます。

この例では Cursemaven をリポジトリとして登録し、JEI を依存関係として登録しています。

詳しくは [#依存関係](../getting-started/dependency.md) を参照してください。

以下他の設定
```gradle title="build.gradle"
/**
    mods.tomlにあるテンプレートリテラルを実際の値に置き換える処理
*/
tasks.named('processResources', ProcessResources).configure {
    var replaceProperties = [
            minecraft_version: minecraft_version, minecraft_version_range: minecraft_version_range,
            forge_version: forge_version, forge_version_range: forge_version_range,
            loader_version_range: loader_version_range,
            mod_id: mod_id, mod_name: mod_name, mod_license: mod_license, mod_version: mod_version,
            mod_authors: mod_authors, mod_description: mod_description,
    ]
    inputs.properties replaceProperties

    filesMatching(['META-INF/mods.toml', 'pack.mcmeta']) {
        expand replaceProperties + [project: project]
    }
}

/**
    Jarファイルのメタデータを設定
*/
tasks.named('jar', Jar).configure {
    manifest {
        attributes([
                'Specification-Title'     : mod_id,
                'Specification-Vendor'    : mod_authors,
                'Specification-Version'   : '1', // We are version 1 of ourselves
                'Implementation-Title'    : project.name,
                'Implementation-Version'  : project.jar.archiveVersion,
                'Implementation-Vendor'   : mod_authors,
                'Implementation-Timestamp': new Date().format("yyyy-MM-dd'T'HH:mm:ssZ")
        ])
    }

    finalizedBy 'reobfJar'
}

/**
    パブリッシング設定
*/
publishing {
    publications {
        register('mavenJava', MavenPublication) {
            artifact jar
        }
    }
    repositories {
        maven {
            url "file://${project.projectDir}/mcmodsrepo"
        }
    }
}

/**
    Javaコンパイル時のエンコーディングをUTF-8に設定
*/
tasks.withType(JavaCompile).configureEach {
    options.encoding = 'UTF-8'
}
```
