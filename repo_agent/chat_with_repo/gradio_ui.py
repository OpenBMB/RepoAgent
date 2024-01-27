import gradio as gr
import markdown

class GradioInterface:
    def __init__(self, respond_function):
        self.respond = respond_function
        self.cssa  =  """
                <style>
                        .outer-box {
                            border: 1px solid #333; /* 外框的边框颜色和大小 */
                            border-radius: 10px; /* 外框的边框圆角效果 */
                            padding: 10px; /* 外框的内边距 */
                        }

                        .title {
                            margin-bottom: 10px; /* 标题和内框之间的距离 */
                        }

                        .inner-box {
                            border: 1px solid #555; /* 内框的边框颜色和大小 */
                            border-radius: 5px; /* 内框的边框圆角效果 */
                            padding: 10px; /* 内框的内边距 */
                        }

                        .content {
                            white-space: pre-wrap; /* 保留空白符和换行符 */
                            font-size: 16px; /* 内容文字大小 */
                            height: 400px;
                            overflow: auto;
                        }
                    </style>
                    <div class="outer-box"">
        
        """
        self.cssb = """
                        </div>
                    </div>
                </div>
        """
        self.setup_gradio_interface()

    def wrapper_respond(self, msg_input, system_input):
        # 调用原来的 respond 函数
        msg, output1, output2, output3, code = self.respond(msg_input, system_input)
        output1 = markdown.markdown(str(output1))
        output2 = markdown.markdown(str(output2))
        code = markdown.markdown(str(code))
        output1 = (
                self.cssa
                +"""
                          <div class="title">Response</div>
                            <div class="inner-box">
                                <div class="content">
                """
                + str(output1)
                +"""
                        </div>
                    </div>
                </div>
                """
            )
        output2 = (
                self.cssa
                +"""
                          <div class="title">Embedding Recall</div>
                            <div class="inner-box">
                                <div class="content">
                """
                + str(output2)
                + self.cssb
            )
        code= (
                self.cssa
                +"""
                          <div class="title">Code</div>
                            <div class="inner-box">
                                <div class="content">
                """
                + str(code)
                +self.cssb
            )

        
        return msg, output1, output2, output3, code

    def setup_gradio_interface(self):
        with gr.Blocks() as demo:
            gr.Markdown("""
                # RepoAgent: Chat with doc
            """)
            with gr.Tab("main chat"):

                with gr.Row():
                    with gr.Column():
                        msg = gr.Textbox(label = "Question Input",lines = 4) 
                        system = gr.Textbox(label = "(Optional)insturction editing", lines = 4)
                        btn = gr.Button("Submit",scale=2)
                    
                    output1 = gr.HTML(self.cssa
                                      +"""
                                        <div class="title">Response</div>
                                            <div class="inner-box">
                                                <div class="content">
                                                这里是内框的文本内容，可以包含多行。
                                                换行符和空格都将被保留。
                                            """+self.cssb)
                with gr.Row():
                    with gr.Column():
                        # output2 = gr.Textbox(label = "Embedding recall")
                        output2 = gr.HTML(self.cssa
                                      +"""
                                        <div class="title">Embedding Recall</div>
                                            <div class="inner-box">
                                                <div class="content">
                                                这里是内框的文本内容，可以包含多行。
                                                换行符和空格都将被保留。
                                            """+self.cssb)
                    output3 = gr.Textbox(label = "key words")
                    code = gr.HTML(self.cssa
                                      +"""
                                        <div class="title">Code</div>
                                            <div class="inner-box">
                                                <div class="content">
                                                这里是内框的文本内容，可以包含多行。
                                                换行符和空格都将被保留。
                                            """+self.cssb)
           
            btn.click(self.wrapper_respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code])
            msg.submit(self.wrapper_respond, inputs = [msg, system], outputs = [msg, output1, output2, output3, code],scroll_to_output = True)  # Press enter to submit

        gr.close_all()
        demo.queue().launch(share=True,height = 800)

# 使用方法
if __name__ == "__main__":
    def respond_function(msg, system):
        # 这里实现您的响应逻辑
        RAG="""

        
        """
        return msg, RAG, "Embedding_recall_output", "Key_words_output", "Code_output"

    gradio_interface = GradioInterface(respond_function)
