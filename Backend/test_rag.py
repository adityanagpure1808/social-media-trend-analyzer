
import warnings
warnings.filterwarnings("ignore")

# from services.rag_service import answer_question_about_report

# def test_rag():
#     report_id = "e34ac9ae-3810-4f8b-85ff-187f4bbf1d42"
#     question = "What are the most popular topics?"

#     answer = answer_question_about_report(report_id, question)
#     print("ANSWER:", answer)

# if __name__ == "__main__":
#     test_rag()


from services.rag_service import answer_question_about_report

def test_rag():
    # 🔴 REPLACE THIS WITH A REAL REPORT ID from database.db
    report_id = input("Enter report ID to test RAG: ").strip()

    question = "What are the most popular topics?"

    answer = answer_question_about_report(report_id, question)

    print("\n====================")
    print("QUESTION:", question)
    print("ANSWER:")
    print(answer)
    print("====================\n")


if __name__ == "__main__":
    test_rag()
