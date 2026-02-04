# モデル

## ビルトイン `parent` モデル

モデルの `"parent"` に指定される、特別なモデル

### builtin/generated

アイテムのテクスチャに合ったモデルが `ItemModelGenerator` によって自動生成されます。

多くのフラットなアイテムはこれによって生成されています。

`item/generated` は `builtin/generated` を親モデルにしており、同じ効果が得られます。

### builtin/entity

`BuiltInModel` としてモデルが登録され、唯一 `IClientItemExtensions`の `getCustomRenderer` が適用されるモデルです。(`BakedModel#isCustomRenderer`が`true`)

その代わりに、モデルが一切描画されません。

## Forge モデルローダー

詳しくは [Custom Model Loader - Neoforge](https://docs.neoforged.net/docs/1.20.4/resources/client/models/modelloaders) を参照してください。

Neoforgeですがネームスペース以外は仕様がほとんど同じです。

| ID | 説明 |
| --- | --- |
| `forge:empty` | 何も描画されない |
| `forge:elements` | `elements`と`transform`で構成されるモデル |
| `forge:obj` | OBJモデルを読み込める。`.obj`と`.mtl`が必要 |
| `forge:fluid_container` | バケツやタンクなど、液体を含むモデル |
| `forge:composite` | 複数のモデルを組み合わせる |
| `forge:item_layers` | レイヤーの数が無制限で、レイヤーごとに `RenderType` を設定可能 |
| `forge:separate_transforms` | 視点によってモデルを変更できる |

## 独自モデルローダーの作成

実行時にモデルを生成して、ロードさせたり、アイテムによってモデルを変更するといったことができます。

以下２つの事が可能です。

### 1. モデル(Quad)を自動生成する

`IUnbakedGeometry#bake` を `SimpleUnbakedGeometry` が事前に定義してくれているため、`addQuads` によるQuadの登録をします。

```java
public class CubeModel extends SimpleUnbakedGeometry<CubeModel> {

    public static final IGeometryLoader<CubeModel> LOADER = CubeModel::deserialize;

    // 別クラスに移動しても良い
    public static CubeModel deserialize(JsonObject json, JsonDeserializationContext context) {
        float size = GsonHelper.getAsFloat(json, "size");

        return new CubeModel(size);
    }

    private final float size;

    public CubeModel(float size) {
        this.size = size;
    }

    @Override
    protected void addQuads(IGeometryBakingContext context, IModelBuilder<?> modelBuilder, ModelBaker modelBaker, Function<Material, TextureAtlasSprite> spriteGetter, ModelState modelState, ResourceLocation modelLocation) {

        List<BlockElement> blockElements = new ArrayList<>();

        Map<Direction, BlockElementFace> faces = new EnumMap<>(Direction.class);

        Material baseLocation = context.getMaterial("base");
        TextureAtlasSprite baseSprite = spriteGetter.apply(baseLocation);
        SpriteContents contents = baseSprite.contents();

        for (Direction face : Direction.values()) {
            faces.put(
                    face,
                    new BlockElementFace(null, -1, baseLocation.texture().toString(), new BlockFaceUV(
                            new float[]{0f, 0f, contents.width(), contents.height()}, 0
                    ))
            );
        }

        blockElements.add(new BlockElement(
                new Vector3f(8f - size, 8f - size, 8f - size),
                new Vector3f(8f + size, 8f + size, 8f + size),
                faces,
                null,
                false
        ));

        UnbakedGeometryHelper.bakeElements(modelBuilder, blockElements, spriteGetter, modelState, modelLocation);
    }
}
```

### 2. アイテムごとにモデルを変更する

`IUnbakedGeometry#bake` で `ItemOverrides` を入れ替えることによって実現できます。

`ItemOverrides#resolve` で動的にモデルを切り替えています。

キャッシュなどを使用し、Quad自動生成と組み合わせることで動的に自由にモデルを変更可能です。

例のJsonモデル:

```json
{
  "loader": "examplemod:example",
  "small": {
    "parent": "examplemod:item/example_small"
  },
  "large": {
    "parent": "examplemod:item/example_large"
  }
}
```

この例では
アイテムの個数が32以上の時、`item/example_small` になり、

32未満の場合 `item/example_large` になります。

```java
public class ExampleModel extends SimpleUnbakedGeometry<ExampleModel> {

    public static final IGeometryLoader<ExampleModel> LOADER = ExampleModel::deserialize;

    public final BlockModel smallModel;
    public final BlockModel largeModel;

    public ExampleModel(BlockModel smallModel, BlockModel largeModel) {
        this.smallModel = smallModel;
        this.largeModel = largeModel;
    }

    // 別クラスに移動しても良い
    public static ExampleModel deserialize(JsonObject json, JsonDeserializationContext context) {
        BlockModel smallModel = context.deserialize(GsonHelper.getAsJsonObject(json, "small"), BlockModel.class);
        BlockModel largeModel = context.deserialize(GsonHelper.getAsJsonObject(json, "large"), BlockModel.class);

        return new ExampleModel(smallModel, largeModel);
    }

    @Override
    public BakedModel bake(IGeometryBakingContext context, ModelBaker baker, Function<Material, TextureAtlasSprite> spriteGetter, ModelState modelState, ItemOverrides overrides, ResourceLocation modelLocation) {
        overrides = new ExampleOverrides();

        BakedModel bakedSmallModel = this.smallModel.bake(baker, this.smallModel, spriteGetter, modelState, modelLocation, context.useBlockLight());
        BakedModel bakedLargeModel = this.largeModel.bake(baker, this.largeModel, spriteGetter, modelState, modelLocation, context.useBlockLight());

        return new Baked(
                context.useAmbientOcclusion(),
                context.isGui3d(),
                context.useBlockLight(),
                spriteGetter.apply(context.getMaterial("particle")),
                overrides,
                bakedSmallModel,
                bakedLargeModel
        );
    }

    @Override
    public void resolveParents(Function<ResourceLocation, UnbakedModel> modelGetter, IGeometryBakingContext context) {
        this.smallModel.resolveParents(modelGetter);
        this.largeModel.resolveParents(modelGetter);
        super.resolveParents(modelGetter, context);
    }

    @Override
    protected void addQuads(IGeometryBakingContext iGeometryBakingContext, IModelBuilder<?> iModelBuilder, ModelBaker modelBaker, Function<Material, TextureAtlasSprite> function, net.minecraft.client.resources.model.ModelState modelState, ResourceLocation resourceLocation) {

    }

    public static class Baked implements IDynamicBakedModel {
        private final boolean isAmbientOcclusion;
        private final boolean isGui3d;
        private final boolean isSideLit;
        private final TextureAtlasSprite particle;
        private final ItemOverrides overrides;
        private final BakedModel smallModel;
        private final BakedModel largeModel;

        public Baked(boolean isAmbientOcclusion, boolean isGui3d, boolean isSideLit, TextureAtlasSprite particle, ItemOverrides overrides, BakedModel smallModel, BakedModel largeModel) {
            this.isAmbientOcclusion = isAmbientOcclusion;
            this.isGui3d = isGui3d;
            this.isSideLit = isSideLit;
            this.particle = particle;
            this.overrides = overrides;

            this.smallModel = smallModel;
            this.largeModel = largeModel;
        }

        public @NotNull List<BakedQuad> getQuads(@Nullable BlockState state, @Nullable Direction side, @NotNull RandomSource rand, @NotNull ModelData data, @Nullable RenderType renderType) {
            return smallModel.getQuads(state, side, rand, data, renderType);
        }

        @Override
        public boolean useAmbientOcclusion() {
            return this.isAmbientOcclusion;
        }

        @Override
        public boolean isGui3d() {
            return this.isGui3d;
        }

        @Override
        public boolean usesBlockLight() {
            return this.isSideLit;
        }

        @Override
        public boolean isCustomRenderer() {
            return false;
        }

        @Override
        public @NotNull TextureAtlasSprite getParticleIcon() {
            return this.particle;
        }

        @Override
        public @NotNull ItemOverrides getOverrides() {
            return overrides;
        }
    }

    public static class ExampleOverrides extends ItemOverrides {

        @Override
        public @Nullable BakedModel resolve(@NotNull BakedModel model, @NotNull ItemStack itemStack, @Nullable ClientLevel level, @Nullable LivingEntity livingEntity, int partialTicks) {
            int count = itemStack.getCount();

            if(model instanceof Baked baked) {
                return count >= 32 ? baked.largeModel : baked.smallModel;
            }
            return model;
        }
    }
```

### モデルローダーの登録

`ModelEvent.RegisterGeometryLoaders` イベントで登録します。

MODバスに登録してください。

```java
@Mod.EventBusSubscriber(modid = ExampleMod.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ModelClientEvents {

    @SubscribeEvent
    public static void registerModelLoaders(ModelEvent.RegisterGeometryLoaders loaders) {
        loaders.register("cube", CubeModel.LOADER);
        loaders.register("example", ExampleModel.LOADER);
    }
}
```

第一引数がIDとなり、これはJsonモデルの `"loader"` に当たります。