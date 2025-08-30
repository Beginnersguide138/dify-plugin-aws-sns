from typing import Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

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
            
            # AWS SNSクライアントを作成して認証情報をテスト
            sns_client = boto3.client(
                'sns',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )
            
            # 認証情報の有効性を確認（トピック一覧を取得）
            # list_topicsを呼び出して認証情報が有効かを確認
            sns_client.list_topics()
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClientTokenId':
                raise ToolProviderCredentialValidationError("Invalid AWS Access Key ID")
            elif error_code == 'SignatureDoesNotMatch':
                raise ToolProviderCredentialValidationError("Invalid AWS Secret Access Key")
            elif error_code == 'AuthFailure':
                raise ToolProviderCredentialValidationError("AWS authentication failed")
            else:
                raise ToolProviderCredentialValidationError(f"AWS SNS error: {str(e)}")
        except BotoCoreError as e:
            raise ToolProviderCredentialValidationError(f"AWS connection error: {str(e)}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

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
