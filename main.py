from langchain_google_genai import ChatGoogleGenrativeAI
from longchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

def main():
    LLM = ChatGoogleGenrativeAI(model="gemini-2.5-flash", 
                                temperature=0.7, max_output_tokens=1024)
    prompt=ChatPromptTemplate.from_messages([
        ("system","you are expert in data engineering"),
        ("Human", "what is Topic{topic} in data engineering?")
    ])
    chain =LLM | prompt
    topic = input("Enter the topic you want to know about: ")
    response = chain.invoke({"topic": "SPARK"})
    print(response.content)

if __name__ == "__main__":
    main()
