import requests
import json
from datetime import datetime

def get_btc_price():
    """
    CoinGecko APIを使用してビットコインの現在価格を取得する
    戻り値: 各種通貨での価格データを含む辞書
    """
    try:
        # CoinGecko APIのエンドポイント
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # APIリクエストのパラメータ
        params = {
            "ids": "bitcoin",  # 仮想通貨ID
            "vs_currencies": "usd,eur,jpy",  # 価格を取得する通貨（米ドル、ユーロ、日本円）
            "include_24hr_change": "true",  # 24時間の価格変動を含める
            "include_last_updated_at": "true"  # 最終更新時刻を含める
        }
        
        # APIリクエストを送信
        response = requests.get(url, params=params)
        response.raise_for_status()  # エラーステータスの場合は例外を発生
        
        # レスポンスをパース
        data = response.json()
        
        # 現在時刻を取得
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 出力データを整形
        price_data = {
            "タイムスタンプ": current_time,
            "ビットコイン": {
                "USD": {
                    "価格": data["bitcoin"]["usd"],
                    "24時間変動": data["bitcoin"]["usd_24h_change"]
                },
                "EUR": {
                    "価格": data["bitcoin"]["eur"],
                    "24時間変動": data["bitcoin"]["eur_24h_change"]
                },
                "JPY": {
                    "価格": data["bitcoin"]["jpy"],
                    "24時間変動": data["bitcoin"]["jpy_24h_change"]
                },
                "最終更新": datetime.fromtimestamp(
                    data["bitcoin"]["last_updated_at"]
                ).strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        return price_data
    
    except requests.exceptions.RequestException as e:
        print(f"ビットコイン価格の取得中にエラーが発生しました: {e}")
        return None

def main():
    """
    ビットコイン価格を取得して表示するメイン関数
    """
    price_data = get_btc_price()
    
    if price_data:
        print(json.dumps(price_data, indent=2, ensure_ascii=False))
        
        # 読みやすい形式で表示
        btc_data = price_data["ビットコイン"]
        print("\nビットコイン価格サマリー:")
        print(f"時刻: {price_data['タイムスタンプ']}")
        print(f"USD: ${btc_data['USD']['価格']:,.2f} ({btc_data['USD']['24時間変動']:.2f}%)")
        print(f"EUR: €{btc_data['EUR']['価格']:,.2f} ({btc_data['EUR']['24時間変動']:.2f}%)")
        print(f"JPY: ¥{btc_data['JPY']['価格']:,.0f} ({btc_data['JPY']['24時間変動']:.2f}%)")
        print(f"最終更新: {btc_data['最終更新']}")

if __name__ == "__main__":
    main()