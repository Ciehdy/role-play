import asyncio

from domain.chat.session import ChatSession
from domain.role.models import Role


async def main():
    from dotenv import load_dotenv

    load_dotenv()

    print("Hello from role-play!")

    role = Role(
        name="萧炎",
        description="",
        tts_voice_type="qiniu_zh_female_tmjxxy",
        tts_speed_ratio=1.0,
    )
    session = ChatSession(role=role)

    print("输入消息并回车发送，输入 'exit' 退出。")

    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "> ")
        if user_input.strip().lower() == "exit":
            print("退出对话。")
            break
        await session.send_message(user_input)


if __name__ == "__main__":
    asyncio.run(main())
