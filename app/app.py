import chainlit as cl
import pandas as pd
import plotly.graph_objects as go
import time
from openai import AsyncOpenAI
import os

# Custom imports
from utils.utils import *
from utils.logging import *

from_env = FromEnv()

chat_api_config = from_env.get_chat_api()

client = AsyncOpenAI(
    api_key=chat_api_config.get("CHAT_API_KEY"),  # Consider storing this in a .env file
    base_url=chat_api_config.get("CHAT_API_URL"),
)


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/asset/light.png",
        ),
        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/asset/chart.png",
        ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/asset/code.png",
        ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/asset/cal.png",
        ),
    ]


@cl.set_chat_profiles
async def chat_profile():

    reasoning_models = from_env.get_models()
    chat_profile_list = []

    for ui_model_name, ollama_model_name in reasoning_models.items():
        chat_profile_list.append(
            cl.ChatProfile(
                name=ollama_model_name,
                markdown_description=f"How can i help you today?",
                # icon="https://picsum.photos/200",
            )
        )
    return chat_profile_list


@cl.on_message
async def main(message: cl.Message):
    elements = None

    if "test" in message.content:
        data = {
            "Name": [
                "Alice",
                "David",
                "Charlie",
                "Bob",
                "Eva",
                "Grace",
                "Hannah",
                "Jack",
                "Frank",
                "Kara",
                "Liam",
                "Ivy",
                "Mia",
                "Noah",
                "Olivia",
            ],
            "Age": [25, 40, 35, 30, 45, 55, 60, 70, 50, 75, 80, 65, 85, 90, 95],
            "City": [
                "New York",
                "Houston",
                "Chicago",
                "Los Angeles",
                "Phoenix",
                "San Antonio",
                "San Diego",
                "San Jose",
                "Philadelphia",
                "Austin",
                "Fort Worth",
                "Dallas",
                "Jacksonville",
                "Columbus",
                "Charlotte",
            ],
            "Salary": [
                70000,
                100000,
                90000,
                80000,
                110000,
                130000,
                140000,
                160000,
                120000,
                170000,
                180000,
                150000,
                190000,
                200000,
                210000,
            ],
        }
        df = pd.DataFrame(data)
        df_element = cl.Dataframe(data=df, display="inline", name="Dataframe")

        fig = go.Figure(
            data=[go.Bar(y=[2, 1, 3])],
            layout_title_text="An example figure",
        )

        chart_element = cl.Plotly(name="chart", figure=fig, display="inline")
        image_element = cl.Image(
            path="./public/asset/cat.jpg", name=message.content, display="side"
        )

        elements = [
            df_element,
            chart_element,
            image_element,
        ]
        await cl.Message(
            content=f"Received: {message.content}", elements=elements
        ).send()
    else:
        start_time = time.time()

        chat_model = cl.user_session.get("chat_profile")
        logger.info(f"Chat model: {chat_model}")

        stream = await client.chat.completions.create(
            model=chat_model,  # Or load from config
            messages=[
                # {"role": "system", "content": "You are a helpful assistant"},
                *cl.chat_context.to_openai(),
            ],
            stream=True,
        )

        thinking = False
        final_answer = cl.Message(content="")  # Initialize final_answer here

        async with cl.Step(name="Thinking") as thinking_step:
            async for chunk in stream:
                delta = chunk.choices[0].delta

                if delta.content == "<think>":
                    thinking = True
                    continue  # Skip to the next chunk

                if delta.content == "</think>":
                    thinking = False
                    thought_time = round(time.time() - start_time)  # More descriptive
                    thinking_step.name = f"Thought for {thought_time}s"
                    await thinking_step.update()
                    continue  # Skip to the next chunk

                if thinking:
                    await thinking_step.stream_token(delta.content)
                else:
                    await final_answer.stream_token(delta.content)

        await final_answer.send()
