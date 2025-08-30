from collections.abc import Generator
from typing import Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class SendEmailTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Send email notifications using AWS SNS"""
        
        # パラメータを取得
        topic_arn = tool_parameters.get("topic_arn")
        email = tool_parameters.get("email")
        subject = tool_parameters.get("subject", "")
        message = tool_parameters.get("message", "")
        
        # パラメータ検証
        if not topic_arn and not email:
            yield self.create_text_message("Error: Either topic_arn or email must be provided.")
            yield self.create_json_message({
                "success": False,
                "status": "Either topic_arn or email must be provided"
            })
            return
            
        if not subject:
            yield self.create_text_message("Error: Subject is required.")
            yield self.create_json_message({
                "success": False,
                "status": "Subject is required"
            })
            return
            
        if not message:
            yield self.create_text_message("Error: Message is required.")
            yield self.create_json_message({
                "success": False,
                "status": "Message is required"
            })
            return
        
        try:
            # 認証情報を取得
            aws_access_key_id = self.runtime.credentials.get("aws_access_key_id", "")
            aws_secret_access_key = self.runtime.credentials.get("aws_secret_access_key", "")
            aws_region = self.runtime.credentials.get("aws_region", "")
            
            if not aws_access_key_id or not aws_secret_access_key or not aws_region:
                yield self.create_text_message("Error: AWS credentials are not configured.")
                yield self.create_json_message({
                    "success": False,
                    "status": "AWS credentials are not configured"
                })
                return
            
            # AWS SNSクライアントを作成
            sns_client = boto3.client(
                'sns',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )
            
            # メッセージを送信
            response = None
            
            if topic_arn:
                # トピックにパブリッシュ
                try:
                    response = sns_client.publish(
                        TopicArn=topic_arn,
                        Subject=subject,
                        Message=message
                    )
                    
                    yield self.create_text_message(f"Message successfully published to topic: {topic_arn}")
                    
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    if error_code == 'NotFound':
                        yield self.create_text_message(f"Error: SNS topic not found: {topic_arn}")
                        yield self.create_json_message({
                            "success": False,
                            "status": f"SNS topic not found: {topic_arn}"
                        })
                        return
                    else:
                        raise
                        
            elif email:
                # 直接メールアドレスにサブスクリプションを作成して送信
                # 注: これは一時的なサブスクリプションのため、最初に確認メールが送信されます
                try:
                    # まず、既存のトピックを使用するか、新しいトピックを作成
                    # プロダクション環境では、専用のトピックを事前に作成することをお勧めします
                    temp_topic_name = f"dify-email-notification-{email.replace('@', '-').replace('.', '-')}"
                    
                    # トピックの作成を試みる
                    try:
                        topic_response = sns_client.create_topic(Name=temp_topic_name)
                        temp_topic_arn = topic_response['TopicArn']
                    except ClientError:
                        # トピックが既に存在する場合は、そのARNを取得
                        topics = sns_client.list_topics()
                        temp_topic_arn = None
                        for topic in topics.get('Topics', []):
                            if temp_topic_name in topic['TopicArn']:
                                temp_topic_arn = topic['TopicArn']
                                break
                        
                        if not temp_topic_arn:
                            raise
                    
                    # メールサブスクリプションを作成
                    subscription_response = sns_client.subscribe(
                        TopicArn=temp_topic_arn,
                        Protocol='email',
                        Endpoint=email,
                        ReturnSubscriptionArn=True
                    )
                    
                    # メッセージをパブリッシュ
                    response = sns_client.publish(
                        TopicArn=temp_topic_arn,
                        Subject=subject,
                        Message=message
                    )
                    
                    yield self.create_text_message(
                        f"Message sent to {email}. "
                        f"Note: The recipient must confirm the subscription first if this is their first notification."
                    )
                    
                except ClientError as e:
                    yield self.create_text_message(f"Error sending email: {str(e)}")
                    yield self.create_json_message({
                        "success": False,
                        "status": f"Error sending email: {str(e)}"
                    })
                    return
            
            # 成功レスポンスを返す
            if response:
                message_id = response.get('MessageId', '')
                yield self.create_json_message({
                    "success": True,
                    "message_id": message_id,
                    "status": "Email sent successfully"
                })
                yield self.create_variable_message("message_id", message_id)
            
        except ClientError as e:
            error_message = f"AWS SNS error: {str(e)}"
            yield self.create_text_message(f"Error: {error_message}")
            yield self.create_json_message({
                "success": False,
                "status": error_message
            })
            
        except BotoCoreError as e:
            error_message = f"AWS connection error: {str(e)}"
            yield self.create_text_message(f"Error: {error_message}")
            yield self.create_json_message({
                "success": False,
                "status": error_message
            })
            
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            yield self.create_text_message(f"Error: {error_message}")
            yield self.create_json_message({
                "success": False,
                "status": error_message
            })