from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

def main():
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",
                                 temperature=0.7, max_output_tokens=1024)
    prompt=ChatPromptTemplate.from_messages([
        ("system","you are expert in data engineering"),
        ("human", "what is Topic {topic} in data engineering?")
    ])
    chain = prompt | llm
    topic = input("Enter the topic you want to know about: ")
    response = chain.invoke({"topic": topic})
    print(response.content[0].get("text"))

if __name__ == "__main__":
    main()
