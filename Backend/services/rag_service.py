






# import os
# import google.generativeai as genai
# from services.embedding_service import semantic_search


# # =========================
# # CONFIGURE GOOGLE
# # =========================

# def configure_google():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not set")

#     genai.configure(api_key=api_key)


# # =========================
# # RAG ANSWERING (GOOGLE)
# # =========================

# def answer_question_about_report(report_id: str, question: str) -> str:
#     try:
#         configure_google()

#         # 1️⃣ Retrieve context
#         result = semantic_search(
#             query=question,
#             report_id=report_id,
#             top_k=5,
#         )

#         documents = result.get("documents", [])
#         if not documents:
#             return "I don't have enough information from the report."

#         context = "\n\n".join(documents)

#         # ✅ ONLY WORKING MODEL
#         # model = genai.GenerativeModel("models/gemini-pro")
#         # model = genai.GenerativeModel("gemini-2.5-flash")
#         model = genai.GenerativeModel("models/gemini-2.5-flash")


#         prompt = f"""
# You are an assistant answering questions strictly using the report content below.

# Rules:
# - Use ONLY the provided context
# - Do NOT hallucinate
# - If the answer is not present, say:
#   "I don't have enough information from the report."

# REPORT CONTENT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

#         response = model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0.2,
#                 "max_output_tokens": 512,
#             }
#         )

#         return response.text.strip()

#     except Exception as e:
#         return f"RAG error: {str(e)}"



# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     if not documents:
#         return True

#     if not answer or len(answer.strip()) < 20:
#         return True

#     bad_phrases = [
#         "i don't know",
#         "not enough information",
#         "cannot answer",
#         "no information available",
#     ]

#     answer_lower = answer.lower()
#     return any(p in answer_lower for p in bad_phrases)









# import os
# from google import genai

# # import google.generativeai as genai
# from services.embedding_service import semantic_search


# # =========================
# # CONFIGURE GOOGLE
# # =========================

# def configure_google():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not set")

#     genai.configure(api_key=api_key)


# # =========================
# # RAG ANSWERING (GOOGLE)
# # =========================

# # def answer_question_about_report(
# #     report_id: str,
# #     question: str,
# #     return_docs: bool = False,   # ✅ NEW
# # ):
# #     """
# #     Answers a question using ONLY report embeddings.
# #     Optionally returns retrieved documents for fallback logic.
# #     """

# #     try:
# #         configure_google()

# #         # 1️⃣ Retrieve context from vector DB
# #         result = semantic_search(
# #             query=question,
# #             report_id=report_id,
# #             top_k=5,
# #         )

# #         documents = result.get("documents", [])

# #         if not documents:
# #             answer = "I don't have enough information from the report."
# #             return (answer, documents) if return_docs else answer

# #         context = "\n\n".join(documents)

# #         # ✅ Stable Gemini model
# #         model = genai.GenerativeModel("models/gemini-2.5-flash")

# #         prompt = f"""
# # You are an assistant answering questions strictly using the report content below.

# # Rules:
# # - Use ONLY the provided context
# # - Do NOT hallucinate
# # - If the answer is not present, say:
# #   "I don't have enough information from the report."

# # REPORT CONTENT:
# # {context}

# # QUESTION:
# # {question}

# # ANSWER:
# # """

# #         response = model.generate_content(
# #             prompt,
# #             generation_config={
# #                 "temperature": 0.2,
# #                 "max_output_tokens": 512,
# #             }
# #         )

# #         answer = response.text.strip()

# #         # ✅ RETURN SHAPE CONTROLLED HERE
# #         if return_docs:
# #             return answer, documents

# #         return answer

# #     except Exception as e:
# #         error_answer = f"RAG error: {str(e)}"
# #         return (error_answer, []) if return_docs else error_answer







# def answer_question_about_report(
#     report_id: str,
#     question: str,
#     return_docs: bool = False,
# ):
#     try:
#         configure_google()

#         # 1️⃣ Retrieve context
#         result = semantic_search(
#             query=question,
#             report_id=report_id,
#             top_k=5,
#         )

#         documents = result.get("documents", [])
#         context = "\n\n".join(documents) if documents else ""

#         model = genai.GenerativeModel("models/gemini-2.5-flash")

#         prompt = f"""
# You are an assistant answering questions strictly using the report content below.

