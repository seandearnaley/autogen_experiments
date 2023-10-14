"""Environment variables."""
from dotenv import load_dotenv
from utils import check_env_vars

# Constants
ENV_VARS = ["OPENAI_API_KEY", "GITHUB_TOKEN", "PERPLEXITY_API_KEY"]


def setup_env_vars():
    """Setup environment variables."""
    # Initialize environment
    load_dotenv()

    # Check environment variables
    check_env_vars(ENV_VARS)
