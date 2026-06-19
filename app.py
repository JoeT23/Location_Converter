# simplify UI with integrated converter py
import gradio as gr
from converter import convert, generate_map

with gr.Blocks() as demo:

    gr.Markdown("# 🇬🇧 UK National Grid Converter")

    with gr.Tabs():

        with gr.Tab("🏠 Home"):
            gr.Markdown("Welcome to the UK National Grid Converter")

        with gr.Tab("🗺 Converter"):

            mode = gr.Radio(
                ["Easting / Northing", "Grid Reference"],
                label="Input Type"
            )

            easting = gr.Number(label="Easting")
            northing = gr.Number(label="Northing")
            gridref = gr.Textbox(label="Grid Reference")

            btn = gr.Button("Convert")

            output_text = gr.Textbox(label="Results")
            output_map = gr.HTML(label="Map")

            def run_convert(mode, easting, northing, gridref):

                result = convert(mode, easting, northing, gridref)

                # If result is an error message
                if "Latitude" not in result:
                    return result, ""

                # Extract lat/lon from string
                try:
                    parts = result.split(",")
                    lat = float(parts[0].split(":")[1])
                    lon = float(parts[1].split(":")[1])
                except:
                    return result, ""

                map_html = generate_map(lat, lon)

                return result, map_html

            btn.click(
                fn=run_convert,
                inputs=[mode, easting, northing, gridref],
                outputs=[output_text, output_map]
            )

demo.launch()
