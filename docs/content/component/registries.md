# レジストリ(1.20.1)

レジストリとは、**名前（ID）とオブジェクト（アイテムやブロックなど）を紐づけて管理する仕組み**です。簡単に言えば、名前を登録済みのオブジェクトに結びつける「辞書（マッピング）」の役割を果たしています。

この名前（レジストリ名）は、同じレジストリの中では**一意である（絶対に被らない）**必要があります。
しかし、**レジストリが違えば同じ名前を使うことができます**。

最も一般的な例は「ブロック」と「アイテム」の関係です。
ブロック用レジストリにある `minecraft:stone`（石ブロック）と、アイテム用レジストリにある `minecraft:stone`（石アイテム）は、同じレジストリ名を持っていますが、それぞれ別のレジストリで管理されているため共存できています。





どのようにレジストリに登録するか見てみましょう。

例としてアイテムの登録を挙げます。

```java title="ModItems.java"
public class ModItems {
    // DeferredRegisterを追加
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MODID);

    // 仮登録
    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () -> new Item(new Item.Properties()));
}
```

```java title="ExampleMod.java"
public class ExampleMod {
    public static final String MODID = "examplemod";
    
    // Neoforge / 1.20.1 Forge (3.10以降) // (1)
    public static void init(FMLJavaModLoadingContext context) {
        IEventBus modBus = context.getModEventBus();

        // 登録
        ModItems.ITEMS.register(modBus);
    }
    
    // else
    @SuppressWarnings("removal")
    public static void init() {
        this(FMLJavaModLoadingContext.get());
    }
}
```

1. #modクラスを参照

基本的に `DeferredRegister` でレジストリへの仮登録をし、Modのコンストラクタで実際に登録するために `.register(modBus)` を実行します。


## DeferredRegister

