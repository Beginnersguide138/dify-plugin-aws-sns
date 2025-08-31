from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AwsSnsPluginProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        極めてシンプルな認証検証
        boto3のインポートを遅延させ、エラーを最小限に
        """
        try:
            # 必須認証情報を取得（空白を除去）
            aws_access_key_id = credentials.get("aws_access_key_id", "").strip()
            aws_secret_access_key = credentials.get("aws_secret_access_key", "").strip()
            aws_region = credentials.get("aws_region", "").strip()
            
            # 基本的な検証のみ
            if not aws_access_key_id:
                raise ToolProviderCredentialValidationError("AWS Access Key ID is required")
            if not aws_secret_access_key:
                raise ToolProviderCredentialValidationError("AWS Secret Access Key is required")
            
            # リージョンのデフォルト値
            if not aws_region:
                aws_region = "us-east-1"
            
            # boto3を動的にインポート（パッケージングの問題を回避）
            try:
                import boto3
                from botocore.exceptions import ClientError, BotoCoreError
            except ImportError as e:
                raise ToolProviderCredentialValidationError(f"Failed to import boto3: {str(e)}")
            
            # 最も基本的な認証確認を試みる
            try:
                # STSクライアントを作成
                sts_client = boto3.client(
                    'sts',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region
                )
                
                # 認証の確認
                sts_client.get_caller_identity()
                
                # 成功 - 何もしない
                
            except ClientError as e:
                # エラーコードを取得
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                error_message = e.response.get('Error', {}).get('Message', 'No message')
                
                # デバッグ用の詳細なエラー情報
                if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch']:
                    raise ToolProviderCredentialValidationError(
                        f"Invalid AWS credentials: {error_code} - {error_message}"
                    )
                else:
                    # その他のエラーも詳細に報告
                    raise ToolProviderCredentialValidationError(
                        f"AWS error: {error_code} - {error_message}"
                    )
                    
            except BotoCoreError as e:
                raise ToolProviderCredentialValidationError(
                    f"Connection error: {str(e)}"
                )
            except Exception as e:
                # boto3関連の予期しないエラー
                raise ToolProviderCredentialValidationError(
                    f"Unexpected boto3 error: {type(e).__name__} - {str(e)}"
                )
                
        except ToolProviderCredentialValidationError:
            # 既にToolProviderCredentialValidationErrorの場合はそのまま再送出
            raise
        except Exception as e:
            # その他の予期しないエラー
            raise ToolProviderCredentialValidationError(
                f"Validation failed: {type(e).__name__} - {str(e)}"
            )