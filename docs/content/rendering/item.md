# アイテムのレンダリング

アイテムのレンダリングをカスタムする大まかな方法は二つあります。

## カスタムレンダラーを作成する

### レンダラーの作成

`BlockEntityWithoutLevelRenderer` の継承クラスを作る。

```java
class ExampleItemRenderer extends BlockEntityWithoutLevelRenderer {

    public ExampleItemRenderer(BlockEntityRenderDispatcher dispatcher, EntityModelSet modelSet) {
        super(dispatcher, modelSet);
    }

    @Override
    public void renderByItem(ItemStack itemStackIn, ItemDisplayContext type, PoseStack poseStack, MultiBufferSource bufferSource, int packedLight, int packedOverlay) {
        // レンダリング
    }
}
```



### Itemに登録

`Item#initializeClient` メソッドをオーバーライドし、
`consumer.accept` に `IClientItemExtensions` の実装を渡します。

例では匿名クラスを使用してとうろくしています。

```java
public class ExampleItem extends Item {
    public ExampleItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public void initializeClient(Consumer<IClientItemExtensions> consumer) {
        consumer.accept(
            new IClientItemExtensions() {
                private final BlockEntityWithoutLevelRenderer renderer = new ExampleItemRenderer(
                    Minecraft.getInstance().getBlockEntityRenderDispatcher(),
                    Minecraft.getInstance().getEntityModels()
                );

                @Override
                public BlockEntityWithoutLevelRenderer getCustomRenderer() {
                    return renderer;
                }
            }
        );
    }
}
```