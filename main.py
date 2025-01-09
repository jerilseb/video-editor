import gradio as gr
from process_video import process_video

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Video Editing App</h1>")
    gr.Markdown("Upload a video and specify the edits you want to apply.")
    with gr.Row():
        video_input = gr.Video(label="Upload Video")
        video_output = gr.Video(label="Edited Video")
    with gr.Row():
        with gr.Column(scale=1):
            edit_instructions = gr.Textbox(label="Edit Instructions")
        with gr.Column(scale=1, min_width=0):
            extract_button = gr.Button("Submit")
    extract_button.click(
        fn=process_video, inputs=[video_input, edit_instructions], outputs=video_output
    )

if __name__ == "__main__":
    demo.launch(
        show_api=False,
        show_settings=False,
    )
