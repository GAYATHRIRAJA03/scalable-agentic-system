from app.agent import Agent


agent = Agent()

queries = [
    "What is a dispute?",
    "What tools are available?",
    "Create an invoice for John for $50",
    "Send a payment of $100 to John",
    "Is there a dispute from user_123?",
    "What were my sales in August?",
]


for query in queries:
    print("=" * 60)
    print(f"Query: {query}")

    result = agent.run(query)

    print("Result:")
    print(result)