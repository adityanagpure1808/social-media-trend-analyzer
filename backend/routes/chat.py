










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



router = APIRouter()


@router.post("/api/reports/chat")
def chat_with_report(payload: ChatRequest):
    from services.rag_service import answer_question_about_report
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

