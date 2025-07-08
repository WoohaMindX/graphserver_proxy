"""
同步方式测试 LangGraph SDK 的 client.assistants.search() 方法
"""
from langgraph_sdk import get_sync_client
from utils import load_env_config, create_headers

def test_assistants_search_sync():
    """
    使用同步客户端测试 assistants.search() 方法
    """
    # 加载环境配置
    config = load_env_config()
    
    # 获取配置参数
    api_url = config.get('LANGGRAPH_API_URL', 'http://127.0.0.1:2024')
    api_key = config.get('LANGGRAPH_API_KEY', 'your_api_key')

    # 由于聚智平台使用了与langsmith不同的认证方式，这里不需要api_key
    # 而是需要传入聚智平台专门的header进行严重
    # client = get_sync_client(url=api_url, api_key=api_key, headers=headers)
    client = get_sync_client(url=api_url, api_key=api_key)

    # 创建同步客户端
    print(f"正在连接到: {api_url}")

    # 聚智平台通过专门的 header 进行认证，这里先创建header


    try:


        # 调用 assistants.search() 方法
        print("正在调用 client.assistants.search()...")
        result = client.assistants.search()
        
        # 输出结果
        print("搜索结果:")
        print(f"类型: {type(result)}")
        print(f"内容: {result}")
        
    except Exception as e:
        print(f"调用失败: {e}")

    try:
        ASSISTANT_ID = config.get('LANGGRAPH_ASSISTANT_ID', 'your_assistant_id')
        
        for chunk in client.runs.stream(
            thread_id=None,
            assistant_id=ASSISTANT_ID,
            input={"messages": [{"type": "human", "content": "你好"}]},
            stream_mode=["messages", "debug"],
            metadata={"run_type": "test_run"}
        ):
            print(f"流式输出: {chunk}")
    except Exception as e:
        print(f"调用失败: {e}")

def main():
    """
    主函数 - 演示同步方式的使用
    """
    print("=== LangGraph SDK 同步客户端测试 ===")
    test_assistants_search_sync()

if __name__ == "__main__":
    main()
