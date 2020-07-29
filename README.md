# JPXlib

jpx のマーケット情報を解析しようとしてみるライブラリ

## 1. 先物・オプション

### 取引参加者別取引高（手口上位一覧）

### 概要

売買手口情報

* 指数先物
    1. 日経225先物
    2. 日経225ミニ
    3. TOPIX先物
* 指数OP
    1. 日経225コール
    2. 日経225プット

### データソース

Trading Volume by Trading Participant

https://www.jpx.co.jp/markets/derivatives/participant-volume/index.html

| field                | type    | desc             | eg                                                     |
| -------------------- | ------- | ---------------- | ------------------------------------------------------ |
| data_source          | Keyword | 取得元ファイル名 | 20200728_volume_by_participant_night.csv               |
| data_date            | Date    | 取引日           | ISO 8601 Format (UTC)                                  |
| product_class        | Keyword | 商品名           | FUT_TOPIX_2009, FUT_NK225_2012, PUT_NK225_200710_21625 |
| participant_code     | Integer | 証券会社コード   | 11560 (追加すべき？)                                                 |
| participant_name     | Keyword | 証券会社名       | ゴールドマンサックス                                   |
| participant_location | Keyword | 海外勢 or 国内勢 | 海外, 国内, あるいは米・欧州などとする？（未定                                             |
| participant_customer | Keyword | 顧客層          | 個人投資家、アービトラージ、CTAトレンドフォロー、長期投資
| price                | Integer | 価格             | 20000                                                  |
| contract_month       | Date    | 限月(期限満了月) | 2007(20年7月), 200710(20年7月10日)                     |
| volume               | Integer | 出来高           | 74                                                     |
| vol                  | Integer | 出来高(売りをマイナス値に)           | -74                                                     |
| trade_type           | Keyword | 買い or 売り     | buy, sell                                              |
| session              | Keyword | 日中 or ナイト   | day, night                                             |
| market               | Keyword | j-net or floor   | j-net, floor

### 包含する取引種別

1. ナイト・セッション
    1. 立会取引
    1. J-NET取引
2. 日中取引
    1. 立会取引
    1. J-NET取引

### コード例

```python
from jpxlib import TradingVolumeByParticipant
from jpxlib.exceptions import InvalidTradeData

t = TradingVolumeByParticipant("20200729_volume_by_participant_whole_day.csv")
for x in t:
    try:
        print(x)
    except InvalidTradeData as err:
        pass
```

```
{'participant_code': '12057', 'participant_name': '楽天証券', 'participant_name_en': 'Rakuten Securities', 'volume': '2', 'trade_type': 'buy', 'vol': 2, 'data_source': '20200728_volume_by_participant_whole_day.csv', 'trade_date': '2020-07-28T00:00:00', 'session': 'whole', 'market': 'floor', 'product_class': 'CAL_NK225', 'contract_month': '2020-08-14T00:00:00', 'price': '22750'}
{'participant_code': '12792', 'participant_name': 'メリルリンチ日本証券', 'participant_name_en': 'Merrill Lynch Japan', 'volume': '3', 'trade_type': 'sell', 'vol': -3, 'data_source': '20200728_volume_by_participant_whole_day.csv', 'trade_date': '2020-07-28T00:00:00', 'session': 'whole', 'market': 'floor', 'product_class': 'CAL_NK225', 'contract_month': '2020-08-14T00:00:00', 'price': '22750'}
{'participant_code': '12410', 'participant_name': 'バークレイズ証券', 'participant_name_en': 'Barclays Japan', 'volume': '2', 'trade_type': 'buy', 'vol': 2, 'data_source': '20200728_volume_by_participant_whole_day.csv', 'trade_date': '2020-07-28T00:00:00', 'session': 'whole', 'market': 'floor', 'product_class': 'CAL_NK225', 'contract_month': '2020-08-14T00:00:00', 'price': '22750'}
['-', '-', '-', '-']
{'participant_code': '11060', 'participant_name': 'ａｕカブコム証券', 'participant_name_en': 'au Kabucom Securitie', 'volume': '2', 'trade_type': 'buy', 'vol': 2, 'data_source': '20200728_volume_by_participant_whole_day.csv', 'trade_date': '2020-07-28T00:00:00', 'session': 'whole', 'market': 'floor', 'product_class': 'CAL_NK225', 'contract_month': '2020-08-14T00:00:00', 'price': '22750'}
```
