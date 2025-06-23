# GraphServer Proxy Python

这是一个项目主要用于连接和测试聚智平台（JoinAI）的 Assistant API。项目使用 LangGraph SDK 实现了同步和异步两种方式的客户端连接。

## 功能特性

- 🔐 **聚智平台认证**：实现了聚智平台专用的认证头生成机制
- 🔄 **同步/异步支持**：提供同步和异步两种客户端连接方式
- ⚙️ **配置管理**：通过 `.env` 文件管理环境配置
- 🛠️ **工具函数**：提供认证头生成、配置加载等实用工具

## 项目结构

```
graphserver_proxy_py/
├── example.py              # 同步客户端测试示例
├── example_async.py        # 异步客户端测试示例
├── utils.py             # 工具函数（认证、配置加载）
├── pyproject.toml       # 项目配置文件
├── .env                 # 环境变量配置
├── .gitignore          # Git 忽略文件
└── README.md           # 项目说明文档
```

## 依赖要求

- Python >= 3.11
- langgraph-sdk >= 0.1.70
- python-dotenv >= 1.1.0

## 安装和配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd graphserver_proxy_py
```

### 2. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env` 文件并填入您的配置信息：

```bash
cp .env.example .env
```

在 `.env` 文件中配置以下参数：

```env
# 聚智平台应用 ID
JOINAI_APP_ID=your_app_id_here

# 聚智平台应用密钥
JOINAI_APP_KEY=your_app_secret_here

# API 服务地址
JOINAI_ASSISTANT_API_URL=http://127.0.0.1:2024

# 应用路径（可选）
JOINAI_APP_PATH=/api/v1/assistants
```

## 使用方法

### 同步方式测试

运行同步客户端测试：

```bash
python example.py
```

示例代码：

```python
from langgraph_sdk import get_sync_client
from utils import load_env_config, create_joinai_header

# 加载配置
config = load_env_config()

# 创建认证头
headers = create_joinai_header(
    config.get('JOINAI_APP_ID'),
    config.get('JOINAI_APP_KEY'),
    config.get('JOINAI_APP_PATH')
)

# 创建同步客户端
client = get_sync_client(
    url=config.get('JOINAI_ASSISTANT_API_URL'),
    api_key=None,
    headers=headers
)

# 调用 API
result = client.assistants.search()
```

### 异步方式测试

运行异步客户端测试：

```bash
python example_async.py
```

示例代码：

```python
import asyncio
from langgraph_sdk import get_client
from utils import load_env_config, create_joinai_header

async def test_async():
    # 加载配置
    config = load_env_config()
    
    # 创建认证头
    headers = create_joinai_header(
        config.get('JOINAI_APP_ID'),
        config.get('JOINAI_APP_KEY'),
        config.get('JOINAI_APP_PATH')
    )
    
    # 创建异步客户端
    client = get_client(
        url=config.get('JOINAI_ASSISTANT_API_URL'),
        api_key=None,
        headers=headers
    )
    
    # 调用 API (异步)
    result = await client.assistants.search()
    return result

# 运行异步函数
asyncio.run(test_async())
```

## API 说明

### 工具函数

#### `load_env_config(env_path: str = ".env") -> dict`

加载 `.env` 文件中的配置信息。

**参数：**
- `env_path`: `.env` 文件路径，默认为当前目录

**返回：**
- `dict`: 包含所有环境变量的字典

#### `create_joinai_header(appid: str, appkey: str, path: str | None = None) -> dict`

创建聚智平台 API 请求所需的认证请求头。

**参数：**
- `appid`: 聚智平台应用 ID
- `appkey`: 聚智平台应用密钥
- `path`: API 路径，可选，默认为 None

**返回：**
- `dict`: 包含认证信息的请求头字典

**请求头包含：**
- `X-Server-Param`: Base64 编码的服务器参数
- `X-CurTime`: 当前时间戳
- `X-CheckSum`: MD5 签名校验值
- `Content-Type`: 请求内容类型

## 认证机制

项目使用聚智平台专用的认证机制：

1. **应用标识**：通过 `JOINAI_APP_ID` 标识应用
2. **签名计算**：使用 `JOINAI_APP_KEY` 计算 MD5 签名
3. **时间戳验证**：包含当前时间戳防止重放攻击
4. **参数编码**：使用 Base64 编码传输服务器参数

签名算法：`MD5(appkey + 时间戳 + Base64编码的服务器参数)`

## 开发说明

### 项目特点

- 兼容聚智平台的认证规范
- 支持同步和异步两种调用方式
- 提供完整的错误处理机制
- 配置文件与代码分离，便于部署

### 扩展开发

如需添加更多 API 调用，可以参考现有的实现方式：

1. 在 `utils.py` 中添加相关工具函数
2. 在 `main.py` 或 `main_async.py` 中添加测试代码
3. 更新配置文件添加新的环境变量

## 故障排除

### 常见问题

1. **认证失败**
   - 检查 `JOINAI_APP_ID` 和 `JOINAI_APP_KEY` 是否正确
   - 确认服务器时间与本地时间同步

2. **连接失败**
   - 检查 `JOINAI_ASSISTANT_API_URL` 是否可访问
   - 确认网络连接正常

3. **导入错误**
   - 确认已正确安装所有依赖包
   - 检查 Python 版本是否 >= 3.11

### 调试模式

可以在代码中添加更多日志输出来调试问题：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
# 您的代码...
```

## 许可证

本项目使用 MIT 许可证。详情请参见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

*本项目是聚智平台 GraphServer 的 Python 客户端实现，用于测试和集成 LangGraph SDK。*