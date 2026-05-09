import streamlit as st
import pandas as pd

# アプリのページ設定
st.set_page_config(page_title="生徒指導対応サポート", layout="centered")

st.title("💡 生徒指導対応サポートアプリ (詳細・Excel連携版)")
st.write("「アプローチ」「NG例」「終着点」を含めた詳細なマニュアルを表示します。")

# Excelファイルを読み込む関数
@st.cache_data
def load_data():
    # Excelファイルを読み込む
    df = pd.read_excel("guidance_data.xlsx")
    # 空白（NaN）がある場合、エラーを防ぐために空文字に変換
    df = df.fillna("")
    return df

try:
    # データの読み込みを実行
    data_table = load_data()
    
    # Excelの「シチュエーション」の列から、選択肢のリストを作る
    situations = data_table['シチュエーション'].tolist()
    
    # プルダウンメニューの作成
    selected_situation = st.selectbox("発生したシチュエーションを選択してください", ["-- 選択してください --"] + situations)
    
    st.markdown("---")
    
    # 選択された結果の表示
    if selected_situation != "-- 選択してください --":
        # 選ばれたシチュエーションの行を引っ張り出す
        selected_row = data_table[data_table['シチュエーション'] == selected_situation].iloc[0]
        
        st.subheader(f"📌 {selected_situation}")
        
        st.markdown("### 📋 対応の基本方針")
        st.info(selected_row["対応の基本方針"])
        
        st.markdown("### 🗺️ アプローチと話し合いの仕方")
        st.write(selected_row["アプローチと話し合いの仕方"])
        
        st.markdown("### ❌ NGな話し合い・対応")
        st.error(selected_row["NGな話し合い・対応"])
        
        st.markdown("### 🎯 指導の終着点（ゴール）")
        st.success(selected_row["指導の終着点（ゴール）"])
        
        # 声かけ例などは折りたたみメニューに入れる
        with st.expander("🗣️ 推奨される声かけ例 と 該当箇所 を見る"):
            st.write("**【OKな声かけ】**")
            st.write(selected_row["推奨される声かけ (OK)"])
            st.write("**【生徒指導提要 該当箇所】**")
            st.caption(selected_row["生徒指導提要 該当箇所"])
            
    else:
        st.write("👆 上のドロップダウンからシチュエーションを選ぶと、詳細な対応マニュアルが表示されます。")

except FileNotFoundError:
    st.error("⚠️ 「guidance_data.xlsx」というExcelファイルが見つかりません。app.pyと同じフォルダに保存されているか確認してください。")
except KeyError as e:
    st.error(f"⚠️ エクセルの列名が間違っているようです。1行目の見出しが正しいか確認してください。（エラー詳細: {e}）")
except Exception as e:
    st.error(f"⚠️ エラーが発生しました: {e}")
