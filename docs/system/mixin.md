# Mixin

MinecraftまたはMODのコードを一部改変できる仕組みです。

## 概要

実際に何ができるかコードで解説します。

Mixinの対象クラス
```java title="SomethingLogic.java"
public class SomethingLogic {
    public void process() {
        System.out.println("Proceed");
    }
}
```

Mixinクラス
``` java title="MixinSomethingLogic.java"
// リマッピングオフでSomethingLogicにMixin
@Mixin(value = SomethingLogic.class, remap = false)
public class MixinSomethingLogic {

    // メソッドの最初に注入
    @Inject(method = "process()V", at = @At("HEAD"))
    private void onProcess(CallbackInfo ci) {
        System.out.println("Injected");
    }
}
```

このMixinがSomethingLogicに適用されると、**概念的には**[^1]以下のようになります。
``` java title="SomethingLogic(Injected).java"
public class SomethingLogic {
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

以下を `plugins {}` ブロックの下に追加。
```diff title="build.gradle"
plugins {
    ...
}
+ apply plugin: 'org.spongepowered.mixin'
```

以下を`build.gradle`の`dependencies {}`ブロックの下に追加。
```diff title="build.gradle"
dependencies {
+    annotationProcessor 'org.spongepowered:mixin:0.8.5:processor'
}
```

以下を`src/main/resources/<modid>.mixins.json`に
```json title="<modid>.mixins.json"
{
  "required": true,
  "minVersion": "0.8",
  "package": "<groupId>.mixin",
  "compatibilityLevel": "JAVA_17",
  "mixins": [],
  "client": [],
  "server": [],
  "injectors": {
    "defaultRequire": 1
  }
}
```
`<modid>`や`<groupID>`は適切なものに置き換えてください。

`compatibilityLevel`はJDKバージョンに合わせましょう。(例は1.20.1)

次に、`build.gradle`の`minecraft {}`ブロックの下に以下を追加。
```gradle
mixin {
    add sourceSets.main, "${mod_id}.refmap.json"

    config "${mod_id}.mixins.json"
}
```
`${mod_id}`はそのままで大丈夫です

## Mixinの使い方

実践的なコードですが、以下が参考になるかと思います。

[Mixin Examples - Fabric Wiki](https://wiki.fabricmc.net/tutorial:mixin_examples)

### Mixinクラスの書き方

クラスの前に`@Mixin`を付けることでMixinクラスとなります。

```java
@Mixin(Example.class)
public class ExampleMixin {
}
```

その後、`src/main/resources/<modid>.mixins.json` にクラスを追加しなければいけません。

!!! warning
    サーバー側ではクライアントクラスが読み込まれないので、クライアントとサーバーのMixinを分ける必要があります。

* `mixins`: クライアントとサーバー両方
* `client`: クライアントのみ
* `server`: サーバーのみ

それぞれのMixinに対応する場所にクラスを指定する必要があります。

クラスの指定は、`<modid>.mixins.json`で指定した`"package"`で指定したパッケージからの相対的な場所を指定します。

```java
package io.github.toapuro.example.mixins;

