from agents import Agent, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from context import AvaloqAgentContext
from guardrails import relevance_guardrail, jailbreak_guardrail
from ba_agent import ba_agent
from dev_agent import dev_agent
from upgrade_agent import upgrade_agent
from faq_agent import avaloq_faq_agent


def triage_instructions(run_context: RunContextWrapper[AvaloqAgentContext], agent: Agent[AvaloqAgentContext]) -> str:
    return f"""
    {RECOMMENDED_PROMPT_PREFIX} 
    你是 Avaloq 智能分流助手，根据用户问题内容，将其分配给最合适的子助手（BA、Dev、Upgrade、FAQ）
    """

avaloq_triage_agent = Agent[AvaloqAgentContext](
    name="Avaloq Triage Agent",
    model="gpt-4.1",
    handoff_description="""
    分流助手，根据用户问题分配到 BA、Dev、Upgrade 或 FAQ agent。
    有关 Avaloq version 版本问题，请分配给 Upgrade agent。
    有关 Avaloq 开发问题，请分配给 Dev agent。
    有关 Avaloq 业务分析问题，请分配给 BA agent。
    有关 Avaloq 常见问题，请分配给 FAQ agent。
    """,
    instructions=triage_instructions,
    handoffs=[
        ba_agent,
        dev_agent,
        upgrade_agent,
        avaloq_faq_agent,
    ],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 设置 handoff 关系，便于子 agent 返回主 agent
ba_agent.handoffs.append(avaloq_triage_agent)
dev_agent.handoffs.append(avaloq_triage_agent)
upgrade_agent.handoffs.append(avaloq_triage_agent)
avaloq_faq_agent.handoffs.append(avaloq_triage_agent) 