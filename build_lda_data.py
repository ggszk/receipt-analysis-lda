"""ai_topics.html 用の事前計算データ lda_data.js を生成する.

receipt_data.csv（generate_data.py の生成元と同期）に対し、トピック数 3-7 の
LDA 結果と支店別ワードクラウドを計算し、ggszk-lab-public 側の静的HTMLが読む
`const LDA_DATA = {...}` 形式の JS に書き出す。
"""

import json
import os

from analysis import analyze_receipt_data, generate_store_wordclouds

OUT_PATH = os.path.expanduser(
    "~/projects/teaching/courses/ggszk-lab-public/ds_for_high_school/lesson03/lda_data.js"
)
STORE_ORDER = ["中央区", "北区", "東区", "西区"]
HEADER = (
    "// 事前計算したLDA結果（トピック数3-7）＋支店別ワードクラウド。"
    "receipt-analysis-lda の analysis.py で生成（random_state=42）。\n"
)


def ordered_stores(stores: dict) -> dict:
    """支店の並びを固定（グラフのラベル順を安定させる）."""
    return {s: stores[s] for s in STORE_ORDER if s in stores}


def main():
    data = {}
    for n in range(3, 8):
        res = analyze_receipt_data(n)
        res["stores"] = ordered_stores(res["stores"])
        data[str(n)] = res

    wc = generate_store_wordclouds()
    data["wordclouds"] = {s: wc[s] for s in STORE_ORDER if s in wc}

    js = HEADER + "const LDA_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"\n✅ 書き出し完了: {OUT_PATH} ({len(js):,} bytes)")


if __name__ == "__main__":
    main()
