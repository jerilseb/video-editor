import gradio as gr
from video_extractor import extract_screenshot

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Video Screenshot Extractor")
    gr.Markdown("Upload a video and specify a timestamp to extract a screenshot from that moment.")
    with gr.Row():
        video_input = gr.Video(label="Upload Video")
        timestamp_input = gr.Number(label="Timestamp (seconds)", value=0)
    screenshot_output = gr.Image(label="Screenshot")
    
    extract_button = gr.Button("Extract Screenshot")
    extract_button.click(fn=extract_screenshot, inputs=[video_input, timestamp_input], outputs=screenshot_output)

if __name__ == "__main__":
    demo.launch()
