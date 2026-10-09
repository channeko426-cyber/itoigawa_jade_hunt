import os
import json
import requests
from datetime import datetime

# 糸魚川周辺の座標
LAT = 37.05
LNG = 137.80
PARAMS = 'waveHeight,waveDirection,wavePeriod,windSpeed,windDirection'

# APIキーを読み込む
API_KEY = os.environ.get("STORMGLASS_API_KEY")
if not API_KEY:
    print("エラー: STORMGLASS_API_KEY が設定されていません。")
    exit(1)

# 【対策】URLの中に直接変数を入れず、リクエスト側の設定（params）で送る形に書き換えました。
# これによりGitHubがURLを誤って破壊するのを防ぎます。
url = 'https://stormglass.io'

query_params = {
    'lat': LAT,
    'lng': LNG,
    'params': PARAMS
}

headers = {
    'Authorization': API_KEY
}

try:
    # params=query_params と指定することで、安全にURLが組み立てられます
    response = requests.get(url, headers=headers, params=query_params)
    
    if response.status_code == 200:
        data = response.json()
        output_file = 'itoigawa_marine.json'
        data['last_updated'] = datetime.now().isoformat()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"成功: 予報データを {output_file} に保存しました。")
    else:
        print(f"APIエラー: ステータスコード {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"通信エラーが発生しました: {e}")
