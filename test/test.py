import gradio as gr

def chat_predict(prompt):
    # 模拟你的 API 调用
    return f"你输入了: {prompt}\n这是扩展回答..."

def handle_chat(chat_input_value, chat_history):
    # import pdb;pdb.set_trace()
    final_prompt = chat_predict(chat_input_value)
    new_history = chat_history + [[chat_input_value, final_prompt]]
    return new_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        height=600,
        value=[["", "欢迎使用！请输入您的问题。"]],
        bubble_full_width=False,
        show_copy_button=True,
        container=True
    )
    chat_input = gr.Textbox(label="输入提示词", placeholder="Enter your prompt here...")
    generate_btn = gr.Button('发送')

    generate_btn.click(
        fn=handle_chat,
        inputs=[chat_input, chatbot],
        outputs=[chatbot]
    )

demo.launch()