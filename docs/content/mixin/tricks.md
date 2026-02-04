# Mixin

## Mixinトリック

### Mixinで継承する

対象クラスの継承・実装しているインターフェースをMixinクラスでも継承することで、スーパークラスのメソッドやフィールド等にアクセスすることができます。

コンストラクタを生成する必要がありますが、無視されるため実装して大丈夫です。

!!! info

    対象が抽象クラスの場合、メソッドを実装する必要が出てくるので、Mixinクラスも抽象クラスにしましょう。

```java
@Mixin(Example.class)
public abstract class ExampleMixin extends ExampleParent implements ExampleInterface {

    public ExampleMixin(...) {
        super(...);
    }
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
