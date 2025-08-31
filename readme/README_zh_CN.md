# AWS SNS 电子邮件通知插件（适用于 Dify）

<p align="center">
  <img src="../_assets/icon.svg" alt="AWS SNS Plugin Icon" width="120">
</p>

<p align="center">
  <a href="https://github.com/Beginnersguide138/dify-plugin-aws-sns/releases">
    <img src="https://img.shields.io/github/v/release/Beginnersguide138/dify-plugin-aws-sns?style=for-the-badge" alt="GitHub release">
  </a>
  <a href="https://github.com/Beginnersguide138/dify-plugin-aws-sns/issues">
    <img src="https://img.shields.io/github/issues/Beginnersguide138/dify-plugin-aws-sns?style=for-the-badge" alt="GitHub issues">
  </a>
  <a href="https://github.com/Beginnersguide138/dify-plugin-aws-sns/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Beginnersguide138/dify-plugin-aws-sns?style=for-the-badge" alt="GitHub license">
  </a>
</p>

**作者:** beginnersguide138  
**版本:** 0.0.2  
**类型:** tool  

此 Dify 插件可通过 AWS Simple Notification Service (SNS) 使用 IAM 身份验证发送电子邮件通知。

📄 **[英文版 README](./README_en.md)**  
📄 **[日本語版 ReadMe](../README.md)**

---

## 功能

- 通过 AWS SNS 发送电子邮件通知
- 支持 SNS 主题推送和直接邮件发送
- 基于 IAM 的安全访问认证
- 多语言支持（英语、日语、中文、葡萄牙语）

## 前置条件

- 启用 SNS 服务的 AWS 账户
- 拥有适当 SNS 权限的 IAM 用户
- AWS 访问密钥 ID（Access Key ID）和私密访问密钥（Secret Access Key）

## 所需 AWS IAM 权限

IAM 用户需要以下权限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "sns:Subscribe",
                "sns:CreateTopic",
                "sns:ListTopics"
            ],
            "Resource": "*"
        }
    ]
}
```

## 安装

1. 在 Dify 实例中安装插件
2. 在插件设置中配置 AWS 凭证：
   - AWS 访问密钥 ID
   - AWS 私密访问密钥
   - AWS 区域（例如：us-east-1, ap-northeast-1）

## 使用方法

### 通过 SNS 主题发送邮件

如果已有包含邮件订阅者的 SNS 主题：

```
工具: Send Email via SNS
参数:
- topic_arn: arn:aws:sns:region:account-id:topic-name
- subject: "邮件主题"
- message: "邮件正文"
```

### 直接发送邮件

直接向特定收件人发送：

```
工具: Send Email via SNS
参数:
- email: recipient@example.com
- subject: "邮件主题"
- message: "邮件正文"
```

**注意:** 发送到新地址时，收件人会先收到 AWS SNS 发送的订阅确认邮件，需确认订阅后方可接收通知。

## 配置

### 环境变量（开发用）

基于 `.env.example` 创建 `.env` 文件：

```bash
cp .env.example .env
```

然后在 `.env` 文件中添加凭证信息。

### 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行插件
python -m main
```

## 安全注意事项

- 切勿将 AWS 凭证提交到版本控制系统
- 使用具有最小权限的 IAM 角色
- 在生产环境中考虑使用 AWS STS 临时凭证
- 为敏感数据启用 SNS 加密

## 故障排查

### 常见问题

1. **Invalid credentials error（无效凭证错误）**
   - 检查 AWS 访问密钥 ID 和私密访问密钥是否正确
   - 确认 IAM 用户具有所需权限

2. **Topic not found error（主题未找到错误）**
   - 确认主题 ARN 是否正确
   - 确认主题存在于指定区域

3. **Email not received（未收到邮件）**
   - 检查收件人是否确认了 SNS 订阅
   - 确认邮件地址有效
   - 检查垃圾邮件文件夹

## 支持

如有问题，请访问: https://github.com/Beginnersguide138/dify-plugin-aws-sns/issues

## 许可证

MIT License - 详情请参阅 LICENSE 文件