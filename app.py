# -*- coding: utf-8 -*-
import gradio as gr
from deal_sourcer import fetch_deals

def source_and_format(model_name):
    deals = fetch_deals(model_name)
    headers = ["Repository", "Founder", "Stars", "Verdict", "Score", "Reasoning"]
    rows = [
        [
            d.get("repo", "N/A"),
            d.get("founder", "N/A"),
            d.get("stars", 0),
            d.get("verdict", "N/A"),
            f"{d.get('score', 0)}/100",
            d.get("reason", "N/A")
        ] for d in deals
    ]
    return gr.update(value=rows, headers=headers)

def load_cached_data():
    import json
    try:
        with open("output.json", encoding="utf-8") as f:
            deals = json.load(f)
    except Exception:
        try:
            with open("ideal_output.json", encoding="utf-8") as f:
                deals = json.load(f)
        except Exception:
            return []
    return [
        [
            d.get("repo", "N/A"),
            d.get("founder", "N/A"),
            d.get("stars", 0),
            d.get("verdict", "N/A"),
            f"{d.get('score', 0)}/100",
            d.get("reason", "N/A")
        ] for d in deals
    ]

with gr.Blocks(title="AI Project Scout") as demo:
    gr.Markdown("# 👁️ AI Project Scout & Deal Finder")
    gr.Markdown("Query GitHub CLI for trending repos, fetch founder profiles, and evaluate investability with local LLMs.")
    
    with gr.Row():
        model_opt = gr.Dropdown(choices=["minicpm5:1b", "llama3.2:3b", "gemma4:e2b"], value="minicpm5:1b", label="Ollama Model")
        btn = gr.Button("🔍 Scan & Evaluate Deals", variant="primary")
        
    table = gr.Dataframe(headers=["Repository", "Founder", "Stars", "Verdict", "Score", "Reasoning"], value=load_cached_data(), interactive=False)
    btn.click(fn=source_and_format, inputs=[model_opt], outputs=[table])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme="soft")
