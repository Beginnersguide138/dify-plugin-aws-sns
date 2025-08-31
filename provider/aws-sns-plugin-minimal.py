from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AwsSnsPluginProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        最小限の検証 - AWS APIを呼び出さずに基本的な検証のみ
        """
        # 必須認証情報を取得
        aws_access_key_id = credentials.get("aws_access_key_id", "").strip()
        aws_secret_access_key = credentials.get("aws_secret_access_key", "").strip()
        
        # 基本的な検証のみ実行
        if not aws_access_key_id:
            raise ToolProviderCredentialValidationError("AWS Access Key ID is required")
        
        if not aws_secret_access_key:
            raise ToolProviderCredentialValidationError("AWS Secret Access Key is required")
        
        # AWS Access Key IDの基本的な形式チェック
        # 通常は20文字の英数字（AKIA...で始まる）
        if len(aws_access_key_id) < 16:
            raise ToolProviderCredentialValidationError("AWS Access Key ID format is invalid (too short)")
        
        # AWS Secret Access Keyの基本的な形式チェック
        # 通常は40文字程度
        if len(aws_secret_access_key) < 30:
            raise ToolProviderCredentialValidationError("AWS Secret Access Key format is invalid (too short)")
        
        # この時点で基本的な検証は成功
        # 実際のAWS認証は、ツール実行時に行う