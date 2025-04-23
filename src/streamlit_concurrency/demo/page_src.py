import streamlit as st
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent


def read_repo_file(file_path: str) -> str:
    """
    Read a file from the repository and return its content as a string.
    """
    with open(REPO_ROOT / file_path, "r") as f:
        return f.read()


def render_page_src(page_file: str):
    st.divider()
    with st.expander("Source code for this page", expanded=False):
        code = Path(page_file).read_text()
        st.code(code, language="python", line_numbers=True)
    # st.markdown(f"Or view on [GitHub]({to_github_url(page_file)})")


def to_github_url(page_file: str) -> str:
    github_tree = "https://github.com/jokester/streamlit-concurrency/tree/main"
    path_in_repo = Path(page_file).relative_to(REPO_ROOT)
    return f"{github_tree}/{path_in_repo}"