@Mixin(Example.class)
public class ExampleMixin {
}
```

この例では以下のようになります
```json title="<modid>.mixins.json"
{
    "package": "io.github.toapuro.example.mixins",
    "mixins": [
        "ExampleMixin"
    ],
    "client": [],
    "server": []
}
```

まずどこにコードを注入するか、どこのコードを改変するかを指定するための@Atを解説します

### @At

`@At` はどこにコードを注入するかを指定します。

`@At("HEAD")`のように使用します

以下がvalue引数の取りうる主な値です。

| 値 | 説明 |
| :--- | :--- |
| `HEAD` | メソッドの最初 |
| `TAIL` | メソッドの最後の `return` の前 |
| `RETURN` | `return` 文の前 |
| `INVOKE` | 特定のメソッドを呼び出す前 (`target`引数必須) |
| `FIELD` | フィールドアクセス (`target`引数必須) |
| `STORE` | 変数代入 (`@ModifyVariable`のみ) |
| `LOAD` | 変数の取得 (`@ModifyVariable`のみ) |

### 引数(任意)

* `remap`: マッピングを適用するかどうか。バニラクラスではない場合`remap = false`を指定する必要があります。ここで指定した値はMixinクラス内のすべてのインジェクション、`@At`にも影響します。
* `targets`: 対象のクラスが非公開な時や、コンパイル時存在しない場合にFQCN[^2]で指定します
* `priority`: Mixinの優先度。高いほど後に適用される。
* `ordinal`: マッチした中で何番目の

[^2]: FQCNは `パッケージ.クラス名` の形式でクラスを指定する。

### 引数 `value`

詳細な説明が必要なものを解説します。

#### INVOKE

`@At(value = "INVOKE", target = "<descriptor>")`

このように使います。

`target`引数はメソッドのデスクリプタを指定します。

!!! info

    IntellijのMinecraft Developmentプラグインが補完してくれるので、
    すぐ覚える必要はないです。

??? デスクリプタの解説

    **デスクリプタで指定するパッケージは全て区切り文字が`.`ではなく`/`であることに注意**

    **クラスの指定**

    クラスは
    `Lパッケージ/クラス名;`

    このようなフォーマットで記述します。

    例えばオブジェクトであれば以下の様に記述します

    `Ljava/lang/Object;`

    **メソッドの指定**

    ```java
    package io.github.toapuro.example;

    class Example {
        public int add(int a, int b)
        {
            return a + b;
        }
    }
    ```

    `Lio/github/toapuro/example/Example;add(II)I`

    この様に対応します。

    ```java
    package io.github.toapuro.example;

    class Example {
        public String concat(String a, String b)
        {
            return a + b;
        }
    }
    ```

    `Lio/github/toapuro/example/Example;concat(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`
    
    この様に対応します。

    なんとなくイメージできたかと思います。

    | 型 | Descriptor |
    | :--- | :--- |
    | byte | B |
    | char | C |
    | double | D |
    | float | F |
    | int | I |
    | long | J |
    | short | S |
    | boolean | Z |
    | Object | Ljava/lang/Object; |

    配列は`[`を先頭につけます。
    `int[]`であれば`[I`となります。

    後は`boolean` が `Z`、`long` が `J` であることに気をつけておけば大丈夫です。


#### FIELD

`@At(value = "FIELD", target = "<descriptor>")`

このように使用します

これもまたIntellijのMinecraft Developmentプラグインが補完してくれます。

??? フィールドのデクスリプタ指定

    フォーマットは以下の通りです。

    `Lパッケージ/クラス名;フィールド名:フィールド型`

    `Boolean.TRUE`であれば

    `Ljava/lang/Boolean;TRUE:Ljava/lang/Boolean;`

    となります

### インジェクション

インジェクションには種類が幾つかあります。

`@Inject`, `@Redirect`, `@ModifyArg`, `@ModifyArgs`, `@ModifyVariable`, `@ModifyConstant`, `@Overwrite`

これらを使い分けることで、様々なコードの改変が可能になります。

| 名前 | 用法 | 説明 |
| :--- | :--- | :--- |
| `@Inject` | コールバック | 元のメソッドの特定位置に処理を挿入します。 |
| `@Redirect` | リダイレクト | メソッド呼び出しやフィールドアクセスなど、特定の処理を完全に置き換えます。 |
| `@ModifyArg` | 引数変更 | 他のメソッドを呼び出す際の、特定の引数を変更します。 |
| `@ModifyArgs` | 引数変更 | 他のメソッドを呼び出す際の、引数をまとめて変更します。 |
| `@ModifyVariable` | 変数変更 | メソッド内のローカル変数を変更します。 |
| `@ModifyConstant` | 定数変更 | メソッド内の定数値を変更します。 |
| `@Overwrite` | 上書き | メソッドの実装を完全に上書きします。競合のリスクが高いため、基本的には使用しません。 |

引数や用法がほぼ同じものはまとめて解説します。

#### 基本的な使用法

元のメソッドの特定位置に処理を挿入します。

**`method`**

基本、対象のメソッドを引数`method`で指定します。

デスクリプタで指定しますが、引数部分はオーバーロードがない場合省略できます。

またワイルドカードが使用できます。

**`at`**

`@At`で指定します

**`remap`**

難読化を解除するかどうかのフラグです。

バニラクラスが対象ではない場合、`remap = false`を指定する必要があります。

`@Mixin`->`@インジェクション` -> `@At` の順番で `remap` は影響されていきます。

そのため `@Mixin` で `remap = false` を指定し、`@At` で難読化されたものを使用する場合、`@At` で `remap = true` を再指定する必要があります。

これは`@At`のtarget引数を指定する際にも気をつける必要があります。

難読化については [#マッピング](mapping.md) で解説しています。

**`require`**

対象が何個マッチする必要があるのかを指定します。

これを下回る個数しか存在しないような環境の場合、クラッシュします。

例えば`require = 0`では、対象が存在しなくてもクラッシュしません。

#### @Inject

基本的に指定した場所の前にコードが注入されます。

引数は元のメソッドと`CallbackInfo`を組み合わせたものになります。
返り値は`void`。

元のメソッドで`return`をしたい場合引数の`CallbackInfo ci`を使用して`ci.cancel()`と呼びます。

返り値がある場合、
引数の`CallbackInfoReturnable<返り値の型> cir`

!!! tips

    Mixinメソッドの引数や返り値は、Minecraft Developmentプラグインの修正機能（Alt+Enterなど）を使うことで自動生成できます。

特殊な引数

##### **`cancellable`**

キャンセルできるかどうかを指定します。`CallbackInfo#cancel`や`CallbackInfoReturnable#setReturnValue`を使用する場合`true`を指定する必要があります。

##### **`locals`**

ローカル変数に関して指定する引数。

主に以下3つの値を指定できます。(`LocalCapture`)

* `NO_CAPTURE`: キャプチャしない(デフォルト)
* `CAPTURE_FAILSOFT`: キャプチャしますが、失敗した場合スキップ
* `CAPTURE_FAILHARD`: キャプチャしますが、失敗した場合クラッシュ

[#MixinExtrasの利用](#mixinextrasの利用) で解説する `@Local` を利用するとより可読性が高く、より安全です。

##### **`shift`**

インジェクションの場所をちょっと調節できます。

基本指定した場所の前にインジェクションをしますが、`shift`を指定することで後ろにインジェクションをすることができます。

主に以下の4つの値を指定できます(`At.Shift`)

* `NONE`: デフォルト
* `BEFORE`: 指定した場所の前
* `AFTER`: 指定した場所の後ろ

#### @Redirect

対象を丸々置き換える。

!!! warning
    特にMixinが被った場合、競合しクラッシュするので使用は控えましょう。

[#MixinExtrasの利用](#mixinextras) で解説する `@ModifyExpressionValue` で記述すると安全です。

#### @ModifyArg

他のメソッドを呼び出す際の、特定の引数を変更します。

特殊な引数

##### **`index`**

何番目の引数を変更するかを指定します。

基本 `void onCall(Args args)` です。

#### @ModifyArgs

`@ModifyArg` をまとめて1メソッドで行うことができます。

メソッドの引数 `Args` を使用して操作します

#### @ModifyVariable

基本的に`@At("STORE")`や`@At("LOAD")`を指定します。

基本 `型 onCall(型 original)` です。

基本的に型でしか指定できないため、`index` や `name`、@Atの`ordinal` で正確に指定します。

引数(任意)

* `index`: 変数の絶対インデックスを指定(バイトコードを見る必要がある)
* `name`: 変数の名前を指定

#### @Overwrite

メソッドをすべて置き換え。

!!! danger
    互換性が無くなるので、他Modを一切考慮しない場合のみ使用してください。

`@Inject`の`HEAD`でキャンセルすると競合が発生せずに、同じ動作を再現できるので安全です。

### @Shadow

Mixinクラス内部でのみ使用できる、対象クラスのフィールドやメソッドにアクセスするためのアノテーションです。

アクセス修飾子(`private`等)を無視してアクセスできます。

対象が `final` フィールドの場合 `@Final` アノテーションを付ける必要があります。

`@Mutable` を付けることによって `final` も無視して代入できるようになります。

!!! warning

    @Shadowのフィールドには `final` 修飾子を使用してはいけません[^3]。

[^3]: コンパイラの副作用が動作に影響するため

```java
@Shadow
private int exampleValue;

@Mutable
@Shadow @Final
private int finalExampleValue;
```

### @Unique

Mixinクラスで使用でき、対象クラスに存在しないフィールドやメソッドを追加定義する際に使用します。

初期値を設定することもできます。

```java
@Unique
private int example$uniqueValue = 5;

@Unique
private void example$uniqueMethod() {

}
```

基本的に `<modid>$メソッド名` で記述するのが良しとされています。

Mixinは実行時、対象のクラスにマージされているので、メソッド名が被ってしまうと競合し、クラッシュする可能性があるためです。

[#Mixinトリック](#mixinトリック) でこれを応用する方法を解説しています。

### アクセッサー(インターフェース)

資料: [AccessorとInvoker - Fabric](https://wiki.fabricmc.net/ja:tutorial:mixin_accessors)

アクセッサーとは、アクセス修飾子を無視してフィールドやメソッドにアクセスするために使用するMixinインターフェースです。

`@Shadow` とは違って、Mixinクラス以外からもアクセスできます。

アクセッサーは`interface`で定義します。

以下例
```java
@Mixin(Example.class, remap = false)
public interface ExampleAccessor {

    @Accessor("exampleValue")
    int getExampleValue();

    @Mutable
    @Accessor("exampleValue")
    void setExampleValue(int exampleValue);

    @Invoker("handle")
    void invokeHandle(int something);
}

// 使用法

Example example = ...;

((ExampleAccessor)(Object)example).setExampleValue(10);

// もしくは

ExampleAccessor accessor = (ExampleAccessor) example;
accessor.setExampleValue(10);
```

#### @Accessor

フィールドの値を取得/設定できます。

**ゲッター(取得)**

`型 メソッド名();`の形式で定義します

メソッド名はなんでもいいですが、ゲッターメソッドの規則に従って`get<FieldName>`にしておきましょう。

**セッター(設定)**

`void メソッド名(型);`の形式で定義します

これも同様にメソッド名はセッターメソッドの規則に従って `set<FieldName>` にしておきましょう。

!!! warning メソッド名について

    対象のクラスに存在するメソッド名を使用してはいけません。

## MixinExtrasの利用

Mixinでは難しい痒いところに手が届くようなライブラリです。

MixinExtrasのWikiは丁寧なので、そちらも参考にしてください。

[MixinExtras Wiki](https://github.com/LlamaLad7/MixinExtras/wiki)

主に以下のような機能を提供します。

* 追加インジェクション
* 構文糖
* 高度な@At指定

### 導入方法

[Setup - Wiki](https://github.com/LlamaLad7/MixinExtras?tab=readme-ov-file#setup) を参照してください。

!!! info "注意点"

    MixinExtrasを使用するとMixinExtrasがjarに埋め込まれ、Modの容量が増加するため、むやみに導入するのは控えましょう。

### 追加インジェクション

**`@ModifyExpressionValue`**

`@Redirect` をより安全に、より汎用に使えるようにしたもの。

非常に便利です。

対象の式の評価結果を改変できます。

```java
@ModifyExpressionValue(
    method = "targetMethod",
    at = @At(value = "INVOKE", target = "...")
)
private int modifyValue(int original) {
    return original + 5;
}
```

**`@ModifyReceiver`**

対象のメソッドコールのレシーバを改変する。

`receiver.call()` の `receiver` を改変できるということです

書き方は省略します。

**`@ModifyReturnValue`**

メソッドの戻り値を改変する。

`at` は `@At("RETURN")` を指定します。

非常に便利です。

```java
@ModifyReturnValue(
	method = "targetMethod",
	at = @At("RETURN")
)
private float halveSpeed(float original) {
	return original / 2f;
}
```

**`WrapMethod`**

メソッドの全てをラムダ式として覆い、操作できるもの。

try-catchで覆ってメソッドを実行し、例外を抑制したり、そのメソッドを複数回実行する等に使えます。

詳しくは[Wiki](https://github.com/LlamaLad7/MixinExtras/wiki/WrapMethod)で確認してください。

**`@WrapWithCondition`**

ある関数呼び出しをif文で囲って、条件付きで実行させるもの。

詳しくは[Wiki](https://github.com/LlamaLad7/MixinExtras/wiki/WrapWithCondition)で確認してください。

### 構文糖

**`@Cancellable`**

`@ModifyExpressionValue` 等の `CallbackInfo` を引数として取らないインジェクション関数でもキャンセル・返り値の操作が可能になるものです。

引数の最後に `@Cancellable CallbackInfo ci` を追加することで使用できます。(`CallbackInfoReturnable<T>`も可能)

**`@Local`**

`@Inject` の `locals` をより便利にしたもの。

`@Inject` に限らず様々なインジェクションで使えます。非常に便利です。

これも引数の最後に使用します。

更に、`LocalRef<T>` や `LocalIntRef`(プリミティブ) を型として使うことで、ローカル変数を操作することもできます。

引数(任意)
* `ordinal`: 何番目のローカル変数か
* `name`: 変数の名前

詳しくは[Wiki](https://github.com/LlamaLad7/MixinExtras/wiki/Local)で確認してください。

**`@Share`**

Mixin同士でローカル変数を作成しシェアできる機能。

詳しくは[Wiki](https://github.com/LlamaLad7/MixinExtras/wiki/Share)で確認してください。

## Mixinトリック

### Mixinで継承する

対象クラスの継承・実装しているインターフェースをMixinクラスでも継承することで、スーパークラスのメソッドやフィールド等にアクセスすることができます。

コンストラクタを生成する必要がありますが、無視されるため実装して大丈夫です。

!!! info

    対象が抽象クラスの場合、メソッドを実装する必要が出てくるので、Mixinクラスも抽象クラスにしましょう。

```java
@Mixin(Example.class)
public abstract class ExampleMixin extends ExampleParent implements ExampleInterface {
}
```

### Mixinでオーバーライドする

Mixinクラスにあるメソッドやフィールドは基本的に対象クラスにマージされるため、そのままオーバーライドが可能です。

他Modが同じクラスで同じメソッドをオーバーライドした場合競合するため、あまりおすすめできません。

できれば [#ソフトオーバーライド](#ソフトオーバーライド) を使用してください。

```java
public class ExampleParent {
    public void exampleMethod() {
        System.out.println("Super");
    }
}

public class Example extends ExampleParent {
}

@Mixin(Example.class)
public class ExampleMixin extends ExampleParent {
    @Override
    public void exampleMethod() {
        super.exampleMethod();
        System.out.println("Override");
    }
}
```

### Mixinでインターフェースを実装する

Mixinクラスは対象クラスにマージされるため、独自インターフェースを実装することができます。

`@Unique` と組み合わせることで、クラスに任意のデータを付与しアクセスすることができます。

```java
public interface MyInterface {
    void example$exampleMethod();
    String example$getExampleValue();
}

@Mixin(Example.class)
public class ExampleMixin implements MyInterface {
    @Unique
    private String example$exampleValue = "Hello World";

    @Unique
    @Override
    public void example$exampleMethod() {
        System.out.println("Mixin");
    }

    @Unique
    @Override
    public String example$getExampleValue() {
        return example$exampleValue;
    }
}

// 使用法
Example example = ...;
MyInterface myInterface = (MyInterface) example;

myInterface.example$exampleMethod();
System.out.println(myInterface.example$getExampleValue());
```

### ソフトオーバーライド

Mixinメソッドを継承して継承できるシステムを利用したものです。

詳しくは [Mixin Inheritance](https://wiki.fabricmc.net/tutorial:mixinheritance) を参照

`@SoftOverride` はなくても良いですが、有効か検証してくれるので書いておきましょう。

```java
public class ExampleParent {
    protected void exampleMethod() {
        System.out.println("Original");
    }
}

public class Example extends ExampleParent {
}

@Mixin(ExampleParent.class)
public class ExampleParentMixin {

    @Inject(method = "exampleMethod", at = @At("HEAD"))
    protected void injectExampleMethod() {
    }

    @Unique
    protected void example$uniqueMethod() {
        System.out.println("Unique");
    }
}

@Mixin(Example.class)
public class ExampleMixin extends ExampleParentMixin {

    @Override
    @SoftOverride
    protected void injectExampleMethod() {
        System.out.println("Mixin");
    }

    @Override
    @SoftOverride
    protected void example$uniqueMethod() {
        System.out.println("Mixin");
    }
}
```

## 内部の仕組みについて

**Java**

* ラムダ式は `lambda$メソッド名$番号` のフォーマットの名前で関数に変換されます。

**Mixin**

* Mixinクラスは対象のクラスにマージされる。
* Mixinクラスは実行時にはロードできない(アクセッサーは可能)。
