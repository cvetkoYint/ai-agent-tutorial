from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime


search = DuckDuckGoSearchRun()


# search web tool
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return search.run(query)
