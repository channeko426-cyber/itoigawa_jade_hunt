import os
import json
import requests
from datetime import datetime

# 糸魚川周辺の座標
LAT = 37.05
LNG = 137.80

# 必要なデータ（波の高さ、風の向き）
PARAMS = 'waveHeight,windDirection'

API_KEY = os.environ.get("STORMGLASS_API_KEY")
if not API_KEY:
    print("エラー: STORMGLASS_API_KEY が設定されていません。")
    exit(1)

# 【これが本物の正しいURL窓口です】
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
    response = requests.get(url, headers=headers, params=query_params)
    
    # 200（成功）のときだけJSONとして読み込む
    if response.status_code == 200:
        data = response.json()
        output_file = 'itoigawa_marine.json'
        data['last_updated'] = datetime.now().isoformat()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"成功: 予報データを {output_file} に保存しました。")
    else:
        # 失敗した時は、Storm Glassが返してきたエラーメッセージをそのまま表示する
        print(f"APIエラー: ステータスコード {response.status_code}")
        print("サーバーからのメッセージ:", response.text)
        
except Exception as e:
    print(f"通信エラーが発生しました: {e}")
