# アイテムの追加

資料
- [Items - Neoforge](https://docs.neoforged.net/docs/items/)
- [Making Items - Forge Community](https://forge.gemwire.uk/wiki/Making_Items)

[#レジストリ](./basic.md) を参考に、アイテムを登録します。

```java
public class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MODID);

    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item", () ->
            new Item(new Item.Properties())
    );
}
```

特に特別な特徴・機能を持たないアイテムを登録しました。

## Item.Properties

アイテムに様々な設定を付与するためのプロパティ郡です。

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

## FoodProperties

`food(FoodProperties)` で指定するプロパティ群。

`new FoodProperties.Builder()` でビルダーを生成し、設定後に `.build()` を呼び出す必要があります。

設定できるプロパティとして以下があります。

- `nutrition`: 回復する満腹ポイントの数を設定
- `saturationMod`: 隠し満腹度の計算に使用される値。計算式は`min(2 * nutrition * saturationMod, プレイヤーの満腹度)`
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
        .effect(new MobEffectInstance(
            MobEffects.HUNGER, 600, 0), 0.3F
        )
        .meat()
        .build();
```