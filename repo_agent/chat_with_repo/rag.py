import json

from llama_index.llms.openai import OpenAI

from repo_agent.chat_with_repo.json_handler import JsonFileProcessor
from repo_agent.chat_with_repo.prompt import (
    query_generation_template,
    rag_ar_template,
    rag_template,
    relevance_ranking_chat_template,
)
from repo_agent.chat_with_repo.text_analysis_tool import TextAnalysisTool
from repo_agent.chat_with_repo.vector_store_manager import VectorStoreManager
from repo_agent.log import logger


class RepoAssistant:
    def __init__(self, api_key, api_base, db_path):
        self.db_path = db_path
        self.md_contents = []

        self.weak_model = OpenAI(
            api_key=api_key,
            api_base=api_base,
            model="gpt-4o-mini",
        )
        self.strong_model = OpenAI(
            api_key=api_key,
            api_base=api_base,
            model="gpt-4o",
        )
        self.textanslys = TextAnalysisTool(self.weak_model, db_path)
        self.json_data = JsonFileProcessor(db_path)
        self.vector_store_manager = VectorStoreManager(top_k=5, llm=self.weak_model)

    def generate_queries(self, query_str: str, num_queries: int = 4):
        fmt_prompt = query_generation_template.format(
            num_queries=num_queries - 1, query=query_str
        )
        response = self.weak_model.complete(fmt_prompt)
        queries = response.text.split("\n")
        return queries

    def rerank(self, query, docs):  # 这里要防止返回值格式上出问题
        response = self.weak_model.chat(
            response_format={"type": "json_object"},
            temperature=0,
            messages=relevance_ranking_chat_template.format_messages(
                query=query, docs=docs
            ),
        )
        scores = json.loads(response.message.content)["documents"]  # type: ignore
        logger.debug(f"scores: {scores}")
        sorted_data = sorted(scores, key=lambda x: x["relevance_score"], reverse=True)
        top_5_contents = [doc["content"] for doc in sorted_data[:5]]
        return top_5_contents

    def rag(self, query, retrieved_documents):
        rag_prompt = rag_template.format(
            query=query, information="\n\n".join(retrieved_documents)
        )
        response = self.weak_model.complete(rag_prompt)
        return response.text

    def list_to_markdown(self, list_items):
        markdown_content = ""

        # 对于列表中的每个项目，添加一个带数字的列表项
        for index, item in enumerate(list_items, start=1):
            markdown_content += f"{index}. {item}\n"

        return markdown_content

    def rag_ar(self, query, related_code, embedding_recall, project_name):
        rag_ar_prompt = rag_ar_template.format_messages(
            query=query,
            related_code=related_code,
            embedding_recall=embedding_recall,
            project_name=project_name,
        )
        response = self.strong_model.chat(rag_ar_prompt)
        return response.message.content

    def respond(self, message, instruction):
        """
        Respond to a user query by processing input, querying the vector store,
        reranking results, and generating a final response.
        """
        logger.debug("Starting response generation.")

        # Step 1: Format the chat prompt
        prompt = self.textanslys.format_chat_prompt(message, instruction)
        logger.debug(f"Formatted prompt: {prompt}")

        questions = self.textanslys.keyword(prompt)
        logger.debug(f"Generated keywords from prompt: {questions}")

        # Step 2: Generate additional queries
        prompt_queries = self.generate_queries(prompt, 3)
        logger.debug(f"Generated queries: {prompt_queries}")

        all_results = []
        all_documents = []

        # Step 3: Query the VectorStoreManager for each query
        for query in prompt_queries:
            logger.debug(f"Querying vector store with: {query}")
            query_results = self.vector_store_manager.query_store(query)
            logger.debug(f"Results for query '{query}': {query_results}")
            all_results.extend(query_results)

        # Step 4: Deduplicate results by content
        unique_results = {result["text"]: result for result in all_results}.values()
        unique_documents = [result["text"] for result in unique_results]
        logger.debug(f"Unique documents: {unique_documents}")

        unique_code = [
            result.get("metadata", {}).get("code_content") for result in unique_results
        ]
        logger.debug(f"Unique code content: {unique_code}")

        # Step 5: Rerank documents based on relevance
        retrieved_documents = self.rerank(message, unique_documents)
        logger.debug(f"Reranked documents: {retrieved_documents}")

        # Step 6: Generate a response using RAG (Retrieve and Generate)
        response = self.rag(prompt, retrieved_documents)
        chunkrecall = self.list_to_markdown(retrieved_documents)
        logger.debug(f"RAG-generated response: {response}")
        logger.debug(f"Markdown chunk recall: {chunkrecall}")

        bot_message = str(response)
        logger.debug(f"Initial bot_message: {bot_message}")

        # Step 7: Perform NER and queryblock processing
        keyword = str(self.textanslys.nerquery(bot_message))
        keywords = str(self.textanslys.nerquery(str(prompt) + str(questions)))
        logger.debug(f"Extracted keywords: {keyword}, {keywords}")

        codez, mdz = self.textanslys.queryblock(keyword)
        codey, mdy = self.textanslys.queryblock(keywords)

        # Ensure all returned items are lists
        codez = codez if isinstance(codez, list) else [codez]
        mdz = mdz if isinstance(mdz, list) else [mdz]
        codey = codey if isinstance(codey, list) else [codey]
        mdy = mdy if isinstance(mdy, list) else [mdy]

        # Step 8: Merge and deduplicate results
        codex = list(dict.fromkeys(codez + codey))
        md = list(dict.fromkeys(mdz + mdy))
        unique_mdx = list(set([item for sublist in md for item in sublist]))
        uni_codex = list(dict.fromkeys(codex))
        uni_md = list(dict.fromkeys(unique_mdx))

        # Convert to Markdown format
        codex_md = self.textanslys.list_to_markdown(uni_codex)
        retrieved_documents = list(dict.fromkeys(retrieved_documents + uni_md))

        # Final rerank and response generation
        retrieved_documents = self.rerank(message, retrieved_documents[:6])
        logger.debug(f"Final retrieved documents after rerank: {retrieved_documents}")

        uni_code = self.rerank(
            message, list(dict.fromkeys(uni_codex + unique_code))[:6]
        )
        logger.debug(f"Final unique code after rerank: {uni_code}")

        unique_code_md = self.textanslys.list_to_markdown(unique_code)
        logger.debug(f"Unique code in Markdown: {unique_code_md}")

        # Generate final response using RAG_AR
        bot_message = self.rag_ar(prompt, uni_code, retrieved_documents, "test")
        logger.debug(f"Final bot_message after RAG_AR: {bot_message}")

        return message, bot_message, chunkrecall, questions, unique_code_md, codex_md
