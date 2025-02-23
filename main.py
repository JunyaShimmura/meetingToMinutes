import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

#.envから環境変数読み込む
load_dotenv()
#環境変数からAPIキー読み込む
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
#セッション　ボタン押下時にリロードされるためdownloadDataはセッション管理
if "downloadData" not in st.session_state:
    st.session_state.downloadData=""

#テキスト関連
st.title  ("会議から議事録")
st.caption("テスト用 WebApp")

#音声ファイルのアップロード
audioFile = st.file_uploader("音声ファイルをアップロードしてください")
if audioFile is not None :
    st.audio(audioFile,format="audio/mp3")
    st.success("音声ファイルをアップロードしました。")

#文字起こし、要約ボタン
transcriptBtn = st.button("文字起こし&要約")
if transcriptBtn:
    st.text("音声ファイルを文字起こし中")
    #文字起こし処理
    transcript = client.audio.transcriptions.create(
        model="whisper-1",file=audioFile,response_format="text"
    )
    #要約処理
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"あなたは優秀なアシスタントです。"},
            {"role":"user","content": f"この文章を要約してください 「{transcript} 」"}
        ]
    )
    resContent = res.choices[0].message.content
    #要約結果をdownloadDataに上書き
    st.session_state.downloadData=resContent

#ダウンロード処理 
outputTitle = st.text_input("議事録のファイル名 : ")
st.download_button(
    label="ダウンロード",
    data=st.session_state.downloadData,
    file_name=f"{outputTitle}.txt",
    mime="text/plain"
)

