import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    user_input: str
    prompt_template: str
    final_prompt: str
    llm_response: str


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "support_agent_prompt_v1.md"


def load_prompt(state: AgentState) -> AgentState:
    """
    Equivalent du nœud Prompt Template.
    Cette fonction charge le prompt versionné depuis le dossier prompts/.
    """
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    final_prompt = prompt_template.replace("{input}", state["user_input"])

    return {
        **state,
        "prompt_template": prompt_template,
        "final_prompt": final_prompt,
    }


def call_groq_llm(state: AgentState) -> AgentState:
    """
    Equivalent du nœud GroqModel / LLM.
    Cette fonction appelle l'API Groq avec le prompt final.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY est absente. "
            "Ajoutez-la dans le fichier .env ou comme variable d'environnement."
        )

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Tu es un agent d'assistance support fiable, prudent et structuré.",
            },
            {
                "role": "user",
                "content": state["final_prompt"],
            },
        ],
        temperature=0.3,
        max_tokens=800,
    )

    llm_response = completion.choices[0].message.content

    return {
        **state,
        "llm_response": llm_response,
    }


def format_response(state: AgentState) -> AgentState:
    """
    Equivalent du nœud Chat Output.
    Pour cette version, on retourne directement la réponse LLM.
    """
    return state


def build_graph():
    """
    Construction du workflow LangGraph.
    """
    graph = StateGraph(AgentState)

    graph.add_node("load_prompt", load_prompt)
    graph.add_node("call_groq_llm", call_groq_llm)
    graph.add_node("format_response", format_response)

    graph.set_entry_point("load_prompt")
    graph.add_edge("load_prompt", "call_groq_llm")
    graph.add_edge("call_groq_llm", "format_response")
    graph.add_edge("format_response", END)

    return graph.compile()


def run_agent(user_input: str) -> str:
    """
    Lance l'agent avec une entrée utilisateur.
    """
    app = build_graph()

    initial_state: AgentState = {
        "user_input": user_input,
        "prompt_template": "",
        "final_prompt": "",
        "llm_response": "",
    }

    result = app.invoke(initial_state)
    return result["llm_response"]

if __name__ == "__main__":
    load_dotenv()

    print("Agent Assistant Support v1.1.0")
    print("--------------------------------")

    user_input = os.getenv("USER_INPUT")

    if user_input:
        print(f"Message reçu depuis USER_INPUT : {user_input}")
    else:
        try:
            user_input = input("Décrivez votre problème : ")
        except EOFError:
            user_input = "J’ai un problème de wifi, la connexion coupe souvent."
            print("Aucune saisie interactive détectée.")
            print(f"Message de test utilisé par défaut : {user_input}")

    response = run_agent(user_input)

    print("\nRéponse de l'agent :")
    print("--------------------")
    print(response)