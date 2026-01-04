import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
# Search up to 3 parent directories for .env file
env_path = Path(__file__).resolve()
for _ in range(3):
    env_path = env_path.parent
    env_file = env_path / '.env'
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
        break
else:
    # Fallback to default behavior
    load_dotenv()

# Load LLM Provider Selection
llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
print(f"Using LLM Provider: {llm_provider}")

# Load OpenAI Configuration
if llm_provider == 'openai':
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    if not openai_api_key:
        print("WARNING: OPENAI_API_KEY not found in environment variables!")
    openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
    print(f"Using OpenAI model: {openai_model}")
else:
    openai_api_key = None
    openai_model = None

# Load DeepSeek Configuration
if llm_provider == 'deepseek':
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', '')
    if not deepseek_api_key:
        print("WARNING: DEEPSEEK_API_KEY not found in environment variables!")
    deepseek_model = os.getenv('DEEPSEEK_MODEL', 'deepseek-v3.2')
    deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    print(f"Using DeepSeek model: {deepseek_model}")
    print(f"DeepSeek API endpoint: {deepseek_base_url}")
else:
    deepseek_api_key = None
    deepseek_model = None
    deepseek_base_url = None

# Put your name
key_owner = "key"

# Maze/Ville assets (if applicable)
maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

# Verbose
debug = True
