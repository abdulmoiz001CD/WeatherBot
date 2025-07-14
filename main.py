import chainlit as cl
from chatbot import run_agent  

@cl.on_chat_start
async def on_chat():
    await cl.Message(
        content="Hello! I am a Weather Agent. How can I help you?"
    ).send()

@cl.on_message
async def message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    async for token in run_agent(message.content):
        await msg.stream_token(token)

    await msg.update()