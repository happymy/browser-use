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
from pydantic import SecretStr

# Load env vars
load_dotenv()

# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "prompt": "bold cyan",
})

console = Console(theme=custom_theme)

def display_welcome():
    """Display welcome message"""
    console.print("\n[bold cyan]AI Web Assistant | 网页助手[/]", justify="center")
    console.print("[dim]Enter task description | 输入任务描述[/]\n", justify="center")

async def run_agent(task: str) -> Optional[str]:
    """Run AI agent"""
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("🤖 Processing... | 处理中...", total=None)
        
        agent = Agent(
            task=task,
            llm=ChatOpenAI(
                model="gpt-4o",
                api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
                base_url=os.getenv("OPENAI_BASE_URL"),
            ),
        )
        
        try:
            result = await agent.run()
            if isinstance(result, str) and "Result:" in result:
                return result.split("Result:", 1)[1].strip()
            return str(result)
        except Exception as e:
            if "Result:" in str(e):
                return str(e).split("Result:", 1)[1].strip()
            console.print(f"\n[error]Error | 错误: {str(e)}[/]")
            return None

def format_result(result: str) -> str:
    """Format result as Markdown"""
    if not result.startswith("```") and not result.endswith("```"):
        result = f"```\n{result}\n```"
    return result

async def main():
    display_welcome()
    
    while True:
        task = Prompt.ask("\n[prompt]Task | 任务[/]")
        
        if task.lower() == 'exit':
            console.print("\n[warning]Exiting... | 退出中...[/]")
            break
        
        console.print("\n[info]Starting... | 开始执行[/]")
        
        result = await run_agent(task)
        
        if result is not None:
            console.print("\n[success]✨ Done! | 完成！[/]")
            if result.strip():
                formatted_result = format_result(result)
                console.print(Markdown(formatted_result))
            else:
                console.print("[dim]No output required | 无需输出[/]")
        else:
            console.print("\n[error]❌ Failed | 失败[/]")

def cli():
    """AI Web Assistant - Smart web automation tool"""
    try:
        typer.run(asyncio.run(main()))
    except KeyboardInterrupt:
        console.print("\n[warning]Terminated | 已终止[/]")
    except Exception as e:
        console.print(f"\n[error]Error | 错误: {str(e)}[/]")

if __name__ == "__main__":
    cli()