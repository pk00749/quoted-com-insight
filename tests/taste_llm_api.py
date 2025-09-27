import os
from dashscope import Generation

def taste_qwen_plus():
    """试用Qwen-Plus大模型"""
    # 若使用新加坡地域的模型，请释放下列注释
    # dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
    messages = [
        {"role": "system", "content": "你是说中文的AI助手"},
        {"role": "user", "content": "你是谁？"},
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )

    if response.status_code == 200:
        print(response.output.choices[0]["message"]["content"])
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


def taste_qwen_doc_turbo():
    """试用Qwen-Doc-Turbo大模型"""
    response = Generation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
        model='qwen-doc-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "你是一个金融领域的专家，善于总结个股公告内容。请你把公告内容总结成一句话，用词简明，适合非金融专业的读者理解，突出公告的核心信息和影响"
                    },
                    {
                        "type": "doc_url",
                        "doc_url": [
                            "https://pdf.dfcfw.com/pdf/H2_AN202509221748475241_1.pdf"
                        ],
                        "file_parsing_strategy": "auto"
                    }
                ]
            }]
    )
    try:
        if response.status_code == 200:
            print(response.output.choices[0].message.content)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误代码: {response.code}")
            print(f"错误信息: {response.message}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
    except Exception as e:
        print(f"发生错误: {e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


if __name__ == "__main__":
    taste_qwen_doc_turbo()