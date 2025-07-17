"""
异步方式测试 LangGraph SDK 的 client.assistants.search() 方法
"""
import asyncio
from langgraph_sdk import get_client
from utils import load_env_config, create_headers

async def test_assistants_search_async():
    """
    使用异步客户端测试 assistants.search() 方法
    """
    # 加载环境配置
    config = load_env_config()
    
    # 获取配置参数
    api_url = config.get('LANGGRAPH_API_URL', 'http://127.0.0.1:2024')
    api_key = config.get('LANGGRAPH_API_KEY', 'your_api_key')
    app_id = config.get("APP_ID", "your_app_id")
    app_secret = config.get("APP_SECRET", "your_app_secret")
    app_host = config.get("APP_HOST", "you_app_host")


    # 创建异步客户端
    print(f"正在连接到: {api_url}")

    # 由于聚智平台使用了与langsmith不同的认证方式，这里不需要api_key
    # 而是需要传入聚智平台专门的header进行认证
    headers = create_headers(
        app_id=app_id, 
        app_secret=app_secret,
        host=app_host
        )
    client = get_client(url=api_url, api_key=api_key, headers=headers)
    # client = get_client(url=api_url, api_key=api_key)
    ASSISTANT_ID = config.get('LANGGRAPH_ASSISTANT_ID')
    try:

        # 调用 assistants.search() 方法 (异步)
        print("正在调用 await client.assistants.search()...")
        result = await client.assistants.search()
        
        # 输出结果
        print("搜索结果:")
        print(f"类型: {type(result)}")
        print(f"内容: {result}")
        ASSISTANT_ID = result[0].get('assistant_id') if result else config.get('LANGGRAPH_ASSISTANT_ID')
    except Exception as e:
        print(f"调用失败: {e}")

    try:

        # ASSISTANT_ID = config.get('LANGGRAPH_ASSISTANT_ID', 'your_assistant_id')
        # 创建thread.run()进行流式对话
        async for chunk in client.runs.stream(
            thread_id=None,
            assistant_id=ASSISTANT_ID,
            input={"messages": [{"type": "human", "content": "你好"}]},
            stream_mode=["messages", "debug"],
            metadata={"run_type": "test_run"}
        ):
            print(f"流式输出: {chunk}")
    except Exception as e:
        print(f"调用失败: {e}")

async def main():
    """
    主函数 - 演示异步方式的使用
    """
    print("=== LangGraph SDK 异步客户端测试 ===")
    await test_assistants_search_async()

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
