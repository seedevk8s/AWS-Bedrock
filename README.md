# AWS Bedrock

## 개요

AWS Bedrock은 Amazon Web Services에서 제공하는 완전 관리형 서비스로, 다양한 고성능 기초 모델(Foundation Models, FM)을 API를 통해 쉽게 사용할 수 있게 해주는 서비스입니다. 생성형 AI 애플리케이션을 빠르게 구축하고 배포할 수 있도록 지원합니다.

## 주요 특징

### 1. 다양한 기초 모델 선택
- **AI21 Labs**: Jurassic-2 시리즈
- **Anthropic**: Claude 시리즈 (Claude 3 Opus, Sonnet, Haiku 등)
- **Cohere**: Command, Embed 시리즈
- **Meta**: Llama 2, Llama 3 시리즈
- **Stability AI**: Stable Diffusion (이미지 생성)
- **Amazon**: Titan 시리즈 (텍스트, 임베딩, 이미지)

### 2. 완전 관리형 서비스
- 인프라 관리 불필요
- 자동 스케일링
- 고가용성 보장
- AWS 보안 기준 적용

### 3. 데이터 프라이버시 및 보안
- 데이터는 모델 학습에 사용되지 않음
- VPC 내에서 실행 가능
- AWS IAM을 통한 세밀한 접근 제어
- 전송 중 및 저장 시 암호화

### 4. 커스터마이징 기능
- **Fine-tuning**: 자체 데이터로 모델 미세 조정
- **RAG (Retrieval-Augmented Generation)**: Knowledge Bases for Amazon Bedrock을 통한 지식 확장
- **Agents for Amazon Bedrock**: 다단계 작업을 수행하는 AI 에이전트 구축

## 주요 사용 사례

### 텍스트 생성 및 처리
- 콘텐츠 생성 (마케팅 카피, 블로그 포스트 등)
- 문서 요약
- 텍스트 분류 및 감성 분석
- 코드 생성 및 설명

### 대화형 AI
- 챗봇 및 가상 비서
- 고객 지원 자동화
- FAQ 시스템

### 검색 및 분석
- 의미론적 검색
- 문서 분석 및 인사이트 추출
- 질의응답 시스템

### 이미지 생성
- 마케팅 자료 생성
- 제품 디자인 프로토타이핑
- 창작 콘텐츠 제작

## 시작하기

### 사전 요구사항
- AWS 계정
- 적절한 IAM 권한
- AWS CLI 또는 SDK 설치

### 기본 사용 방법

#### 1. AWS Console에서 접근
1. AWS Management Console에 로그인
2. Amazon Bedrock 서비스로 이동
3. 원하는 모델에 대한 액세스 요청
4. Model access 승인 후 사용 가능

#### 2. AWS SDK를 통한 프로그래밍 방식 접근

**Python 예제 (Boto3)**
```python
import boto3
import json

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# Claude 모델 사용 예제
prompt = "AWS Bedrock이란 무엇인가요?"

body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
})

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=body
)

response_body = json.loads(response['body'].read())
print(response_body['content'][0]['text'])
```

**Node.js 예제 (AWS SDK v3)**
```javascript
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-1" });

const prompt = "AWS Bedrock이란 무엇인가요?";

const input = {
  modelId: "anthropic.claude-3-sonnet-20240229-v1:0",
  contentType: "application/json",
  accept: "application/json",
  body: JSON.stringify({
    anthropic_version: "bedrock-2023-05-31",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: prompt
      }
    ]
  })
};

const command = new InvokeModelCommand(input);
const response = await client.send(command);
const responseBody = JSON.parse(new TextDecoder().decode(response.body));
console.log(responseBody.content[0].text);
```

## Knowledge Bases for Amazon Bedrock

Knowledge Bases를 사용하면 자체 데이터로 기초 모델을 확장할 수 있습니다 (RAG 패턴).

### 주요 기능
- 데이터 소스 연결 (S3, 데이터베이스 등)
- 자동 벡터화 및 임베딩
- 의미론적 검색
- 모델 응답에 소스 인용 포함

## Agents for Amazon Bedrock

복잡한 다단계 작업을 자동으로 수행하는 AI 에이전트를 구축할 수 있습니다.

### 주요 기능
- 작업 계획 및 실행
- 외부 API 및 도구 통합
- 대화 상태 관리
- 자동 오류 처리 및 재시도

## 비용 구조

AWS Bedrock의 요금은 다음과 같이 책정됩니다:

- **On-Demand**: 처리한 입력/출력 토큰 수에 따라 과금
- **Provisioned Throughput**: 일정한 처리량이 필요한 경우 시간당 과금
- **모델 커스터마이징**: Fine-tuning 및 저장 비용 별도

*자세한 요금은 [AWS Bedrock 요금 페이지](https://aws.amazon.com/bedrock/pricing/)를 참조하세요.*

## 지원 리전

AWS Bedrock은 다음 리전에서 사용 가능합니다:
- 미국 동부 (버지니아 북부, 오하이오)
- 미국 서부 (오레곤)
- 아시아 태평양 (싱가포르, 도쿄, 서울)
- 유럽 (프랑크푸르트, 아일랜드, 런던)

*최신 지원 리전은 AWS 공식 문서를 확인하세요.*

## 제한 사항 및 모범 사례

### 제한 사항
- 모델별 최대 토큰 수 제한
- API 호출 속도 제한 (조정 가능)
- 특정 모델은 일부 리전에서만 사용 가능

### 모범 사례
1. **프롬프트 엔지니어링**: 명확하고 구체적인 지침 제공
2. **에러 처리**: 재시도 로직 및 예외 처리 구현
3. **비용 최적화**: 적절한 모델 선택 및 토큰 사용량 모니터링
4. **보안**: IAM 역할 및 정책을 통한 최소 권한 원칙 적용
5. **모니터링**: CloudWatch를 통한 사용량 및 성능 추적

## 참고 자료

- [AWS Bedrock 공식 문서](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock 사용자 가이드](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [AWS Bedrock API 레퍼런스](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [AWS Bedrock Workshop](https://github.com/aws-samples/amazon-bedrock-workshop)

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

기여를 환영합니다! Issue나 Pull Request를 자유롭게 제출해주세요.
