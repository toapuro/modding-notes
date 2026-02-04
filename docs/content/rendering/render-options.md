# 描画設定

## RenderType

描画についての設定。

半透明処理や深度テストの挙動を決めます。

`RenderType` 内に定数として存在します。

詳しくはクラスを参照してください。

### RenderTypeでよく使われる用語

| RenderType | 説明 | 備考 |
| --- | --- | ---- |
| `solid` | 不透明 |
| `cutout` | 切り抜き | アルファ値が閾値(通常0.1)を下回るピクセルを破棄し、それ以外を不透明として描画する |
| `mipped` | ミップマップ | 距離に応じてテクスチャ解像度を下げる。遠景のノイズを防ぐ |
| `translucent` | 半透明 | 深度書き込みは無効 |
| `entity` | テクスチャやテクスチャアトラスを指定できる |
| `text` | テキスト | GUIやネームタグのテキスト描画用 |
| `lines` | 線 |
| `gui` | GUI |

### 独自RenderTypeの作成

バニラのRenderTypeに必要な設定がない場合作成します。

**RenderType.create**

- `VertexFormat`: 頂点フォーマット。大体 `DefaultVertexFormat` から指定
- `VertexFormat.Mode`: 頂点モード
- `bufferSize`: レンダリングバッファサイズ。頻度や内容によるが小規模なら256で十分
- `RenderType.CompositeState`: `CompositeStateBuilder#createCompositeState` でビルドし渡す

**CompositeStateBuilder**

`RenderType.CompositeState.builder()` で作成する。

