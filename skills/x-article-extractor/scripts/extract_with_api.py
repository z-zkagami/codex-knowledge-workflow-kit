#!/usr/bin/env python3
"""
使用官方 X API 提取推文内容
需要设置环境变量 X_API_KEY 或通过命令行参数传入
"""

import os
import sys
import json
import requests
from datetime import datetime

# API 配置
API_BASE_URL = "https://api.twitter.com/2"

def get_tweet_by_url(url, api_key):
    """从 URL 提取推文 ID 并获取内容"""
    # 提取推文 ID
    import re
    match = re.search(r'/status/(\d+)', url)
    if not match:
        raise ValueError(f"无法从 URL 中提取推文 ID: {url}")

    tweet_id = match.group(1)
    return get_tweet_by_id(tweet_id, api_key)

def get_tweet_by_id(tweet_id, api_key):
    """使用 API v2 获取推文详细信息"""
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # 请求参数 - 获取完整信息
    params = {
        "tweet.fields": "created_at,author_id,conversation_id,text,public_metrics,referenced_tweets",
        "expansions": "author_id,referenced_tweets.id",
        "user.fields": "name,username,verified"
    }

    url = f"{API_BASE_URL}/tweets/{tweet_id}"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("API Key 无效或已过期，请检查你的 API Key")
        elif e.response.status_code == 403:
            raise Exception("无权访问此推文（可能是私密推文或已删除）")
        elif e.response.status_code == 429:
            raise Exception("API 请求次数已达上限，请稍后再试")
        else:
            raise Exception(f"API 请求失败: {e}")

def format_tweet_data(data):
    """格式化推文数据为 Markdown"""
    tweet = data.get('data', {})
    includes = data.get('includes', {})

    # 获取作者信息
    author = None
    if 'users' in includes and includes['users']:
        author = includes['users'][0]

    # 提取基本信息
    text = tweet.get('text', '')
    created_at = tweet.get('created_at', '')

    # 构建元数据
    metadata = {
        'title': text[:50] + ('...' if len(text) > 50 else ''),
        'author': f"{author.get('name', '')} (@{author.get('username', '')})" if author else '',
        'url': f"https://x.com/{author.get('username', 'unknown')}/status/{tweet.get('id', '')}" if author else '',
        'date': created_at,
        'type': 'tweet'
    }

    # 检查是否是推文串
    referenced_tweets = tweet.get('referenced_tweets', [])
    is_thread = any(ref.get('type') == 'replied_to' for ref in referenced_tweets)

    if is_thread:
        metadata['type'] = 'thread'

    # 格式化内容
    content = text

    # 添加统计信息（如果有）
    metrics = tweet.get('public_metrics', {})
    if metrics:
        stats = f"\n\n---\n\n**统计数据**：\n"
        stats += f"- 转发: {metrics.get('retweet_count', 0)}\n"
        stats += f"- 点赞: {metrics.get('like_count', 0)}\n"
        stats += f"- 回复: {metrics.get('reply_count', 0)}\n"
        content += stats

    return content, metadata

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 extract_with_api.py <tweet_url> [api_key]")
        print("或设置环境变量: X_API_KEY=你的密钥")
        sys.exit(1)

    tweet_url = sys.argv[1]

    # 获取 API Key（优先使用命令行参数）
    api_key = sys.argv[2] if len(sys.argv) > 2 else os.getenv('X_API_KEY')

    if not api_key:
        print("错误: 未提供 API Key")
        print("请通过命令行参数传入或设置环境变量 X_API_KEY")
        sys.exit(1)

    try:
        print(f"🔍 正在获取推文内容...")
        data = get_tweet_by_url(tweet_url, api_key)

        print(f"✅ 成功获取推文数据")

        # 格式化数据
        content, metadata = format_tweet_data(data)

        # 输出 JSON 格式（供脚本调用）
        result = {
            'content': content,
            'metadata': metadata
        }

        print("\n" + "="*50)
        print("RESULT_JSON_START")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("RESULT_JSON_END")
        print("="*50)

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
