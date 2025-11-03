from dotenv import load_dotenv
load_dotenv() 

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

# モデル設定
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

# 関数
def generate_response(selected_item: str, input_message: str) -> str:
    """選択された相談相手と入力テキストをもとにLLMの回答を返す関数（非ストリーミング版）"""
    if not input_message:
        return "質問が入力されていません。"

    # モードに応じたsystemプロンプトを設定
    if selected_item == "占い師":
        system_prompt = (
            "あなたはスピリチュアルな占い師です。"
            "星座・タロット・直感を用いて、相談者の運勢や気持ちを読み取り、"
            "優しく導くように答えてください。"
        )
    else:
        system_prompt = (
            "あなたは現実主義の科学者です。"
            "心理学や統計データに基づいて冷静に分析し、"
            "根拠のあるアドバイスをわかりやすく伝えてください。"
        )

    # プロンプトを組み立て
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    # メッセージを整形してLLMに渡す
    messages = prompt.format_messages(question=input_message)
    result = llm.invoke(messages)

    return result.content  # 回答文字列を返す

def generate_response_stream(selected_item: str, input_message: str):
    """選択された相談相手と入力テキストをもとにLLMの回答をストリーミングで返す関数"""
    if not input_message:
        yield "質問が入力されていません。"
        return

    # モードに応じたsystemプロンプトを設定
    if selected_item == "占い師":
        system_prompt = (
            "あなたはスピリチュアルな占い師です。"
            "星座・タロット・直感を用いて、相談者の運勢や気持ちを読み取り、"
            "優しく導くように答えてください。"
        )
    else:
        system_prompt = (
            "あなたは現実主義の科学者です。"
            "心理学や統計データに基づいて冷静に分析し、"
            "根拠のあるアドバイスをわかりやすく伝えてください。"
        )

    # プロンプトを組み立て
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    # メッセージを整形してLLMにストリーミングで渡す
    messages = prompt.format_messages(question=input_message)
    
    # ストリーミングで回答を生成
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content

# アプリ本体
st.title("Lesson 21: 提出課題用Webアプリ")

st.write("このアプリでは、2人の異なる専門家に相談できます。")
st.write("占い師は直感と神秘の力で、科学者はデータと論理の力であなたの質問に答えます。")
st.write("どちらに相談するかを選んで、質問を入力してください。")

# 相談相手の選択
selected_item = st.radio(
    "相談相手を選んでください。",
    ["占い師", "科学者"]
)

st.divider()

# 入力フォーム
if selected_item == "占い師":
    input_message = st.text_input(label="占い師に聞きたいことを入力してください。")
else:
    input_message = st.text_input(label="科学者に聞きたいことを入力してください。")

# 実行ボタン
if st.button("実行"):
    st.divider()

    if input_message:
        st.subheader(f"{selected_item}の回答")
        # ストリーミングで回答を表示
        st.write_stream(generate_response_stream(selected_item, input_message))
    else:
        st.warning("質問を入力してください。")
