from src.client.unified_api import UnifiedAPI
from src.configs import logger

def main():
    # 指定平台
    platform = input("请选择平台 (openai/volcengine/transformer/vllm，默认为 transformer): ") or "transformer"
    if platform not in ["openai", "volcengine", "transformer", "vllm"]:
        print("无效的平台，默认使用 transformer")
        platform = "transformer"

    # 初始化 UnifiedAPI
    api = UnifiedAPI()
    print(f"使用 {platform} 平台。输入提示词进行问答，输入 'exit' 退出。")

    # 进入问答循环
    while True:
        prompt = input("> ")
        if prompt.lower() == "exit":
            print("退出程序")
            break
        try:
            response = api.chat(prompt, platform=platform)
            print(response)
        except Exception as e:
            logger.error(f"CLI chat failed for {platform}: {str(e)}", exc_info=True)
            print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()