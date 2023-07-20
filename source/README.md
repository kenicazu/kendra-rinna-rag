# AWS Langchain
This repo provides a set of samples to work with [Langchain](https://github.com/hwchase17/langchain/tree/master) and Amazon Kendra. It currently has samples for working with a [Kendra retriever class](https://python.langchain.com/docs/modules/data_connection/retrievers/integrations/amazon_kendra_retriever) to execute a QA chain for SageMaker, Open AI and Anthropic providers. 

## Installing

Clone the repository
```bash
git clone https://github.com/aws-samples/amazon-kendra-langchain-extensions.git
```

Move to the repo dir
```bash
cd amazon-kendra-langchain-extensions
```

Move to the samples dir
```bash
cd kendra_retriever_samples
```

Install the dependencies

If you are using pip
```bash
pip install -r requirements.txt
```

If you are using Conda
```bash
conda env create -f environment.yml 
```

## Running samples
Ensure that the environment variables are set for the aws region, kendra index id and the provider/model used by the sample.
For example, for running the `kendra_chat_flan_xl.py` sample, these environment variables must be set: AWS_REGION, KENDRA_INDEX_ID
and FLAN_XL_ENDPOINT.

You can use commands as below to set the environment variables.
```bash
export AWS_REGION="<YOUR-AWS-REGION>"
export KENDRA_INDEX_ID="<YOUR-KENDRA-INDEX-ID>"
export FLAN_XL_ENDPOINT="<YOUR-SAGEMAKER-ENDPOINT-FOR-FLAN-T-XL>"
export FLAN_XXL_ENDPOINT="<YOUR-SAGEMAKER-ENDPOINT-FOR-FLAN-T-XXL>"
export OPENAI_API_KEY="<YOUR-OPEN-AI-API-KEY>"
export ANTHROPIC_API_KEY="<YOUR-ANTHROPIC-API-KEY>"
```

### Running samples from the streamlit app
The samples directory is bundled with an `app.py` file that can be run as a web app using streamlit. 

```bash
streamlit run app.py rinna
```

The above command will run the `kendra_chat_rinna` as the LLM chain.
