# 💰Loan Product Recommendation System 💰
#### 20-30대 사회초년생을 위한 사용자 맞춤 대출상품 추천시스템

---

## 😎 Team

심재혁(팀장) : EDA & 데이터 생성, 웹 애플리케이션 개발

박지원 : EDA & 데이터 생성 , flan-T5 fine tuning , 웹 애플리케이션 개발

이소정 : EDA & 데이터 생성, flan-T5 fine tuning 

박혜원 : EDA & 데이터 생성, Feature Engineering

백지연 : EDA & 데이터 생성, 연관분석, Zero shot modeling(Reverse Inference) , 웹 애플리케이션 개발

---

## 🪜Introduction
현재 시장에는 다양한 대출 상품들이 존재하며, 대출 신청자는 각자의 경제적 상황에 맞는 적합한 상품을 선택해야 합니다. 

그러나 대출 상품이 너무 많고, 신청자의 상황에 따라 어떤 상품이 적합한지 판단하는 것이 어렵습니다.

이 프로젝트는 신청자가 자신의 정보를 입력하면, LLM(대형 언어 모델)을 활용하여 그에 맞는 대출 상품을 추천하는 챗봇 시스템을 구현합니다. 

이를 통해 사용자는 빠르고 정확한 대출 상품 추천을 받을 수 있습니다.

---

## 💾 Dataset
1. 신청자 정보 데이터 ( $M_u$ ): kaggle에서 제공된 Financial Risk for Loan Approval
2. 대출상품 정보 as Product Metadata ( $M_i$ ) : 금융감독원에서 제공된 대출상품 데이터를 활용합니다. (제1금융권)
   
   대출상품은 주택담보대출, 전세자금대출, 개인신용대출 총 3가지 종류의 대출 상품을 추천합니다.
---

## 📖 참고 논문
[Leveraging LLM Reasoning Enhances Personalized Recommender Systems
](https://arxiv.org/abs/2408.00802)

--- 

## 📦 Architecture

- **📂 eda**
   - **EDA_VariableSelection_HW.ipynb**
  
- **📂 연관분석**
  - **20-30대연관분석다운샘플링.ipynb** 

- **📂 dataset**
  - **Preprocessing_HW.ipynb**
  - **reasoning_generator.ipynb**

- **📂 역추론**
  - **llm역추론찐최종코드.ipynb**
 
- **📂추천 챗봇**
  - **streamlit_demo.py**

## 📑Project Summary

### 1) EDA & Scaling & 연관분석

EDA 및 연관분석을 진행하고, 대출 승인 여부와 높은 상관도를 가진 변수를 선별합니다.

대출 상품 데이터는 한국 금융 대출 상품이기 때문에,미국 신용점수 범위(300 ~ 850)를 한국 신용점수(KCB 기준) 범위(350 ~ 1,000)로 변환합니다.

또한 소수 클래스 수에 맞춰 다운샘플링을 진행합니다.

### 2) reasoning &  생성

신청자 정보와 대출 상품 데이터를 결합하여 새로운 조합을 생성합니다. 이 과정에서는 각 대출 상품에 대해 대출 승인 여부를 예측하는 목표 평점을 산출하고, 해당 예측에 대한 이유를 생성합니다. 

이를 통해 각 대출 상품에 대한 추천 시스템 구축을 위한 학습 데이터로 활용하게 됩니다.

이 단계에서 생성되는 'Reason'은 대출 승인 여부를 예측한 근거를 명확히 하여, 모델의 설명 가능성을 높이는 데 기여합니다.

### 3) 역추론

앞서 생성된 'Reason'이 실제로 유효한지 검증하는 역추론 과정을 진행합니다. 이를 위해 Zero-shot GenAI 모델을 활용하여, 생성된 'Reason'을 입력값으로 주고 실제 목표 평점과 일치하는 예측값을 도출하는지 확인합니다. 

이 과정을 통해 생성된 이유가 실제로 대출 승인 여부를 잘 설명하는지 검증하며, 이를 바탕으로 모델의 신뢰성을 평가합니다. 

최종적으로, 역추론 과정에서 정확히 예측된 데이터만을 선별하여 최종 데이터셋에 포함시키며, 이를 통해 모델의 품질과 신뢰도를 높입니다.

### 4) Modeling
사용 모델 : flan-T5-small
- sequence classification head가 있는 T5ForSequenceClassification 이용
- 


### 5) chat bot 

1️⃣앞서 생성한 모델을 활용하여 예측 평점 및 승인 여부를 예측합니다.

2️⃣ TOP-3 상품에 대한 예측 평점과 해당 상품들의 데이터를 예측 평점 기준 내림차순 정렬하여 추천 상품을 결정합니다.

3️⃣ 신청자 정보를 context로 주어 LLM에게 고객에게 내어줄 메세지를 생성하도록 합니다.
