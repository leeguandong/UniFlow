import gradio as gr
from client.unified_api import UnifiedAPI
from configs import logger


def chat_interface(prompt, platform, system_prompt, image_file, chatbot_history):
    api = UnifiedAPI()
    image_path = image_file.name if image_file else None
    chatbot_history.append([prompt if not image_path else f"{prompt} (with image: {image_path})", None])

    try:
        result = api.chat(prompt, platform=platform, system_prompt=system_prompt, image_path=image_path)
        chatbot_history[-1][1] = result
        logger.info(f"Gradio chat successful for {platform}: Prompt: {prompt}, Response: {result}")
        return chatbot_history, "", None
    except Exception as e:
        logger.error(f"Gradio chat failed: {str(e)}", exc_info=True)
        chatbot_history[-1][1] = f"Error: {str(e)}"
        return chatbot_history, "", None


def show_logs():
    with open("logs/uniflow.log", "r", encoding="utf-8") as f:
        return f.read()


with gr.Blocks() as demo:
    gr.Markdown("# Uniflow Chat")
    chatbot = gr.Chatbot(label="对话历史")
    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(label="输入提示词", placeholder="请输入您的问题...")
            platform_input = gr.Dropdown(label="平台", choices=["openai", "volcengine", "transformer", "vllm"],
                                         value="openai")
            system_prompt_input = gr.Textbox(label="System Prompt", value="You are a helpful assistant.")
            image_input = gr.File(label="上传图片（可选）")
        with gr.Column():
            submit_btn = gr.Button("提交")
            log_output = gr.Textbox(label="日志", lines=10)
            log_btn = gr.Button("查看日志")

    submit_btn.click(
        fn=chat_interface,
        inputs=[prompt_input, platform_input, system_prompt_input, image_input, chatbot],
        outputs=[chatbot, prompt_input, image_input]
    )
    log_btn.click(fn=show_logs, outputs=log_output)

if __name__ == "__main__":
    demo.launch()