"""
Simple try of the agent.

@dev You need to add GOOGLE_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from langchain_google import ChatGoogleGenerativeAI

from browser_use import Agent

# 使用 Gemini API
llm = ChatGoogleGenerativeAI(
	model="gemini-pro",
	google_api_key="AIzaSyAD2Ow4E1umuX0oYaCkK61Nd9Eg56cnnak",
	temperature=0.7
)

agent = Agent(
	task='前往 amazon.com，搜索笔记本电脑，按最佳评分排序，并返回第一个结果的价格',
	llm=llm,
)

async def main():
	# 运行代理并获取结果
	result = await agent.run(max_steps=3)
	# 打印结果
	print("搜索结果：", result)

if __name__ == "__main__":
	asyncio.run(main())
