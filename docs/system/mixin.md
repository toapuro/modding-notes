# Mixin

MinecraftまたはMODのコードを一部改変できる仕組み。

## 概要
実際に何ができるかコードで解説します。

対象クラス
```java title="SomethingLogic.java"
class SomethingLogic {
    public void process() {
        System.out.println("Proceed");
    }
}
```
Mixinサイド
``` java title="MixinSomethingLogic.java"
@Mixin(value = SomethingLogic.class, remap = false)
public class MixinSomethingLogic {

    @Inject(method = "process()V", at = @At("HEAD"))
    private void onProcess(CallbackInfo ci) {
        System.out.println("Injected");
    }
}
```

このように記述できます。

このMixinがSomethingLogicに適応されると、**概念的には**[^1]以下のようになります。
``` java title="SomethingLogic(Injected).java"
class SomethingLogic {
    public void process() {
        onProcess(new CallbackInfo(...))
        System.out.println("Proceed");
    }

    private void onProcess(CallbackInfo ci) {
        System.out.println("Injected");
    }
}
```
[^1]: 実際はonProcessのメソッド名やアノテーションなどが異なる。

## Mixinセットアップ

以下を`build.gradle`の冒頭に追加。
```gradle title="build.gradle"
buildscript {
    repositories {
        maven { url = 'https://repo.spongepowered.org/repository/maven-public/' }
        mavenCentral()
    }
    dependencies {
        classpath 'org.spongepowered:mixingradle:0.7-SNAPSHOT'
    }
}
```

以下を`plugins {}`ブロックの下に追加。
```gradle title="build.gradle"
apply plugin: 'org.spongepowered.mixin'
```

以下を`src/main/resources/$(modid).mixins.json`に
```json title="$(modid).mixins.json"
{
  "required": true,
  "minVersion": "0.8",
  "package": "$(groupId).mixin",
  "compatibilityLevel": "JAVA_17",
  "mixins": [],
  "client": [],
  "server": [],
  "injectors": {
    "defaultRequire": 1
  }
}
```
`$(modid)`はModのIDに置き換え、
`$(groupId)`は実際のグループIDに置き換えてください。


次に、`build.gradle`の`minecraft {}`ブロックの下に以下を追加。
```gradle
mixin {
    add sourceSets.main, "${mod_id}.refmap.json"

    config "${mod_id}.mixins.json"
}
```

