# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat"
)
'''
print(agent)
# <langgraph.graph.state.CompiledStateGraph object at 0x0000029F300D0E50>
# Graph:nodes--edges   点加线 网状结构
print(agent.nodes)
# {
# '__start__': <langgraph.pregel._read.PregelNode object at 0x0000015F2BDF6410>,
# 'model': <langgraph.pregel._read.PregelNode object at 0x0000015F2BDF6750>
# }
# pregel:google 2010 发布的技术
'''
# 消息（信息）列表 dict[str,list[dict[str,str]]]
results = agent.invoke({"messages": [{"role": "human", "content": "上海今天的的天气怎么样？"}]})
'''
print(results)
# {'messages': 
# [
# HumanMessage(content='上海今天的的天气怎么样？', additional_kwargs={}, response_metadata={}, id='761cf4bf-a3cd-4ac2-93a7-78ada704ed46'), 
# AIMessage(content='要查询上海今天的实时天气，建议您通过以下方式获取最准确的信息：\n\n1. **天气预报应用/网站**：如中国天气网、Weather.com、或手机自带天气应用（如苹果天气、谷歌天气等）。\n2. **搜索引擎**：在百度、谷歌等搜索“上海今日天气”。\n3. **语音助手**：询问手机上的Siri、小爱同学等。\n\n如果您需要出行建议，上海近期天气多变，夏季常有阵雨或高温，建议随身携带雨具并注意防暑。如需更具体的天气信息（如温度、湿度、空气质量等），请告诉我，我可以帮您查找最新数据！ 🌤️', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 137, 'prompt_tokens': 10, 'total_tokens': 147, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 10}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': 'bbacfe98-ba30-4d75-b8ec-3fc0482c9047', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019b7c2e-0a72-7ee0-925f-36fb9b66cec6-0', usage_metadata={'input_tokens': 10, 'output_tokens': 137, 'total_tokens': 147, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})
# ]
# }
'''
messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()  # 比直接print简单，输出更美观
