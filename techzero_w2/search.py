# search_pages() の全体 — コメントを手がかりに自分で書いてみよう

def search_pages(query: str, pages: list) -> list:
    # ↑ 「: str」「: list」は型ヒント / 「-> list」は戻り値の型宣言

    # ① キーワードが空欄ならすぐ終了（空リストを返す）
    # ↓ ここにコードを書いてください
    if not query.strip():
        return []
    # ② 結果を入れる空のリストを用意
    # ↓ ここにコードを書いてください
    results = []
    # ③ query を小文字に統一（.lower() を使う）
    # ↓ ここにコードを書いてください
    query_lower = query.lower()

    # ④ ページを1件ずつ取り出してループ（for ループ）
    # ↓ ここにコードを書いてください
    for page in pages:
        # ⑤ title + description + keywords を1つの文字列に結合
        # ↓ ここにコードを書いてください
        search_text = "".join([
            page["title"],
            page["description"],
            "".join(page["keywords"]),  # keywords はリストなのでさらに結合
        ])
        # ⑥ キーワードが含まれていたら results に追加（.append() を使う）
        # ↓ ここにコードを書いてください
        if query_lower in search_text.lower():
            results.append(page)

    # ⑦ マッチしたページのリストを return する
    # ↓ ここにコードを書いてください
    return results

# ── 実際に動かしてみよう ──
if __name__ == "__main__":
    import json
    with open("pages.json", "r", encoding="utf-8") as f:
        all_pages = json.load(f)

    hits = search_pages("DX", all_pages)
    print(f"'DX' の検索結果: {len(hits)} 件")
    print()
    for h in hits:
        print(f"  ✅ {h['title']}  （{h['author']}）")




import re  # re = Regular Expression（正規表現）標準ライブラリ、pip install 不要

def highlight_match(text: str, query: str) -> str:

    if not query:       # キーワードが空なら何もしない
        return text

    # re.compile() でパターン（検索ルール）を作る
    pattern = re.compile(
        re.escape(query),  # re.escape：「?」「+」などの特殊文字が含まれても壊れない安全策
        re.IGNORECASE      # IGNORECASE：大文字・小文字を区別しない
    )

    # pattern.sub(置換後の文字列, 元テキスト)：マッチした部分を置換する
    return pattern.sub(f"**{query}**", text)
    #                  ↑
    #   「**DX**」← Markdown で ** で囲むと太字になる！


# ── 動かしてみよう ──
if __name__ == "__main__":
    original = "大手メーカー勤務、DX推進担当として新規事業開発に従事"
    result1  = highlight_match(original, "DX")
    result2  = highlight_match(original, "dx")   # 小文字でもOK（IGNORECASE のおかげ）

    print("【変換前】")   ; print(" ", original)
    print("【変換後 DX】") ; print(" ", result1)
    print("【変換後 dx】") ; print(" ", result2)
    print()
    print("※ Streamlit画面では **DX** の部分が太字で表示されます")