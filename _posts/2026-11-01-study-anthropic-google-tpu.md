---
layout: post
categories: [study]
title: "[구글][앤트로픽] TPU와 투자금으로 서로 구속되어 있고 TPU 사용량 늘리는 중 (ft. 메르)"
description: 메르의 블로그 글을 읽고 정리한 공부요약입니다. 앤트로픽이 엔비디아 GPU보다 구글 TPU 계약에 더 묶여 있는 이유와, 투자금 때문에 TPU 사용량을 늘리는 상황을 정리했습니다.
tags: [메르의블로그, 앤트로픽, TPU, 구글, 브로드컴, AI]
---

<div class="tldr" markdown="1">

## 3줄 요약

1. TPU가 GPU보다 30~40% 저렴
2. 구글이 앤트로픽에 400억불 투자
3. 앤트로픽은 TPU 메인, GPU 서브

</div>

### [앤트로픽과 구글(TPU)]

- 엔비디아(GPU)보다 <span class="red">구글(TPU) 계약 더 구속적</span>
- GPU는 범용, <span class="red">TPU는 AI 연산 특화용</span>으로 좋음
- 앤트로픽이 TPU 픽한 건 돈 문제 때문으로 보임

### [TPU 장점 : 저렴하고 AI성능 특화]

- 제품가, 연산비용 모두 TPU가 30~40% 저렴
- 그리고 AI는 학습+추론 비용이 드는데
- 요즘 <span class="red">에이전틱AI 늘면서 '추론(TPU)'</span> 더 필요
- 앤트로픽은 추론 성능 관점에서 TPU 좋음

### [앤트로픽은 투자금 때문에라도 구속됨]

- 구글은 앤트로픽에 400억 달러 투자했음
- 추가 투자금 받으려면 <span class="red">TPU 일정 이상 써줘야만</span> 함
- 브로드컴과도 전환사채 형태로 투자금 받는 중
- (브로드컴 : 구글 TPU를 생산해주는 중)
- 반대로 스페이스X(GPU)는 언제든 해지 가능상태

### [메르님 의견]

- 앤트로픽은 <span class="red">싸고 효율 좋은 TPU를 메인</span>으로 쓰고
- 스페이스X<span class="red">(GPU)는 서브</span>로 두려는 모습
- GPU, TPU 모두 HBM 쓰이니 삼전닉스는 다 좋음

<hr>

요즘 AI 기업들은 칩 메이커들과 서로 엮여있음<br>
앤트로픽(TPU), 오픈AI(GPU)...<br>
그리고 이런 특수성을 생각해서 구글 수량 조금씩 늘리기 시작한건데 ㅋㅋ 아 물렸네... 이후에도 돈 생길 때마다 조금씩 사줘야지

### 출처 : 「앤트로픽은 왜 구글 TPU를 썼을까?」
{: .src}

원문 : [메르의 블로그](https://m.blog.naver.com/ranto28/224461024209)<br>
내 블로그 : [멍멍짱구 작업실](https://m.blog.naver.com/kgu3405/)
