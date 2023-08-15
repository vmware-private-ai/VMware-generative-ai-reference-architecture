import argparse
import json
import gradio as gr
import requests

def http_bot(prompt):
    headers = {"User-Agent": "vLLM Client"}
    pload = {
        "prompt": prompt,
        "stream": False,
        "max_tokens": 200,
        "temperature": 0,
        "n": 1,
        "stop": ">",  # Stop generation character
    }
    response = requests.post(args.model_url,
                             headers=headers,
                             json=pload,
                             stream=True)

    for chunk in response.iter_lines(chunk_size=8192,
                                     decode_unicode=False,
                                     delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode("utf-8"))
            output = data["text"][0]
            yield output


def build_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# vLLM on Ray Serve: Prompt Completion Demo\n")
        inputbox = gr.Textbox(label="Input",
                              placeholder="Enter your prompt and press ENTER")
        outputbox = gr.Textbox(label="Output",
                               placeholder="Prompt completion from the model")
        inputbox.submit(http_bot, [inputbox], [outputbox])
    return demo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--model-url",
                        type=str,
                        default="http://:8000/generate")
    args = parser.parse_args()

    demo = build_demo()
    demo.queue(concurrency_count=100).launch(server_name=args.host,
                                             server_port=args.port,
                                             share=True)
