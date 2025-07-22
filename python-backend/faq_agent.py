from agents import Agent, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from context import AvaloqAgentContext
from tools import avaloq_faq_lookup_tool
from guardrails import relevance_guardrail, jailbreak_guardrail

def avaloq_faq_instructions(run_context: RunContextWrapper[AvaloqAgentContext], agent: Agent[AvaloqAgentContext]) -> str:
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "你是 Avaloq FAQ 助手，专注于解答常见的 Avaloq 相关问题。"
        "请根据用户问题，使用 FAQ 工具查找答案并回复。"
    )

avaloq_faq_agent = Agent[AvaloqAgentContext](
    name="Avaloq FAQ Agent",
    model="gpt-4.1",
    handoff_description="FAQ助手，解答 Avaloq 常见问题。",
    instructions=avaloq_faq_instructions,
    tools=[avaloq_faq_lookup_tool],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
) 