# Rules:
# - Use ONLY the provided context
# - Do NOT hallucinate
# - If the answer is not present, say:
#   "I don't have enough information from the report."

# REPORT CONTENT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

#         response = model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0.2,
#                 "max_output_tokens": 512,
#             }
#         )

#         answer = response.text.strip()

#         if return_docs:
#             return answer, documents

#         return answer

#     except Exception:
#         if return_docs:
#             return "", []
#         return ""












# # =========================
# # RAG QUALITY CHECK
# # =========================

# # def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
# #     """
# #     Heuristic to decide whether Tavily fallback is needed.
# #     """

# #     if not documents:
# #         return True

# #     if not answer or len(answer.strip()) < 20:
# #         return True

# #     bad_phrases = [
# #         "i don't know",
# #         "not enough information",
# #         "cannot answer",
# #         "no information available",
# #         "rag error",
# #     ]

# #     answer_lower = answer.lower()
# #     return any(p in answer_lower for p in bad_phrases)



# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     if not answer:
#         return True

#     answer_lower = answer.lower().strip()

#     # ❗ Explicit RAG failure phrases
#     failure_phrases = [
#         "i don't have enough information",
#         "not enough information",
#         "cannot answer",
#         "i don't know",
#         "no information available",
#         "insufficient information",
#     ]

#     # 1️⃣ RAG explicitly admits failure
#     if any(p in answer_lower for p in failure_phrases):
#         return True

#     # 2️⃣ No retrieved documents
#     if not documents:
#         return True

#     # 3️⃣ Very short / generic answers
#     if len(answer_lower) < 40:
#         return True

#     return False






# import os
# from google import genai
# from services.embedding_service import semantic_search


# # =========================
# # CLIENT (NEW GOOGLE SDK)
# # =========================
# def get_client():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not set")

#     return genai.Client(api_key=api_key)


# # =========================
# # RAG ANSWERING
# # =========================
# def answer_question_about_report(
#     report_id: str,
#     question: str,
#     return_docs: bool = False,
# ):
#     """
#     True RAG:
#     1) retrieve chunks
#     2) if none → RAG failed
#     3) else → LLM formats answer
#     """

#     try:
#         # 1️⃣ Retrieve context from vector DB
#         result = semantic_search(
#             query=question,
#             report_id=report_id,
#             top_k=5,
#         )

#         documents = result.get("documents", [])

#         # 🚨 CRITICAL: DO NOT CALL LLM IF NO CONTEXT
#         if not documents:
#             return ("", []) if return_docs else ""

#         context = "\n\n".join(documents)

#         # 2️⃣ Call Gemini (NEW SDK)
#         client = get_client()

#         prompt = f"""
# Answer ONLY using the report context below.

# If answer not present, reply:
# "Not found in report."

# REPORT:
# {context}

# QUESTION:
# {question}
# ANSWER:
# """

#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )

#         answer = (response.text or "").strip()

#         return (answer, documents) if return_docs else answer

#     except Exception as e:
#         print("RAG ERROR:", e)
#         return ("", []) if return_docs else ""





# import os
# from google import genai
# from services.embedding_service import semantic_search

# # =========================
# # CONFIGURE GOOGLE (NEW SDK)
# # =========================

# def configure_google():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not set")
#     return genai.Client(api_key=api_key)


# # =========================
# # RAG ANSWERING (GOOGLE)
# # =========================

# def answer_question_about_report(
#     report_id: str,
#     question: str,
#     return_docs: bool = False,
# ):
#     try:
#         client = configure_google()

#         # 1️⃣ Retrieve context from vector DB
#         result = semantic_search(
#             query=question,
#             report_id=report_id,
#             top_k=5,
#         )

#         documents = result.get("documents", [])

#         # 🚨 If no documents → TRUE RAG FAILURE
#         if not documents:
#             return ("", []) if return_docs else ""

#         context = "\n\n".join(documents)

#         prompt = f"""
# Answer strictly using the provided report context.

# If answer is not in context, say:
# "Not found in report."

# REPORT:
# {context}

# QUESTION:
# {question}
# ANSWER:
# """

#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )

#         answer = response.text.strip() if response.text else ""

#         return (answer, documents) if return_docs else answer

#     except Exception:
#         return ("", []) if return_docs else ""


# # =========================
# # RAG QUALITY CHECK
# # =========================

# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     if not answer:
#         return True

