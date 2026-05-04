# HiSponsor 웹사이트

스폰서십 & 취업 정보 플랫폼

## 📁 파일 구조

```
hisponsor/
├── index.html          ← 홈페이지
├── job.html            ← 구인 정보 페이지
├── information.html    ← 정보 게시판
├── contact.html        ← 문의 페이지
├── style.css           ← 전체 디자인
├── posts/              ← AI 자동 생성 포스트 백업
├── scripts/
│   └── generate_post.py ← AI 자동 포스팅 스크립트
└── .github/
    └── workflows/
        └── auto-post.yml ← GitHub Actions 자동화
```

## 🔧 자주 수정하는 것들

### 색상 변경
`style.css` 파일 상단 `:root` 블록에서 색상 코드만 바꾸면 됩니다.

### 구인 공고 추가
`job.html`에서 `job-item` 블록을 복사해서 추가하세요.

### 정보글 추가
`information.html`에서 `post-full` 블록을 복사해서 추가하세요.

### 연락처 변경
`contact.html`에서 이메일, 카카오톡 링크를 수정하세요.

## 🤖 AI 자동 포스팅

GitHub Secrets에 `ANTHROPIC_API_KEY`를 설정하면
매주 월요일 자동으로 새 글이 올라갑니다.

## 📞 문의
roytry425@gmail.com
