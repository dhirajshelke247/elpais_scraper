def translate_text(text, to_lang="en"):
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()

    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "google-translate113.p.rapidapi.com",
    }
    payload = {
        "from": "auto",
        "to": to_lang,
        "text": text
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("trans", text)
    except Exception as e:
        print(f"[Translation Error] '{text}' → {e}")
        return text
