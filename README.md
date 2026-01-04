# Commit Message Formatter Action

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Commit%20Message%20Formatter-blue?logo=github)](https://github.com/marketplace/actions/commit-message-formatter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automatically format your commit messages to follow [Conventional Commits](https://www.conventionalcommits.org/) specification using AI via [OpenRouter](https://openrouter.ai/).

## Features

- 🤖 **AI-Powered**: Uses OpenRouter to access GPT, Claude, Llama, and many other models
- 📝 **Conventional Commits**: Automatically converts informal messages to proper format
- 🌍 **Multi-language Support**: Generate commit messages in various languages
- 🔒 **Smart Detection**: Skips commits that already follow the convention
- 🧪 **Dry Run Mode**: Preview changes without modifying commits

## Quick Start

```yaml
name: Format Commit Messages

on:
  push:
    branches:
      - main
      - 'feature/**'

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: seoyeonmun/commit-formatter@v1
        with:
          openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Examples

| Before | After |
|--------|-------|
| `fixed the login bug` | `fix: resolve login authentication issue` |
| `added new feature for users` | `feat: add user dashboard feature` |
| `updated readme` | `docs: update README with usage examples` |
| `버그 수정함` | `fix: 로그인 버그 수정` |

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `openrouter-api-key` | OpenRouter API key | Yes | - |
| `model` | Model to use via OpenRouter | No | `openai/gpt-4o-mini` |
| `github-token` | GitHub token for pushing | Yes | - |
| `dry-run` | Preview without modifying | No | `false` |
| `language` | Output language code | No | `en` |
| `custom-prompt` | Additional AI instructions | No | - |

## Outputs

| Output | Description |
|--------|-------------|
| `original-message` | The original commit message |
| `formatted-message` | The formatted commit message |
| `was-modified` | Whether the message was changed |

## Configuration Examples

### Using Claude

```yaml
- uses: seoyeonmun/commit-formatter@v1
  with:
    openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
    model: anthropic/claude-3-haiku
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Using Llama

```yaml
- uses: seoyeonmun/commit-formatter@v1
  with:
    openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
    model: meta-llama/llama-3-8b-instruct
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Korean commit messages

```yaml
- uses: seoyeonmun/commit-formatter@v1
  with:
    openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    language: ko
```

### Custom instructions

```yaml
- uses: seoyeonmun/commit-formatter@v1
  with:
    openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    custom-prompt: "Always include the ticket number if mentioned. Use past tense."
```

### Dry run for testing

```yaml
- uses: seoyeonmun/commit-formatter@v1
  with:
    openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    dry-run: 'true'
```

## Available Models (via OpenRouter)

| Model | ID |
|-------|-----|
| GPT-4o Mini | `openai/gpt-4o-mini` (default) |
| GPT-4o | `openai/gpt-4o` |
| Claude 3 Haiku | `anthropic/claude-3-haiku` |
| Claude 3.5 Sonnet | `anthropic/claude-3.5-sonnet` |
| Llama 3 8B | `meta-llama/llama-3-8b-instruct` |
| Mistral 7B | `mistralai/mistral-7b-instruct` |

See [OpenRouter Models](https://openrouter.ai/models) for the full list.

## Supported Languages

| Code | Language |
|------|----------|
| `en` | English (default) |
| `ko` | Korean |
| `ja` | Japanese |
| `zh` | Chinese |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `ru` | Russian |
| `it` | Italian |

## Conventional Commits Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, etc.) |
| `refactor` | Code refactoring |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `build` | Build system changes |
| `ci` | CI configuration changes |
| `chore` | Other changes |
| `revert` | Reverting a previous commit |

## Important Notes

⚠️ **Force Push Warning**: This action uses `git push --force` to update the commit. Use with caution on shared branches.

**Recommended setup**:
- Use on feature branches only
- Avoid using on `main`/`master` if multiple people are pushing
- Consider using `dry-run: true` first to preview changes

## Permissions

The action requires the following permissions:

```yaml
permissions:
  contents: write
```

## Getting an OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Add it to your repository secrets as `OPENROUTER_API_KEY`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.
