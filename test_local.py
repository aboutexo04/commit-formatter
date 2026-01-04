#!/usr/bin/env python3
"""
로컬 테스트용 스크립트
사용법: python test_local.py "your commit message here"
"""

import sys
import os

# formatter.py의 함수들 import
from formatter import format_with_ai, is_conventional_commit

def main():
    # OpenRouter API 키 확인
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY 환경변수를 설정해주세요:")
        print("   export OPENROUTER_API_KEY='your-api-key'")
        sys.exit(1)

    # 테스트할 메시지 받기
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = input("테스트할 커밋 메시지를 입력하세요: ")

    print(f"\n📝 원본 메시지: {message}")

    # 이미 conventional commit인지 확인
    if is_conventional_commit(message):
        print("✅ 이미 Conventional Commits 형식입니다!")
        return

    # AI로 변환
    print("\n🤖 AI로 변환 중...")
    try:
        model = os.environ.get('MODEL', 'meta-llama/llama-3-8b-instruct')
        language = os.environ.get('LANGUAGE', 'en')
        custom_prompt = os.environ.get('CUSTOM_PROMPT', '')

        formatted = format_with_ai(message, api_key, model, language, custom_prompt)
        print(f"✨ 변환 결과: {formatted}")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
