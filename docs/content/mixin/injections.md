# Mixin

## インジェクション

まずどこにコードを注入するか、どこのコードを改変するかを指定するための@Atを解説します

### @At

`@At` はどこにコードを注入するかを指定します。

`@At("HEAD")`のように使用します

#### 引数

* `value`(必須): 場所の種類
* `remap`: マッピングを適用するかどうか。バニラクラスではない場合`remap = false`を指定する必要があります。ここで指定した値はMixinクラス内のすべてのインジェクション、`@At`にも影響します。
* `targets`: 対象のクラスが非公開な時や、コンパイル時存在しない場合にFQCN[^2]で指定します
* `priority`: Mixinの優先度。高いほど後に適用される。
* `ordinal`: マッチした中で何番目か

以下が`value`引数の取りうる主な値です。

| 値 | 説明 |
| :--- | :--- |
| `HEAD` | メソッドの最初 |
| `TAIL` | メソッドの最後の `return` の前 |
| `RETURN` | `return` 文の前 |
| `INVOKE` | 特定のメソッドを呼び出す前 (`target`引数必須) |
| `FIELD` | フィールドアクセス (`target`引数必須) |
| `STORE` | 変数代入 (`@ModifyVariable`のみ) |
| `LOAD` | 変数の取得 (`@ModifyVariable`のみ) |

[^2]: FQCNは `パッケージ.クラス名` の形式でクラスを指定する。

以下詳細な説明が必要なものを解説します。

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

難読化については [#マッピング](../advanced/mapping.md) で解説しています。

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

[#MixinExtrasの利用](./mixin-extras.md) で解説する `@Local` を利用するとより可読性が高く、より安全です。

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

[#MixinExtrasの利用](#mixinextrasの利用) で解説する `@ModifyExpressionValue` で記述すると安全です。

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

[#Mixinトリック](./tricks.md) でこれを応用する方法を解説しています。

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
