# AWS SNSメール通知プラグイン（Dify用）

<p align="center">
  <img src="./_assets/icon.svg" alt="AWS SNS Plugin Icon" width="120">
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
**バージョン:** 0.0.2
**タイプ:** tool

このDifyプラグインは、AWS Simple Notification Service (SNS) を使用してIAM認証によりEメール通知を送信できる機能を提供します。

📄 **[English README](./readme/README_en.md)**
📄 **[中文说明](./readme/README_zh_CN.md)**

---

## 機能

- AWS SNSを介したEメール通知送信
- SNSトピック宛および直接メール送信の両方をサポート
- セキュアアクセスのためのIAM認証
- 多言語対応（英語、日本語、中国語、ポルトガル語）

## 前提条件

- SNSサービスが有効なAWSアカウント
- 必要なSNS権限を持つIAMユーザー
- AWSアクセスキーIDとシークレットアクセスキー

## 必要なIAM権限

IAMユーザーは以下の権限を持つ必要があります：

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

## インストール

1. Difyインスタンスにプラグインをインストール
2. プラグイン設定でAWS認証情報を入力：
   - AWSアクセスキーID
   - AWSシークレットアクセスキー
   - AWSリージョン（例: us-east-1, ap-northeast-1）

## 使い方

### SNSトピック経由でメール送信

既存のSNSトピック（メール購読者あり）がある場合：

```
ツール: Send Email via SNS
パラメータ:
- topic_arn: arn:aws:sns:region:account-id:topic-name
- subject: "メール件名"
- message: "メール本文"
```

### 直接メール送信

特定の受信者に直接送信する場合：

```
ツール: Send Email via SNS
パラメータ:
- email: recipient@example.com
- subject: "メール件名"
- message: "メール本文"
```

**注意:** 新しいメールアドレスに送信する場合、AWS SNSから購読確認メールが届きます。受信者が購読を承認するまで通知は送信されません。

## 設定

### 環境変数（開発用）

`.env.example`をもとに`.env`ファイルを作成：

```bash
cp .env.example .env
```

その後、認証情報を設定します。

### ローカルテスト

```bash
# 依存関係のインストール
pip install -r requirements.txt

# プラグインを実行
python -m main
```

## セキュリティ上の注意

- AWS認証情報をバージョン管理に含めない
- 必要最小限の権限を持つIAMロールを使用
- 本番環境では一時認証情報（AWS STS）の利用を検討
- 機密データのSNS暗号化を有効化

## トラブルシューティング

### よくある問題

1. **Invalid credentials error（認証エラー）**
   - AWSアクセスキーIDとシークレットアクセスキーを確認
   - IAMユーザーに必要な権限が付与されているか確認

2. **Topic not found error（トピックが見つからない）**
   - トピックARNが正しいか確認
   - 指定リージョンにトピックが存在するか確認

3. **Email not received（メール未着）**
   - 受信者がSNS購読を承認しているか確認
   - メールアドレスが有効か確認
   - スパム/迷惑メールフォルダを確認

## サポート

質問や不具合は以下へ: https://github.com/Beginnersguide138/dify-plugin-aws-sns/issues

## ライセンス

MIT License - 詳細はLICENSEファイル参照
