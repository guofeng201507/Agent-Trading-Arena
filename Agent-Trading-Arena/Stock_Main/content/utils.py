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

# Load OpenAI API Key from environment
openai_api_key = os.getenv('OPENAI_API_KEY', '')
if not openai_api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")

# Load OpenAI Model from environment (default to gpt-4)
openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
print(f"Using OpenAI model: {openai_model}")

# Put your name
key_owner = "key"

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

# Verbose
debug = True