- `setTextureState`: [テクスチャアトラス](./api.md#テクスチャアトラス)の指定
- `setShaderState`: シェーダーの指定
- `setTransparencyState`: 半透明の処理方法([#ブレンドモード](#ブレンドモード))の指定
- `setDepthTestState`: 深度テストの指定
- `setCullState`: カリングの指定(`CULL`：背面を描画しない)
- `setLightmapState`: [ライトマップ](#ライトマップ)の適用の有無
- `setOverlayState`: [オーバーレイ](#オーバーレイテクスチャ)の適用の有無
- `setLayeringState`: レイヤリング(ポリゴンオフセットなど)の指定
- `setOutputState`: 出力先[レンダーターゲット](#レンダーターゲット)の指定
- `setTexturingState`: テクスチャの準備の指定
- `setWriteMaskState`: 書き込むバッファのマスク設定(カラーバッファや深度バッファ)
- `setLineState`: 線の太さを指定
- `setColorLogicState`: 色調整ののモードを指定
- `createCompositeState`: 設定をビルドする

バニラのRenderTypeの例

```java
// RenderType.SOLID
private static final RenderType SOLID = RenderType.create(
    "solid",
    DefaultVertexFormat.BLOCK,
    VertexFormat.Mode.QUADS,
    2097152,
    true,
    false,
    RenderType.CompositeState.builder()
        .setLightmapState(LIGHTMAP)
        .setShaderState(RENDERTYPE_SOLID_SHADER)
        .setTextureState(BLOCK_SHEET_MIPPED)
        .createCompositeState(true)
```

## VertexFormat

GPUに送る情報のレイアウトを決定するためのフォーマット。

各要素は Vertex Shader の `attribute` 変数に対応します。

基本、`DefaultVertexFormat`から取得します。

!!! warning

    `VertexFormat` で指定されている順番通りに `VertexConsumer` に頂点情報を渡す必要があります。

**DefaultVertexFormat** の定数

| 名前 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `BLIT_SCREEN` | Position | UV | Color |
| `BLOCK` | Position | Color | UV0 | UV2 | Normal | Padding |
| `NEW_ENTITY` | Position | Color | UV0 | UV1 | UV2 | Normal | Padding |
| `PARTICLE` | Position | UV0 | Color | UV2 |
| `POSITION` | Position |
| `POSITION_COLOR` | Position | Color |
| `POSITION_COLOR_NORMAL` | Position | Color | Normal | Padding |
| `POSITION_COLOR_LIGHTMAP` | Position | Color | UV2 |
| `POSITION_TEX` | Position | UV0 |
| `POSITION_COLOR_TEX` | Position | Color | UV0 |
| `POSITION_TEX_COLOR` | Position | UV0 | Color |
| `POSITION_COLOR_TEX_LIGHTMAP` | Position | Color | UV0 | UV2 |
| `POSITION_TEX_LIGHTMAP_COLOR` | Position | UV0 | UV2 | Color |
| `POSITION_TEX_COLOR_NORMAL` | Position | UV0 | Color | Normal | Padding |

`"UV0"` と `"UV"` は同値である。

**VertexFormatの要素**

| 名前 | 説明 | 対応するメソッド(VertexConsumer) |
| --- | --- | --- |
| Position | 頂点座標 | `vertex(x, y, z)` |
| Color | 色 | `color(r, g, b, a)` |
| UV0 | テクスチャUV | `uv(u, v)` |
| UV1 | オーバーレイUV | `overlayCoords(u, v)` |
| UV2 | ライトマップUV | `uv2(u, v)` |
| Normal | 法線 | `normal(x, y, z)` |
| Padding | 余白 |

## ブレンドモード

ブレンドモードとは、透明度によってどのように描画色を決定するかの設定の事です。

`RenderStateShard` の中の定数としていくつか存在する。

- `src`: ソースのRGB色(描画対象)
- `src.a`: ソースの透明度
- `dst`: デスティネーションのRGB色(既に描画されている色)
- `dst.a`: デスティネーションの透明度

| 名称 | 説明 | 式 | 備考 |
| --- | ---- | ---- | --- |
| `NO_TRANSPARENCY` | 不透明 |
| `ADDITIVE_TRANSPARENCY` | 加算合成 | `src + dst` | alpha無視 |
| `LIGHTNING_TRANSPARENCY` | 発光合成 | `src * src.a + dst` |
| `GLINT_TRANSPARENCY` | エンチャントの輝き | `rgb = src * src.a + dst, a = dst.a` |
| `CRUMBLING_TRANSPARENCY` | 破壊表現の合成 | `rgb = 2 * src * dst, a = src.a` |
| `TRANSLUCENT_TRANSPARENCY` | 半透明合成 | `rgb = src * src.a + dst * (1 - src.a), a = src.a + dst.a * (1 - src.a)` |

## 深度

奥行きのこと。
描画順にかかわらず、奥のオブジェクトが手前のオブジェクトに常に隠れるようにするために存在する。

**深度バッファ**というものが存在し、各ピクセルに深度が保存されています。

### 深度テスト

深度値と既存の深度バッファ内の値を比較し、判定をパスしたピクセルのみを書き込むことで、前後関係を再現するためのもの。

#### 比較関数

| 名称 | 説明 |
| --- | --- |
| `NO_DEPTH_TEST` | 深度テストを行わない |
| `EQUAL_DEPTH_TEST` | 深度値が対象と等しい場合のみ描画 |
| `LEQUAL_DEPTH_TEST`(既定値) | 深度値が対象以下の場合のみ描画 |
| `GREATER_DEPTH_TEST` | 深度値が対象より大きい場合のみ描画 |

## カリング

裏面を描画するかどうか。

- `CULL`: 裏面を描画しない
- `NO_CULL`: 裏面を描画する

## ライトマップ

ブロックライト(U)とスカイライト(V)を組み合わせた結果の明るさの色をキャッシュした16x16のテクスチャ。

実際に頂点に格納するUVの値は圧縮されており、

その値は `LightTexture.pack(int blockLight, int skyLight)` で指定する値を取得できます。

## オーバーレイテクスチャ

汎用なオーバーレイ用の16x16のテクスチャ。

ライトマップと同じく頂点に格納するUVの値は圧縮されており、

`OverlayTexture.pack(int u, int v)` で指定する値を取得できます。

以下の用途で使われています。

- 負傷時/死亡時の赤色表示
- クリーパー点滅時の白色
- TNT点滅時の白色

## レイヤリング

Z-Fightingを回避するために使用されるオプション

| 名称 | 説明 |
| --- | --- |
| `NO_LAYERING` | レイヤリングを行わない |
| `POLYGON_OFFSET_LAYERING` | `glPolygonOffset` を使用し深度値を手前にずらす |
| `VIEW_OFFSET_Z_LAYERING` | `PoseStack` を微妙に内側にスケールする |

## レンダーターゲット

描画対象のバッファ。

大抵は最終的にmainレンダーターゲットに描画されます。

例えば半透明な描画の場合 `translucent` ターゲットに描画され、最終的に `main` レンダーターゲットに合成されます。