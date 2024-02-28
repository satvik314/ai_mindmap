# ai_mindmap

Create Mindmaps using AI.

by [Satvik](https://www.linkedin.com/in/satvik-paramkusham/)


## Getting Started

Follow these instructions to get the Streamlit app running on your local machine:

### 1. Clone the repository
```bash
git clone https://github.com/satvik314/ai_mindmap.git
```

### 2. Navigate to the cloned repository
```bash
cd ai_mindmap
```

### 3.1. (For GPT model) Add Anyscale Key to ```secrets.toml```
```bash
ANYSCALE_API_TOKEN = <"your_token">
```

### 3.2. (Optional) Add Supabase keys to ```secrets.toml```
```bash
SUPABASE_URL = <"your_url">
SUPABASE_KEY = <"your_token">
```

### 4. Install required Python libraries
```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit App
```bash
streamlit run app.py
```

In the app, enter the topic you want to learn and let the app create an amazing mindmap!
