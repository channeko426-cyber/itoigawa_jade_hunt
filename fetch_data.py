import json
import requests
from datetime import datetime

# 気象庁の新潟県（糸魚川含む）の天気予報データURL
# 会員登録もAPIキーも一切不要で、誰でも24時間いつでも取得できます！
url = 'https://jma.go.jp'

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        output_file = 'itoigawa_marine.json'
        
        # 地図側でいつのデータか分かるように最終更新日時を追加
        # 辞書型ではなくリスト型で返ってくるため、今回は別の形（またはそのまま）保存します
        result_data = {
            "jma_data": data,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"成功: 気象庁から糸魚川の予報データを取得し、{output_file} に保存しました！")
    else:
        print(f"気象庁エラー: ステータスコード {response.status_code}")
        
except Exception as e:
    print(f"通信エラーが発生しました: {e}")
