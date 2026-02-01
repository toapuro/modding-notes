# 基本概念

## 座標変換と回転行列

### PoseStack

座標変換(移動・回転・拡大縮小)を管理するスタックです。

これによってプレイヤーの手に持った剣だけを回転させる、といったことが可能になります。

- `push`: 現在の状態(位置・回転)を保存する。ここから局所的な作業を始める合図。
- `translate`: 座標を移動する。
- `scale`: 座標を拡大縮小する。
- `rotate`: 座標を回転する。
- `pop`: 保存した状態に戻す。作業終了。

!!! warning

    `push` と `pop` は必ずセットで行ってください。

### Quaternion

回転を表す数学的概念。

`Axis.YP.rotationDegrees(90)` のように軸を指定して回転を作成し、PoseStackに適用できます。

## 描画バッファ

### MultiBufferSource(BufferSource)

結果的にバッチレンダリングされるように `VertexConsumer` を振り分けてくれるクラス。

`MultiBufferSource#getBuffer(RenderType)` で `VertexConsumer` を取得できます。

動作としては、
異なる `RenderType` が渡された場合 `endBatch` され、描画される
というもので、

その `endBatch` が呼び出されるまで描画が行われません。

しかし、`GuiGraphics` 等は自動で `endBatch` を呼ぶため、手動で呼ぶ必要はありません。

### VertexConsumer(BufferBuilder)

基本的な描画は `VertexConsumer` というインターフェースを通して頂点を登録します。

頂点は以下の値を持ちます。

`RenderType` によって必要な変数が異なります。

!!! warning

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

| 参照 | ID | 説明 |
| --- | --- | --- |
| `Sheets.BANNER_SHEET` | banner_patterns | バナー |
| `Sheets.BED_SHEET` | beds | ベッド |
| `Sheets.CHEST_SHEET` | chests | チェスト |
| `Sheets.SHIELD_SHEET` | shield_patterns | シールド |
| `Sheets.SIGN_SHEET` | signs | 看板 |
| `Sheets.SHULKER_SHEET` | shulker_boxes | シャーカーボックス |
| `Sheets.ARMOR_TRIMS_SHEET` | armor_trims | アーマートリム |
| `Sheets.DECORATED_POT_SHEET` | decorated_pot | 飾り壺 |
| `TextureAtlas.LOCATION_BLOCKS` | blocks | ブロック |
| `TextureAtlas.LOCATION_PARTICLES` | particle | パーティクル |
| `textures/atlas/paintings.png` | paintings | 絵画 |
| `textures/atlas/mob_effects.png` | mob_effects | モブエフェクト |

比較的汎用に使えるのは `TextureAtlas.LOCATION_BLOCKS` です。

## RenderType

[#RenderType](./render-type.md) で解説しています。

