



# from services.embedding_service import semantic_search
# from services.tavily_client import get_platform_trends
# import re


# # ============================================================
# # RAG ROUTING DECISION (FINAL — RETRIEVAL BASED)
# # ============================================================

# def _is_question_about_report(documents: list[str]) -> bool:
#     """
#     Proper RAG routing:
#     If vector DB retrieved chunks -> question belongs to report
#     If nothing retrieved -> fallback to web
#     """
#     return bool(documents and len(documents) > 0)


# # ============================================================
# # ROBUST EXTRACTIVE QA (NO LLM)
# # ============================================================




# def _extract_answer_from_context(question: str, documents: list[str]) -> str:
#     """
#     Deterministic QA over report text.
#     Returns answer ONLY if explicitly found.
#     Otherwise returns 'Not found in report'
#     """

#     if not documents:
#         return "Not found in report"

#     text = "\n".join(documents).lower()
#     q = question.lower()

#     # ---------- PLATFORM ----------
#     if "platform" in q:
#         patterns = [
#             r"platform\s*[:\-]\s*([a-z0-9 _-]+)",
#             r"platform\s+is\s+([a-z0-9 _-]+)",
#         ]
#         for p in patterns:
#             match = re.search(p, text, re.IGNORECASE)
#             if match:
#                 return match.group(1).strip()

#         return "Not found in report"

#     # ---------- TOPICS ----------
#     if "topic" in q or "trend" in q:
#         topics = []
#         for line in text.split("\n"):
#             if ":" in line and len(line) < 120:
#                 left = line.split(":")[0].strip()
#                 if 3 < len(left) < 40:
#                     topics.append(left)

#         if topics:
#             return ", ".join(topics[:5])

#         return "Not found in report"

#     # ---------- SUMMARY ----------
#     if "summary" in q:
#         for line in text.split("\n"):
#             if len(line.split()) > 8:
#                 return line.strip()

#         return "Not found in report"

#     # ---------- ANY OTHER QUESTION ----------
#     return "Not found in report"


# # def _extract_answer_from_context(question: str, documents: list[str]) -> str:
# #     """
# #     Deterministic QA over report text.
# #     Works even if chunks are fragmented.
# #     """

# #     if not documents:
# #         return "Not found in report"

# #     text = "\n".join(documents).lower()
# #     q = question.lower()

# #     # ---------- PLATFORM ----------
# #     if "platform" in q:
# #         patterns = [
# #             r"platform\s*[:\-]\s*([a-z0-9 _-]+)",
# #             r"platform\s+is\s+([a-z0-9 _-]+)",
# #             r"platform\s+([a-z0-9 _-]+)"
# #         ]
# #         for p in patterns:
# #             match = re.search(p, text, re.IGNORECASE)
# #             if match:
# #                 return match.group(1).strip().split("\n")[0]

# #     # ---------- TOPICS ----------
# #     if "topic" in q or "trend" in q:
# #         topics = []
# #         for line in text.split("\n"):
# #             if ":" in line and len(line) < 120:
# #                 left = line.split(":")[0].strip()
# #                 if 3 < len(left) < 40:
# #                     topics.append(left)

# #         if topics:
# #             return ", ".join(topics[:5])

# #     # ---------- SUMMARY ----------
# #     if "summary" in q:
# #         for line in text.split("\n"):
# #             if len(line.split()) > 8:
# #                 return line.strip()

# #     # ---------- GENERIC FALLBACK ----------
# #     sentences = re.split(r'[.\n]', text)
# #     sentences = [s.strip() for s in sentences if len(s.split()) > 6]

# #     return sentences[0] if sentences else "Not found in report"


# # ============================================================
# # MAIN HYBRID RAG SYSTEM
# # ============================================================


# def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

#     # STEP 1 — Retrieve context
#     result = semantic_search(query=question, report_id=report_id, k=5)
#     documents = result.get("documents", [])

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(documents))

#     # STEP 2 — Try extracting from report
#     report_answer = _extract_answer_from_context(question, documents)

#     # STEP 3 — Validate answer quality
#     invalid_answers = [
#         "",
#         "not found in report",
#         "unknown",
#         "none",
#         "n/a",
#     ]