#     answer_lower = answer.lower().strip()

#     failure_phrases = [
#         "i don't have enough information",
#         "not enough information",
#         "cannot answer",
#         "i don't know",
#         "no information available",
#         "insufficient information",
#         "not found in report",
#     ]

#     if any(p in answer_lower for p in failure_phrases):
#         return True

#     if not documents:
#         return True

#     if len(answer_lower) < 40:
#         return True

#     return False



# import os
# from google import genai
# from services.embedding_service import semantic_search


# # =========================
# # CONFIGURE GOOGLE
# # =========================
# def configure_google():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not set")
#     return genai.Client(api_key=api_key)


# # =========================
# # RAG ANSWERING (STRICT GROUNDED MODE)
# # =========================
# def answer_question_about_report(
#     report_id: str,
#     question: str,
#     return_docs: bool = False,
# ):
#     """
#     Performs grounded retrieval QA over stored report chunks.
#     The model is forced into extraction-only behavior.
#     """

#     try:
#         client = configure_google()

#         # 1️⃣ Retrieve context from vector DB
#         result = semantic_search(
#             query=question,
#             report_id=report_id,
#             k=5
#         )

#         documents = result.get("documents", [])

#         # 🚨 Retrieval failure
#         if not documents:
#             return ("Not found in report", []) if return_docs else "Not found in report"

#         context = "\n\n".join(documents)

#         # 🔒 HARD GROUNDED PROMPT
#         prompt = f"""
# You are a retrieval QA system.

# STRICT RULES:
# - Answer ONLY using the REPORT text
# - Do NOT use outside knowledge
# - Do NOT explain
# - Do NOT add extra words
# - If answer not present, reply exactly: Not found in report
# - Maximum 15 words
# -make the answer as concise as possible, ideally 5-10 words. Only use more if necessary.

# REPORT:
# ----------------
# {context}
# ----------------

# QUESTION:
# {question}

# FINAL ANSWER:
# """

#         # 🧠 Less creative, better grounding
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )

#         answer = (response.text or "").strip()

#         if not answer:
#             answer = "Not found in report"

#         return (answer, documents) if return_docs else answer

#     except Exception as e:
#         print("RAG ERROR:", e)
#         return ("Not found in report", []) if return_docs else "Not found in report"


# # =========================
# # RAG QUALITY CHECK
# # =========================
# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     """
#     Decide whether to fallback to Tavily.

#     IMPORTANT:
#     Short answers like "instagram" are VALID.
#     Only fallback if model truly failed.
#     """

#     if not answer:
#         return True

#     answer_lower = answer.lower().strip()

#     # Only true failures
#     failure_phrases = [
#         "not found in report",
#         "i don't know",
#         "cannot answer",
#         "insufficient information",
#         "",
#     ]

#     if answer_lower in failure_phrases:
#         return True

#     if not documents:
#         return True

#     # Valid grounded answer (even 1 word)
#     return False










# from services.embedding_service import semantic_search
# from services.tavily_client import get_platform_trends
# import re


# # ============================================================
# # CHECK IF QUESTION MATCHES REPORT CONTENT
# # ============================================================

# # def _is_question_about_report(question: str, documents: list[str]) -> bool:
# #     """
# #     Determines whether retrieved chunks actually relate to the question.
# #     Prevents wrong RAG answers and enables Tavily fallback.
# #     """

# #     if not documents:
# #         return False

# #     q_words = set(question.lower().split())
# #     score = 0

# #     for doc in documents:
# #         doc_words = set(doc.lower().split())
# #         overlap = q_words.intersection(doc_words)
# #         score += len(overlap)

# #     # tuned for small report size
# #     return score >= 3









# def _is_question_about_report(question: str, documents: list[str]) -> bool:
#     """
#     Detect whether the user is asking about the generated report.
#     Uses intent detection + loose similarity instead of strict overlap.
#     """

#     if not documents:
#         return False

#     q = question.lower().strip()

#     # -------------------------------
#     # 1️⃣ Direct report intent detection
#     # -------------------------------
#     report_keywords = [
#         "report",
#         "platform",
#         "topic",
#         "trend",
#         "trending",
#         "summary",
#         "analysis",
#         "sentiment",
#         "generated",
#         "this data",
#         "this result",
#     ]

#     if any(word in q for word in report_keywords):
#         return True

