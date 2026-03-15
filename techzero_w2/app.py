import streamlit as st
import json
from datetime import datetime
from search import search_pages, highlight_match

FEEDBACK_FILE = "feedback.json"

@st.cache_data
def load_pages():
    try:
        with open("pages.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_pages(pages):
    with open("pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

def load_feedback():
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_feedback(entry):
    data = load_feedback()
    data.append(entry)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

pages = load_pages()

# タイトル・キャプション
st.title("Tech0 Search v0.1")
st.caption("PROJECT ZERO — 新世代テック検索エンジン")

# タブ切り替え
tab1, tab2, tab3 = st.tabs(["検索", "登録", "一覧"])

# ── 検索タブ ──
with tab1:
    st.header("🔍 キーワード検索")
    query = st.text_input("🔍 キーワードを入力")

    results = search_pages(query, pages)
    st.markdown(f"検索結果: **{len(results)} 件**")

    for page in results:
        # タイトル（クリック可能リンク）
        st.markdown(f"### [{page['title']}]({page['url']})")

        # 説明文（キーワードをハイライト）
        st.markdown(highlight_match(page["description"], query))

        # キーワードタグ
        tags = ", ".join([f"`{kw}`" for kw in page["keywords"]])
        st.markdown(f"タグ: {tags}")

        # 作者・日付（横2列）
        c1, c2 = st.columns(2)
        c1.caption(f"作者: {page['author']}")
        c2.caption(f"日付: {page['created_at']}")

        # フィードバック（スター評価）
        selected = st.feedback("stars", key=f"fb_{page['id']}_{query}")
        if selected is not None:
            save_feedback({
                "page_id": page["id"],
                "title": page["title"],
                "query": query,
                "stars": selected + 1,  # 0-4 → 1-5
                "timestamp": datetime.now().isoformat(),
            })
            st.caption(f"{'⭐' * (selected + 1)} ありがとうございます！")

        st.markdown("---")

# ── 登録タブ ──
with tab2:
    st.header("➕ 新しいページを登録")
    with st.form("register_form"):
        title  = st.text_input("タイトル")
        url    = st.text_input("URL")
        desc   = st.text_area("説明文")
        author = st.text_input("作者名")
        kws    = st.text_input("キーワード（カンマ区切り）")
        cat    = st.text_input("カテゴリ")
        submitted = st.form_submit_button("登録する")

    if submitted and title and url:
        new_page = {
            "id": len(pages) + 1,
            "url": url,
            "title": title,
            "description": desc,
            "keywords": [k.strip() for k in kws.split(",") if k.strip()],
            "author": author,
            "created_at": "2025-01-01",
            "category": cat,
        }
        pages.append(new_page)
        save_pages(pages)
        st.success(f"「{title}」を登録しました！")
        st.cache_data.clear()

# ── 一覧タブ ──
with tab3:
    st.header("📋 登録済み一覧")
    st.metric("総件数", f"{len(pages)} 件")
    for page in pages:
        st.markdown(f"**[{page['title']}]({page['url']})**  —  {page['author']}  |  {page['category']}")
        st.caption(page["description"])
        st.markdown("---")
