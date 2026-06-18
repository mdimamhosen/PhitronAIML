import streamlit as st
import json
import os
from datetime import datetime
# pyrefly: ignore [missing-import]
from langchain_openai import ChatOpenAI
# pyrefly: ignore [missing-import]
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
# pyrefly: ignore [missing-import]
from langchain_core.tools import tool

# Page Configuration (Mobile-First responsive layout)
st.set_page_config(
    page_title="AI Personal Agent",
    page_icon="💼",
    layout="centered"
)

# Custom Styling for premium glassmorphism feel and touch-friendly mobile elements
st.markdown("""
    <style>
    /* Premium Title Gradients */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(90deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Touch friendly buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        background-color: #262730;
        border: 1px solid #464646;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        background-color: #1e1e24;
    }
    
    /* KPI Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# File paths for storing notes and budget local databases
NOTES_FILE = "notes.json"
BUDGET_FILE = "budget.json"

# Initialize budget limits in session state if not set
if "budget_limits" not in st.session_state:
    st.session_state.budget_limits = {
        "food": 200.0,
        "shopping": 150.0,
        "utilities": 100.0,
        "entertainment": 100.0,
        "other": 150.0
    }

# ---------------------------------------------------------------------------
# LangChain Tools Setup
# ---------------------------------------------------------------------------

@tool
def get_current_time() -> str:
    """Returns the current date and time on the system."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def add_note(title: str, content: str) -> str:
    """Saves a personal note with a title and text content. Use this to track ideas, tasks, or list notes."""
    note = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes = []
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        except Exception:
            notes = []
    notes.append(note)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)
    return f"Successfully saved note: '{title}'."

@tool
def get_notes() -> str:
    """Retrieves all stored personal notes."""
    if not os.path.exists(NOTES_FILE):
        return "No notes stored yet."
    try:
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
        if not notes:
            return "No notes stored yet."
        output = []
        for i, n in enumerate(notes, 1):
            output.append(f"{i}. [{n['timestamp']}] **{n['title']}**: {n['content']}")
        return "\n".join(output)
    except Exception as e:
        return f"Error retrieving notes: {str(e)}"

