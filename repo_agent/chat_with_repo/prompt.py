from llama_index.core import ChatPromptTemplate, PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

# Query Generation Prompt
query_generation_prompt_str = (
    "You are a helpful assistant that generates multiple search queries based on a "
    "single input query. Generate {num_queries} search queries, one on each line, "
    "related to the following input query:\n"
    "Query: {query}\n"
    "Queries:\n"
)
query_generation_template = PromptTemplate(query_generation_prompt_str)

# Relevance Ranking Prompt
relevance_ranking_instruction = (
    "You are an expert relevance ranker. Given a list of documents and a query, your job is to determine how relevant each document is for answering the query. "
    "Your output is JSON, which is a list of documents. Each document has two fields, content and relevance_score. relevance_score is from 0.0 to 100.0. "
    "Higher relevance means higher score."
)
relevance_ranking_guideline = "Query: {query} Docs: {docs}"

relevance_ranking_message_template = [
    ChatMessage(content=relevance_ranking_instruction, role=MessageRole.SYSTEM),
    ChatMessage(
        content=relevance_ranking_guideline,
        role=MessageRole.USER,
    ),
]
relevance_ranking_chat_template = ChatPromptTemplate(
    message_templates=relevance_ranking_message_template
)

# RAG (Retrieve and Generate) Prompt
rag_prompt_str = (
    "You are a helpful assistant in repository Q&A. Users will ask questions about something contained in a repository. "
    "You will be shown the user's question, and the relevant information from the repository. Answer the user's question only with information given.\n\n"
    "Question: {query}.\n\n"
    "Information: {information}"
)
rag_template = PromptTemplate(rag_prompt_str)

# RAG_AR (Advanced RAG) Prompt
rag_ar_prompt_str = (
    "You are a helpful Repository-Level Software Q&A assistant. Your task is to answer users' questions based on the given information about a software repository, "
    "including related code and documents.\n\n"
    "Currently, you're in the {project_name} project. The user's question is:\n"
    "{query}\n\n"
    "Now, you are given related code and documents as follows:\n\n"
    "-------------------Code-------------------\n"
    "Some most likely related code snippets recalled by the retriever are:\n"
    "{related_code}\n\n"
    "-------------------Document-------------------\n"
    "Some most relevant documents recalled by the retriever are:\n"
    "{embedding_recall}\n\n"
    "Please note:   \n"
    "1. All the provided recall results are related to the current project {project_name}. Please filter useful information according to the user's question and provide corresponding answers or solutions.\n"
    "2. Ensure that your responses are accurate and detailed. Present specific answers in a professional manner and tone.\n"
    "3. The user's question may be asked in any language. You must respond **in the same language** as the user's question, even if the input language is not English.\n"
    "4. If you find the user's question completely unrelated to the provided information or if you believe you cannot provide an accurate answer, kindly decline. Note: DO NOT fabricate any non-existent information.\n\n"
    "Now, focusing on the user's query, and incorporating the given information to offer a specific, detailed, and professional answer IN THE SAME LANGUAGE AS the user's question."
)


rag_ar_template = PromptTemplate(rag_ar_prompt_str)
