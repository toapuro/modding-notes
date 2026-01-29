# レンダリング (1.20.1)

## 主要概念

### Lwjgl

MinecraftはLwjglというライブラリを経由してOpenGLで描画しています。

基本的にはOpenGLのコマンドを直接叩くことは少なく、用意されたAPIを通して描画します。

## 描画方法

OpenGLにおいて、すべての物体は頂点の集まりによって構成されています。

頂点は単なる「位置（X, Y, Z）」だけではなく、以下のような情報を持ったデータの塊です。

- Position: 位置情報
- Color: 色情報
- UV: テクスチャ座標
- Normal: 法線
- Light: 光量

## テクスチャアトラス

OpenGLではテクスチャを切り替える（Bindする）処理は比較的重い処理です。
そのため、Minecraftでは大量のブロックやアイテムのテクスチャを**1枚の巨大な画像**にまとめて扱うことで、描画時の切り替えコストを削減しています。これをテクスチャアトラスと呼びます。

## Stitch

- **Stitching (スティッチング)**: Moddingにおいては、個別のテクスチャファイルを用意すれば、ゲーム起動時に自動的にこの巨大な画像に「縫い合わせ（Stitch）」されます。
- **UV座標**: 頂点データには「この巨大な画像のどこからどこまでを使うか」という0.0~1.0の座標(UV)を指定します。
- **Missing Texture**: テクスチャが見つからない場合に表示される「紫と黒の市松模様」も、このアトラス内にデフォルトで含まれているスプライトの一つです。



## 主要クラス

### PoseStack

座標変換(移動・回転・拡大縮小)を管理するスタックです。

これによってプレイヤーの手に持った剣だけを回転させる、といったことが可能になります。

- `push`: 現在の状態(位置・回転)を保存する。ここから局所的な作業を始める合図。
- `translate`: 座標を操作する。
- `scale`: 座標を操作する。
- `rotate`: 座標を操作する。
- `pop`: 保存した状態に戻す。作業終了。

!!! warning

    `push` と `pop` は必ずセットで行ってください。

### VertexConsumer & BufferBuilder

3Dモデルは最終的に頂点の集合としてGPUに送られます。

Moddingでは直接OpenGLを叩くことは少なく、基本的な描画は `VertexConsumer` というインターフェースを通して頂点データを登録します。

- Position: 位置情報
- Color: 色情報
- UV: テクスチャ座標
- Normal(法線): 光の当たり方等を計算するために必要
- ライトマップ: 光のテクスチャ
- オーバーレイテクスチャ: ダメージ表現やTNTの点滅等に使われるテクスチャのUVの指定

### RenderType

描画についての設定。

半透明処理や深度テストの挙動を決めます。

#### RenderTypeの作成

**RenderType.create**

- `VertexFormat`: 頂点フォーマット。大体 `DefaultVertexFormat` から指定
- `VertexFormat.Mode`: 頂点モード
- `bufferSize`: レンダリングバッファサイズ。頻度や内容によるが小規模なら256で十分
- `RenderType.CompositeState`: `CompositeStateBuilder#createCompositeState` でビルドし渡す

**CompositeStateBuilder**

`RenderType.CompositeState.builder()` で作成する。

- `setTextureState`: テクスチャアトラスの指定
- `setShaderState`: シェーダーの指定
- `setTransparencyState`: 半透明の処理方法の指定
- `setDepthTestState`: 深度テストの指定
- `setCullState`: カリングの指定
- `setLightmapState`: ライトマップの指定
- `setOverlayState`: オーバーレイの指定
- `setLayeringState`: レイヤリングの指定
- `setOutputState`: 出力先レンダーターゲットの指定
- `setTexturingState`: テクスチャの準備の指定
- `setWriteMaskState`: 書き込みマスクの指定
- `setLineState`: 線の太さを指定
- `setColorLogicState`: 色合成の方法を指定
- `createCompositeState`: ビルドする

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
);
```