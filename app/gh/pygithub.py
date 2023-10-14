""" This script prints the directory structure of a github repository. """
from github import Github

# First create a Github instance using an access token
g = Github("<your access token>")

# Then get the repository
repo = g.get_repo("<username>/<repository name>")

# Get the contents of the root directory of the repo
r_contents = repo.get_contents("")


# Function to recursively print directory structure
def print_directory_contents(contents, indent=0):
    """Print the directory contents."""
    for content in contents:
        if content.type == "dir":
            print("\t" * indent + content.name)
            print_directory_contents(repo.get_contents(content.path), indent + 1)
        else:
            print("\t" * indent + content.name)


# Call the function to print the directory structure
print_directory_contents(r_contents)
