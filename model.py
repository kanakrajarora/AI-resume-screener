import google.generativeai as genai

genai.configure(api_key="AIzaSyCyFg-j8XybpZcXKd2M_-GaAiJUEzpyi2g")

models = genai.list_models()

for m in models:
    print(m.name, m.supported_generation_methods)