@tool
def add_budget_transaction(amount: float, category: str, type: str, description: str = "") -> str:
    """Adds a budget transaction (expense or income).
    Args:
        amount: The monetary amount.
        category: The category (e.g. food, shopping, utilities, entertainment, salary, other).
        type: Must be either 'expense' or 'income'.
        description: A short description of the transaction.
    """
    category = category.lower().strip()
    type = type.lower().strip()
    if type not in ["expense", "income"]:
        return "Error: type must be either 'expense' or 'income'."
        
    transaction = {
        "amount": amount,
        "category": category,
        "type": type,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    transactions = []
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as f:
                transactions = json.load(f)
        except Exception:
            transactions = []
            
    transactions.append(transaction)
    with open(BUDGET_FILE, "w") as f:
        json.dump(transactions, f, indent=4)
        
    # Check limit status for alert
    limit_status = ""
    if type == "expense":
        category_total = sum(t["amount"] for t in transactions if t["type"] == "expense" and t["category"] == category)
        limit = st.session_state.budget_limits.get(category, 0.0)
        if limit > 0:
            if category_total > limit:
                limit_status = f" **[ALERT]** You have exceeded your budget for {category}! Spent: ${category_total:.2f}, Limit: ${limit:.2f}."
            elif category_total >= limit * 0.8:
                limit_status = f" **[WARNING]** You have spent over 80% of your budget for {category}! Spent: ${category_total:.2f}, Limit: ${limit:.2f}."
                
    return f"Successfully added {type} of ${amount:.2f} to {category}.{limit_status}"

@tool
def get_budget_summary() -> str:
    """Computes total income, total expense, net balance, and checks for category budget alerts."""
    if not os.path.exists(BUDGET_FILE):
        return "No transactions logged yet."
    try:
        with open(BUDGET_FILE, "r") as f:
            transactions = json.load(f)
        if not transactions:
            return "No transactions logged yet."
            
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        net_balance = total_income - total_expense
        
        category_spending = {}
        for t in transactions:
            if t["type"] == "expense":
                cat = t["category"]
                category_spending[cat] = category_spending.get(cat, 0.0) + t["amount"]
                
        alerts = []
        breakdown_lines = []
        for cat, spent in category_spending.items():
            limit = st.session_state.budget_limits.get(cat, 0.0)
            if limit > 0:
                percent = (spent / limit) * 100
                breakdown_lines.append(f"- **{cat.capitalize()}**: ${spent:.2f} of ${limit:.2f} ({percent:.1f}%)")
                if spent > limit:
                    alerts.append(f"⚠️ **ALERT**: Exceeded limit for {cat}! (Spent: ${spent:.2f}, Limit: ${limit:.2f})")
                elif spent >= limit * 0.8:
                    alerts.append(f"🔔 **WARNING**: Approaching limit for {cat}! (Spent: ${spent:.2f}, Limit: ${limit:.2f})")
            else:
                breakdown_lines.append(f"- **{cat.capitalize()}**: ${spent:.2f} (No limit set)")
                
        alert_text = "\n".join(alerts) if alerts else "✅ All categories within budget limits."
        breakdown_text = "\n".join(breakdown_lines)
        
        return (
            f"### Budget Summary\n"
            f"- **Total Income**: ${total_income:.2f}\n"
            f"- **Total Expenses**: ${total_expense:.2f}\n"
            f"- **Net Balance**: ${net_balance:.2f}\n\n"
            f"### Category Breakdown\n"
            f"{breakdown_text}\n\n"
            f"### Alerts\n"
            f"{alert_text}"
        )
    except Exception as e:
        return f"Error retrieving budget summary: {str(e)}"

# Define list of tools
tools = [get_current_time, add_note, get_notes, add_budget_transaction, get_budget_summary]

# Helper function to read current budget details for UI rendering
def load_budget_data():
    if not os.path.exists(BUDGET_FILE):
        return 0.0, 0.0, 0.0, {}
    try:
        with open(BUDGET_FILE, "r") as f:
            transactions = json.load(f)
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        net_balance = total_income - total_expense
        
        category_spending = {}
        for t in transactions:
            if t["type"] == "expense":
                cat = t["category"]
                category_spending[cat] = category_spending.get(cat, 0.0) + t["amount"]
        return total_income, total_expense, net_balance, category_spending
    except Exception:
        return 0.0, 0.0, 0.0, {}

# Helper function to load notes for UI rendering
def load_notes_data():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

# ---------------------------------------------------------------------------
# Sidebar Settings
# ---------------------------------------------------------------------------
st.sidebar.title("🛠️ Agent Configuration")

# Verify OpenAI API Key from Streamlit Secrets
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=st.secrets.get("OPENAI_API_KEY", ""),
    type="password",
    help="Pre-loaded from secrets, or edit here if needed."
)

if not openai_api_key:
    st.info("👈 Please enter your OpenAI API key in the sidebar to run the agent.")
    st.stop()

