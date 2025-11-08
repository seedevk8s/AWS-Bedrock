# AWS Bedrock 아키텍처

## 목차
1. [개요](#개요)
2. [아키텍처 다이어그램](#아키텍처-다이어그램)
3. [레이어별 상세 설명](#레이어별-상세-설명)
4. [데이터 흐름](#데이터-흐름)
5. [주요 구성 요소](#주요-구성-요소)
6. [보안 및 규정 준수](#보안-및-규정-준수)

## 개요

AWS Bedrock은 여러 계층으로 구성된 완전 관리형 Foundation Model 플랫폼입니다. 이 문서는 AWS Bedrock의 전반적인 아키텍처와 각 구성 요소 간의 상호작용을 설명합니다.

## 아키텍처 다이어그램

![AWS Bedrock Architecture](bedrock-architecture.svg)

## 레이어별 상세 설명

### 1. 클라이언트 애플리케이션 레이어 (Client Applications Layer)

AWS Bedrock을 사용하는 다양한 클라이언트 애플리케이션:

- **웹 애플리케이션**: 브라우저 기반 인터페이스
- **모바일 앱**: iOS/Android 네이티브 애플리케이션
- **백엔드 서비스**: 마이크로서비스 아키텍처
- **IoT 디바이스**: 엣지 컴퓨팅 디바이스
- **챗봇**: 대화형 AI 인터페이스
- **데이터 분석**: 비즈니스 인텔리전스 도구

### 2. API 게이트웨이 레이어 (API Gateway Layer)

AWS Bedrock API는 모든 클라이언트 요청의 진입점입니다:

**주요 기능:**
- **IAM 인증**: AWS Identity and Access Management를 통한 보안 인증
- **VPC 엔드포인트**: 프라이빗 네트워크를 통한 안전한 연결
- **CloudWatch 모니터링**: 실시간 로깅 및 메트릭 수집
- **엔드포인트**: `bedrock-runtime.{region}.amazonaws.com`

**API 유형:**
- `InvokeModel`: 단일 모델 추론 호출
- `InvokeModelWithResponseStream`: 스트리밍 응답
- `ListFoundationModels`: 사용 가능한 모델 목록
- `GetFoundationModel`: 모델 세부 정보 조회

### 3. 핵심 서비스 레이어 (Core Services Layer)

#### 3.1 Foundation Models (기초 모델)

AWS Bedrock이 제공하는 다양한 기초 모델:

| 제공사 | 모델 | 주요 용도 |
|--------|------|-----------|
| **Anthropic** | Claude 3 (Opus, Sonnet, Haiku) | 대화, 분석, 코드 생성 |
| **Amazon** | Titan (Text, Embeddings, Image) | 텍스트 생성, 임베딩, 이미지 생성 |
| **Meta** | Llama 3 | 오픈소스 기반 텍스트 생성 |
| **AI21 Labs** | Jurassic-2 | 고급 텍스트 생성 |
| **Cohere** | Command, Embed | 텍스트 생성 및 임베딩 |
| **Stability AI** | Stable Diffusion | 이미지 생성 및 편집 |

**모델 추론 엔진 (Model Inference Engine):**
- 토큰 처리 (Token Processing)
- 응답 생성 (Response Generation)
- 배치 처리 (Batch Processing)
- 스트리밍 지원 (Streaming Support)

#### 3.2 Knowledge Bases (지식 기반)

**RAG (Retrieval-Augmented Generation) 패턴 구현:**

- 자체 데이터로 모델 응답 향상
- 벡터 데이터베이스를 통한 의미론적 검색
- 소스 인용 및 출처 추적
- 실시간 데이터 업데이트

**구성 요소:**
```
데이터 소스 → 임베딩 → 벡터 DB → 검색 → 모델 컨텍스트
```

#### 3.3 Agents (에이전트)

**다단계 작업 자동화:**

- 복잡한 워크플로우 오케스트레이션
- 외부 API 및 도구 통합
- 대화 상태 관리
- 자동 오류 처리 및 재시도

**에이전트 실행 흐름:**
1. 사용자 요청 분석
2. 작업 계획 수립
3. 필요한 도구/API 호출
4. 결과 종합 및 응답

#### 3.4 Model Customization (모델 커스터마이징)

**Fine-tuning (미세 조정):**
- 도메인 특화 데이터로 모델 훈련
- 프라이빗 모델 엔드포인트
- 성능 최적화
- 비용 효율적인 배포

**지원 방법:**
- Continued Pre-training
- Fine-tuning with labeled data
- Custom model endpoints

#### 3.5 Guardrails (가드레일)

**콘텐츠 필터링 및 안전 제어:**

- 유해 콘텐츠 차단
- 민감 정보 필터링 (PII)
- 주제 제한 (Topic Filtering)
- 응답 검증 및 승인 워크플로우

**정책 유형:**
- Content filters
- Denied topics
- Word filters
- Sensitive information filters
- Contextual grounding checks

#### 3.6 Model Evaluation (모델 평가)

**성능 측정 및 비교:**

- 자동화된 평가 지표
- A/B 테스팅
- 모델 간 벤치마크
- 사용자 정의 평가 기준

**평가 메트릭:**
- Accuracy
- Latency
- Token efficiency
- Cost per request

#### 3.7 Prompt Management (프롬프트 관리)

**프롬프트 플로우 및 템플릿:**

- 재사용 가능한 프롬프트 템플릿
- 버전 관리
- A/B 테스팅
- 프롬프트 체이닝

### 4. 데이터 소스 및 통합 레이어 (Data Sources & Integration)

#### 4.1 Amazon S3
- 대용량 데이터 저장
- 문서, 이미지, 비디오 보관
- Knowledge Base 소스

#### 4.2 Vector Database (OpenSearch)
- 임베딩 벡터 저장
- 의미론적 검색
- 실시간 인덱싱

#### 4.3 Databases (RDS / DynamoDB)
- 구조화된 데이터
- 트랜잭션 데이터
- 메타데이터 관리

#### 4.4 External APIs (Lambda Functions)
- 써드파티 서비스 통합
- 커스텀 비즈니스 로직
- 실시간 데이터 조회

#### 4.5 Data Processing (ETL Pipelines)
- 데이터 변환 및 정제
- 배치 처리
- 실시간 스트리밍

#### 4.6 Training Data
- Fine-tuning 데이터셋
- 평가 데이터
- 벤치마크 데이터

### 5. 보안 및 규정 준수 레이어 (Security & Compliance)

#### 5.1 IAM & Access Control
- 세분화된 권한 관리
- 역할 기반 접근 제어 (RBAC)
- 서비스 간 신뢰 관계
- 임시 자격 증명

#### 5.2 VPC & Network Isolation
- 프라이빗 서브넷
- VPC 엔드포인트
- 네트워크 ACL
- 보안 그룹

#### 5.3 Encryption
- **전송 중 암호화**: TLS 1.2+
- **저장 시 암호화**: AWS KMS
- **키 관리**: 고객 관리형 키 (CMK) 지원

#### 5.4 CloudTrail Logging
- 모든 API 호출 로깅
- 감사 추적
- 규정 준수 보고
- 이상 탐지

#### 5.5 Data Privacy
- **학습 비사용 보장**: 고객 데이터는 모델 학습에 사용되지 않음
- **데이터 레지던시**: 리전별 데이터 격리
- **GDPR 준수**: EU 규정 준수
- **HIPAA 적격**: 의료 데이터 처리 가능

## 데이터 흐름

### 일반적인 요청 흐름

```
1. 클라이언트 → API Gateway
   ↓ (IAM 인증)

2. API Gateway → Bedrock Runtime
   ↓ (요청 라우팅)

3. Bedrock Runtime → Foundation Model
   ↓ (모델 추론)

4. Foundation Model → 응답 생성
   ↓

5. 응답 → 클라이언트
   (CloudWatch에 로깅)
```

### RAG (Knowledge Base) 흐름

```
1. 사용자 쿼리 → Knowledge Base
   ↓

2. 쿼리 임베딩 생성
   ↓

3. Vector DB 검색 (유사도 기반)
   ↓

4. 관련 문서 조회 (S3)
   ↓

5. 컨텍스트 + 쿼리 → Foundation Model
   ↓

6. 증강된 응답 생성
   (소스 인용 포함)
```

### Agent 실행 흐름

```
1. 복잡한 사용자 요청
   ↓

2. Agent가 작업 분해
   ↓

3. 필요한 도구 식별
   ↓

4. 순차적 도구 호출:
   - Lambda 함수
   - 외부 API
   - Knowledge Base
   - 다른 AWS 서비스
   ↓

5. 결과 종합 및 응답
```

## 주요 구성 요소

### 1. Bedrock Runtime

**책임:**
- 모델 호출 라우팅
- 토큰 제한 관리
- 응답 스트리밍
- 오류 처리

**API 작업:**
- `InvokeModel`
- `InvokeModelWithResponseStream`
- `ApplyGuardrail`

### 2. Bedrock Control Plane

**책임:**
- 모델 액세스 관리
- Fine-tuning 작업
- 평가 작업
- Knowledge Base 관리

**API 작업:**
- `CreateModelCustomizationJob`
- `CreateKnowledgeBase`
- `CreateAgent`
- `CreateGuardrail`

### 3. Model Endpoints

**특징:**
- On-demand 엔드포인트
- Provisioned Throughput
- 자동 스케일링
- 지연 시간 최적화

## 보안 및 규정 준수

### 규정 준수 인증

- **SOC 1, 2, 3**
- **ISO 27001, 27017, 27018**
- **PCI DSS**
- **HIPAA 적격**
- **GDPR 준수**

### 보안 모범 사례

1. **최소 권한 원칙**
   - IAM 정책으로 필요한 권한만 부여
   - 역할 기반 접근 제어 사용

2. **네트워크 격리**
   - VPC 엔드포인트 사용
   - 퍼블릭 인터넷 노출 최소화

3. **데이터 암호화**
   - 전송 중 TLS 사용
   - 저장 시 KMS 암호화

4. **모니터링 및 감사**
   - CloudWatch 메트릭 설정
   - CloudTrail 로깅 활성화
   - 이상 탐지 알림 구성

5. **Guardrails 활용**
   - 콘텐츠 필터링 정책 설정
   - PII 정보 자동 제거
   - 주제 제한 적용

## 성능 최적화

### 지연 시간 최적화

- **리전 선택**: 사용자와 가까운 리전 사용
- **Provisioned Throughput**: 예측 가능한 워크로드에 사용
- **응답 스트리밍**: 대규모 응답에 스트리밍 활용
- **캐싱**: 반복적인 쿼리 캐시 구현

### 비용 최적화

- **모델 선택**: 작업에 적합한 크기의 모델 선택
  - 간단한 작업: Claude Haiku, Titan Text Express
  - 복잡한 작업: Claude Opus, Claude Sonnet

- **토큰 관리**:
  - 프롬프트 최적화
  - 불필요한 컨텍스트 제거
  - max_tokens 파라미터 조정

- **배치 처리**:
  - 여러 요청을 그룹화
  - 비동기 처리 활용

## 모니터링 및 관찰성

### CloudWatch 메트릭

- **ModelInvocationLatency**: 모델 호출 지연 시간
- **ModelInputTokenCount**: 입력 토큰 수
- **ModelOutputTokenCount**: 출력 토큰 수
- **ModelInvocationClientErrors**: 클라이언트 오류
- **ModelInvocationServerErrors**: 서버 오류

### 로깅

- **API 호출 로그**: CloudTrail
- **애플리케이션 로그**: CloudWatch Logs
- **성능 로그**: X-Ray 트레이싱

## 확장성

### 자동 스케일링

AWS Bedrock은 완전 관리형 서비스로서 자동으로 스케일링됩니다:

- **On-Demand 모드**: 자동 스케일링, 사용량에 따른 과금
- **Provisioned Throughput**: 예약된 용량, 일정한 성능 보장

### 고가용성

- **다중 가용 영역**: 자동 장애 조치
- **리전 간 복제**: 재해 복구 계획
- **SLA**: 99.9% 가용성 보장

## 통합 패턴

### 1. 서버리스 패턴

```
API Gateway → Lambda → Bedrock → DynamoDB
```

- 완전 관리형 스택
- 자동 스케일링
- 사용량 기반 과금

### 2. 마이크로서비스 패턴

```
Application Load Balancer → ECS/EKS → Bedrock
```

- 컨테이너 기반 배포
- 서비스 메시 통합
- 수평 확장

### 3. 이벤트 기반 패턴

```
EventBridge → Lambda → Bedrock → SNS/SQS
```

- 비동기 처리
- 이벤트 기반 워크플로우
- 느슨한 결합

### 4. 배치 처리 패턴

```
S3 → Step Functions → Batch → Bedrock → S3
```

- 대용량 데이터 처리
- 오케스트레이션
- 오류 처리 및 재시도

## 사용 사례별 아키텍처

### 챗봇 아키텍처

```
사용자 → WebSocket API → Lambda → Bedrock (Claude)
                                    ↓
                                DynamoDB (세션 관리)
```

### RAG 기반 Q&A 시스템

```
문서 → S3 → Lambda → Bedrock (Titan Embeddings)
                       ↓
                  OpenSearch
                       ↓
사용자 쿼리 → Knowledge Base → Bedrock (Claude) → 응답
```

### 이미지 생성 파이프라인

```
사용자 프롬프트 → API Gateway → Lambda → Bedrock (Stable Diffusion)
                                           ↓
                                        S3 (이미지 저장)
                                           ↓
                                   CloudFront (배포)
```

## 결론

AWS Bedrock의 아키텍처는 다음과 같은 핵심 원칙을 기반으로 설계되었습니다:

1. **완전 관리형**: 인프라 관리 불필요
2. **확장 가능**: 자동 스케일링 및 고가용성
3. **보안**: 다층 보안 및 규정 준수
4. **유연성**: 다양한 모델 및 커스터마이징 옵션
5. **통합성**: AWS 서비스 및 써드파티 도구와의 원활한 통합

이러한 아키텍처를 통해 개발자는 생성형 AI 애플리케이션을 빠르고 안전하게 구축하고 배포할 수 있습니다.

## 다음 단계

- [빠른 시작 가이드](02-quickstart.md) (예정)
- [모델 선택 가이드](03-model-selection.md) (예정)
- [보안 모범 사례](04-security-best-practices.md) (예정)
- [비용 최적화 전략](05-cost-optimization.md) (예정)

## 참고 자료

- [AWS Bedrock 공식 문서](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock API 참조](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
