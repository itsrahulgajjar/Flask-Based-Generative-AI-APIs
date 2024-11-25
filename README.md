# **Flask-Based Generative AI APIs**

This project provides a set of APIs leveraging Flask, Generative AI models, and other tools to perform tasks such as text-to-speech generation, summarization of documents, heading generation for paragraphs, and identifying similar content between text segments.

## **Features**
1. **Text-to-Speech API**
   - Converts input text into an audio file and uploads it to Azure Blob Storage.

2. **Paragraph Heading API**
   - Generates a concise heading for a given input paragraph using AI-based models.

3. **Similar Text API**
   - Finds similarities between two input paragraphs and generates text reflecting the similarity.

4. **Judgement Summary API**
   - Extracts text from a PDF and generates a concise summary using AI-driven summarization techniques.

---

## **Technologies Used**
- **Python**: Core language for the project.
- **Flask**: Web framework for creating APIs.
- **OpenAI**: For Generative AI tasks like text summarization.
- **Google Generative AI**: Used for generating headings and similar text.
- **Azure Blob Storage**: For storing generated audio files.
- **Slate3k**: For extracting text from PDF files.

---

## **Setup and Installation**

### **Pre-requisites**
- Python 3.8+
- Azure Storage account with a configured container.
- API keys for OpenAI and Google Generative AI.

### **Steps**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   .\.env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables for:
   - `OPENAI_API_KEY`
   - `GOOGLE_API_KEY`
   - `AZURE_STORAGE_CONNECTION_STRING`
   - `AZURE_CONTAINER_NAME`
   - `AZURE_CONTAINER_NAME_AUDIO_SUMMARY`
   - `AUDIO_PATH`
   - `SECURITY_KEY`

5. Run the application:
   ```bash
   python app.py
   ```

---

## **API Endpoints**

### 1. **Text-to-Speech API**
- **Endpoint**: `/text-to-speech`
- **Method**: `POST`
- **Input**:
  ```json
  {
      "text": "Your text here",
      "file_name": "audio_file_name"
  }
  ```
- **Output**:
  ```json
  {
      "file_name": "uploaded_audio_file_name"
  }
  ```

### 2. **Paragraph Heading API**
- **Endpoint**: `/generate-heading`
- **Method**: `POST`
- **Input**:
  ```json
  {
      "paragraph": "Your paragraph here"
  }
  ```
- **Output**:
  ```json
  {
      "heading": "Generated heading"
  }
  ```

### 3. **Similar Text API**
- **Endpoint**: `/similar-text`
- **Method**: `POST`
- **Input**:
  ```json
  {
      "paragraph1": "First paragraph",
      "paragraph2": "Second paragraph"
  }
  ```
- **Output**:
  ```json
  {
      "similar_text": "Generated similar text"
  }
  ```

### 4. **Judgement Summary API**
- **Endpoint**: `/summary`
- **Method**: `POST`
- **Input**:
  ```json
  {
      "file_name": "uploaded_file_name.pdf"
  }
  ```
- **Output**:
  ```json
  {
      "summary": "Generated summary"
  }
  ```

---

## **Error Handling**
- **Unauthorized Access**: Returns a `401 Unauthorized` response if the `Authorization` header is invalid.
- **API Errors**: Returns a `400 Bad Request` with a predefined error message.