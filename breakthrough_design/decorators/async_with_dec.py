import asyncio
import functools
import re

from ollama import AsyncClient


# 定义一个带有参数的异步装饰器
def async_decorator(system, model, user):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"[INFO] 埋点调用: {func.__name__}")

            # 构造消息
            messages = [
                append_prompt(system, "system"),
                append_prompt(user, "user"),
            ]

            content = ""
            async for part in await AsyncClient().chat(
                model=model,
                messages=messages,
                stream=True,
            ):
                content += part.message.content
                print(part["message"]["content"], end="", flush=True)

            print(f"\nRunning {func.__name__} with args: {args} and kwargs: {kwargs}")

            result = await func(content, *args, **kwargs)

            print(f"[INFO] 埋点调用: {func.__name__}")
            return result

        return wrapper

    return decorator


def append_prompt(msg, role="user"):
    return {"role": role, "content": msg}


def extract_code_blocks(markdown_text):
    code_block_pattern = r"```([^\s]+)\n([\s\S]*?)\n```"
    code_blocks = []
    for match in re.finditer(code_block_pattern, markdown_text, re.DOTALL):
        language = match.group(1)
        content = match.group(2).strip()
        code_blocks.append((language, content))
    return code_blocks


def save_code_blocks_to_markdown(markdown_text, code_blocks, output_file):
    lines = markdown_text.split("\n")
    in_code_block = False
    new_lines = []
    for i, line in enumerate(lines):
        if "```" in line:
            in_code_block = not in_code_block
        if in_code_block:
            if line.strip():
                new_lines.append(line)
        else:
            for language, content in code_blocks:
                if re.search(rf"^{language}\s*$", line):
                    new_lines.extend(content.split("\n"))
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(new_lines))


# 使用装饰器装饰异步函数，并传入参数
@async_decorator(
    system="你是一位专业的Python工程师，只会编写代码并且只会给出用户需要的各种python代码，会采用设计模式来优化整个代码，你只会输出核心代码，没有其他回复内容。",
    model="qwen2.5-coder:1.5b",
    user="""采用python编写一段订阅发布者模式,希望实现一个类似于宗门任务发布之后,任务会被视作主题,并且其他宗门子弟会接收到消息,可以选择去做与否,一旦某个任务被接收就会暂时将整个状态通知下去,并且更新其他的剩余的任务.""",
)
async def async_function(markdown_text, x, *args, **kwargs):
    # print(markdown_text, x)
    # 提取代码块
    code_blocks = extract_code_blocks(markdown_text)

    # 保存到新的Markdown文件中
    save_code_blocks_to_markdown(markdown_text, code_blocks, "output.md")
    return x * 2


# 测试异步函数
async def main():
    import time

    start = time.time()
    result = await async_function(5, (1,), {"x": "x"})
    end = time.time()
    print(f"\nResult: {result}, Time taken: {end - start:.2f} seconds")


asyncio.run(main())
