import gradio as gr
from converter import easting_northing_to_latlon, gridref_to_en

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

            def convert_ui(mode, easting, northing, gridref):

                if mode == "Easting / Northing":

                    if easting is None or northing is None:
                        return "Please enter values."

                    lat, lon = easting_northing_to_latlon(float(easting), float(northing))
                    return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

                else:

                    result = gridref_to_en(gridref)

                    if result is None:
                        return "Invalid grid reference"

                    e, n = result
                    lat, lon = easting_northing_to_latlon(e, n)

                    return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

            btn.click(
                fn=convert_ui,
                inputs=[mode, easting, northing, gridref],
                outputs=output_text
            )

demo.launch()
