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

if __name__ == "__main__":
    llm_response = llm_by_api("""合肥城建发展股份有限公司（以下简称“公司”）于 2025 年 9 月 8 日召开的
    # # 第八届董事会第二十二次会议和第八届监事会第十八次会议审议通过了《关于全
    # # 资子公司对外投资的议案》，公司全资子公司安徽琥珀物业服务有限公司拟与合
    # # 肥市中房物业管理有限公司共同投资设立合肥慧城运营管理有限公司（暂定名，
    # # 以工商部门核准为准，以下简称“慧城管理”），具体内容详见公司 2025 年 9 月
    # # 9 日在巨潮资讯网披露的《关于全资子公司对外投资的公告》（公告编
    # # 号:2025073）""")
    print(llm_response)