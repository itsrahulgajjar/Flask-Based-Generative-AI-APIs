# Heading generation prompt for paragraph
PARAGRAPH_HEADING_PROMPT = """
Generate a short, professional, and engaging heading (max 10 words) that captures the essence of the following paragraph:
{paragraph}
"""

# Map custom prompt for summary generation
MAP_CUSTOM_PROMPT = """
Summarize the following text into a concise and coherent paragraph without omitting key details:
{text}
Your response should be clear and professional.
"""

# Combine custom prompt for summary generation
COMBINE_CUSTOM_PROMPT = """
You are provided with multiple summary paragraphs generated from different parts of a document. Your task is to combine 
these summaries into a single, coherent, and concise summary that captures the essence of the entire document.
Here are the summaries:
{text}
Provide the combined summary in a single paragraph.
"""

# Prompt for generate similar text from different paragraph
SIMILAR_PARAGRAPH_PROMPT = """
You are tasked with identifying the similar or overlapping content between two provided paragraphs. Analyze the key ideas, 
phrases, or sentences that are common to both paragraphs and express the similarity in a concise and coherent manner.

Your output should:
1. Highlight the shared meaning or text between the two paragraphs.
2. Avoid introducing any new or unrelated information.
3. Be written clearly and professionally.

Proceed with the analysis for the paragraphs provided.
"""
