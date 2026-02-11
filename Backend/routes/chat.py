




# from fastapi import APIRouter
# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import answer_question_about_report

# router = APIRouter()


# @router.post("/api/reports/chat")
# def chat_with_report(payload: ChatRequest):
#     try:
#         # 1️⃣ Get answer from RAG
#         answer = answer_question_about_report(
#             report_id=payload.report_id,
#             question=payload.question
#         )

#         if not answer:
#             answer = "I don’t have enough information in this report yet."

#         # 2️⃣ ✅ FIX APPLIED — user_id PASSED
#         save_chat_message(
#             user_id=payload.user_id,
#             report_id=payload.report_id,
#             question=payload.question,
#             answer=answer,
#             source="rag"
#         )

#         # 3️⃣ Return response
#         return {
#             "answer": answer,
#             "source": "rag"
#         }

#     except Exception as e:
#         return {
#             "answer": "An error occurred while answering the question.",
#             "error": str(e)
#         }


# @router.get("/api/reports/{report_id}/chat")
# def get_report_chat(report_id: str):
#     return get_chat_history(report_id)




# from fastapi import APIRouter
# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import answer_question_about_report
# from services.tavily_client import research_with_tavily

# router = APIRouter()


# @router.post("/api/reports/chat")
# def chat_with_report(payload: ChatRequest):
#     try:
#         # 1️⃣ RAG attempt (original behavior)
#         rag_answer = answer_question_about_report(
#             report_id=payload.report_id,
#             question=payload.question
#         )

#         source = "rag"
#         final_answer = rag_answer

#         # 2️⃣ SIMPLE insufficiency check (NO refactor needed)
#         if not rag_answer or len(rag_answer.strip()) < 40:
#             tavily_answer = research_with_tavily(payload.question)

#             if tavily_answer:
#                 final_answer = tavily_answer
#                 source = "tavily"

#         # 3️⃣ Final guard
#         if not final_answer:
#             final_answer = "I don’t have enough information to answer this yet."

#         # 4️⃣ Store chat (UNCHANGED)
#         save_chat_message(
#             user_id=payload.user_id,
#             report_id=payload.report_id,
#             question=payload.question,
#             answer=final_answer,
#             source=source
#         )

#         # 5️⃣ Return response
#         return {
#             "answer": final_answer,
#             "source": source
#         }

#     except Exception as e:
#         return {
#             "answer": "An error occurred while answering the question.",
#             "error": str(e)
#         }


# @router.get("/api/reports/{report_id}/chat")
# def get_report_chat(report_id: str):
#     return get_chat_history(report_id)



# from fastapi import APIRouter
# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import (
#     answer_question_about_report,
#     is_rag_answer_insufficient,
# )
# from services.tavily_client import research_with_tavily

# router = APIRouter()


# @router.post("/api/reports/chat")
# def chat_with_report(payload: ChatRequest):
#     try:
#         # 1️⃣ RAG attempt (IMPORTANT: return_docs=True)
#         rag_answer, documents = answer_question_about_report(
#             report_id=payload.report_id,
#             question=payload.question,
#             return_docs=True,
#         )

#         source = "rag"
#         final_answer = rag_answer

#         # 2️⃣ Decide fallback using REAL signal
#         if is_rag_answer_insufficient(rag_answer, documents):
#             tavily_answer = research_with_tavily(payload.question)

#             if tavily_answer:
#                 final_answer = tavily_answer
#                 source = "tavily"

#         # 3️⃣ Final guard
#         if not final_answer:
#             final_answer = "I couldn’t find a reliable answer yet."

#         # 4️⃣ Store chat
#         save_chat_message(
#             user_id=payload.user_id,
#             report_id=payload.report_id,
#             question=payload.question,
#             answer=final_answer,
#             source=source,
#         )

#         # 5️⃣ Return response
#         return {
#             "answer": final_answer,
#             "source": source,
#         }

#     except Exception as e:
#         return {
#             "answer": "An error occurred while answering the question.",
#             "error": str(e),
#         }


# @router.get("/api/reports/{report_id}/chat")
# def get_report_chat(report_id: str):
#     return get_chat_history(report_id)










