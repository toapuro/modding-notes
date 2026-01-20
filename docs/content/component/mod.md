# Modクラス

Modクラスは、基本的にModの起点となるクラスです。

=== "Neoforge/Forge1.20.1(47.3.10以降)"

    ```java title="ExampleMod.java"
    @Mod(ExampleMod.MODID)
    public class ExampleMod {
        public static final String MODID = "examplemod";

        public ExampleMod(FMLJavaModLoadingContext context) {
            IEventBus modBus = context.getModEventBus();
        }
    }
    ```

=== "Forge(47.3.10以前)"

    ```java title="ExampleMod.java"
    @Mod(ExampleMod.MODID)
    public class ExampleMod {
        public static final String MODID = "examplemod";

        @SuppressWarnings("removal")
        public ExampleMod() {
            IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        }
    }
    ```

