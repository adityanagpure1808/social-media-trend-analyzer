




# from services.embedding_service import semantic_search
# import re


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


# # ============================================================
# # MAIN HYBRID RAG SYSTEM
# # ============================================================

# def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

#     # STEP 1 — Retrieve context (vector DB)
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
#         and len(report_answer.split()) <= 40
#     )

#     # STEP 4 — Decide source
#     if is_valid_report_answer:
#         print("📊 Answered from REPORT")
#         final_answer = report_answer
#         source = "report"

#     else:
#         print("🌐 Falling back to Tavily — report had no answer")

#         # Lazy import → prevents startup memory usage
#         from services.tavily_client import get_platform_trends

#         tavily = get_platform_trends(question)

#         if tavily.get("success") and tavily.get("data"):
#             final_answer = tavily["data"][0].get("content", "No web result found")
#         else:
#             final_answer = "I couldn't find reliable information online."

#         source = "web"

#     if return_docs:
#         return final_answer, documents, source
#     return final_answer


# # ============================================================
# # COMPATIBILITY FUNCTION
# # ============================================================

# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     return False





from services.embedding_service import semantic_search
import re


# ============================================================
# ROBUST EXTRACTIVE QA (NO LLM)
# ============================================================

def _extract_answer_from_context(question: str, documents: list[str]) -> str:
    """
    Deterministic QA over report text.
    Returns answer ONLY if explicitly found.
    Otherwise returns 'Not found in report'
    """

    if not documents:
        return "Not found in report"

    text = "\n".join(documents).lower()
    q = question.lower()

    # ---------- PLATFORM ----------
    if "platform" in q:
        patterns = [
            r"platform\s*[:\-]\s*([a-z0-9 _-]+)",
            r"platform\s+is\s+([a-z0-9 _-]+)",
        ]
        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Not found in report"

    # ---------- TOPICS ----------
    if "topic" in q or "trend" in q:
        topics = []
        for line in text.split("\n"):
            if ":" in line and len(line) < 120:
                left = line.split(":")[0].strip()
                if 3 < len(left) < 40:
                    topics.append(left)

        if topics:
            return ", ".join(topics[:5])

        return "Not found in report"

    # ---------- SUMMARY ----------
    if "summary" in q:
        for line in text.split("\n"):
            if len(line.split()) > 8:
                return line.strip()

        return "Not found in report"

    # ---------- ANY OTHER QUESTION ----------
    return "Not found in report"


# ============================================================
# MAIN HYBRID RAG SYSTEM (FIXED ROUTER)
# ============================================================

def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

    # STEP 1 — Retrieve context (vector DB)
    result = semantic_search(query=question, report_id=report_id, k=5)
    documents = result.get("documents", [])

    print("🔍 semantic_search report_id:", report_id)
    print("📄 documents found:", len(documents))

    # STEP 2 — Extract answer
    report_answer = _extract_answer_from_context(question, documents)

    # ============================================================
    # 🔥 FIXED DECISION RULE (retrieval-based RAG)
    # ============================================================
    # If chunks exist → ALWAYS report
    if documents:
        print("📊 Using REPORT context")

        if not report_answer or report_answer.lower().strip() == "not found in report":
            final_answer = "The report does not explicitly mention this information."
        else:
            final_answer = report_answer

        source = "report"

    # Only fallback when NO chunks retrieved
    else:
        print("🌐 No relevant report chunks → Tavily fallback")

        # Lazy import keeps startup memory low
        from services.tavily_client import get_platform_trends

        tavily = get_platform_trends(question)

        if tavily.get("success") and tavily.get("data"):
            final_answer = tavily["data"][0].get("content", "No web result found")
        else:
            final_answer = "I couldn't find reliable information online."

        source = "web"

    if return_docs:
        return final_answer, documents, source
    return final_answer


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
    return False
