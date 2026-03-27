# Namuwiki Speedrun Game

나무위키를 기반으로 한 스피드런 게임입니다. 시작 페이지에서 목표 페이지로 내부 링크만 클릭하여 도달하세요!

## 기능

- Python Flask 서버
- 나무위키 raw API를 사용하여 내부 링크 파싱
- 웹 브라우저에서 실행되는 게임
- PWA 지원 (모바일 홈화면 추가 가능)
- Railway 배포 지원

## 설치 및 실행

1. 의존성 설치:
   ```
   pip install -r requirements.txt
   ```

2. 앱 실행:
   ```
   python app.py
   ```

3. 브라우저에서 http://localhost:5000 접속

## 배포

Railway에 배포하려면, 이 리포지토리를 Railway에 연결하세요. Procfile과 railway.toml이 포함되어 있습니다.

## 게임 규칙

- 시작 페이지와 목표 페이지를 설정합니다.
- 내부 링크만 클릭하여 목표 페이지에 도달하세요.
- 시간을 측정하여 스피드런을 즐기세요!