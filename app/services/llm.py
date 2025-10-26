import os
from http import HTTPStatus
from dashscope import Generation


def llm_by_api(announcement_contents):
    # 若使用新加坡地域的模型，请释放下列注释
    # dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
    messages = [
        {"role": "system", "content": "你是一个金融领域的专家，善于总结个股公告内容。请你把公告内容总结成一句话，用词简明，适合非金融专业的读者理解，突出公告的核心信息和影响"},
        {"role": "user", "content": announcement_contents},
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]["message"]["content"]
