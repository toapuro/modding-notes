# ネットワーキング (1.20.1)

ここでは、サーバーとクライアント間での通信の仕組みや、独自パケットを定義してデータを送受信する方法を解説します。

## 資料

- [Forge 公式ドキュメント - SimpleImpl](https://docs.minecraftforge.net/en/1.20.x/networking/simpleimpl/)

## パケット

クライアントでの操作をサーバーに送信したり、サーバーのデータをクライアントに同期したりするため、Minecraftでは **パケット** という単位でデータの送受信を行います。

パケット送受信の方向によって、主に以下の2種類に分類できます。

- **Serverbound (C2S)**: クライアントからサーバーへの送信（例: GUIボタンの押下通知、インタラクトなど）
- **Clientbound (S2C)**: サーバーからクライアントへの送信（例: エンティティデータの同期、ブロック更新など）

## 実践

### チャンネル作成

パケットを送受信するには、まずMod専用の通信チャンネル（`SimpleChannel`）を作成する必要があります。

```java
private static final String PROTOCOL_VERSION = "1";

public static final SimpleChannel CHANNEL = NetworkRegistry.newSimpleChannel(
    new ResourceLocation(MOD_ID, "main"),
    () -> PROTOCOL_VERSION,
    PROTOCOL_VERSION::equals,
    PROTOCOL_VERSION::equals
);
```

!!! info "バージョン検証について"
    `PROTOCOL_VERSION::equals` と指定すると、サーバーとクライアントでプロトコルバージョンが一致しない場合に接続が拒否されます。
    
    クライアント専用Modなどでサーバー側にModが入っていなくても接続を許可したい場合は、`NetworkRegistry.acceptMissingOr(PROTOCOL_VERSION)` などを指定します。

### パケットクラスの作成

通信するデータ構造とその処理をまとめたパケットクラスを作成します。

パケットには以下の3つの要素が必要です：

- **エンコード (`encode`)**: インスタンスのデータを `FriendlyByteBuf` に書き込む処理。
- **デコード (`decode`)**: 受信した `FriendlyByteBuf` からデータを読み出し、パケットインスタンスを生成する処理。
- **ハンドラー (`handle`)**: パケットを受信した際に実行する実際の処理。

=== "例"

    ```java
    public class ExamplePacket {
        private final int intValue;
        private final boolean booleanValue;
        private final Item item;
        
        public ExamplePacket(int intValue, boolean booleanValue, Item item) {
            this.intValue = intValue;
            this.booleanValue = booleanValue;
            this.item = item;
        }
        
        public static ExamplePacket decode(FriendlyByteBuf buf) {
            int intValue = buf.readVarInt();
            boolean booleanValue = buf.readBoolean();
            Item item = buf.readById(BuiltInRegistries.ITEM);
            return new ExamplePacket(intValue, booleanValue, item);
        }
        
        public void encode(FriendlyByteBuf buf) {
            buf.writeVarInt(intValue);
            buf.writeBoolean(booleanValue);
            buf.writeId(BuiltInRegistries.ITEM, item);
        }

        public void handle(Supplier<NetworkEvent.Context> contextSupplier) {
            NetworkEvent.Context context = contextSupplier.get();
            // ネットワークスレッド
            context.enqueueWork(() -> {
                // メインスレッドでの処理
                
                ServerPlayer sender = context.getSender();
                if (sender == null) return;
                // プレイヤーの操作など
            });
            context.setPacketHandled(true);
        }
    }
    ```

=== "テンプレート"

    ```java
    public class ExamplePacket {
        
        public ExamplePacket() {
        }
        
        public static ExamplePacket decode(FriendlyByteBuf buf) {
            return new ExamplePacket();
        }
        
        public void encode(FriendlyByteBuf buf) {
        }

        public void handle(Supplier<NetworkEvent.Context> contextSupplier) {
            NetworkEvent.Context context = contextSupplier.get();
            context.enqueueWork(() -> {
            });
            context.setPacketHandled(true);
        }
    }
    ```

!!! warning "書き込みと読み込みの順序"

    `encode` でデータを書き込んだ順番および型と、`decode` で読み出す順番および型は完全に一致させる必要があります。

!!! warning "スレッドについて"

    パケットの受信処理は、Minecraftのメインスレッドではなく ネットワークワーカースレッドで非同期に実行されます。
    ワールドの変更やエンティティの操作など、ゲームデータにアクセスする処理は必ず `enqueueWork` を使用してメインスレッドで実行する必要があります。

!!! tip "`writeVarInt` と `writeInt` の違い"

    `writeVarInt` は数値の大きさに応じて可変長で書き込むため、多くの場合バイト数を抑えられます。

    頻繁に非常に 大きな数を扱う場合ではない限り、`writeVarInt` を使用することをおすすめします。

### パケット登録

作成したパケットクラスは、Modの初期化段階（Modのコンストラクタや、`FMLCommonSetupEvent`等）で `SimpleChannel` に登録する必要があります。

パケットの登録方法には以下の2つがあります。

#### `SimpleChannel#messageBuilder` (推奨)

ビルダーパターンで分かりやすく登録できます。

`NetworkDirection` ではパケット送受信の方向を指定します：
- Serverbound（C2S）: `NetworkDirection.PLAY_TO_SERVER`
- Clientbound（S2C）: `NetworkDirection.PLAY_TO_CLIENT`


```java
int id = 0;

CHANNEL.messageBuilder(ExamplePacket.class, id++, NetworkDirection.PLAY_TO_SERVER)
        .encoder(ExamplePacket::encode)
        .decoder(ExamplePacket::decode)
        .consumerNetworkThread(ExamplePacket::handle)
        .add();
```

!!! note "`consumerNetworkThread` と `consumerMainThread` について"
    - `consumerNetworkThread`: パケットのハンドラをネットワークスレッドでそのまま実行します。
    - `consumerMainThread`: Forge側で自動的に `enqueueWork` と `setPacketHandled(true)` を行ってメインスレッドでハンドラーを実行します。これを使用する場合、ハンドラ内での `enqueueWork` や `setPacketHandled(true)` の呼び出しは不要です。

!!! warning "パケットIDの重複"

    `id` は同じチャンネル内で重複しない整数にする必要があります。

#### `SimpleChannel#registerMessage`

1つのメソッドでコンパクトに記述できますが、引数が多いため上記の `messageBuilder` の使用を推奨します。

```java
int id = 0;

CHANNEL.registerMessage(
    id++,
    ExamplePacket.class,
    ExamplePacket::encode,
    ExamplePacket::decode,
    ExamplePacket::handle,
    Optional.of(NetworkDirection.PLAY_TO_SERVER)
);
```

### パケット送信

パケットの送信は、送信する方向（C2S または S2C）によって使用するメソッドや引数が異なります。

#### クライアントからサーバーへ送信 (C2S)

クライアント側からサーバーへ送信する場合は `sendToServer` を使用します。

```java
CHANNEL.sendToServer(new ExamplePacket(intValue, booleanValue, item));
```

#### サーバーからクライアントへ送信 (S2C)

サーバー側から特定のプレイヤーや範囲内にいるプレイヤーに送信する場合は `send` を使用します。

##### 特定のプレイヤーに送信
```java
CHANNEL.send(PacketDistributor.PLAYER.with(() -> serverPlayer), new ExamplePacket(intValue, booleanValue, item));
```

##### すべてのプレイヤーに送信
```java
CHANNEL.send(PacketDistributor.ALL.noArg(), new ExamplePacket(intValue, booleanValue, item));
```

##### 特定のディメンションにいる全プレイヤーに送信
```java
CHANNEL.send(PacketDistributor.DIMENSION.with(() -> level.dimension()), new ExamplePacket(intValue, booleanValue, item));
```

#### PacketDistributor の種類一覧

`PacketDistributor` には主に以下の送信先が用意されています：

- `PacketDistributor.PLAYER`: 特定のプレイヤーに送信
- `PacketDistributor.ALL`: 全プレイヤーに送信
- `PacketDistributor.DIMENSION`: 指定したディメンション内の全プレイヤーに送信
- `PacketDistributor.NEAR`: 指定した座標から一定範囲内にいるプレイヤーに送信
- `PacketDistributor.TRACKING_ENTITY`: 特定のエンティティをロードしているプレイヤー群に送信
- `PacketDistributor.TRACKING_ENTITY_AND_SELF`: 対象のエンティティをロードしているプレイヤー群および対象エンティティ（プレイヤーの場合）自身に送信
- `PacketDistributor.TRACKING_CHUNK`: 特定のチャンクをロードしているプレイヤーに送信
- `PacketDistributor.SERVER`: サーバーに送信（`sendToServer` の代わりに使用可能）
- `PacketDistributor.NMLIST`: 指定したすべての `Connection` に送信