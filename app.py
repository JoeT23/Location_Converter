# simplify UI with integrated converter py
import gradio as gr
from converter import convert

with gr.Blocks() as demo:

    gr.Markdown("# 🇬🇧 UK National Grid Converter")

    with gr.Tabs():

        with gr.Tab("Home"):
            gr.Markdown("Welcome to the UK National Grid Converter")

        with gr.Tab("Converter"):

            mode = gr.Radio(
                ["Easting / Northing", "Grid Reference"],
                label="Input Type"
            )

            easting = gr.Number(label="Easting")
            northing = gr.Number(label="Northing")
            gridref = gr.Textbox(label="Grid Reference")

            btn = gr.Button("Convert")
            output_text = gr.Textbox(label="Results")

            def run_convert(mode, easting, northing, gridref):
                return convert(mode, easting, northing, gridref)

            btn.click(
                fn=run_convert,
                inputs=[mode, easting, northing, gridref],
                outputs=output_text
            )

demo.launch()
