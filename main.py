from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
# from pdf import canada_engine

load_dotenv()

population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

# test = population_df.loc[population_df['Country'] == 'Canada']['Population2023'].values[0]
# print(test)

# print(population_df.head())

population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})
# population_query_engine.query("What is the population of Canada?")

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="this gives information at the world population and demographics",
        ),
    )
    # QueryEngineTool(
    #     query_engine=canada_engine,
    #     metadata=ToolMetadata(
    #         name="canada_data",
    #         description="this gives detailed information about canada the country",
    #     ),
    # ),
]

llm = OpenAI(model="gpt-3.5-turbo-0125")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
