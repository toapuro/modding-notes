# レンダリングAPI

## 座標変換と回転行列

### PoseStack

座標変換(移動・回転・拡大縮小)を管理するスタックです。

これによってプレイヤーの手に持った剣だけを回転させる、といったことが可能になります。

| メソッド名 | 説明 |
| --- | --- |
| `push` | 現在の状態(位置・回転)を保存する。ここから局所的な作業を始める合図。 |
| `translate` | 座標を移動する。 |
| `scale` | 座標を拡大縮小する。 |
| `rotate` | 座標を回転する。 |
| `pop` | 保存した状態に戻す。作業終了。 |

!!! warning

    `push` と `pop` は必ずセットで行ってください。

### Quaternion

回転を表す数学的概念。

`Axis.YP.rotationDegrees(90)` のように軸を指定して `Quaternion` を作成し、`PoseStack` に適用できます。

```java
// Y軸中心に+90度回転します
poseStack.mulPose(Axis.YP.rotationDegrees(90));
// Y軸中心に-90度回転します
poseStack.mulPose(Axis.Y.rotationDegrees(90));
```

## 描画バッファ

### MultiBufferSource(BufferSource)

VertexConsumer を RenderType ごとに振り分け、結果的にバッチレンダリングを行うためのクラスです。

複数の描画をまとめて処理できるため、レンダリング効率が向上します。

`MultiBufferSource#getBuffer(RenderType)` を呼び出すことで、指定した RenderType に対応する VertexConsumer を取得できます。

異なる RenderType が渡された場合、それまでのバッチは `endBatch` によって終了され、その時点で描画が実行されます。

!!! warning

    バッチが終了したタイミングで描画されるため、`endBatch` が呼ばれない限り描画されません。(GuiGraphics等は自動で`endBatch`を呼ぶ)

### Tesselator

即時レンダリング用のクラス。

`MultiBufferSource` とは異なり、自動的にバッチレンダリングはされない。

`Tesselator.getInstance()` で取得し、
`.getBuilder(RenderType)` で `VertexConsumer` を取得する。

`.end` で明示的に描画します。

### VertexConsumer(BufferBuilder)

基本的な描画は `VertexConsumer` というインターフェースを通して頂点を登録します。

頂点は以下の値を持ちます。

`RenderType` で指定されている `VertexFormat` によって必要な変数が異なります

[#VertexFormat](./render-options.md#vertexformat) を参照

!!! warning

    `VertexFormat` で指定されている順番通りに `VertexConsumer` に頂点情報を渡す必要があります。

!!! danger

    必要な変数を設定しない場合クラッシュします。

| 変数名 | 説明 |
| --- | --- |
| `x` | X座標 |
| `y` | Y座標 |
| `z` | Z座標 |
| `red` | 赤成分 |
| `green` | 緑成分 |
| `blue` | 青成分 |
| `alpha` | 透明度(float0.0~1.0, int0~255) |
| `texU` | テクスチャ座標(U) |
| `texV` | テクスチャ座標(V) |
| `overlayUV` | オーバーレイUV座標(被ダメージ時の赤色等)(パック済み) |
| `lightmapUV` | ライトマップUV |
| `normalX` | 法線ベクトルX |
| `normalY` | 法線ベクトルY |
| `normalZ` | 法線ベクトルZ |

!!! info

    線は特殊で、視点から終点へ向かう方向を表すベクトルとして設定する必要があります。

```java
public static void drawHorizontalQuad(
        PoseStack poseStack,
        MultiBufferSource buffer,
        float x0, float y, float z0,
        float width, float depth,
        float u, float v,
        int r, int g, int b, int a
) {
    Matrix4f matrix4f = poseStack.last().pose();

    // 単色
    VertexConsumer consumer = buffer.getBuffer(RenderType.lightning());

    float x1 = x0 + width;
    float z1 = z0 + depth;

    consumer.vertex(matrix4f, x0, y, z0)
            .color(r, g, b, a)
            .endVertex();

    consumer.vertex(matrix4f, x1, y, z0)
            .color(r, g, b, a)
            .endVertex();
    
    consumer.vertex(matrix4f, x1, y, z1)
            .color(r, g, b, a)
            .endVertex();

    consumer.vertex(matrix4f, x0, y, z1)
            .color(r, g, b, a)
            .endVertex();
}

// 線の描画
public static void drawLine(
        PoseStack poseStack,
        MultiBufferSource buffer,
        float x1, float y1, float z1,
        float x2, float y2, float z2,
        int r, int g, int b, int a
) {
    Matrix4f matrix4f = poseStack.last().pose();
    Matrix3f matrix3f = poseStack.last().normal();

    VertexConsumer consumer = buffer.getBuffer(RenderType.lines());

    float dx = x2 - x1;
    float dy = y2 - y1;
    float dz = z2 - z1;

    consumer.vertex(matrix4f, x1, y1, z1)
            .color(r, g, b, a)
            .normal(matrix3f, dx, dy, dz)
            .endVertex();

    consumer.vertex(matrix4f, x2, y2, z2)
            .color(r, g, b, a)
            .normal(matrix3f, dx, dy, dz)
            .endVertex();
}
```

## テクスチャアトラス

### 資料

- [Minecraft Wiki](https://ja.minecraft.wiki/w/テクスチャ#テクスチャアトラス)

OpenGLではテクスチャを切り替える(Bind)処理は比較的重い処理です。

そのため、Minecraftでは大量のブロックやアイテムのテクスチャを**1枚の巨大な画像**にまとめて扱うことで、描画時の切り替えコストを削減しています。

このまとめられた1枚の画像を**テクスチャアトラス**と呼びます。

!!! tips

    エンティティのテクスチャはテクスチャアトラスを使用していません。

### 種類

以下の静的なテクスチャアトラスが存在します。

| 参照 | ID | ディレクトリ | 説明 |
| --- | --- | --- | --- |
| `Sheets.BANNER_SHEET` | banner_patterns | entity/banner_base, entity/banner/\* | バナー |
| `Sheets.BED_SHEET` | beds | entity/bed/\* | ベッド |
| `Sheets.CHEST_SHEET` | chests | entity/chest/\* | チェスト |
| `Sheets.SHIELD_SHEET` | shield_patterns | entity/shield_base, entity/shield_base_nopattern, entity/shield/\* | シールド |
| `Sheets.SIGN_SHEET` | signs | entity/signs/\* | 看板 |
| `Sheets.SHULKER_SHEET` | shulker_boxes | entity/shulker/\* | シャーカーボックス |
| `Sheets.ARMOR_TRIMS_SHEET` | armor_trims | 特殊[^1] | アーマートリム |
| `Sheets.DECORATED_POT_SHEET` | decorated_pot | entity/decorated_pot/\* | 飾り壺 |
| `TextureAtlas.LOCATION_BLOCKS` | blocks | block/\*, item/\*, entity/conduit, ... | ブロック |
| `TextureAtlas.LOCATION_PARTICLES` | particles | particle/\* | パーティクル |
| `textures/atlas/paintings.png` | paintings | painting/\* | 絵画 |
| `textures/atlas/mob_effects.png` | mob_effects | mob_effect/\* | モブエフェクト |

比較的汎用に使えるのは `TextureAtlas.LOCATION_BLOCKS` です。

[^2]: `paletted_permutations` を使用している。`PalettedPermutations` を参照。

## RenderType

[#RenderType](./render-options.md#rendertype) で解説しています。