# 🌿 Dr. Green: AI 기반 식물 질병 진단 풀스택 웹 서비스

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-ResNet50-EE4C2C?logo=pytorch)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-green)

> **"식물의 주치의, Dr. Green"** > 딥러닝(ResNet50)을 활용하여 38종의 식물 질병을 정밀 진단하고, 질병별 맞춤형 솔루션을 실시간으로 제공하는 End-to-End 웹 애플리케이션입니다.

---

## 📖 목차 (Table of Contents)
1. [프로젝트 개요 (Overview)](#-프로젝트-개요-overview)
2. [시스템 아키텍처 (System Architecture)](#-시스템-아키텍처-system-architecture)
3. [핵심 기술 및 개발 내용 (Key Features)](#-핵심-기술-및-개발-내용-key-features)
4. [AI 모델 성능 (Model Performance)](#-ai-모델-성능-model-performance)
5. [기술적 챌린지 및 해결 (Troubleshooting)](#-기술적-챌린지-및-해결-troubleshooting)
6. [설치 및 실행 가이드 (Installation)](#-설치-및-실행-가이드-installation)

---

## 🧐 프로젝트 개요 (Overview)

### 📅 개발 배경
최근 홈 가드닝(Home Gardening) 시장이 급성장하고 있으나, 비전문가들은 식물의 잎만 보고 질병을 파악하기 어렵습니다. 잘못된 진단은 식물의 고사를 초래하므로, **누구나 쉽게 사용할 수 있는 AI 기반 진단 솔루션**의 필요성을 느껴 본 프로젝트를 기획하였습니다.

### 🎯 목표
* **정확성**: 38개 클래스(질병/정상)에 대해 85% 이상의 분류 정확도 달성
* **실용성**: 단순 진단을 넘어 구체적인 **대처 방안(방제법, 관리법)** 제공
* **확장성**: 추후 모바일 앱으로 확장이 용이한 RESTful API 기반 백엔드 구축

---

## 🏗 시스템 아키텍처 (System Architecture)

본 서비스는 **Model-View-Controller (MVC)** 패턴을 변형한 3-Tier 아키텍처를 따릅니다.

```mermaid
graph LR
    A[User (Client)] -- Image Upload --> B(React Frontend)
    B -- REST API (POST /analyze) --> C{FastAPI Backend}
    C -- Image Processing --> D[PyTorch Model (ResNet50)]
    D -- Prediction Result --> C
    C -- Query Solution --> E[(JSON Database)]
    E -- Solution Data --> C
    C -- JSON Response --> B
    B -- Result Display --> A
