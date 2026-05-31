from agent.graph import graph

result = graph.invoke(
    {
        "task": "Create a FastAPI Todo API",
    }
)

print(result['generated_files'])