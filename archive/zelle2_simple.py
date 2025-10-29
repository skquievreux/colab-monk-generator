# =====================================================
# ZELLE 2: EINFACHE GRADIO UI
# =====================================================

%%blocks
import gradio as gr

with gr.Blocks(title="ACID MONK Hook Generator") as demo:
    gr.Markdown("# ACID MONK Hook Generator")
    gr.Markdown("Lade `.txt` mit `---` hoch → bekomme emotionale MP3-Hooks!")

    txt_in = gr.File(label="TXT hochladen", file_types=[".txt"])
    btn = gr.Button("GENERIEREN", variant="primary")
    zip_out = gr.File(label="Deine Hooks als ZIP")
    status = gr.Textbox(label="Status")

    btn.click(generate_hooks, txt_in, [zip_out, status])

demo.launch(share=True, debug=True)