import os
import json
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


# ------------------------
# HARD-CODE YOUR API KEY HERE
# ------------------------
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text.strip()


def get_recommendations_from_resume(pdf_path: str) -> dict:
    resume_text = extract_text_from_pdf(pdf_path)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    # Define schema
    response_schemas = [
        ResponseSchema(
            name="career_path",
            description="List of 2–3 career options (job titles only)"
        ),
        ResponseSchema(
            name="courses",
            description="List of at most 5 relevant online courses with platforms"
        ),
        ResponseSchema(
            name="links",
            description="A list of URLs corresponding to the courses in the same order"
        ),
    ]

    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""
You are an expert career counselor.

Given this resume:

{resume_text}

Return only a JSON object with exactly these keys:
- "career_path": list of 2–3 career options (job titles only).
- "courses": list of up to 5 online courses (with platforms).
- "links": list of URLs to those courses in the same order as 'courses'.

{format_instructions}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)

    result = chain.run(resume_text=resume_text)
    return result


if __name__ == "__main__":
    pdf_path = "resume-3.pdf"
    output = get_recommendations_from_resume(pdf_path)
    print(json.dumps(output, indent=2))
