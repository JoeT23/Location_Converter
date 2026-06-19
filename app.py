import gradio as gr

# ----------------------------
# UI ONLY for the location conversion section of the app
# ----------------------------

with gr.Blocks() as demo:

    gr.Markdown("# UK Location Converter")

    with gr.Tabs():

        # HOME TAB
        with gr.Tab("Home"):
            gr.Markdown("Welcome to the UK National Grid Converter")

        # CONVERTER TAB
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
            output_map = gr.HTML(label="Map Output")

demo.launch()
