import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_german_word_info(word):
    url = f"https://de.wiktionary.org/wiki/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"❌ failed:HTTP {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # 获取 IPA 音标
    ipa_spans = soup.find_all("span", class_="ipa")
    ipa_list = [span.get_text(strip=True) for span in ipa_spans]
    ipa_list = list(dict.fromkeys(ipa_list))  # 去重
    l =len(ipa_list)

    # 获取发音音频链接（.ogg 格式）
    audio_links = []
    for a in soup.find_all("a", href=True):
        if a["href"].endswith(".ogg"):
            full_url = "https:" + a["href"] if a["href"].startswith("//") else a["href"]
            audio_links.append(full_url)

    # 获取 Worttrennung（找 ID 为 mwDQ 的 <dd>）
    worttrennung = None
    dd_tag = soup.find("dd", id="mwDQ")
    if dd_tag:
        worttrennung = dd_tag.get_text(strip=True).split("Plural:")[0].strip(", ")

    return {
        "ipa": ipa_list,
        "audio": audio_links, 
        "worttrennung": worttrennung or "not found"
    }


st.title("📖 check transcription")

word = st.text_input("please enter german word: case sensitive")

if word:
    with st.spinner("🔍 searching..."):
        result = get_german_word_info(word)

    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("🔊 IPA ")
        # st.write(", ".join(result["ipa"]) if result["ipa"] else "未找到")
        st.write(result["ipa"][0] if result["ipa"] else "not found")

        st.subheader("📡 audio")
        if result["audio"]:
            st.markdown(f"[Audio]({result['audio'][0]})")
            # for i, link in enumerate(result["audio"], start=1):
            #     st.markdown(f"[Audio {i}]({link})")
        else:
            st.write("audio link not found")

        st.subheader("✂️ Worttrennung")
        st.write(result["worttrennung"])