#     # -------------------------------
#     # 2️⃣ Loose semantic overlap
#     # -------------------------------
#     q_words = set(q.split())
#     doc_text = " ".join(documents).lower()
#     doc_words = set(doc_text.split())

#     overlap = len(q_words.intersection(doc_words))

#     # only need minimal similarity
#     return overlap >= 1












# # ============================================================
# # EXTRACT ANSWER FROM REPORT (NO LLM)
# # ============================================================

# def _extract_answer_from_context(question: str, documents: list[str]) -> str:
#     """
#     Deterministic QA over report text.
#     """

#     text = "\n".join(documents)
#     q = question.lower()

#     # -------- PLATFORM --------
#     if "platform" in q:
#         match = re.search(r"platform:\s*([a-zA-Z0-9 _-]+)", text, re.IGNORECASE)
#         if match:
#             return match.group(1).strip()

#     # -------- TOPICS --------
#     if "topic" in q or "trend" in q:
#         lines = [l.strip() for l in text.split("\n") if ":" in l]
#         topics = [l.split(":")[0] for l in lines if len(l) < 120]
#         if topics:
#             return ", ".join(topics[:5])

#     # -------- SUMMARY --------
#     if "summary" in q:
#         for line in text.split("\n"):
#             if len(line.split()) > 8:
#                 return line.strip()

#     # -------- GENERIC FALLBACK (best matching sentence) --------
#     sentences = re.split(r'[.\n]', text)
#     sentences = [s.strip() for s in sentences if len(s.split()) > 4]

#     return sentences[0] if sentences else "Not found in report"


# # ============================================================
# # MAIN HYBRID RAG ROUTER
# # ============================================================

# def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):
#     """
#     Hybrid QA system:
#     1) Try report RAG
#     2) If unrelated → Tavily web fallback
#     """

#     # STEP 1 — retrieve from vector DB
#     result = semantic_search(query=question, report_id=report_id, k=5)
#     documents = result.get("documents", [])

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(documents))

#     # STEP 2 — decide source
#     if _is_question_about_report(question, documents):
#         answer = _extract_answer_from_context(question, documents)
#         source = "report"
#     else:
#         print("🌐 Tavily fallback triggered")

#         tavily = get_platform_trends(question)

#         if tavily.get("success") and tavily.get("data"):
#             answer = tavily["data"][0].get("content", "No web result found")
#         else:
#             answer = "No information available"

#         source = "web"

#     if return_docs:
#         return answer, documents, source
#     return answer




# # ============================================================
# # VALIDATION (NO LONGER NEEDED — ALWAYS VALID)
# # ============================================================

# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     return False









# from services.embedding_service import semantic_search
# from services.tavily_client import get_platform_trends
# import re


# # ============================================================
# # INTENT DETECTION
# # ============================================================

# def _is_question_about_report(question: str, documents: list[str]) -> bool:
#     """
#     Detect whether the user is asking about the generated report.
#     """

#     if not documents:
#         return False

#     q = question.lower().strip()

#     report_keywords = [
#         "report",
#         "platform",
#         "topic",
#         "trend",
#         "trending",
#         "summary",
#         "analysis",
#         "sentiment",
#         "generated",
#         "this data",
#         "this result",
#     ]

#     if any(word in q for word in report_keywords):
#         return True

#     # loose similarity fallback
#     q_words = set(q.split())
#     doc_text = " ".join(documents).lower()
#     doc_words = set(doc_text.split())

#     return len(q_words.intersection(doc_words)) >= 1


# # ============================================================
# # ROBUST EXTRACTIVE QA (NO LLM)
# # ============================================================

# def _extract_answer_from_context(question: str, documents: list[str]) -> str:
#     """
#     Robust deterministic QA over report text.
#     Works even if chunks split lines.
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
#             r"platform\s+([a-z0-9 _-]+)"
#         ]

#         for p in patterns:
#             match = re.search(p, text, re.IGNORECASE)
#             if match:
#                 return match.group(1).strip().split("\n")[0]

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

#     # ---------- SUMMARY ----------
#     if "summary" in q:
#         for line in text.split("\n"):
#             if len(line.split()) > 8:
#                 return line.strip()

#     # ---------- GENERIC ----------
#     sentences = re.split(r'[.\n]', text)
#     sentences = [s.strip() for s in sentences if len(s.split()) > 6]

