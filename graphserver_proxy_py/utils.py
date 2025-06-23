import math
import time
import base64
import json
import hashlib
import uuid
import os
from dotenv import dotenv_values
from typing import Optional


def load_env_config(env_path: str = ".env") -> dict:
    """
    加载并返回 .env 文件中的所有配置
    Args:
        env_path (str): .env 文件的路径，默认为当前目录下的 .env 文件
    Returns:
        dict: 包含所有环境变量的字典
    """
    # 加载 .env 文件
    config = dotenv_values(env_path)
    
    return config




def create_joinai_header(appid: str, appkey: str, path: str | None = None) -> dict:
    """
    创建 JoinAI Assistant API 请求所需的认证请求头

    该函数根据 JoinAI Assistant API 的认证规范，生成包含签名验证信息的 HTTP 请求头。
    请求头包含以下关键字段：
    - X-Server-Param: Base64 编码的服务器参数（包含 appid 和 csid）
    - X-CurTime: 当前时间戳
    - X-CheckSum: MD5 签名校验值
    - Content-Type: 请求内容类型
    
    Args:
        appid (str): JoinAI Assistant 应用 ID，用于标识应用身份
        appkey (str): JoinAI Assistant 应用密钥，用于签名计算
        path (str | None, optional): API 路径，用于提取应用名称。
                                   如果为 None，则使用默认应用名称 "default"。
                                   默认值为 None。
    
    Returns:
        dict: 包含认证信息的请求头字典，包含以下键值对：
            - "X-Server-Param": Base64 编码的服务器参数
            - "X-CurTime": 时间戳字符串
            - "X-CheckSum": MD5 签名字符串
            - "Content-Type": "application/json"
    
    Example:
        >>> header = create_joinai_header("your_app_id", "your_app_key", "/api/v1/chat")
        >>> print(header["Content-Type"])
        application/json
        
        >>> header = create_joinai_header("your_app_id", "your_app_key")
        >>> # 使用默认 path，应用名称为 "default"
    
    Note:
        - 应用名称会被填充到 24 位长度（不足部分用 "0" 填充）
        - csid 由 appid + 应用名称 + UUID 组成
        - 签名计算公式：MD5(appkey + 时间戳 + Base64编码的服务器参数)
    """
    
    _app_id = appid
    _app_key = appkey
    uuid_str = str(uuid.uuid1())
    if path is None:
        _app_name = "default"
    else:
        _app_name = path.split('/')[1]
    for i in range(24 - len(_app_name)):
        _app_name += "0"
    capabilityname = _app_name
    csid = _app_id + capabilityname + uuid_str
    tmp_xServerParam = {
        "appid": _app_id,
        "csid": csid
    }
    TDEV = 0
    xCurTime = str(int(math.floor(time.time())) + TDEV)
    xServerParam = str(base64.b64encode(json.dumps(
        tmp_xServerParam).encode('utf-8')), encoding="utf8")
    xCheckSum = hashlib.md5(
        bytes(_app_key + xCurTime + xServerParam, encoding="utf8")).hexdigest()
    
    # 构建请求头
    header = {
        "X-Server-Param": xServerParam,
        "X-CurTime": xCurTime,
        "X-CheckSum": xCheckSum,
        'Content-Type': 'application/json'
    }
    return header