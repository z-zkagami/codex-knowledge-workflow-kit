#!/usr/bin/env python3
"""Extract X/Twitter post content through the official X API."""

import json
import os
import re
import sys

import requests

API_BASE_URL = "https://api.twitter.com/2"


def get_tweet_by_url(url, api_key):
    """Extract a tweet ID from a URL and fetch its content."""
    match = re.search(r"/status/(\d+)", url)
    if not match:
        raise ValueError(f"Could not extract tweet ID from URL: {url}")
    return get_tweet_by_id(match.group(1), api_key)


def get_tweet_by_id(tweet_id, api_key):
    """Fetch tweet details with API v2."""
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "tweet.fields": "created_at,author_id,conversation_id,text,public_metrics,referenced_tweets",
        "expansions": "author_id,referenced_tweets.id",
        "user.fields": "name,username,verified",
    }
    url = f"{API_BASE_URL}/tweets/{tweet_id}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code
        if status == 401:
            raise Exception("API key is invalid or expired") from exc
        if status == 403:
            raise Exception("No access to this post; it may be private or deleted") from exc
        if status == 429:
            raise Exception("API rate limit reached; retry later") from exc
        raise Exception(f"API request failed: {exc}") from exc


def format_tweet_data(data):
    """Format tweet API data for the Markdown saver."""
    tweet = data.get("data", {})
    includes = data.get("includes", {})
    author = includes.get("users", [{}])[0] if includes.get("users") else None

    text = tweet.get("text", "")
    created_at = tweet.get("created_at", "")
    username = author.get("username", "unknown") if author else "unknown"
    metadata = {
        "title": text[:50] + ("..." if len(text) > 50 else ""),
        "author": f"{author.get('name', '')} (@{username})" if author else "",
        "url": f"https://x.com/{username}/status/{tweet.get('id', '')}",
        "date": created_at,
        "type": "tweet",
    }

    referenced_tweets = tweet.get("referenced_tweets", [])
    if any(ref.get("type") == "replied_to" for ref in referenced_tweets):
        metadata["type"] = "thread"

    content = text
    metrics = tweet.get("public_metrics", {})
    if metrics:
        content += "\n\n---\n\n**Stats**:\n"
        content += f"- Retweets: {metrics.get('retweet_count', 0)}\n"
        content += f"- Likes: {metrics.get('like_count', 0)}\n"
        content += f"- Replies: {metrics.get('reply_count', 0)}\n"

    return content, metadata


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_with_api.py <tweet_url> [api_key]")
        print("Or set X_API_KEY in the environment")
        sys.exit(1)

    tweet_url = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else os.getenv("X_API_KEY")

    if not api_key:
        print("Error: no API key provided", file=sys.stderr)
        print("Pass it as an argument or set X_API_KEY", file=sys.stderr)
        sys.exit(1)

    try:
        print("Fetching post content...")
        data = get_tweet_by_url(tweet_url, api_key)
        content, metadata = format_tweet_data(data)
        result = {"content": content, "metadata": metadata}
        print("RESULT_JSON_START")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("RESULT_JSON_END")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
