#!/usr/bin/env python3
"""
Commit Message Formatter - Automatically format commit messages to Conventional Commits
"""

import os
import re
import subprocess
import requests

SYSTEM_PROMPT = """You are a commit message formatter that converts informal commit messages into Conventional Commits format.

Conventional Commits format:
<type>(<optional scope>): <description>

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- build: Changes that affect the build system or external dependencies
- ci: Changes to CI configuration files and scripts
- chore: Other changes that don't modify src or test files
- revert: Reverts a previous commit

Rules:
1. Analyze the commit message and determine the most appropriate type
2. Keep the description concise (50 characters or less)
3. Use imperative mood (e.g., "add" not "added" or "adds")
4. Do not end the description with a period
5. If the commit message already follows conventional commits, return it as-is"""

LANGUAGES = {
    'en': 'English', 'ko': 'Korean', 'ja': 'Japanese', 'zh': 'Chinese',
    'es': 'Spanish', 'fr': 'French', 'de': 'German', 'pt': 'Portuguese',
    'ru': 'Russian', 'it': 'Italian'
}


def run_command(cmd: list[str]) -> str:
    """Run a shell command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def set_output(name: str, value: str):
    """Set GitHub Actions output."""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"{name}={value}\n")


def is_conventional_commit(message: str) -> bool:
    """Check if message already follows Conventional Commits."""
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?\!?:\s*.+'
    return bool(re.match(pattern, message.strip(), re.IGNORECASE))


def format_with_ai(message: str, api_key: str, model: str, language: str, custom_prompt: str) -> str:
    """Format commit message using OpenRouter API."""
    lang_instruction = ''
    if language != 'en':
        lang_name = LANGUAGES.get(language, language)
        lang_instruction = f"\n\nIMPORTANT: Write the commit message in {lang_name}. The type prefix (feat, fix, etc.) should remain in English, but the description should be in {lang_name}."

    custom_instruction = f"\n\nAdditional instructions: {custom_prompt}" if custom_prompt else ''

    user_prompt = f'''Convert the following commit message to Conventional Commits format:

"{message}"

Return ONLY the formatted commit message, nothing else.{lang_instruction}{custom_instruction}'''

    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/seoyeonmun/commit-formatter',
            'X-Title': 'Commit Message Formatter',
        },
        json={
            'model': model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt},
            ],
            'temperature': 0.3,
            'max_tokens': 500,
        },
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    content = data.get('choices', [{}])[0].get('message', {}).get('content', '')

    if not content:
        raise ValueError('No response from OpenRouter')

    return content.strip()


def main():
    # Get environment variables
    api_key = os.environ.get('OPENROUTER_API_KEY')
    model = os.environ.get('MODEL', 'meta-llama/llama-3-8b-instruct')
    github_token = os.environ.get('GITHUB_TOKEN')
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    language = os.environ.get('LANGUAGE', 'en')
    custom_prompt = os.environ.get('CUSTOM_PROMPT', '')

    if not api_key:
        raise ValueError('OPENROUTER_API_KEY is required')
    if not github_token:
        raise ValueError('GITHUB_TOKEN is required')

    # Get current commit info
    commit_sha = os.environ.get('GITHUB_SHA')
    original_message = run_command(['git', 'log', '-1', '--format=%B', commit_sha])

    print(f"Original commit message: {original_message}")
    set_output('original-message', original_message)

    # Check if already conventional
    if is_conventional_commit(original_message):
        print("Commit message already follows Conventional Commits. Skipping...")
        set_output('formatted-message', original_message)
        set_output('was-modified', 'false')
        return

    # Format with AI
    formatted_message = format_with_ai(original_message, api_key, model, language, custom_prompt)
    print(f"Formatted commit message: {formatted_message}")
    set_output('formatted-message', formatted_message)

    if original_message == formatted_message:
        print("No changes needed for the commit message.")
        set_output('was-modified', 'false')
        return

    if dry_run:
        print(f"[DRY RUN] Would amend commit with: {formatted_message}")
        set_output('was-modified', 'false')
        return

    # Amend commit
    run_command(['git', 'config', 'user.name', 'github-actions[bot]'])
    run_command(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
    run_command(['git', 'commit', '--amend', '-m', formatted_message])
    print("Commit amended successfully.")

    # Force push
    github_ref = os.environ.get('GITHUB_REF', '')
    branch = github_ref.replace('refs/heads/', '')
    repo = os.environ.get('GITHUB_REPOSITORY')

    remote_url = f"https://x-access-token:{github_token}@github.com/{repo}.git"
    run_command(['git', 'remote', 'set-url', 'origin', remote_url])
    run_command(['git', 'push', '--force', 'origin', f'HEAD:{branch}'])

    print(f"Force pushed to {branch}")
    set_output('was-modified', 'true')


if __name__ == '__main__':
    main()
