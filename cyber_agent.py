import os
import random
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# TOOL 1: YOUR AI MALWARE SANDBOX SHELL
# ==========================================
@tool
def run_malware_sandbox_analysis(file_name: str) -> str:
    """Useful when a new or unknown file is uploaded. Parses binary structures using PEfile and ML."""
    verdicts = ["MALICIOUS_PAYLOAD", "SAFE_BENIGN_FILE"]
    result = random.choice(verdicts)
    print(f"\n🔬 [SANDBOX TRACE] Opening {file_name} -> Extracting section headers & computing entropy...")
    return f"Analysis complete for {file_name}. Machine Learning Classifier Verdict: {result}"

# ==========================================
# TOOL 2: YOUR AUTOMATED AI WEB FIREWALL SHELL
# ==========================================
@tool
def update_firewall_blocklist(ip_address: str) -> str:
    """Useful when an attack is verified. Updates network access tables to drop all incoming packets."""
    print(f"\n🛡️ [FIREWALL TRACE] Intercepting network layer -> IP {ip_address} has been permanently blocked.")
    return f"Gateway secured. Outbound rule applied: Drop all traffic from {ip_address}."

# ==========================================
# ORCHESTRATION: THE LANGCHAIN LOG ANALYZER BRAIN
# ==========================================
# 1. PASTE YOUR FREE GOOGLE GEMINI API KEY HERE
os.environ["GOOGLE_API_KEY"] = "AIzaSyCu4iLHU96i1oNBFPeVUooyosIxRb6LB7Y"

tools = [run_malware_sandbox_analysis, update_firewall_blocklist]
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an autonomous AI Incident Response Agent monitoring live server traffic logs. "
               "Step 1: Read the incoming log. If an executable file upload is detected, execute 'run_malware_sandbox_analysis'. "
               "Step 2: Review the sandbox output. If the result is 'MALICIOUS_PAYLOAD', immediately execute 'update_firewall_blocklist' using the log's IP. "
               "Step 3: Provide a concise final summary of your action to the console."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    # Simulated log stream event (The Log Analyzer component)
    simulated_log = "ALERT: Executable file upload 'payload_exploit.exe' received from network origin IP 197.221.3.4"
    
    print(f"📥 Streaming Live Log Input: '{simulated_log}'\n")
    print("🚀 Triggering Autonomous Agent Loop...")
    agent_executor.invoke({"input": simulated_log})