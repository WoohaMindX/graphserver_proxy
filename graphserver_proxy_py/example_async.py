"""
异步方式测试 LangGraph SDK 的 client.assistants.search() 方法
"""
import asyncio
from langgraph_sdk import get_client
from utils import load_env_config, create_joinai_header

async def test_assistants_search_async():
    """
    使用异步客户端测试 assistants.search() 方法
    """
    # 加载环境配置
    config = load_env_config()
    
    # 获取配置参数
    api_url = config.get('JOINAI_ASSISTANT_API_URL', 'http://127.0.0.1:2024')

    # 聚智平台通过专门的 header 进行认证，这里先创建header
    app_id = config.get('JOINAI_APP_ID', 'your_app_id')
    app_key = config.get('JOINAI_APP_Key', 'your_app_key')
    app_path = config.get('JOINAI_APP_PATH', None)

    headers = create_joinai_header(app_id, app_key, app_path)

    try:
        # 创建异步客户端
        print(f"正在连接到: {api_url}")

        # 由于聚智平台使用了与langsmith不同的认证方式，这里不需要api_key
        # 而是需要传入聚智平台专门的header进行严重
        client = get_client(url=api_url, api_key=None, headers=headers)
        
        # 调用 assistants.search() 方法 (异步)
        print("正在调用 await client.assistants.search()...")
        result = await client.assistants.search()
        
        # 输出结果
        print("搜索结果:")
        print(f"类型: {type(result)}")
        print(f"内容: {result}")
        
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
