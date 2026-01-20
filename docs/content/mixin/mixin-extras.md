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