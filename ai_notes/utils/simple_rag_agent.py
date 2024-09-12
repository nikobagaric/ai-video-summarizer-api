from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

local_llm = 'llama3'

llm = ChatOllama(model=local_llm, temperature=0)

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a highly organized assistant trained to take effective notes for academic purposes. 
Your goal is to extract key points, important concepts, and main ideas from the provided text, 
as if you were taking notes during a lecture or while reading a textbook. 
The input text can be from any subject, but your notes should be clear, concise, and well-structured for easy studying.
\n
Instructions:\n
1. Read the provided text carefully.\n
2. Identify key points, main ideas, and important concepts.\n
3. Break the notes into logical sections using bullet points or headings as needed.\n
4. Avoid unnecessary details, focusing only on the essential information that would be useful for studying or revision.\n
<|eot_id|><|start_header_id|>user<|end_header_id|>\n
Text to summarize as notes:\n\n
"{text}"\n
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
""",
    input_variables=["text"],
)

rag_chain = llm | prompt | StrOutputParser()

def summarize_text(text):
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    # Process each chunk and generate summarized notes
    summarized_notes = []
    for chunk in chunks:
        result = rag_chain.invoke({"text": chunk})
        summarized_notes.append(result)

    # Combine the summarized notes into a single output
    combined_notes = "\n\n".join(summarized_notes)
    return combined_notes