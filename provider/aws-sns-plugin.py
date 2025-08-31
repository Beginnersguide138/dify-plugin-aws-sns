from typing import Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError, NoCredentialsError

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AwsSnsPluginProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 必須認証情報を取得
            aws_access_key_id = credentials.get("aws_access_key_id", "")
            aws_secret_access_key = credentials.get("aws_secret_access_key", "")
            aws_region = credentials.get("aws_region", "")
            
            # 認証情報の検証
            if not aws_access_key_id:
                raise ToolProviderCredentialValidationError("AWS Access Key ID is required")
            if not aws_secret_access_key:
                raise ToolProviderCredentialValidationError("AWS Secret Access Key is required")
            if not aws_region:
                raise ToolProviderCredentialValidationError("AWS Region is required")
            
            # STSを使用してより確実に認証を検証
            # STSは全てのAWSアカウントで利用可能で、最小限の権限で動作
            try:
                sts_client = boto3.client(
                    'sts',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region
                )
                
                # GetCallerIdentityは最も基本的なAWS API呼び出し
                # 認証が有効であれば必ず成功する
                caller_identity = sts_client.get_caller_identity()
                
                # 認証成功 - アカウント情報が取得できた
                # SNSクライアントも作成してみる（エラーがあってもここでは無視）
                try:
                    sns_client = boto3.client(
                        'sns',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=aws_region
                    )
                    # SNSサービスが利用可能か軽くチェック（エラーは無視）
                    # これは認証の検証ではなく、サービスの利用可能性の確認
                except:
                    # SNSクライアント作成に失敗しても、認証自体は成功している
                    pass
                    
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                error_message = e.response.get('Error', {}).get('Message', '')
                
                # 明確な認証エラーのみを処理
                if error_code == 'InvalidClientTokenId':
                    raise ToolProviderCredentialValidationError("Invalid AWS Access Key ID")
                elif error_code == 'SignatureDoesNotMatch':
                    raise ToolProviderCredentialValidationError("Invalid AWS Secret Access Key")
                elif error_code in ['AuthFailure', 'UnrecognizedClientException', 'TokenRefreshRequired']:
                    raise ToolProviderCredentialValidationError("AWS authentication failed")
                elif error_code == 'RequestExpired':
                    raise ToolProviderCredentialValidationError("Request expired - please check your system time")
                elif 'security token' in error_message.lower():
                    raise ToolProviderCredentialValidationError("Security token issue - please check credentials")
                else:
                    # その他のエラーは詳細を含めて報告
                    raise ToolProviderCredentialValidationError(f"AWS API error: {error_code} - {error_message}")
                    
            except NoCredentialsError:
                raise ToolProviderCredentialValidationError("AWS credentials not found or invalid format")
            except BotoCoreError as e:
                # ネットワークエラーなど
                raise ToolProviderCredentialValidationError(f"AWS connection error: {str(e)}")
                
        except ToolProviderCredentialValidationError:
            # 既にToolProviderCredentialValidationErrorの場合はそのまま再送出
            raise
        except Exception as e:
            # 予期しないエラー
            raise ToolProviderCredentialValidationError(f"Unexpected error during validation: {str(e)}")

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for aws-sns-plugin OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""
        
    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
