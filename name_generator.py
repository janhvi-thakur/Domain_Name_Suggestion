from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_names_llm(url: str, description: str):
    if not description:
        return []

    prompt = f"""
You are a branding expert.

Task:
Generate 5 to 7 meaningful, short, brandable Hindi domain name suggestions.

Rules:
- Use only Hindi (Devanagari script)
- No English words
- No spaces (join words naturally)
- Keep names short (max ~20 characters)
- Sound professional and trustworthy
- Do not add explanations
- Return only a numbered list (1. ..., 2. ...)

Context:
Website URL (for context only): {url}
Company/Website description: {description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate brandable Hindi domain names."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )

        raw_text = response.choices[0].message.content or ""

        names = []
        for line in raw_text.split("\n"):
            line = line.strip()
            if re.match(r"^\d+\.", line):
                name = line.split(".", 1)[1].strip()
                # extra cleaning: remove spaces if LLM accidentally includes
                name = name.replace(" ", "")
                names.append(name)

        return names[:7]

    except Exception as e:
        print("LLM error:", repr(e))
        return []
