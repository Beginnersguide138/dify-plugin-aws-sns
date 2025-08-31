# AWS SNS Email Notification Plugin for Dify

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

**Author:** beginnersguide138  
**Version:** 0.0.2  
**Type:** tool  

A Dify plugin that enables sending email notifications through AWS Simple Notification Service (SNS) using IAM authentication.

---

## Features

- Send email notifications via AWS SNS
- Support for both SNS Topics and direct email sending
- IAM-based authentication for secure access
- Multi-language support (English, Japanese, Chinese, Portuguese)

## Prerequisites

- AWS Account with SNS service enabled
- IAM user with appropriate SNS permissions
- AWS Access Key ID and Secret Access Key

## Required AWS IAM Permissions

The IAM user needs the following permissions:

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

## Installation

1. Install the plugin in your Dify instance
2. Configure the AWS credentials in the plugin settings:
   - AWS Access Key ID
   - AWS Secret Access Key
   - AWS Region (e.g., us-east-1, ap-northeast-1)

## Usage

### Sending Email via SNS Topic

If you have an existing SNS topic with email subscribers:

```
Tool: Send Email via SNS
Parameters:
- topic_arn: arn:aws:sns:region:account-id:topic-name
- subject: "Your Email Subject"
- message: "Your email message body"
```

### Sending Direct Email

To send email directly to a recipient:

```
Tool: Send Email via SNS
Parameters:
- email: recipient@example.com
- subject: "Your Email Subject"
- message: "Your email message body"
```

**Note:** When sending to a new email address, the recipient will first receive a confirmation email from AWS SNS. They must confirm the subscription before receiving notifications.

## Configuration

### Environment Variables (for development)

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then edit the `.env` file with your credentials.

### Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the plugin
python -m main
```

## Security Considerations

- Never commit AWS credentials to version control
- Use IAM roles with minimal required permissions
- Consider using AWS STS for temporary credentials in production
- Enable SNS encryption for sensitive data

## Troubleshooting

### Common Issues

1. **Invalid credentials error**
   - Verify your AWS Access Key ID and Secret Access Key
   - Check that the IAM user has the required permissions

2. **Topic not found error**
   - Ensure the topic ARN is correct
   - Verify the topic exists in the specified region

3. **Email not received**
   - Check if the recipient has confirmed the SNS subscription
   - Verify the email address is valid
   - Check spam/junk folders

## Support

For issues and questions, please visit: https://github.com/Beginnersguide138/dify-plugin-aws-sns/issues

## License

MIT License - see LICENSE file for details