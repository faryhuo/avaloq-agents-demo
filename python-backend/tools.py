from agents import function_tool

@function_tool(
    name_override="avaloq_faq_lookup_tool", description_override="Lookup Avaloq frequently asked questions."
)
async def avaloq_faq_lookup_tool(question: str) -> str:
    q = question.lower()
    if "core" in q:
        return "Avaloq Core Platform 是 Avaloq 的核心银行系统，支持多币种、多语言和跨国业务。"
    elif "api" in q:
        return "Avaloq 提供丰富的 API 支持，包括 RESTful API、SOAP 等，便于集成第三方系统。"
    elif "upgrade" in q:
        return "升级 Avaloq 需遵循官方文档流程，建议先在测试环境验证所有自定义开发。"
    return "很抱歉，暂时没有该问题的答案。"

@function_tool(
    name_override="ba_helper_tool",
    description_override="帮助业务分析师（BA）解答 Avaloq 相关业务需求、流程、最佳实践等问题。"
)
async def ba_helper_tool(query: str) -> str:
    return "BA助手：请详细描述您的业务需求或流程问题，我会为您提供 Avaloq 相关建议。"

@function_tool(
    name_override="dev_helper_tool",
    description_override="帮助开发人员解答 Avaloq 开发、定制、API、脚本等相关问题。"
)
async def dev_helper_tool(query: str) -> str:
    return "开发助手：请说明您的开发问题（如 API、脚本、定制等），我会为您提供 Avaloq 技术支持。"

@function_tool(
    name_override="upgrade_helper_tool",
    description_override="帮助用户解答 Avaloq 升级相关问题，包括流程、注意事项、兼容性等。"
)
async def upgrade_helper_tool(query: str) -> str:
    return "升级助手：请描述您的升级场景或遇到的问题，我会为您提供 Avaloq 升级建议。" 