from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. Define the graph state
# ============================================================

class State(TypedDict):
    name: str
    account_type: str
    message: str


# ============================================================
# 2. Define nodes
# ============================================================

def greet(state: State) -> State:
    state["message"] = f"Hello {state['name']}!"
    return state


def set_account_type(state: State) -> State:
    state["account_type"] = "savings"
    return state


def compose(state: State) -> State:
    state["message"] = (
        f"{state['message']} "
        f"Your account type is {state['account_type']}."
    )
    return state


# ============================================================
# 3. Build the graph
# ============================================================

builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("set_account_type", set_account_type)
builder.add_node("compose", compose)


# ============================================================
# 4. Connect the nodes
# ============================================================

builder.add_edge(START, "greet")
builder.add_edge("greet", "set_account_type")
builder.add_edge("set_account_type", "compose")
builder.add_edge("compose", END)


# ============================================================
# 5. Compile the graph
# ============================================================

app = builder.compile()


# ============================================================
# 6. Invoke the graph
# ============================================================

result = app.invoke(
    {
        "name": "Asha",
        "account_type": "",
        "message": "",
    }
)


# ============================================================
# 7. Print final state
# ============================================================

print("Final state:")
print(result)
