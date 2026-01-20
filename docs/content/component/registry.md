# レジストリ(1.20.1)

レジストリとはアイテム、ブロック、エンティティ等の種類を管理する仕組みです。

## アイテムの作成

まずどうレジストリに登録するか見てみましょう

```java title="ModItems.java"
public class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MODID);

    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () -> new Item(new Item.Properties()));
}
```

次に、`ITEMS` をゲームレジストリに登録する必要があります。

```java title="ExampleMod.java"
public class ExampleMod {
    public static final String MODID = "examplemod";

    public static void init() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();

        ModItems.ITEMS.register(modBus);
    }
}
```

