import os
import json
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# --- Import BOTH of your tools ---
from tools import scrape_uk_financial_data, search_tool

# --- SET YOUR GOOGLE API KEY ---
os.environ["GOOGLE_API_KEY"] = "Paste your google API key here"

# 1. Initialize the Brain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# 2. Assemble the Agent with BOTH tools
tools = [scrape_uk_financial_data, search_tool]
agent_executor = create_react_agent(llm, tools)

if __name__ == "__main__":
    print("\n[SYSTEM] Waking up the Autonomous Corporate Risk Radar...")
    
    # --- 1. THE UPDATED CLIENT DATABASE ---
    # --- 1. THE INSTITUTIONAL MACRO DATABASE ---
    client_database = [
        # --- THE REGULATORS & GOVERNMENT ---
        {
            "client_id": "GOV-BOE",
            "company_name": "Bank of England",
            "sector": "Central Bank",
            "focus": "Base Rate & Macroeconomic Outlook"
        },
        {
            "client_id": "GOV-ONS",
            "company_name": "Office for National Statistics (ONS) UK",
            "sector": "Government Statistics",
            "focus": "Latest CPI Inflation & GDP Growth"
        },
        # --- THE BIG FOUR UK RETAIL/COMMERCIAL BANKS ---
        {
            "client_id": "BNK-HSBC",
            "company_name": "HSBC Holdings plc",
            "sector": "Tier-1 Global Bank",
            "focus": "Net Interest Income & Global Credit Impairments"
        },
        {
            "client_id": "BNK-BARC",
            "company_name": "Barclays PLC",
            "sector": "Tier-1 Investment/Commercial Bank",
            "focus": "Net Interest Income & Investment Banking Risk"
        },
        {
            "client_id": "BNK-LLOY",
            "company_name": "Lloyds Banking Group",
            "sector": "Tier-1 UK Retail Bank",
            "focus": "Mortgage Defaults & Net Interest Margin"
        },
        {
            "client_id": "BNK-NWG",
            "company_name": "NatWest Group",
            "sector": "Tier-1 UK Commercial Bank",
            "focus": "Corporate Loan Defaults & Deposit Flight"
        },
        # --- SPECIALIZED UK LENDERS ---
        {
            "client_id": "BNK-STAN",
            "company_name": "Standard Chartered PLC",
            "sector": "Tier-1 International Bank",
            "focus": "Emerging Market Exposure & Impairments"
        },
        {
            "client_id": "BNK-SANT",
            "company_name": "Santander UK",
            "sector": "Major Retail Bank",
            "focus": "UK Consumer Credit Health"
        },
        {
            "client_id": "BNK-NBS",
            "company_name": "Nationwide Building Society",
            "sector": "Mortgage Lender",
            "focus": "House Price Index & Mortgage Arrears"
        },
        # --- SYSTEMIC RISK MONITOR ---
        {
            "client_id": "REG-FCA",
            "company_name": "Financial Conduct Authority (FCA)",
            "sector": "Financial Regulator",
            "focus": "Recent warnings on systemic risk or consumer duty"
        }
    ]

    # --- 2. THE BATCH PROCESSOR LOOP ---
    for client in client_database:
        
        print(f"\n========================================================")
        print(f"[SYSTEM] Agent is researching: {client['company_name']}")
        print(f"========================================================")
        
        # --- THE FIX: The Graceful Fallback ---
        # If the client has an 'our_exposure' key, it uses it. 
        # If they don't (like the Bank of England), it defaults to "Systemic Macro".
        exposure = client.get('our_exposure', 'Systemic Macro (Indirect Exposure)')
        
        # --- 3. THE STRATEGIC RISK & IMPACT PROMPT ---
        query = f"""
        You are an elite Senior Risk Auditor and Strategic Consultant reporting to the Chief Risk Officer.
        You are investigating {client['company_name']} in the {client['sector']} sector.
        Our bank has an exposure of {exposure} to this entity.
        Your primary focus for this entity is: {client['focus']}.
        
        STEP 1: DATA GATHERING
        Use your search tool to find their official Q1 2026 reports, press releases, or official data releases.
        Use your web scraping tool to read the official source material.
        
        CRITICAL ZERO-HALLUCINATION GUARDRAILS FOR DATA:
        - Extract the raw numbers strictly from the text. If a metric is missing, state "DATA NOT DISCLOSED".
        - Do NOT use data from 2025. Verify the date is Q1 2026.
        - Cite the exact URL used.
        
        STEP 2: THE DIAGNOSTIC ANALYSIS (The "What" and "Why")
        Based ONLY on the verified data you extracted, provide a deep diagnostic breakdown:
        - The Core Problem: What is the primary risk or negative trend identified?
        - Root Cause & Factors: What macroeconomic or operational factors are causing this problem? Why is it occurring now?
        - Ripple Effects: What secondary issues come with this problem?
        - Criticality Score: Rate the severity of this problem from 1-10 and justify why.
        
        STEP 3: THE IMPACT & PRESCRIPTIVE ANALYSIS (The "So What" and "Now What")
        Put on your strategic consultant hat to advise our Chief Risk Officer regarding our {exposure} exposure:
        - Firm Impact: Exactly how will this entity's problem affect our business?
        - Solution Paths: What are 2-3 strategic options our bank can take to hedge against this specific risk?
        - Action Plan: What are the immediate next steps our risk team must take today?
        - Preventative Modeling: What specific statistical models (e.g., Value at Risk, Stress Testing scenarios, Credit Transition Matrices) or key statistical indicators should we deploy to monitor this risk going forward?
        - Reliability & Confidence: Assess the reliability of your proposed solutions based on the quality of the data extracted.
        
        Format your response as a highly professional, boardroom-ready intelligence brief.
        """
        
        
        # --- 4. EXECUTE AND SAVE ---
        try:
            result = agent_executor.invoke({"messages": [("user", query)]})
            raw_content = result["messages"][-1].content
            
            if isinstance(raw_content, list):
                clean_analysis = raw_content[0].get('text', 'No text found.')
            else:
                clean_analysis = raw_content
                
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            safe_company_name = client['company_name'].replace(" ", "_")
            filename = f"report_{safe_company_name}_{timestamp}.txt"
            
            report_data = f"""FINANCIAL INTELLIGENCE REPORT
-----------------------------
Client ID: {client['client_id']}
Company: {client['company_name']}
Exposure: {exposure}  <-- USING THE SAFE FALLBACK VARIABLE
Analyzed at: {timestamp}

{clean_analysis}
"""
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_data)
                
            print(f"[SUCCESS] Research complete! Report saved as: {filename}")
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze {client['company_name']}. Error: {e}")
            
    print("\n[SYSTEM] Batch processing complete! Check your folder for the highly accurate reports.")