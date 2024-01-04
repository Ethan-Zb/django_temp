# coding=utf8
"""
open AI
"""
import openai

OPEN_AI_KEY = ''


def openai_completion(prompt):
    """
    open ai分析
    @param prompt:
    @return:
    """
    openai.api_key = OPEN_AI_KEY
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.0
    )
