# mzmzkgu.github.io

공모주·무한매수 투자 기록 도구와 사용 가이드, 투자 공부 기록을 올리는 투자 전용 Jekyll 사이트 (GitHub Pages).
어두운 배경 + 주황 포인트의 터미널 느낌 디자인.

## 구성
- `index.html` — 홈 (사이트 소개 + 앱 카드 2개 + 최신 글 5개)
- `ipo.html`(`/ipo/`), `infinity.html`(`/infinity/`), `study.html`(`/study/`) — 분야별 글 목록, `posts.html` — 전체 글 목록
- `_data/sections.yml` — 상단 메뉴와 분야 정의 (분야를 추가하려면 여기 한 줄 + 목록 페이지 하나)
- `_posts/` — 글 (`.md`만 추가하면 자동 반영)
- `CLAUDE.md` — 글 작성 규칙(3줄 요약 등), `tools/check_tldr.py` — 3줄 요약 규칙 검사 (둘 다 사이트에는 배포되지 않음)
- `contact.md` / `privacy.md` — 소개·문의(합쳐진 페이지) / 개인정보 처리방침 (`about.html`은 `/about/` → `/contact/` 이동용)
- `market.html` — 마켓시그널 탭 (`/marketTraffic/signals.json`을 읽어 카드로 표시)
- `_layouts/` — 공통 레이아웃(`default`, `post`), `assets/style.css` — 스타일
- `ads.txt` — Google AdSense 인증 파일 (루트에 있어야 함, 수정 금지)
- `index_old.html` — 이전 "프로젝트 데스크톱" 홈 백업 (사이트에는 배포되지 않음)
- 앱들(`/ipotracker`, `/infinityBuy`)은 각각 별도 저장소의 프로젝트 페이지

## 글 올리는 법
`_posts/YYYY-MM-DD-영문제목.md` 파일을 추가하면 끝.

```markdown
---
layout: post
categories: [ipo]        # ipo(공모주 수익관리), infinity(무한매수법), study(공부요약)
title: "글 제목"
description: 목록에 보일 한두 줄 요약
tags: [투자, IPO]
---
도입 문단 (한 문단)

<div class="tldr" markdown="1">

## 3줄 요약

1. 첫 번째 핵심 (한 문장, 폰에서 한 줄에 들어가게 짧게)
2. 두 번째 핵심
3. 세 번째 핵심

</div>

## 첫 번째 소제목
본문을 마크다운으로 작성
```

**모든 글에는 도입 문단 바로 아래에 "3줄 요약"이 있어야 한다.** 쓰고 나서 `python3 tools/check_tldr.py`로 검사한다. 자세한 작성 규칙은 `CLAUDE.md`에 있다.

태그에 `투자`, `IPO`, `무한매수` 중 하나가 있으면 글 아래에 "투자 권유 아님" 안내가 자동으로 붙는다.

## 로컬 미리보기
```
gem install jekyll jekyll-sitemap jekyll-feed webrick
jekyll serve
```

## 직접 채워야 할 곳
- `contact.md` — 이메일 주소를 실제 주소로 교체
- `contact.md` — 본인 소개 2~3줄 추가
- `index.html` — 앱 카드 설명을 실제 기능에 맞게 수정

## 애드센스
- 모든 페이지 `<head>`에 `google-adsense-account` 메타태그와 AdSense 스크립트가 들어 있음 (`_layouts/default.html`)
- `ads.txt`는 `https://mzmzkgu.github.io/ads.txt` 로 접근 가능해야 함
- 신청 전 체크: 글 10편 이상(각 1,000자 이상), 문의 이메일 교체, 소개 보강