# from fastapi import APIRouter
# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import (
#     answer_question_about_report,
#     is_rag_answer_insufficient,
# )
# from services.tavily_client import research_with_tavily

# router = APIRouter()





# @router.post("/api/reports/chat")
# def chat_with_report(payload: ChatRequest):
#     try:
#         # 1️⃣ RAG attempt (NEW RETURN FORMAT)
#         rag_answer, documents, source = answer_question_about_report(
#             report_id=payload.report_id,
#             question=payload.question,
#             return_docs=True,
#         )

#         final_answer = rag_answer
#         final_source = source   # "report" or "web"

#         # 2️⃣ Safety fallback (only if rag_service explicitly failed)
#         if not final_answer or final_answer.strip() == "Not found in report":
#             tavily_answer = research_with_tavily(payload.question)

#             if tavily_answer:
#                 final_answer = tavily_answer
#                 final_source = "tavily"

#         # 3️⃣ Final guard
#         if not final_answer:
#             final_answer = "I couldn’t find a reliable answer yet."
#             final_source = "none"

#         # 4️⃣ Store chat
#         save_chat_message(
#             user_id=payload.user_id,
#             report_id=payload.report_id,
#             question=payload.question,
#             answer=final_answer,
#             source=final_source,
#         )

#         # 5️⃣ Return response (FRONTEND SAFE FORMAT)
#         return {
#             "answer": final_answer,
#             "source": final_source,
#         }

#     except Exception as e:
#         print("CHAT ROUTE ERROR:", e)
#         return {
#             "answer": "An error occurred while answering the question.",
#             "source": "error",
#         }
# @router.get("/api/reports/{report_id}/chat")
# def get_report_chat(report_id: str):
#     try:
#         return get_chat_history(report_id)
#     except Exception as e:
#         print("CHAT HISTORY ERROR:", e)
#         return []
# ###working fine, no changes needed here








# from fastapi import APIRouter
# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import (
#     answer_question_about_report,
#     is_rag_answer_insufficient,
# )
# from services.tavily_client import research_with_tavily



from fastapi import APIRouter
from models.chat import ChatRequest
from services.chat_service import save_chat_message, get_chat_history
from services.rag_service import answer_question_about_report


router = APIRouter()


@router.post("/api/reports/chat")
def chat_with_report(payload: ChatRequest):
    try:
        # ask hybrid RAG
        answer, documents, source = answer_question_about_report(
            report_id=payload.report_id,
            question=payload.question,
            return_docs=True,
        )

        # 🔒 NORMALIZE SOURCE LABELS
        if source == "report":
            ui_source = "report"
        else:
            ui_source = "web"

        if not answer:
            answer = "I couldn’t find a reliable answer."
            ui_source = "none"

        # save chat history
        save_chat_message(
            user_id=payload.user_id,
            report_id=payload.report_id,
            question=payload.question,
            answer=answer,
            source=ui_source,
        )

        return {
            "answer": answer,
            "source": ui_source,
        }

    except Exception as e:
        print("CHAT ROUTE ERROR:", e)
        return {
            "answer": "An error occurred while answering the question.",
            "source": "error",
        }


# @router.post("/api/reports/chat")
# def chat_with_report(payload: ChatRequest):
#     try:
#         # rag_service is the ONLY decision maker
#         answer, documents, source = answer_question_about_report(
#             report_id=payload.report_id,
#             question=payload.question,
#             return_docs=True,
#         )

#         if not answer:
#             answer = "I couldn’t find a reliable answer."
#             source = "none"

#         # store chat
#         save_chat_message(
#             user_id=payload.user_id,
#             report_id=payload.report_id,
#             question=payload.question,
#             answer=answer,
#             source=source,
#         )

#         return {
#             "answer": answer,
#             "source": source,
#         }

#     except Exception as e:
#         print("CHAT ROUTE ERROR:", e)
#         return {
#             "answer": "An error occurred while answering the question.",
#             "source": "error",
#         }


@router.get("/api/reports/{report_id}/chat")
def get_report_chat(report_id: str):
    try:
        return get_chat_history(report_id)
    except Exception as e:
        print("CHAT HISTORY ERROR:", e)
        return []