#     is_valid_report_answer = (
#         report_answer
#         and report_answer.lower().strip() not in invalid_answers
#         and len(report_answer.split()) <= 40   # prevents long random paragraphs
#     )

#     # STEP 4 — Decide source
#     if is_valid_report_answer:
#         print("📊 Answered from REPORT")
#         final_answer = report_answer
#         source = "report"

#     else:
#         print("🌐 Falling back to Tavily — report had no answer")

#         tavily = get_platform_trends(question)

#         if tavily.get("success") and tavily.get("data"):
#             final_answer = tavily["data"][0].get("content", "No web result found")
#         else:
#             final_answer = "I couldn't find reliable information online."

#         source = "web"

#     if return_docs:
#         return final_answer, documents, source
#     return final_answer


# # def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

# #     result = semantic_search(query=question, report_id=report_id, k=5)
# #     documents = result.get("documents", [])

# #     print("🔍 semantic_search report_id:", report_id)
# #     print("📄 documents found:", len(documents))

# #     # ---------- RAG ----------
# #     if _is_question_about_report(documents):
# #         answer = _extract_answer_from_context(question, documents)
# #         source = "report"

# #     # ---------- WEB FALLBACK ----------
# #     else:
# #         print("🌐 Tavily fallback triggered")
# #         tavily = get_platform_trends(question)

# #         if tavily.get("success") and tavily.get("data"):
# #             answer = tavily["data"][0].get("content", "No web result found")
# #         else:
# #             answer = "No information available"

# #         source = "web"

# #     if return_docs:
# #         return answer, documents, source
# #     return answer


# # ============================================================
# # NOT USED ANYMORE (kept for compatibility)
# # ============================================================

# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     return False






from services.embedding_service import semantic_search
from services.tavily_client import get_platform_trends
import re


# ============================================================
# DETERMINE SOURCE (ONLY RETRIEVAL BASED)
# ============================================================
def _has_report_context(documents: list[str]) -> bool:
    """
    If vectors retrieved → belongs to report
    Deterministic RAG routing
    """
    return len(documents) > 0


# ============================================================
# EXTRACT ANSWER FROM REPORT (NO LLM)
# ============================================================
def _extract_answer(question: str, documents: list[str]) -> str:

    if not documents:
        return "No relevant information found in the report."

    text = "\n".join(documents)
    lower = text.lower()
    q = question.lower()

    # ---------- PLATFORM ----------
    if "platform" in q:
        match = re.search(r"platform[:\-\s]+([a-zA-Z0-9 ]+)", lower)
        if match:
            return match.group(1).strip().title()

    # ---------- TOPICS ----------
    if "trend" in q or "topic" in q:
        topics = []
        for line in text.split("\n"):
            if ":" in line:
                left = line.split(":")[0].strip()
                if 3 < len(left) < 50:
                    topics.append(left)
        if topics:
            return ", ".join(topics[:5])

    # ---------- SUMMARY ----------
    if "summary" in q:
        for line in text.split("\n"):
            if len(line.split()) > 8:
                return line.strip()

    # ---------- DEFAULT ----------
    # return best matching sentence
    sentences = re.split(r'[.\n]', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 6]
    return sentences[0] if sentences else documents[0][:200]


# ============================================================
# WEB FALLBACK (CONTROLLED)
# ============================================================
def _web_fallback(question: str) -> str:

    search_query = f"{question} social media trend"

    tavily = get_platform_trends(search_query)

    if tavily.get("success") and tavily.get("data"):
        return tavily["data"][0].get("content", "")[:300]

    return "I couldn't find reliable information online."


# ============================================================
# MAIN HYBRID RAG
# ============================================================
def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

    # STEP 1 — Retrieve
    result = semantic_search(query=question, report_id=report_id, k=5)
    documents = result.get("documents", [])

    print("🔍 documents retrieved:", len(documents))

    # STEP 2 — ROUTE (deterministic)
    if _has_report_context(documents):
        answer = _extract_answer(question, documents)
        source = "report"
        print("📊 Source: REPORT")

    else:
        answer = _web_fallback(question)
        source = "web"
        print("🌐 Source: WEB")

    if return_docs:
        return answer, documents, source
    return answer
