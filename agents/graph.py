from langgraph.graph import StateGraph
from agents.parser_agent import parser
from agents.categorizer_agent import categorizer
from agents.critic_agent import critic
from agents.memory_agent import memory

def build_graph():

    graph = StateGraph(dict)

    graph.add_node("parse", parser)
    graph.add_node("categorize", categorizer)
    graph.add_node("critic", critic)
    graph.add_node("memory", memory)

    graph.set_entry_point("parse")

    graph.add_edge("parse", "categorize")
    graph.add_edge("categorize", "critic")

    graph.add_conditional_edges(
        "critic",
        lambda state: "retry" if not state["valid"] else "memory",
        {
            "retry": "categorize",
            "memory": "memory"
        }
    )

    graph.set_finish_point("memory")

    return graph.compile()