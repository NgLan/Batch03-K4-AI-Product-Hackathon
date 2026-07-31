# -*- coding: utf-8 -*-
"""Mô-đun quản lý kết nối và gửi yêu cầu tới Google GenAI API."""

import os
from google import genai
from google.genai import types

def get_genai_client() -> genai.Client:
    """Khởi tạo và cấu hình client Google GenAI.

    Returns:
        Đối tượng client GenAI.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
    return genai.Client(api_key=api_key)

def generate_text(prompt: str, system_instruction: str = "", model_name: str = "gemini-3.5-flash") -> str:
    """Gọi Gemini API bằng SDK google-genai để sinh văn bản dạng JSON.

    Args:
        prompt: Nội dung câu lệnh gửi tới model.
        system_instruction: Hướng dẫn hệ thống (System Prompt).
        model_name: Tên của model sử dụng.

    Returns:
        Văn bản kết quả dạng JSON từ Gemini.
    """
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
