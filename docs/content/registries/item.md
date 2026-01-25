# アイテム

## 資料

- [Items - Neoforge](https://docs.neoforged.net/docs/items/)
- [Making Items - Forge Community](https://forge.gemwire.uk/wiki/Making_Items)

## アイテムの追加

### レジストリに追加

[#レジストリ](./basic.md) を参考に、アイテムを登録します。

```java
public class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MODID);

    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () ->
            new Item(new Item.Properties())
    );
}
```

これは特に特別な特徴・機能を持たないアイテムを登録します。

### Item.Properties

アイテムに様々な設定を付与するためのプロパティ群。

設定できるプロパティとして以下があります。

- `food`: 食料としての設定
- `stacksTo`: 最大スタック数を設定 (必ず耐久値設定の前にする必要がある)
- `defaultDurability`: 未設定の場合のみ耐久値を設定
- `durability`: 耐久値を設定
- `craftRemainder`: クラフト時に残るアイテムを設定
- `rarity`: レアリティを設定
- `fireResistant`: 火に耐性を持つ
- `setNoRepair`: 修理不可
- `requiredFeatures`: 追加するうえで必要な`実験的機能`のフラグ

```java
public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () ->
        new Item(new Item.Properties().stacksTo(1).defaultDurability(1024).rarity(Rarity.UNCOMMON))
);
```

#### FoodProperties

`food(FoodProperties)` で指定するプロパティ群。

`new FoodProperties.Builder()` でビルダーを生成し、設定後に `.build()` を呼び出す必要があります。

設定できるプロパティとして以下があります。

- `nutrition`: 回復する満腹ポイントの数を設定
- `saturationMod`: 隠し満腹度の計算に使用される値。計算式は `min(2 * nutrition * saturationMod, プレイヤーの満腹度)`
- `meat`: 肉かどうか。狼が食べるかどうかに影響する
- `alwaysEat`: 満腹度が最大でも食べられるようにする
- `fast`: 食べる時間を短くする
- `effect`: 食べたときに付与される可能性のあるエフェクト

バニラの例
```java
public static final FoodProperties APPLE = new FoodProperties.Builder()
        .nutrition(4)
        .saturationMod(0.3F)
        .build();

public static final FoodProperties CHICKEN = new FoodProperties.Builder()
        .nutrition(2)
        .saturationMod(0.3F)
        .effect(
            new MobEffectInstance(
                MobEffects.HUNGER,
                600, // 持続時間
                0 // 強さ
            ),
            0.3F // 確率
        )
        .meat()
        .build();
```

### Itemクラス

アイテムの実際の動作が定義されているクラス。

Modでよく利用されるバニラのアイテム継承クラスは以下の通りです。

ツール・武器・装備

- `SwordItem`
- `BowItem`
- `PickaxeItem`
- `AxeItem`
- `ShovelItem`
- `HoeItem`
- `FishingRodItem`
- `CrossbowItem`
- `TridentItem`
- `ShieldItem`
- `ArmorItem`

その他

- `BlockItem`
- `PotionItem`
- `BucketItem`
- `SpawnEggItem`

独自に機能を追加したい場合、`Item` かそれらの継承クラスを継承してオーバーライドなどで実装します。

```java
class ExampleItem extends Item {
    public ExampleItem(Item.Properties properties) {
        super(properties);
    }

    /**
     * 右クリック時の処理
     */
    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        // ...

        /*
        InteractionResultHolder.success: アクション成功
        InteractionResultHolder.consume: アクション処理済み
        InteractionResultHolder.fail: アクション失敗 (次のuseコールバックに移る)
        InteractionResultHolder.pass: 続行 (次のuseコールバックに移る)
        */
        return InteractionResultHolder.success(player.getItemInHand(hand));
    }

    /**
     * ホバーテキスト
     */
    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.examplemod.example_item"));
    }
}

```

## ItemStack

状態を含んだ変更可能なアイテム1枠分の実態データ。

ItemStackは以下を持ちます:

- `Item item`: アイテムの種類
- `int count`: スタック数
- `CompoundTag tag`: NBTタグ

例えば、インベントリの1スロットなどや、手に持っているアイテムなども `ItemStack` で表現されます。

## クリエイティブタブへの追加

### 既存のクリエイティブタブ

イベントを使用して、既存のクリエイティブタブにアイテムを追加します。

```java
@Mod.EventBusSubscriber(modid = ExampleMod.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ModCreativeTabs {
    @SubscribeEvent
    public static void buildContents(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(ModItems.EXAMPLE_ITEM);
        }
    }
}
```

### カスタムクリエイティブタブ

レジストリを使用して独自クリエイティブタブを追加し、アイテムを追加します。

```java
public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
        DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ExampleMod.MODID);

public static final RegistryObject<CreativeModeTab> EXAMPLE_TAB = CREATIVE_TABS.register("example", () -> CreativeModeTab.builder()
  .title(Component.translatable("item_group." + ExampleMod.MODID + ".example"))
  .icon(() -> new ItemStack(ModItems.EXAMPLE_ITEM.get()))
  .displayItems((params, output) -> {
    output.accept(ModItems.EXAMPLE_ITEM.get());
    // ...
  })
  .build()
);
```

最後に、通常の通りレジストリを紐づけます。

```java
CREATIVE_TABS.register(modBus);
```

<!-- NOTE: モデル、テクスチャの説明を追加したい -->

## リソースの追加(モデルやテクスチャ)

アイテムを追加しただけでは、テクスチャやモデルが存在せず、`Missing Texture` が表示されます。

手動で作成する場合の配置場所:

- モデル定義: `assets/<modid>/models/item/<item_id>.json`
- テクスチャ: `assets/<modid>/textures/item/<texture_name>.png`

`texture_name` はよく `item_id` と一致させることが多いです。