import argparse

def start_transformer_server():
    from server.transformer_server import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

def start_vllm_server():
    from server.vllm_server import start_vllm_service
    start_vllm_service()

def start_gradio_ui():
    from frontend.gradio_ui import demo
    demo.launch()

def start_client_test():
    from client.unified_api import UnifiedAPI
    api = UnifiedAPI()
    print(api.chat("Hello", platform="openai"))
    print(api.chat("Hello", platform="transformer"))
    print(api.chat("Hello", platform="vllm"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="启动 Uniflow 服务")
    parser.add_argument("--service", choices=["transformer", "vllm", "gradio", "client"], default="gradio")
    args = parser.parse_args()

    if args.service == "transformer":
        start_transformer_server()
    elif args.service == "vllm":
        start_vllm_server()
    elif args.service == "gradio":
        start_gradio_ui()
    else:
        start_client_test()