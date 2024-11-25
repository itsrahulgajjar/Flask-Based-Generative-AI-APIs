import io
import slate3k as slate
from openai import OpenAIError
import google.generativeai as genai
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from flask import Flask, request, jsonify
from routes import (
    PARAGRAPH_HEADING_API,
    SUMMARY_API,
    TEXT_TO_SPEECH_API,
    SIMILAR_TEXT_API
)
from constants import (
    OPENAI_ERROR,
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_CONTAINER_NAME,
    SECURITY_KEY,
    GOOGLE_API_KEY,
    safety_config
)
from prompts import (
    PARAGRAPH_HEADING_PROMPT,
    MAP_CUSTOM_PROMPT,
    COMBINE_CUSTOM_PROMPT,
    SIMILAR_PARAGRAPH_PROMPT
)
from helpers import (
    download_blob,
    generate_and_upload_audio,
    remove_special_characters,
)


# Initialise flask app
app = Flask(__name__)
app.config['SECURITY_KEY'] = SECURITY_KEY

# Configuring Google API key
genai.configure(api_key=GOOGLE_API_KEY) 


# API to generate speech from text
@app.route(TEXT_TO_SPEECH_API, methods=["POST"])
def generate_speech():
    """
    API for Text-to-speech.

    Input:
        - JSON data in the request body.
        - Format:
            {
                "text": "input_text"
                "filename": "filename_for_audio"
            }

    Output:
        - JSON response containing the filename of uploaded file in Azure blob storage.
        - Format:
            {
                "file_name": "audio_file_name"
            }
    """
    
    # Verify Security key
    if 'Authorization' not in request.headers or request.headers['Authorization'] != app.config['SECURITY_KEY']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        text = data["text"]
        file_name = data["file_name"]
        
        # Remove special characters
        text = remove_special_characters(text)
        
        # Generate and upload audio file
        generate_and_upload_audio(text, file_name, app)
        
    except Exception as e:
        app.logger.error(f"Error in Generating Speech of text: {e}")
        return OPENAI_ERROR, 400
    
    app.logger.info("Audio file generated and uploaded to Azure blob storage.")
    return jsonify({'file_name': file_name}), 200


# API for Generate Heading for input paragraph
@app.route(PARAGRAPH_HEADING_API, methods=["POST"])
def generate_heading():
    """
    API for Generate Heading for input paragraph
    
    Input:
        - JSON data in the request body.
        - Format:
            {
                "paragraph": "input_paragraph"
            }
            
    Output:
        - JSON response containing the generated heading.
        - Format:
            {
                "heading": "generated_heading"
            }
    """
    
    # Verify Security key
    if 'Authorization' not in request.headers or request.headers['Authorization'] != app.config['SECURITY_KEY']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    
    data = request.get_json()
    paragraph = data["paragraph"]
    try:
        prompt = PARAGRAPH_HEADING_PROMPT.format(paragraph=paragraph)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt], safety_settings=safety_config)
        heading = response.candidates[0].content.parts[0].text.strip().replace("*", "").replace('"', "")
        app.logger.info("Heading generated for paragraph: %s", paragraph) 
        
    except OpenAIError as e:
        app.logger.error("Fact - %s & openai error %s", paragraph, str(e))
        return OPENAI_ERROR, 400
    
    app.logger.info("Paragraph-%s, feedback-%s", paragraph, response.prompt_feedback)
    return jsonify({"heading": heading}), 200


# API to get similar text from different paragraph
@app.route(SIMILAR_TEXT_API, methods=["POST"])
def similar_text():
    """
    Input:
    {
        "paragraph1": "paragraph1_text"
        "paragraph2": "paragraph2_text"
    }
    
    Output:
    {
        "similar_text": "generated_similar_text"
    }
    """
    
    # Verify Security key
    if 'Authorization' not in request.headers or request.headers['Authorization'] != app.config['SECURITY_KEY']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    paragraph1 = data["paragraph1"]
    paragraph2 = data["paragraph2"]

    system_prompt = SIMILAR_PARAGRAPH_PROMPT
    
    try: 
        messages = [
            SystemMessage(
                content=system_prompt
            ),
            HumanMessage(
                content=f"paragraph1 = {paragraph1}, paragraph2 = {paragraph2}",
            ),
        ]
        chat = ChatOpenAI(temperature=0, model="gpt-4o", max_tokens=2000)
        response = chat(messages)
        
    except OpenAIError as e:
        app.logger.error("Openai error - %s", str(e))
        return OPENAI_ERROR, 400
    
    return jsonify({"similar_text": response.content}), 200


# API for summary generation of whole pdf
@app.route(SUMMARY_API, methods=["POST"])
def judgement_summary():
    """
    API for Summary Generation of Whole pdf

    Input:
        - JSON data in the request body.
        - Format:
            {
                "file_name": "input_file_name",
            }
            
    Output:
        - JSON response containing the generated summary.
        - Format:
            {
                "summary": "generated_summary_text"
            }
            
    Error Handling:
        - Returns 400 status code with OPENAI_ERROR message in case of OpenAI API error.

    Dependencies:
        - Requires 'slate' library for PDF text extraction.
        - Requires 'ChatOpenAI', 'RecursiveCharacterTextSplitter', 'PromptTemplate', and 'load_summarize_chain'
          from the custom summarization module.
    """
    
    # Verify Security key
    if 'Authorization' not in request.headers or request.headers['Authorization'] != app.config['SECURITY_KEY']:
        return jsonify({'message': 'Unauthorized'}), 401 
    
    data = request.get_json()
    file_name = data["file_name"]

    try:
        text = ""
        pdf_content = download_blob(
            AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME, file_name
        )
        pdf_content_bytesio = io.BytesIO(pdf_content)
        text = slate.PDF(pdf_content_bytesio).text().replace("\t", " ")
        pdf_content_bytesio.close()        

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=7000, chunk_overlap=150
        )

        chunks = text_splitter.create_documents([text])

        # Prompts
        map_prompt_template = PromptTemplate(
            input_variables=["text"], template=MAP_CUSTOM_PROMPT
        )

        combine_prompt_template = PromptTemplate(
            template=COMBINE_CUSTOM_PROMPT, input_variables=["text"]
        )

        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            combine_prompt=combine_prompt_template,
            verbose=False,
        )

        summary = summary_chain.run(chunks)

    except OpenAIError as e:
        app.logger.error("file_name - %s & openai error %s", file_name, str(e))
        return OPENAI_ERROR, 400

    app.logger.info("Summary generated for %s", file_name)
    return jsonify({"summary": summary}), 200


if __name__ == "__main__":
    app.run(debug=True)