


# import os
# from dotenv import load_dotenv
# from tavily import TavilyClient

# load_dotenv()

# # Create Tavily client
# client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# # =========================
# # GENERIC TAVILY SEARCH
# # =========================
# def get_platform_trends(query: str):
#     """
#     Generic Tavily search wrapper.
#     The caller is responsible for constructing the query.
#     """
#     response = client.search(
#         query=query,
#         search_depth="advanced",
#         max_results=5
#     )

#     return {
#         "success": True,
#         "data": response.get("results", [])
#     }



import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# =========================
# SAFE TAVILY CLIENT SETUP
# =========================
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None


# # =========================
# # GENERIC TAVILY SEARCH
# # =========================
# def get_platform_trends(query: str):
#     """
#     Generic Tavily search wrapper.
#     Tavily is OPTIONAL for this issue.
#     """

#     # 🔒 Guard: do NOT crash app if Tavily is not configured
#     if not client:
#         return {
#             "success": False,
#             "data": [],
#             "error": "Tavily API key not configured"
#         }

#     response = client.search(
#         query=query,
#         search_depth="advanced",
#         max_results=5
#     )

#     return {
#         "success": True,
#         "data": response.get("results", [])
#     }





# =========================
# REPORT GENERATION
# =========================
def get_platform_trends(query: str):
    if not client:
        return {
            "success": False,
            "data": [],
            "error": "Tavily API key not configured"
        }

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return {
        "success": True,
        "data": response.get("results", [])
    }


# =========================
# CHAT FALLBACK (RAG FAILS)
# =========================
def research_with_tavily(query: str):
    if not client:
        return None

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        results = response.get("results", [])
        if not results:
            return None

        summary = "\n".join(
            f"- {r.get('title')}: {r.get('content')}"
            for r in results[:3]
        )

        return summary

    except Exception:
        return None
