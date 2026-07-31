# -*- coding: utf-8 -*-
"""Mô-đun quản lý kết nối và gửi yêu cầu tới các nhà cung cấp LLM (Gemini/Anthropic)."""

import os
from google import genai
from google.genai import types
import anthropic

def get_genai_client() -> genai.Client:
    """Khởi tạo và cấu hình client Google GenAI.

    Returns:
        Đối tượng client GenAI.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
    return genai.Client(api_key=api_key)

def get_anthropic_client() -> anthropic.Anthropic:
    """Khởi tạo và cấu hình client Anthropic.

    Returns:
        Đối tượng client Anthropic.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Không tìm thấy ANTHROPIC_API_KEY trong biến môi trường.")
    return anthropic.Anthropic(api_key=api_key)

def _generate_with_gemini(prompt: str, system_instruction: str, model_name: str) -> str:
    """Sinh văn bản qua Gemini API."""
    client = get_genai_client()
    config = types.GenerateContentConfig(
        system_instruction=system_instruction if system_instruction else None,
        response_mime_type="application/json"
    )
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )
    return response.text

def _generate_with_anthropic(prompt: str, system_instruction: str, model_name: str) -> str:
    """Sinh văn bản qua Anthropic API."""
    client = get_anthropic_client()
    response = client.messages.create(
        model=model_name,
        max_tokens=8192,
        system=system_instruction if system_instruction else None,
        messages=[{"role": "user", "content": prompt}]
    )
    return next(block.text for block in response.content if block.type == "text")

def generate_text(prompt: str, system_instruction: str = "", model_name: str = "") -> str:
    """Gọi LLM (Gemini hoặc Anthropic, chọn qua biến môi trường LLM_PROVIDER) để sinh văn bản dạng JSON.

    Args:
        prompt: Nội dung câu lệnh gửi tới model.
        system_instruction: Hướng dẫn hệ thống (System Prompt).
        model_name: Tên model cụ thể. Nếu bỏ trống sẽ dùng model mặc định của provider đang chọn.

    Returns:
        Văn bản kết quả dạng JSON từ LLM.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider == "anthropic":
        return _generate_with_anthropic(prompt, system_instruction, model_name or "claude-haiku-4-5")
    return _generate_with_gemini(prompt, system_instruction, model_name or "gemini-3.5-flash")