# Initialize LangChain LLM binded with tools
model_name = st.secrets.get("OPENAI_CHAT_MODEL", "gpt-4o-mini")
llm = ChatOpenAI(api_key=openai_api_key, model=model_name, temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Sidebar Monthly Budget Limits Configuration
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Monthly Budget Limits")
for cat in st.session_state.budget_limits.keys():
    st.session_state.budget_limits[cat] = st.sidebar.number_input(
        f"{cat.capitalize()} Limit ($)",
        value=float(st.session_state.budget_limits[cat]),
        step=10.0,
        min_value=0.0
    )

# Clear Chats
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------------------------
st.title("💼 Personal Assistant Agent")
st.write("Your mobile-responsive agent for managing notes, tracking budgets, and receiving alert warnings.")

# Create tabs for interactive chat and structured dashboard
tab_chat, tab_dashboard = st.tabs(["💬 Agent Chat", "📊 View Notes & Budgets"])

# 1. TAB: CHAT INTERFACE
with tab_chat:
    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display conversation messages
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            if msg.content:
                with st.chat_message("assistant"):
                    st.markdown(msg.content)

    # User Input
    if user_prompt := st.chat_input("Ask the agent (e.g., 'Track $15 expense on lunch', 'List notes')"):
        # Append and draw user message
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Agent thinking loop
        with st.chat_message("assistant"):
            current_messages = [
                SystemMessage(content=(
                    f"You are a helpful personal automation assistant. The current system time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. "
                    f"You have access to tools to save and read personal notes, and to log/summarize budget transactions (income/expense). "
                    f"If the user adds an expense, check if it triggers a warning (>=80% of limit) or alert (exceeds limit) and report it in your response. "
                    f"Always reply to the user using clean markdown."
                ))
            ] + st.session_state.messages

            max_iterations = 6
            for _ in range(max_iterations):
                # Status loader for mobile transparency
                with st.status("Thinking...", expanded=True) as status:
                    response = llm_with_tools.invoke(current_messages)
                    
                    if not response.tool_calls:
                        status.update(label="Response generated", state="complete")
                        break
                    
                    status.write(f"Executing tools...")
                    current_messages.append(response)
                    
                    for tool_call in response.tool_calls:
                        func_name = tool_call["name"]
                        func_args = tool_call["args"]
                        
                        status.write(f"Running `{func_name}` tool...")
                        
                        try:
                            # Invoke corresponding LangChain tool
                            if func_name == "get_current_time":
                                tool_output = get_current_time.invoke(func_args)
                            elif func_name == "add_note":
                                tool_output = add_note.invoke(func_args)
                            elif func_name == "get_notes":
                                tool_output = get_notes.invoke(func_args)
                            elif func_name == "add_budget_transaction":
                                tool_output = add_budget_transaction.invoke(func_args)
                            elif func_name == "get_budget_summary":
                                tool_output = get_budget_summary.invoke(func_args)
                            else:
                                tool_output = f"Error: Tool {func_name} not found."
                        except Exception as e:
                            tool_output = f"Error running tool {func_name}: {str(e)}"
                            
                        status.write(f"Result: {tool_output}")
                        
                        tool_msg = ToolMessage(
                            content=str(tool_output),
                            tool_call_id=tool_call["id"]
                        )
                        current_messages.append(tool_msg)
                        
                    status.update(label="Tools executed successfully", state="complete")

            # Final response generation
            if response.tool_calls:
                response = llm_with_tools.invoke(current_messages)
                
            st.markdown(response.content)
            
            # Save assistant messages to session state
            new_msgs = current_messages[len(st.session_state.messages) + 1:]
            st.session_state.messages.extend(new_msgs)
            if response not in st.session_state.messages:
                st.session_state.messages.append(response)

# 2. TAB: DASHBOARD
with tab_dashboard:
    # Load fresh data
    income, expense, balance, category_spending = load_budget_data()
    notes = load_notes_data()
    
    st.subheader("💰 Financial Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Balance", f"${balance:.2f}", delta=None)
    col2.metric("Total Income", f"${income:.2f}", delta=None)
    col3.metric("Total Expense", f"${expense:.2f}", delta=None)
    
    st.write("---")
    st.subheader("📊 Budgets & Alert Warnings")
    
    for cat, limit in st.session_state.budget_limits.items():
        spent = category_spending.get(cat, 0.0)
        if limit > 0:
            percent = min(spent / limit, 1.0)
            
            # Display warning/alerts in UI
            if spent > limit:
                st.error(f"🚨 **{cat.capitalize()}**: Exceeded budget! Spent: ${spent:.2f} of ${limit:.2f}")
            elif spent >= limit * 0.8:
                st.warning(f"⚠️ **{cat.capitalize()}**: Approaching limit! Spent: ${spent:.2f} of ${limit:.2f}")
            else:
                st.success(f"✅ **{cat.capitalize()}**: Spent: ${spent:.2f} of ${limit:.2f}")
                
            st.progress(percent)
        else:
            st.info(f"💡 **{cat.capitalize()}**: Spent: ${spent:.2f} (No limit set)")

    st.write("---")
    st.subheader("📝 Stored Personal Notes")
    if not notes:
        st.info("No personal notes found. You can add one by talking to the agent!")
    else:
        for n in reversed(notes):
            with st.expander(f"📌 {n['title']} ({n['timestamp']})"):
                st.markdown(n['content'])
