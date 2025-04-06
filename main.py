from flask import Flask, request, jsonify
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import gradio as gr

app = Flask(__name__)

class ContextWindow(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class MCPRequest(BaseModel):
    contexts: List[ContextWindow]
    query: str
    parameters: Optional[Dict[str, Any]] = None

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        mcp_request = MCPRequest(**data)

        # Process the contexts and query
        response = {
            "result": "Processed request",
            "contexts": [c.dict() for c in mcp_request.contexts],
            "query": mcp_request.query
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

from huggingface_hub import InferenceClient

def process_text(context, query):
    try:
        prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
        
        response = client.text_generation(
            prompt,
            model=model,
            max_new_tokens=100
        )
        return response
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Create Gradio interface
def create_gradio_ui():
    iface = gr.Interface(
        fn=process_text,
        inputs=[
            gr.Textbox(label="Context", lines=5),
            gr.Textbox(label="Query")
        ],
        outputs=gr.Textbox(label="Result"),
        title="MCP Interface"
    )
    return iface

if __name__ == '__main__':
    # Launch Gradio interface
    demo = create_gradio_ui()
    demo.launch(server_name="0.0.0.0", server_port=5000, share=False)