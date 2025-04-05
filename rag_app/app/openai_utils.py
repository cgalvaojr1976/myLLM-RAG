from openai import OpenAI

client = OpenAI()

def responder_com_openai(prompt: str, modelo: str = "gpt-3.5-turbo") -> str:
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
