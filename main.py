import chainlit as cl
from chatbot import run_agent  

@cl.on_chat_start
async def on_chat():
    await cl.Message(
        content="Hello! I am a Weather Agent. How can I help you?"
    ).send()

@cl.on_message
async def message(message: cl.Message):
    if message:
        result_chain = run_agent(message.content)
        await cl.Message(content=result_chain).send()
