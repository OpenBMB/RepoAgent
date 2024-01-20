import gradio as gr
import markdown

class GradioInterface:
    def __init__(self, respond_function):
        self.respond = respond_function
        self.setup_gradio_interface()

    def wrapper_respond(self, msg_input, system_input):
        # 调用原来的 respond 函数
        msg, output1, output2, output3, code, question = self.respond(msg_input, system_input)
        output1 = markdown.markdown(str(output1))
        output2 = markdown.markdown(str(output2))
        code = markdown.markdown(str(code))
        output1 = (
                "<div style='border: 1px solid white;max-width:100%; max-height:400px; overflow:auto'>"
                +"<h1>RAG</h1>"
                + str(output1)
                + "</div>"
            )
        output2 = (
                "<div style='border: 1px solid white;max-width:100%; max-height:650px; overflow:auto'>"
                +"<h1>Embedding Recall</h1>"
                + str(output2)
                + "</div>"
            )
        code = (
                "<div style='border: 1px solid white;max-width:100%; max-height:540px; overflow:auto'>"
                +"<h1>Code</h1>"
                + str(code)
                + "</div>"
            )
        
        return msg, output1, output2, output3, code, question

    def setup_gradio_interface(self):
        with gr.Blocks() as demo:
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
                    output1 = gr.HTML("""
                                      
                    <div style='border: 1px solid white; max-width: 100%; height: 400px; overflow: auto; padding: 10px;'>
                    <h1>RAG</h1>
                    </div>
                                          """)

                with gr.Column(scale=1):
                    # output2 = gr.Textbox(label = "Embedding recall")
                    output2 = gr.HTML("""
                                          
                    <div style='border: 1px solid white;max-width:100%; height:650px; overflow:auto'>
                    <h1>Embedding Recall</h1>
                    </div>
                                          """)
                with gr.Column(scale=1):
                    output3 = gr.Textbox(label = "key words")
                    code = gr.HTML("""
                                          
                    <div style='border: 1px solid white;max-width:100%; height:540px; overflow:auto'>
                    <h1>Code</h1>
                    </div>
                                          """)
            btn = gr.Button("Submit")
            btn.click(self.wrapper_respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code, question])
            msg.submit(self.wrapper_respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code, question])  # Press enter to submit

        gr.close_all()
        demo.queue().launch(share=True)

# 使用方法
if __name__ == "__main__":
    def respond_function(msg, system):
        # 这里实现您的响应逻辑
        return msg, "RAG_output", "Embedding_recall_output", "Key_words_output", "Code_output", "QA_output"

    gradio_interface = GradioInterface(respond_function)