#     return sentences[0] if sentences else "Not found in report"


# # ============================================================
# # HYBRID RAG ROUTER
# # ============================================================

# def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

#     result = semantic_search(query=question, report_id=report_id, k=5)
#     documents = result.get("documents", [])

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(documents))

#     if _is_question_about_report(question, documents):
#         answer = _extract_answer_from_context(question, documents)
#         source = "report"
#     else:
#         print("🌐 Tavily fallback triggered")
#         tavily = get_platform_trends(question)

#         if tavily.get("success") and tavily.get("data"):
#             answer = tavily["data"][0].get("content", "No web result found")
#         else:
#             answer = "No information available"

#         source = "web"

#     if return_docs:
#         return answer, documents, source
#     return answer


# # ============================================================
# # ALWAYS VALID
# # ============================================================

# def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
#     return False




from services.embedding_service import semantic_search
from services.tavily_client import get_platform_trends
import re


# ============================================================
# RAG ROUTING DECISION (FINAL — RETRIEVAL BASED)
# ============================================================

def _is_question_about_report(documents: list[str]) -> bool:
    """
    Proper RAG routing:
    If vector DB retrieved chunks -> question belongs to report
    If nothing retrieved -> fallback to web
    """
    return bool(documents and len(documents) > 0)


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


# def _extract_answer_from_context(question: str, documents: list[str]) -> str:
#     """
#     Deterministic QA over report text.
#     Works even if chunks are fragmented.
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
#             r"platform\s+([a-z0-9 _-]+)"
#         ]
#         for p in patterns:
#             match = re.search(p, text, re.IGNORECASE)
#             if match:
#                 return match.group(1).strip().split("\n")[0]

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

#     # ---------- SUMMARY ----------
#     if "summary" in q:
#         for line in text.split("\n"):
#             if len(line.split()) > 8:
#                 return line.strip()

#     # ---------- GENERIC FALLBACK ----------
#     sentences = re.split(r'[.\n]', text)
#     sentences = [s.strip() for s in sentences if len(s.split()) > 6]

#     return sentences[0] if sentences else "Not found in report"


# ============================================================
# MAIN HYBRID RAG SYSTEM
# ============================================================


def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

    # STEP 1 — Retrieve context
    result = semantic_search(query=question, report_id=report_id, k=5)
    documents = result.get("documents", [])

    print("🔍 semantic_search report_id:", report_id)
    print("📄 documents found:", len(documents))

    # STEP 2 — Try extracting from report
    report_answer = _extract_answer_from_context(question, documents)

    # STEP 3 — Validate answer quality
    invalid_answers = [
        "",
        "not found in report",
        "unknown",
        "none",
        "n/a",
    ]

    is_valid_report_answer = (
        report_answer
        and report_answer.lower().strip() not in invalid_answers
        and len(report_answer.split()) <= 40   # prevents long random paragraphs
    )

    # STEP 4 — Decide source
    if is_valid_report_answer:
        print("📊 Answered from REPORT")
        final_answer = report_answer
        source = "report"

    else:
        print("🌐 Falling back to Tavily — report had no answer")

        tavily = get_platform_trends(question)

        if tavily.get("success") and tavily.get("data"):
            final_answer = tavily["data"][0].get("content", "No web result found")
        else:
            final_answer = "I couldn't find reliable information online."

        source = "web"

    if return_docs:
        return final_answer, documents, source
    return final_answer


# def answer_question_about_report(report_id: str, question: str, return_docs: bool = False):

#     result = semantic_search(query=question, report_id=report_id, k=5)
#     documents = result.get("documents", [])

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(documents))

#     # ---------- RAG ----------
#     if _is_question_about_report(documents):
#         answer = _extract_answer_from_context(question, documents)
#         source = "report"

#     # ---------- WEB FALLBACK ----------
#     else:
#         print("🌐 Tavily fallback triggered")
#         tavily = get_platform_trends(question)

#         if tavily.get("success") and tavily.get("data"):
#             answer = tavily["data"][0].get("content", "No web result found")
#         else:
#             answer = "No information available"

#         source = "web"

#     if return_docs:
#         return answer, documents, source
#     return answer


# ============================================================
# NOT USED ANYMORE (kept for compatibility)
# ============================================================

def is_rag_answer_insufficient(answer: str, documents: list) -> bool:
    return False
