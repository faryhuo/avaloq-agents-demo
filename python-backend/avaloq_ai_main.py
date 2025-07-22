
from triage_agent import avaloq_triage_agent

# 入口函数示例：返回主分流 agent

def get_main_agent():
    return avaloq_triage_agent

# 可选：如果需要直接运行或测试
if __name__ == "__main__":
    agent = get_main_agent()
    print(f"Main agent loaded: {agent.name}")
