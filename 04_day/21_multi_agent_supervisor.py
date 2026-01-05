# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import init_chat_model

from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

# 初始化模型
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
)

from langchain.tools import tool


# 创建子agent的工具
@tool
def create_calendar_event(
        title: str,
        start_time: str,
        end_time: str,
        attendees: list[str],
        location: str = ""
) -> str:
    """创建一个日历事件，需要确切的ISO时间格式"""
    return f"创建事件：参加人数{len(attendees)};日程是{title};地点：{location};开始：{start_time}--结束{end_time}。 "


@tool
def send_email(
        to: list[str],
        subject: str,
        content: str,
        cc: list[str] = []
) -> str:
    """通过电子邮件api发送邮件，需要正确的格式化地址"""
    return f"收件人：{','.join(to)}--主题：{subject}"


@tool
def get_available_time_slots(
        attendees: list[str],
        data: str,
        duration_minutes: int,
) -> list[str]:
    """查看参加会议人员的计划日期的空闲情况"""
    return ["09:00", "14:00", "16:00"]


# 构建 子agent
from langchain.agents import create_agent

calendar_agent_prompt = """
你是日程安排助理。
解析自然语言调度请求（例如，‘下周二下午2点’）
转换成合适的ISO日期时间格式。
在需要时使用get_available_time_slots来检查可用性。
使用create_calendar_event来安排事件。
一定要在最后的回复中确认你的计划。
"""

calendar_agent = create_agent(
    model=model,
    system_prompt=calendar_agent_prompt,
    tools=[create_calendar_event, get_available_time_slots],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"create_calendar_event": True},
            description_prefix="日历事件需要批准"
        )
    ],
)

email_prompt = """
你是电子邮件助理。
根据自然语言的要求撰写专业的电子邮件。
提取收件人的信息，制作合适的主题行和正文。
使用send_email发送消息。
在最后的回复中一定要确认发送的内容。
"""

email_agent = create_agent(
    model=model,
    system_prompt=email_prompt,
    tools=[send_email],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True},
            description_prefix="外发邮件等待审批"
        )
    ],
)


# 将 子agent 封装成工具
@tool
def schedule_event(request: str) -> str:
    """使用自然语言安排日历事件。
    当用户想要创建、修改或检查日历约会时，使用此选项。
    处理日期/时间解析、可用性检查和事件创建。
    输入：自然语言调度请求（例如，与设计团队开会）
    下星期二下午2时)
    """
    response = calendar_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return response["messages"][-1].text


@tool
def manage_email(request: str) -> str:
    """
    使用自然语言发送电子邮件。
    当用户想要发送通知、提醒或任何电子邮件时，使用此选项
    沟通。处理收件人提取、主题生成和电子邮件组成。
    输入：自然语言的电子邮件请求（例如，“向他们发送关于……的提醒会议”)
    """
    response = email_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return response["messages"][-1].text


# 构建主agent
supervisor_prompt = """
你是个有用的私人助理。
你可以安排日程活动和发送电子邮件。
将用户请求分解为适当的工具调用，并协调结果。
当一个请求涉及多个操作时，请按顺序使用多个工具。
"""

checkpointer = InMemorySaver()

supervisor_agent = create_agent(
    model=model,
    system_prompt=supervisor_prompt,
    tools=[schedule_event, manage_email],
    checkpointer=checkpointer,
)

user_request = """
下周二下午两点和设计团队在会议室开一个1小时的模型检查会议。
会议主题：AI应用模型检查。
内容概要：检查AI应用开发模型的类型、效果等等。
给他们发一封电子邮件，提醒他们检查新的模型。
成员邮箱如下：
alex.chen@sparkcreatives.com；
maya.rodriguez@sparkcreatives.com；
leo.wang@sparkcreatives.com；
jasmine.patel@sparkcreatives.com
"""
config = {"configurable": {"thread_id": "multi_agent"}}

for step in supervisor_agent.stream(
        {"messages": [{"role": "user", "content": user_request}]},
        stream_mode="values",
        config=config,
):
    step["messages"][-1].pretty_print()

    if "__interrupt__" in step:
        print("INTERRUPTED")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(request["description"])

    for step in supervisor_agent.stream(
            Command(resume={"decisions": [{"type": "approve"}]}),
            stream_mode="values",
            config=config,
    ):
        if "__interrupt__" in step:
            print("INTERRUPTION")
            interrupt = step["__interrupt__"][0]
            for request in interrupt.value["action_requests"]:
                print(request["description"])
"""
if "__interrupt__" in step:
    print("INTERRUPTED")
    interrupt = step["__interrupt__"][0]
    ''' print(interrupt)
    Interrupt(value={'action_requests': [{'name': 'create_calendar_event',
                                          'args': {'title': 'AI应用模型检查会议', 'start_time': '2024-12-17T14:00:00',
                                                   'end_time': '2024-12-17T15:00:00', 'attendees': ['设计团队'],
                                                   'location': '会议室'},
                                          'description': "日历事件需要批准\n\nTool: create_calendar_event\nArgs: {'title': 'AI应用模型检查会议', 'start_time': '2024-12-17T14:00:00', 'end_time': '2024-12-17T15:00:00', 'attendees': ['设计团队'], 'location': '会议室'}"}],
                     'review_configs': [
                         {'action_name': 'create_calendar_event', 'allowed_decisions': ['approve', 'edit', 'reject']}]},
              id='680c7dbb2feeb83cc8b9b750fb85d4e5')'''
    for request in interrupt.value["action_requests"]:
        print(request["description"])
elif "messages" in step:
    step["messages"][-1].pretty_print()
else:
    pass

for step in supervisor_agent.stream(
        Command(resume={"decisions": [{"type": "approve"}]}),
        stream_mode="values",
        config=config,
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    if "__interrupt__" in step:
        print("INTERRUPTION")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(request["description"])
    else:
        pass
"""
