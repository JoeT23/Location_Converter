import gradio as gr
from converter import convert, generate_map, export_csv

with gr.Blocks() as demo:

    gr.Markdown("# 🇬🇧 UK National Grid Converter")

    # Store last result
    state = gr.State(None)

    with gr.Tabs():

        with gr.Tab("🏠 Home"):
            gr.Markdown("UK National Grid Converter with CSV export functionality")

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

            # ---------------- CONVERT FUNCTION ----------------
            def run_convert(mode, easting, northing, gridref):

                result = convert(mode, easting, northing, gridref)

                if "Latitude" not in result:
                    return result, "", None

                try:
                    parts = result.split(",")
                    lat = float(parts[0].split(":")[1])
                    lon = float(parts[1].split(":")[1])
                except:
                    return result, "", None

                map_html = generate_map(lat, lon)

                return result, map_html, {
                    "mode": mode,
                    "easting": easting,
                    "northing": northing,
                    "gridref": gridref,
                    "result": result
                }

            btn.click(
                fn=run_convert,
                inputs=[mode, easting, northing, gridref],
                outputs=[output_text, output_map, state]
            )

        # ---------------- EXPORT TAB ----------------
        with gr.Tab("⬇ Export CSV"):

            export_btn = gr.Button("Export Last Result")
            csv_file = gr.File(label="Download CSV")

            def do_export(data):
                if data is None:
                    return None
                return export_csv(
                    data.get("mode"),
                    data.get("easting"),
                    data.get("northing"),
                    data.get("gridref"),
                    data.get("result")
                )

            export_btn.click(
                fn=do_export,
                inputs=[state],
                outputs=[csv_file]
            )

demo.launch()
