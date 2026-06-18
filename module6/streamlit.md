# Streamlit: Complete Guide from Newbie to Pro

Streamlit is an open-source Python framework that allows developers, data scientists, and AI engineers to build and share interactive web applications in minutes. With Streamlit, you don't need any front-end experience (HTML, CSS, or JavaScript); you write standard Python code, and Streamlit dynamically turns it into a responsive, beautiful web app.

---

## Table of Contents
1. [What is Streamlit?](#1-what-is-streamlit)
2. [Prerequisites and Full Setup Guide](#2-prerequisites-and-full-setup-guide)
3. [How Streamlit Works (Core Architecture)](#3-how-streamlit-works-core-architecture)
4. [Newbie Level: Core UI Components](#4-newbie-level-core-ui-components)
5. [Intermediate Level: Layouts, Forms, and Caching](#5-intermediate-level-layouts-forms-and-caching)
6. [Pro Level: State Management, Secrets, and Custom styling](#6-pro-level-state-management-secrets-and-custom-styling)
7. [Deploying Streamlit Apps](#7-deploying-streamlit-apps)
8. [Best Practices & Common Gotchas](#8-best-practices--common-gotchas)

---

## 1. What is Streamlit?

Traditionally, building a web interface for a Python-based machine learning model or data analysis pipeline required:
1. Writing a backend server (e.g., Flask, FastAPI, Django).
2. Writing a frontend UI (e.g., HTML, CSS, JavaScript/React/Vue).
3. Setting up API routes, AJAX requests, and managing CORS issues.

**Streamlit replaces all of this.** It allows you to build data applications directly in Python using standard Python scripts. 

### Why Streamlit?
- **Python Only**: No HTML, CSS, JS, or API routing required.
- **Fast Prototyping**: Write code, save the file, and watch the app update instantly in the browser.
- **Out-of-the-box Aesthetics**: Clean, modern, and responsive user interface layout with dark mode support.
- **Interactive Widgets**: Native support for sliders, dropdowns, buttons, file uploaders, and chart libraries (Matplotlib, Plotly, Altair, Bokeh).

---

## 2. Prerequisites and Full Setup Guide

Follow this guide to configure a clean Python development environment on your Windows system.

### Step 1: Verify Python Installation
Streamlit requires Python 3.8 to 3.12+. Open your terminal (PowerShell or Command Prompt) and check your Python version:
```powershell
python --version
```
> [!NOTE]
> If Python is not installed or not added to your system PATH, download the installer from [python.org](https://www.python.org/) and ensure you check the box labeled **"Add Python to PATH"** during installation.

### Step 2: Set Up a Dedicated Virtual Environment
Using a virtual environment prevents package conflicts between different Python projects.

1. Navigate to your project directory:
   ```powershell
   cd c:\Error\PhitronAIML\module6-streamlit
   ```
2. Create a virtual environment named `.venv`:
   ```powershell
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **In Git Bash / MINGW64 (Bash)**:
     ```bash
     source .venv/Scripts/activate
     ```
   - **In PowerShell**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **In Command Prompt (cmd)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   *(You should now see `(.venv)` prepended to your command prompt line, indicating the virtual environment is active.)*

### Step 3: Install Streamlit
With the virtual environment activated, upgrade `pip` and install `streamlit` inside the virtual environment:
```bash
python -m pip install --upgrade pip
pip install streamlit
```
To verify the installation was successful, launch Streamlit's built-in demo app:
```powershell
streamlit hello
```
*This command launches a local web server and opens your default browser to `http://localhost:8501`, showing interactive demos.*

### Step 4: Write and Run Your First "Hello World" App
1. Create a file named `app.py` in your project folder.
2. Open `app.py` in your text editor and write:
   ```python
   import streamlit as st

   st.title("My First Streamlit App!")
   st.write("Hello, world! This is a web app built entirely in Python.")
   ```
3. Run the application from your terminal:
   ```powershell
   streamlit run app.py
   ```
4. Streamlit will start a local server and output URLs:
   - **Local URL**: `http://localhost:8501`
   - **Network URL**: `http://192.168.x.x:8501` (accessible by other devices on the same Wi-Fi network)

---

## 3. How Streamlit Works (Core Architecture)

Before writing complex applications, you must understand Streamlit's execution model. 

Unlike traditional web applications that use event listeners to update specific parts of the page, **Streamlit runs your entire Python script from top to bottom every time a user interacts with a widget.**

```
+-------------------------------------------------------------+
|                     User Interaction                        |
|   (Clicks a button, slides a slider, enters text, etc.)     |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                Streamlit triggers a Rerun                   |
|          (The entire script runs from top to bottom)        |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|             Widgets return their updated value              |
|        (e.g., slider = st.slider(...) returns current value) |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Browser View Updates                       |
|           (Changes are drawn on the webpage)                |
+-------------------------------------------------------------+
```

### Key Rules of the Execution Model:
1. **Top-to-Bottom**: When a widget value changes, the script is executed again from line 1.
2. **State Retention**: Normally, all variables are reset on rerun. To store values across runs, you *must* use `st.session_state`.
3. **No Event Handlers**: Instead of writing `on_click_callback()`, widgets act as simple value producers. For example:
   ```python
   # Traditional Web App: button triggers a callback function
   # Streamlit App:
   if st.button("Click Me"):
       st.write("You clicked the button!")
   ```

---

## 4. Newbie Level: Core UI Components

Streamlit provides built-in components for displaying content and capturing inputs. Let's look at the foundational elements.

### 4.1 Displaying Text & Code
Streamlit handles text rendering effortlessly. It fully supports GitHub-flavored Markdown.

```python
import streamlit as st

# Titles & Headers
st.title("This is a Title (H1)")
st.header("This is a Header (H2)")
st.subheader("This is a Subheader (H3)")

# Plain Text and Markdown
st.text("This is plain monospace text.")
st.markdown("This is **bold markdown**, *italic*, and [links](https://streamlit.io).")

# Code display with syntax highlighting
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

# The Swiss Army Knife: st.write
# st.write accepts strings, numbers, dataframes, charts, etc. and formats them automatically
st.write("You can write normal text or show structures directly:", {"key": "value", "list": [1, 2, 3]})
```

### 4.2 Interactive Input Widgets
Widgets capture input from users. The returned value is assigned to a variable on execution.

```python
import streamlit as st

# Button
if st.button("Say Hello"):
    st.write("Hello there!")

# Checkbox
agree = st.checkbox("I agree to the terms")
if agree:
    st.write("Thank you for agreeing!")

# Text input
username = st.text_input("Enter your username", placeholder="e.g. johndoe")

# Number input
age = st.number_input("Enter your age", min_value=0, max_value=120, value=25)

# Selection controls
option = st.selectbox("Choose a programming language", ["Python", "JavaScript", "Go", "Rust"])
st.write("You selected:", option)

# Sliders
slider_val = st.slider("Select a threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
```

### 4.3 Displaying Data
Streamlit can render Pandas DataFrames, tables, and raw JSON interactively.

```python
import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# st.dataframe provides interactive searching, filtering, and sorting
st.subheader("Interactive DataFrame")
st.dataframe(chart_data)

# st.table displays static data tables
st.subheader("Static Table")
st.table(chart_data.head())
```

---

## 5. Intermediate Level: Layouts, Forms, and Caching

As your app grows, you need layout controls to build clean grids, cache operations to keep responses fast, and forms to batch interactions.

### 5.1 Layout Containers
Streamlit offers structural components to organize your content.

#### Sidebar
Keep inputs separated from outputs by using the sidebar.
```python
import streamlit as st

# Add items directly to the sidebar using `st.sidebar.`
st.sidebar.title("App Sidebar Settings")
user_role = st.sidebar.selectbox("Select Role", ["Admin", "User", "Guest"])
```

#### Columns
Arrange elements side-by-side using grids.
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("Inputs here")

with col2:
    st.header("Column 2")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=150)

with col3:
    st.header("Column 3")
    st.write("Metrics here")
```

#### Tabs
Organize different sections of your app into navigation tabs.
```python
tab1, tab2 = st.tabs(["📊 Analytics", "⚙️ System Configuration"])

with tab1:
    st.write("Here you'll find charts and statistics.")

with tab2:
    st.write("Settings and server adjustments go here.")
```

#### Expanders
Create collapsible sections to hide advanced parameters.
```python
with st.expander("See Advanced Parameter Explanations"):
    st.write("Here are the detailed algorithms behind the selected model settings...")
```

### 5.2 Caching: Speeding Up Performance
Because Streamlit runs the script from top-to-bottom on every user interaction, heavy tasks like database queries, ML model loading, or API requests would freeze the app. Streamlit solves this using two main cache decorators:

1. **`@st.cache_data`**: Used for caching functions that return **data** (DataFrames, arrays, dictionaries, basic types).
2. **`@st.cache_resource`**: Used for caching **non-serializable resources** (Database connections, PyTorch/TensorFlow model sessions, API clients).

```python
import streamlit as st
import pandas as pd
import time

# Cache data returned from a CSV read or heavy analysis
@st.cache_data
def load_large_dataset(url):
    time.sleep(3) # Simulate a heavy network latency/processing step
    df = pd.read_csv(url)
    return df

# Cache a database connection
from sqlalchemy import create_engine
@st.cache_resource
def get_db_connection():
    # Establishes connection once; re-uses it across reruns and users
    engine = create_engine("sqlite:///mydb.db")
    return engine
```

### 5.3 Forms: Preventing Unnecessary Reruns
If you have multiple inputs (e.g., text fields, parameters), you don't want the app to rerun with every keystroke. Use `st.form` to batch inputs until the user explicitly clicks a submit button.

```python
with st.form("my_input_form"):
    st.write("Enter your credentials below:")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Forms MUST have a submit button
    submitted = st.form_submit_button("Log In")
    if submitted:
        st.success(f"Form submitted! Logging in: {email}")
```

---

## 6. Pro Level: State Management, Secrets, and Custom Styling

To build professional, production-grade applications, you must master user session tracking, configuration, styling, and secure key storage.

### 6.1 State Management (`st.session_state`)
Since Streamlit variables clear on rerun, you need a dictionary-like object that persists data between reruns. That object is `st.session_state`.

#### Simple Counter Example
```python
import streamlit as st

# Initialize session state variable if it doesn't exist yet
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Create functions to modify state
def increment_counter():
    st.session_state.counter += 1

def reset_counter():
    st.session_state.counter = 0

st.write(f"Current Count: {st.session_state.counter}")

# Use callbacks to execute functions before the rest of the script reruns
st.button("Increment", on_click=increment_counter)
st.button("Reset", on_click=reset_counter)
```

#### Advanced Example: To-Do List Application
```python
import streamlit as st

# Initialize to-do list in session state
if "todos" not in st.session_state:
    st.session_state.todos = []

# Input field and button to add a new task
new_todo = st.text_input("Add a new task:", key="todo_input")

if st.button("Add Task") and new_todo:
    st.session_state.todos.append(new_todo)
    # Clear input element value by modifying its corresponding state key
    st.session_state.todo_input = "" 
    st.rerun() # Force a rerun to update the UI instantly

# Display list of current tasks
st.subheader("Your Task List")
for idx, todo in enumerate(st.session_state.todos):
    col_task, col_delete = st.columns([0.85, 0.15])
    with col_task:
        st.write(f"{idx + 1}. {todo}")
    with col_delete:
        if st.button("Delete", key=f"del_{idx}"):
            st.session_state.todos.pop(idx)
            st.rerun()
```

### 6.2 Managing Database Secrets and Configs
Never hardcode passwords, API keys, or database secrets in your code. Streamlit handles configuration and secrets natively.

#### Directory Structure
```
my_app/
├── .streamlit/
│   ├── config.toml    # Theming & server parameters
│   └── secrets.toml   # Secure passwords & API keys (Add to .gitignore!)
└── app.py
```

#### `.streamlit/secrets.toml`
```toml
# Store secrets in TOML format
DB_USER = "admin"
DB_PASS = "super_secure_password"
OPENAI_API_KEY = "sk-..."
```

#### Accessing Secrets in `app.py`
```python
import streamlit as st

# Streamlit automatically loads secrets.toml into st.secrets
openai_key = st.secrets["OPENAI_API_KEY"]
db_password = st.secrets["DB_PASS"]

st.write(f"API key loaded successfully: {openai_key[:6]}...")
```

### 6.3 Themes and Custom Styling
You can style your app by editing `.streamlit/config.toml` or using inline HTML/CSS.

#### Customizing Themes via `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

#### Injecting Custom CSS
If you need surgical styling for specific elements:
```python
import streamlit as st

# Allow HTML rendering using unsafe_allow_html=True
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border-radius: 10px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
```

---

## 7. Deploying Streamlit Apps

Once your application is ready, you'll want to share it with the world.

### Method A: Streamlit Community Cloud (Recommended)
Streamlit hosts your apps for free, connected directly to your GitHub repository.
1. Commit your project and push it to a public GitHub repository. (Ensure your environment has a `requirements.txt` listing packages like `streamlit`, `pandas`, etc.)
2. Sign up at [share.streamlit.io](https://share.streamlit.io).
3. Click "New app", select your repository, branch, and entry point file (`app.py`).
4. Click "Deploy". Within minutes, your app is live on a public URL.

### Method B: Deploying with Docker
If you need to deploy to platforms like AWS, Google Cloud, or Azure, containerizing the application is standard practice.

#### `Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/your-username/your-repo.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 8. Best Practices & Common Gotchas

Keep these heuristics in mind to write clean, high-performance applications:

- **Use Caching Generously**: If a function takes more than 100ms to run or reads files/APIs, decorate it with `@st.cache_data` or `@st.cache_resource`.
- **Avoid Global Mutable State**: Streamlit apps are multi-user environments. Global variables are shared across all active sessions. Modifying global variables will affect all concurrent users. Always use `st.session_state` for user-specific data.
- **Never Save Secrets to Git**: Always put `.streamlit/secrets.toml` in your `.gitignore` file. Use platform environment variables when deploying in production.
- **Utilize `st.empty` for Dynamic Content**: If you need to construct loading animations, logs, or live updates, create a placeholder using `placeholder = st.empty()`, and call `placeholder.write(new_value)` dynamically to replace existing container contents.
- **Keep Requirements Minimal**: Only install required libraries in your production environment to keep your Docker builds and Cloud Cloud spin-up times fast.
