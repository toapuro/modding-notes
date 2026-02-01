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
| `translucent` | 半透明 | 深度書き込みは無効になることが多い |
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

- `setTextureState`: テクスチャアトラスの指定([参照](./concepts.md#テクスチャアトラス))
- `setShaderState`: シェーダーの指定
- `setTransparencyState`: 半透明の処理方法(ブレンドモード)の指定
- `setDepthTestState`: 深度テストの指定
- `setCullState`: カリングの指定(`CULL`：背面を描画しない)
- `setLightmapState`: ライトマップ(明るさ)の適用の有無
- `setOverlayState`: オーバーレイ(ダメージ時の赤色表示など)の適用の有無
- `setLayeringState`: レイヤリング(ポリゴンオフセットなど)の指定
- `setOutputState`: 出力先レンダーターゲットの指定
- `setTexturingState`: テクスチャの準備の指定
- `setWriteMaskState`: バッファへの書き込み設定
- `setLineState`: 線の太さを指定
- `setColorLogicState`: 色合成の方法を指定
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
);
```
