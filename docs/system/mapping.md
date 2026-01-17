# マッピング

## 資料
[Neoforge - What are Mappings](https://neoforged.net/personal/sciwhiz12/what-are-mappings/)

[SpongePowered - MCP](https://docs.spongepowered.org/stable/en/plugin/internals/mcp.html)

[マッピング - FabricMC](https://wiki.fabricmc.net/ja:tutorial:mappings)

## 難読化とマッピング
Minecraft（Java版）のjarファイルは**難読化**されています。

難読化されたフィールド名、クラス名、メソッド名などは、そのままでは非常に読み解くのが困難です。

これらを開発者が理解できる名前に変換するための対応表を**マッピング**と呼びます。

Forgeでは通常、実行時はSRGマッピングを使用します。

しかし開発環境での実行の時のみ、その環境のマッピングを使用して起動されます。

そのためMixinなどが開発環境と本番環境と動作が異なるということが発生する。

そのため開発環境のみならず本番環境でもテストする必要があります。

## SRG

バージョン間で名前が変わってしまうため、共通化するのが目的の中間マッピングです。

`m_286052_`や`f_90981_`等のように表記されます。

## マッピングの種類(Forge)

### MCP (Mod Coder Pack)
古くから使われているコミュニティ主導のマッピングです。SRG名を経由する仕組みが特徴です。

Forge等は内部処理でSRG名を使用しているため、エラーログ等で見かけることがあります。

### Official Mappings (Mojang Mappings)
Mojang公式のマッピングです。現在のMOD開発の主流ですが、引数名やローカル変数名までは復元されません。

### Parchment
Official Mappingsを拡張し、**引数名やローカル変数名を読みやすくした**マッピングです。

Official Mappingsと互換性があるため、開発の途中から導入しても基本的に問題ありません。

## Parchmentの導入方法(1.20.1)

1. プロジェクト直下の `settings.gradle` に以下の maven リポジトリを追加します。
    ```diff title="settings.gradle"
    pluginManagement {
        repositories {
    +       maven { url = 'https://maven.parchmentmc.org' }
        }
    }
    ```
2. `build.gradle` でプラグインを適用します。
    ```diff title="build.gradle"
    plugins {
        id 'net.minecraftforge.gradle' version '[6.0.16,6.2)'
    +   id 'org.parchmentmc.librarian.forgegradle' version '1.+'
    }
    ```

    !!! warning
        必ず `net.minecraftforge.gradle` の下に追加してください。

3. マッピング設定を変更します。
```diff title="build.gradle"
minecraft {
-    mappings channel: 'official', version: '1.20.1'
+    mappings channel: 'parchment', version: '2023.09.03-1.20.1'
}
```
`mapping_channel` などと変数で指定されている場合は、`gradle.properties` から編集してください。

!!! note "バージョンの指定について"

    上記は1.20.1の例（`2023.09.03-1.20.1`）です。
    [ParchmentMC 公式サイト](https://parchmentmc.org) や [Mavenブラウザ](https://ldtteam.jfrog.io/ui/native/parchmentmc-public/org/parchmentmc/data/) で、使用しているMinecraftバージョンに対応するParchmentバージョンを確認して設定してください。

4. Gradleの更新
    設定を変更したら、Gradleプロジェクトをリフレッシュ、もしくは同期してください。IDE上で変更が反映されるはずです。

## Parchmentの導入方法(Neoforge)

以下を参照してください。

https://docs.neoforged.net/toolchain/docs/parchment/
