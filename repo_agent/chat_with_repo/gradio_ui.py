import gradio as gr

class GradioInterface:
    def __init__(self, respond_function):
        self.respond = respond_function
        self.setup_gradio_interface()

    def setup_gradio_interface(self):
        css="""
            .markdown-container:nth-of-type(2){
                max-height: 200px; /* 设置最大高度 */
                overflow-y: auto; /* 超出部分显示滚动条 */
            }

            .output-container:nth-of-type(5) {  
                max-height: 150px;
                overflow-y: auto;
            }
        """

        with gr.Blocks(css = css) as demo:
            gr.Markdown("""
                # RepoChat Test
                This is a test for retrieval repo 
            """)
            with gr.Row():
                with gr.Column(scale = 2):
                    msg = gr.Textbox(label = "Question Input")
                    gr.Markdown("### question") 
                    question = gr.Markdown(label = "qa")
                    with gr.Accordion(label = "Advanced options", open = False):
                        system = gr.Textbox(label = "System message", lines = 2, value = "A conversation between a user and an LLM-based AI assistant. The assistant gives helpful and honest answers.")
                    output1 = gr.Textbox(label = "RAG")

                with gr.Column(scale=1):
                    output2 = gr.Textbox(label = "Embedding recall")
                with gr.Column(scale=1):
                    output3 = gr.Textbox(label = "key words")
                    code = gr.Textbox(label = "code")
            
            btn = gr.Button("Submit")
            btn.click(self.respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code, question])
            msg.submit(self.respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code, question])  # Press enter to submit

        gr.close_all()
        demo.queue().launch(share=True)

# 使用方法
if __name__ == "__main__":
    def respond_function(msg, system):
        # 这里实现您的响应逻辑
        return msg, "RAG_output", "Embedding_recall_output", "Key_words_output", "Code_output", "QA_output"

    gradio_interface = GradioInterface(respond_function)
