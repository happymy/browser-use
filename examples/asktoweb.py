from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
import typer
from rich.theme import Theme
from typing import Optional

# 加载环境变量
load_dotenv()

# 创建自定义主题
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "prompt": "bold cyan",
})

console = Console(theme=custom_theme)

def display_welcome():
    """显示欢迎信息"""
    console.print("\n[bold cyan]🤖 AI网页助手[/]", justify="center")
    console.print("[dim]让AI成为您的智能网页操作专家[/]\n", justify="center")

async def run_agent(task: str) -> Optional[str]:
    """运行AI代理"""
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("🤖 AI正在处理您的任务...", total=None)
        
        agent = Agent(
            task=task,
            llm=ChatOpenAI(
                model="gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
            ),
        )
        
        try:
            result = await agent.run()
            return str(result)
        except Exception as e:
            console.print(f"\n[error]错误: {str(e)}[/]")
            return None

def format_result(result: str) -> str:
    """格式化结果为Markdown格式"""
    # 确保结果是以代码块形式显示
    if not result.startswith("```") and not result.endswith("```"):
        result = f"```\n{result}\n```"
    return result

async def main():
    display_welcome()
    
    while True:
        # 获取用户输入
        task = Prompt.ask("\n[prompt]请描述您的任务[/]")
        
        if task.lower() == 'exit':
            console.print("\n[warning]正在退出程序...[/]")
            break
        
        console.print("\n[info]开始执行任务...[/]")
        
        # 执行任务
        result = await run_agent(task)
        
        if result:
            # 显示结果
            console.print("\n[success]✨ 任务完成！[/]")
            formatted_result = format_result(result)
            console.print(Markdown(formatted_result))
        else:
            console.print("\n[error]❌ 任务执行失败[/]")

def cli():
    """AI 网页助手 - 智能网页操作工具"""
    try:
        typer.run(asyncio.run(main()))
    except KeyboardInterrupt:
        console.print("\n[warning]程序已被用户终止[/]")
    except Exception as e:
        console.print(f"\n[error]程序发生错误: {str(e)}[/]")

if __name__ == "__main__":
    cli()