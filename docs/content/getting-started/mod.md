# Modクラス

## 資料

- [Neoforge Wiki](https://docs.neoforged.net/docs/gettingstarted/modfiles#mod-entrypoints)
- [Forge Wiki (Newer)](https://docs.minecraftforge.net/en/latest/gettingstarted/modfiles/#mod-entrypoints)
- [Forge Wiki (Older)](https://docs.minecraftforge.net/en/1.20.1/gettingstarted/modfiles/)

Modクラスは、Modの起点となるクラスで、必要なデータの初期化やレジストリ登録を行います。

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
    
!!! info

    1.20.1以降で開発しているのであれば、基本的にコンストラクタに `FMLJavaModLoadingContext` を入れる書き方の方で大丈夫です。
    元々Neoforgeの機能だったものがForge(47.3.10)で導入されています。

