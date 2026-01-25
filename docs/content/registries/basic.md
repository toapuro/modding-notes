# レジストリ

レジストリとは、ID (`ResourceLocation`) とオブジェクト（アイテムやブロックなど）を紐づけて管理する仕組みです。

登録されたオブジェクトをレジストリと呼び分けるため、**レジストリエントリ**と呼称します。

レジストリエントリのIDは、同じレジストリの中では**一意**である必要があります。

どのようにレジストリに登録するか見てみましょう。
例としてアイテムの登録を挙げてみます。

```java title="ModItems.java"
public class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MODID);

    // "example_item"というIDとして仮登録
    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () -> new Item(new Item.Properties()));
}
```

```java title="ExampleMod.java"
public class ExampleMod {
    public static final String MODID = "examplemod";
    
    // Neoforge / 1.20.1 Forge (3.10以降) (1)
    public ExampleMod(FMLJavaModLoadingContext context) {
        IEventBus modBus = context.getModEventBus();

        // 登録
        ModItems.ITEMS.register(modBus);
    }
    
    // else
    @SuppressWarnings("removal")
    public ExampleMod() {
        this(FMLJavaModLoadingContext.get());
    }
}
``` 

1. コンストラクタについては [#Modクラス](../getting-started/mod.md) を参照

!!! warning

    `.register(modBus)` の書き忘れに注意！

## 登録方法

### DeferredRegister

`DeferredRegister` はレジストリの登録内容を保持して、レジストリが初期化される `RegistryEvent` のタイミングで登録します。

名前通り遅延して登録するものです。

```java
public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(
        // レジストリを指定
        ForgeRegistries.ITEMS,
        // MODID
        ExampleMod.MODID
);
```

第一引数は以下から指定できます。

- `ForgeRegistries.*`: Forgeで用意されているレジストリ
- `ForgeRegistries.Keys.*`
- `Registries.*`: バニラレジストリ

`DeferredRegister` は情報を保持しているだけなので、最後に実際に `RegistryEvent` に紐づける必要があります。

```java
ModItems.ITEMS.register(modBus);
```

#### RegistryObject

`DeferredRegister` が扱う、登録後に取得可能になるレジストリエントリへの参照を保持するラッパー。

```java
public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () -> new Item(new Item.Properties()));
```

`EXAMPLE_ITEM.get()` で実体を取得できます。

!!! danger

    実際の登録前に中身にアクセスすると例外が発生するため注意です。
    
    例外: `Registry Object not present: ...`

### RegisterEvent

RegisterEvent を使ってレジストリに登録することも可能ですが、通常はあまり使用されません。

```java
@SubscribeEvent // Modイベントバスで登録
public void register(RegisterEvent event) {
    event.register(
        ForgeRegistries.Keys.BLOCKS,
        helper -> {
            helper.register(ResourceLocation.fromNamespaceAndPath(MODID, "example_block_1"), new Block(...));
            helper.register(ResourceLocation.fromNamespaceAndPath(MODID, "example_block_2"), new Block(...));
            helper.register(ResourceLocation.fromNamespaceAndPath(MODID, "example_block_3"), new Block(...));
            // ...
        }
    );
}
```
!!! info
    
    `ResourceLocation.fromNamespaceAndPath` は Forge1.20.1(47.3.10) 以降または Neoforge でサポートされています。未サポートの場合 `new ResourceLocation` を利用してください。

参考:

- [RegisterEvent - Forge](https://docs.minecraftforge.net/en/latest/concepts/registries/#registerevent)

- [RegisterEvent - Neoforge](https://docs.neoforged.net/docs/concepts/registries#registerevent)

## レジストリエントリの取得

特定のレジストリエントリを取得するためには対象の `ResourceLocation` が必要です。

逆の操作も可能で、レジストリエントリから `ResourceLocation` を取得することができます。

```java
// ResourceLocation -> Block
BuiltInRegistries.BLOCKS.get(ResourceLocation.fromNamespaceAndPath("minecraft", "stone"));

// Block -> ResourceLocation
BuiltInRegistries.BLOCKS.getKey(Blocks.STONE);

// 対象のエントリが存在するか
BuiltInRegistries.BLOCKS.containsKey(ResourceLocation.fromNamespaceAndPath("yourmod", "custom_block"))
```

!!! warning

    必ずレジストリ初期化後に実行してください。

レジストリに登録されたすべてのエントリに対して処理をすることもできます。

```java
for (ResourceLocation id : BuiltInRegistries.BLOCKS.keySet()) {
    // ...
}
for (Map.Entry<ResourceKey<Block>, Block> entry : BuiltInRegistries.BLOCKS.entrySet()) {
    // ...
}
```

## カスタムレジストリの作成

`RegistryBuilder` を使いレジストリの設定をします。

```java
private static final ResourceLocation CUSTOM_REGISTRY_ID = ResourceLocation.fromNamespaceAndPath("yourmodid", "custom_id");
public static final RegistryBuilder<Spell> CUSTOM_REGISTRY = RegistryBuilder.<Spell>of(CUSTOM_REGISTRY_ID)
        // 数値IDの割り当てられる範囲
        .setIDRange(0, Integer.MAX_VALUE) // = .setMaxID(Integer.MAX_VALUE)

        // クライアントとの数値IDの同期を無効化
        // .disableSync()

        // 存在しない場合に置き換えられるエントリ。任意
        .setDefaultKey(ResourceLocation.fromNamespaceAndPath("yourmodid", "empty"));
```

```java
@SubscribeEvent // Modバスに登録
public static void registerRegistries(NewRegistryEvent event) {
    event.register(CUSTOM_REGISTRY);
}
```

### データパックレジストリ

データパックでエントリを追加することができるレジストリ。

```java
@SubscribeEvent // Modバスに登録
public static void registerDatapackRegistries(DataPackRegistryEvent.NewRegistry event) {
        event.dataPackRegistry(
                ResourceKey.createRegistryKey(CUSTOM_REGISTRY_ID),
                Spell.CODEC
        );
    }
```

