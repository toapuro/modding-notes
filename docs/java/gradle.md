# Gradle

Gradle とは、Java ビルド用のツールです。

そして初心者が真っ先に躓きやすい部分です。

しかしGradleもプログラミング言語であるので、一つ一つ見ていくとブラックボックスではなくどれも意味があることがわかります。

1.20.1の Forge の [build.gradle](https://github.com/MinecraftForge/MinecraftForge/blob/1.20.1/mdk/build.gradle) を例に説明していきます。

```gradle title="build.gradle"

plugins {
    id 'eclipse' // Eclipse IDE
    id 'idea' // Intellij IDEA
    id 'maven-publish' // Maven公開用
    id 'net.minecraftforge.gradle' version '[6.0,6.2)' // ForgeGradle
}
```
Gradle プラグインという、Gradle を拡張するツールを記述する部分です。
マイクラの関連では ForgeGradle, MixinGradle などがあります。

``` title="build.gradle"
minecraft {
    mappings channel: mapping_channel, version: mapping_version

    copyIdeResources = true
}
```
ここは開発環境のマッピングを指定しています。
[#マッピング](../system/mapping.md)で解説していますが、

クラス名やメソッド名、フィールド名等を読みやすくするための物です。

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

```gardle title="build.gradle"
sourceSets.main.resources { srcDir 'src/generated/resources' }
```

datagen の generated リソースを追加。

```gardle title="build.gradle"
repositories {
}

dependencies {
    minecraft "net.minecraftforge:forge:${minecraft_version}-${forge_version}"
}
```

依存関係を設定する部分です。

`dependencies` に記述された依存関係は、`repositories`ブロックの中に記述されたレポジトリから参照してきます。

詳しくは [#依存関係](dependency.md) を参照してください。


```gradle title="build.gradle"
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

tasks.withType(JavaCompile).configureEach {
    options.encoding = 'UTF-8' // Use the UTF-8 charset for Java compilation
}
```
