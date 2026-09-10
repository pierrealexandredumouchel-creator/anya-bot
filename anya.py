import httpx

def anya_ai(prompt: str) -> str:
    """
    Backend IA pour Anya.
    Remplace l’URL et la clé par ton provider réel (xAI, Gemini, etc.)
    """
    try:
        if not prompt.strip():
            return "Tu dois me donner quelque chose à analyser."

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }

        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {OPENAI_KEY}"},
            timeout=20
        )

        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]

        # coupe si trop long pour IRC
        if len(reply) > 400:
            reply = reply[:397] + "..."

        return reply

    except Exception as e:
        return f"Erreur IA: {e}"
