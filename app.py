import gradio as gr
from converter import easting_northing_to_latlon

# ----------------------------
# UI
# ----------------------------

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

            def convert_ui(easting, northing):
                lat, lon = easting_northing_to_latlon(easting, northing)
                return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

            btn.click(
                fn=convert_ui,
                inputs=[easting, northing],
                outputs=output_text
            )

demo.launch()
