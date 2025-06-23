import crypto from "crypto";
import { v4 as uuidv4 } from "uuid";
import { Buffer } from "buffer";


/**
 * 创建用于 JoinAI Assistant API 请求的认证头部信息
 *
 * 该函数生成访问 JoinAI Assistant 服务所需的认证头部，包含服务器参数、时间戳和校验和。
 * 头部信息用于验证请求的合法性和完整性。
 * 
 * @param appid - 应用程序 ID，用于标识应用程序
 * @param appkey - 应用程序密钥，用于生成请求签名
 * @param path - 可选的路径参数，用于提取应用名称，默认为 "default"
 * @returns 包含认证信息的头部对象，包括：
 *   - X-Server-Param: Base64 编码的服务器参数
 *   - X-CurTime: 当前时间戳（秒）
 *   - X-CheckSum: MD5 校验和
 *   - Content-Type: 请求内容类型
 * 
 * @example
 * ```typescript
 * const headers = createJoinAIHeader("your-app-id", "your-app-key", "/app/endpoint");
 * // 返回类似：
 * // {
 * //   "X-Server-Param": "eyJhcHBpZCI6InlvdXItYXBwLWlkIiwiY3NpZCI6IjEyMzQ1Njc4OTAifQ==",
 * //   "X-CurTime": "1672531200",
 * //   "X-CheckSum": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
 * //   "Content-Type": "application/json"
 * // }
 * ```
 */
export function createJoinAIHeader(appid: string, appkey: string, path?: string): Record<string, string> {

  // Step 1: 获取应用名称（从 path 中提取，默认值为 "default"）
  let appName = path ? path.split("/")[1] : "default";

  // Step 2: 填充到 24 位长度（不足用 '0' 补齐）
  if (appName.length < 24) {
    appName = appName.padEnd(24, "0");
  }

  const csid = appid + appName + uuidv4(); // 构造 csid
  const serverParamObj = {
    appid: appid,
    csid: csid,
  };

  // Step 3: 当前时间戳（单位：秒）
  const xCurTime = Math.floor(Date.now() / 1000).toString();

  // Step 4: Base64 编码服务器参数
  const serverParamStr = JSON.stringify(serverParamObj);
  const xServerParam = Buffer.from(serverParamStr, "utf-8").toString("base64");

  // Step 5: 生成签名 CheckSum：MD5(appkey + xCurTime + xServerParam)
  const raw = appkey + xCurTime + xServerParam;
  const xCheckSum = crypto.createHash("md5").update(raw, "utf8").digest("hex");

  // Step 6: 构造请求头
  const headers: Record<string, string> = {
    "X-Server-Param": xServerParam,
    "X-CurTime": xCurTime,
    "X-CheckSum": xCheckSum,
    "Content-Type": "application/json",
  };

  return headers;
}