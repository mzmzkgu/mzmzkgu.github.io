# mzmzkgu.github.io

공모주·무한매수 투자 기록 도구와 사용 가이드, 투자 공부 기록을 올리는 투자 전용 Jekyll 사이트 (GitHub Pages).
어두운 배경 + 주황 포인트의 터미널 느낌 디자인.

## 구성
- `index.html` — 홈 (사이트 소개 + 앱 카드 2개 + 최신 글 5개)
- `posts.html` — 글 목록, `_posts/` — 글 (`.md`만 추가하면 자동 반영)
- `about.md` / `contact.md` / `privacy.md` — 소개 / 문의 / 개인정보 처리방침
- `_layouts/` — 공통 레이아웃(`default`, `post`), `assets/style.css` — 스타일
- `ads.txt` — Google AdSense 인증 파일 (루트에 있어야 함, 수정 금지)
- `index_old.html` — 이전 "프로젝트 데스크톱" 홈 백업 (사이트에는 배포되지 않음)
- 앱들(`/ipotracker`, `/infinityBuy`)은 각각 별도 저장소의 프로젝트 페이지

## 글 올리는 법
`_posts/YYYY-MM-DD-영문제목.md` 파일을 추가하면 끝.

```markdown
---
layout: post
title: "글 제목"
description: 목록에 보일 한두 줄 요약
tags: [투자, IPO]
---
본문을 마크다운으로 작성
```

태그에 `투자`, `IPO`, `무한매수` 중 하나가 있으면 글 아래에 "투자 권유 아님" 안내가 자동으로 붙는다.

## 로컬 미리보기
```
gem install jekyll jekyll-sitemap jekyll-feed webrick
jekyll serve
```

## 직접 채워야 할 곳
- `contact.md` — 이메일 주소를 실제 주소로 교체
- `about.md` — 본인 소개 2~3줄 추가
- `index.html`, `_posts/2026-10-23-site-guide.md` — 앱 설명을 실제 기능에 맞게 수정

## 애드센스
- 모든 페이지 `<head>`에 `google-adsense-account` 메타태그와 AdSense 스크립트가 들어 있음 (`_layouts/default.html`)
- `ads.txt`는 `https://mzmzkgu.github.io/ads.txt` 로 접근 가능해야 함
- 신청 전 체크: 글 10편 이상(각 1,000자 이상), 문의 이메일 교체, 소개 보강
