import boto3


bedrock_agent_runtime = boto3.client(service_name="bedrock-agent-runtime")




def retrieve(query, kbId, numberOfResults=5):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery={"text": query},
        knowledgeBaseId=kbId,
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": numberOfResults}
        },
    )




if __name__ == "__main__":
    response = retrieve(
        query="서울시 온실가스 저감 정책은?",
        kbId="2WS5SBEUKI",                  # 본인의 지식 베이스 ID로 변경
    )
    results = response["retrievalResults"]
    print(results)