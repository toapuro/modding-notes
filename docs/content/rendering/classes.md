
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

3Dモデルは最終的に「頂点（Vertex）」の集合としてGPUに送られます。

Moddingでは直接OpenGLを叩くことは少なく、基本的な描画は `VertexConsumer` というインターフェースを通して頂点データを登録します。

- 位置 (x, y, z)
- 色 (r, g, b, a)
- テクスチャ座標 (u, v)
- 法線 (normal)
- ライトマップ (lightmap)