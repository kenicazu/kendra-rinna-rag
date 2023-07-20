from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import sys
import json
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MAX_HISTORY_LENGTH = 5

def build_chain():
    region = "ap-northeast-1"
    kendra_index_id = "05f6c45e-53f6-48fb-878e-1a0624da6fb5"
    endpoint_name = "japanese-gpt-neox-3-6b-instruction-ppoEndpoint"

    class RinnaContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps(
                {
                    "instruction": "",
                    #"input": prompt.replace("\n", "<NL>"),
                    "prompt": prompt.replace("\n", "<NL>"),
                    **model_kwargs,
                }
            )
            print("prompt: ", prompt)
            return input_str.encode("utf-8")

        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            #return response_json.replace("<NL>", "\n")
            #print(response_json)
            return response_json["result"]

    content_handler = RinnaContentHandler()

    llm=SagemakerEndpoint(
            endpoint_name=endpoint_name, 
            region_name=region, 
            model_kwargs={
                "max_new_tokens": 256,
                "do_sample": True,
                "temperature" : 0.7,
                "repetition_penalty": 1.3,
            },
            content_handler=content_handler
        )

      
    retriever = AmazonKendraRetriever(
        index_id=kendra_index_id,
        region_name=region,
        top_k=3,
        credentials_profile_name=None,
        attribute_filter={
            "EqualsTo": {      
                "Key": "_language_code",
                "Value": {
                    "StringValue": "ja"
                    }
                }
        }
#        return_source_documents=True
    )

    prompt_template = """
システム: システムは資料から抜粋して質問に答えます。資料にない内容には答えず、正直に「わかりません」と答えます。

{context}

上記の資料に基づいて以下の質問について資料から抜粋して回答を生成します。資料にない内容には答えず「わかりません」と答えます。
ユーザー: {question}
システム:
"""
    PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context", "question"]
  )

    condense_qa_template = """
次のような会話とフォローアップの質問に基づいて、フォローアップの質問を独立した質問に言い換えてください。

フォローアップの質問: {question}
独立した質問:"""
    standalone_question_prompt = PromptTemplate.from_template(condense_qa_template)

    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=llm, 
    #     retriever=retriever, 
    #     condense_question_prompt=standalone_question_prompt, 
    #     return_source_documents=True, 
    #     combine_docs_chain_kwargs={"prompt":PROMPT})
    # return qa
    
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True,
        verbose=True,
    )
    return qa

# def run_chain(chain, prompt: str, history=[]):
#      return chain({"question": prompt, "chat_history": history})

def run_chain(chain, prompt: str):
  return chain(prompt)

if __name__ == "__main__":
    qa = build_chain()
    print(bcolors.OKBLUE + "こんにちは。何か質問はありますか？" + bcolors.ENDC)
    print(bcolors.OKCYAN + "質問して検索を開始してください: or CTRL-D to exit." + bcolors.ENDC)
    print(">", end=" ", flush=True)
    for query in sys.stdin:
        query = query.strip().lower().replace("new search:","")
        result = run_chain(qa, query)
        print(bcolors.OKGREEN + result['result'] + bcolors.ENDC)
        if 'source_documents' in result:
            print(bcolors.OKGREEN + 'Sources:')
        for d in result['source_documents']:
            print(d.metadata['source'])
        print(bcolors.ENDC)
        print(bcolors.OKCYAN + "Ask a question, start a New search: or CTRL-D to exit." + bcolors.ENDC)
        print(">", end=" ", flush=True)
    print(bcolors.OKBLUE + "Bye" + bcolors.ENDC)