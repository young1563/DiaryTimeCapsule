# 개발 환경 설정
## 1. Dev Containers Extensions 사용
![Dev Containers Extension](Readme_Image/extension.png)

## 2. work directory(프로젝트 root 폴더) 이동
## 3. 명령 팔레트 열기
### windows: ctrl + shift + p
### mac: cmd + shift + p  
## 4. Dev Containers Extensions에서 Reopen in Container 클릭
![Dev Containers Options](Readme_Image/option.png)

---
<br>

---

# 브랜치 전략

0. 코드 병합은 팀장만 진행

1. main - 배포 가능 상태의 코드 유지

2. dev - 다음 배포를 위해 개발 중인 코드

3. feature/[front or back or ai]/[기능명] - 특정 기능 또는 작업을 개발 -> dev로 병합

4. release/[버전] - 배포 준비를 위한 브랜치