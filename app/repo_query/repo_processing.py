"""Process a list of repositories and return a dictionary of embedded documents."""
import logging
import os

from llama_index import GithubRepositoryReader

from app.repo_query.data_persistence import load_pickle, save_pickle


class RepoProcessor:
    """Process a list of repositories and return a dictionary of embedded documents."""

    def __init__(self, command_args, github_token, pickle_docs_dir):
        self.debug = command_args.debug
        self.github_token = github_token
        self.pickle_docs_dir = pickle_docs_dir

    def process_single_repo(self, repo, repo_info):
        """Process a single repository."""
        logging.debug("Processing %s", repo)
        repo_owner, repo_name_at_sha = repo.split("/")
        repo_name, commit_sha = repo_name_at_sha.split("@")
        docs_filename = f"{repo_owner}-{repo_name}-{commit_sha}-docs.pkl"
        if os.path.exists(os.path.join(self.pickle_docs_dir, docs_filename)):
            return load_pickle(docs_filename, self.pickle_docs_dir)

        loader = GithubRepositoryReader(
            github_token=self.github_token,
            owner=repo_owner,
            repo=repo_name,
            ignore_directories=repo_info.get("ignore_directories"),
            ignore_file_extensions=repo_info.get("ignore_file_extensions"),
            verbose=self.debug,
            concurrent_requests=10,
        )
        embedded_docs = loader.load_data(commit_sha=commit_sha)
        save_pickle(embedded_docs, docs_filename, self.pickle_docs_dir)
        return embedded_docs

    def process_repos(self, repos):
        """Process the repositories."""
        g_docs = {}
        for repo, repo_info in repos.items():
            g_docs[repo] = self.process_single_repo(repo, repo_info)
        return g_docs
