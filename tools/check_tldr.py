#!/usr/bin/env python3
"""모든 글(_posts/*.md)이 '3줄 요약' 규칙을 지키는지 검사한다.
공부요약(categories: [study]) 글은 '출처' 형식도 함께 검사한다.

규칙
  1. 도입 문단 바로 다음에 <div class="tldr" markdown="1"> 블록이 있다.
     (공부요약 글처럼 본문이 3줄 요약으로 바로 시작하는 것도 허용한다.)
  2. 블록 안에 '## 3줄 요약' 제목과 번호 목록 3개가 있다.
  3. 각 줄은 폰(360px)에서 한 줄에 들어가도록 짧다. (한글 1글자 = 1.0 기준 15.5 이하)

사용법:  python3 tools/check_tldr.py          # 전체 글 검사
         python3 tools/check_tldr.py 글.md   # 특정 글만 검사
"""
import glob, re, sys

LIMIT = 15.5  # 360px 폰에서 한 줄에 들어가는 폭(실측으로 보정한 값)
SRC_LIMIT = 20.6  # 출처 제목(14px)이 360px 폰에서 한 줄에 들어가는 폭(실측으로 보정한 값)


def units(text):
    u = 0.0
    for ch in text:
        if '가' <= ch <= '힣' or 'ㄱ' <= ch <= 'ㆎ' or '一' <= ch <= '鿿':
            u += 1.0
        elif ch == ' ':
            u += 0.32
        elif ch.isdigit():
            u += 0.58
        elif ch.isascii() and ch.isalpha():
            u += 0.66
        elif ch in '×·~+-/%':
            u += 0.62
        else:
            u += 0.38
    return u


def check_source(s):
    """공부요약 글 맨 아래 출처 블록 형식:

        ### 출처 : 「원문 제목」
        {: .src}

        원문 : [원문 블로그 이름](링크)<br>
        내 블로그 : [멍멍짱구 작업실](링크)
    """
    errs = []
    m = re.search(r'^### 출처 : 「(.+?)」\n\{: \.src\}\n\n원문 : (.+?)(?:<br>)?\n내 블로그 : (.+?)\s*$', s, re.M)
    if not m:
        return ['공부요약 글 맨 아래에 "### 출처 : 「원문 제목」" + "{: .src}" + "원문 :" + "내 블로그 :" 형식의 출처 블록이 없습니다']
    w = units('출처 : 「' + m.group(1) + '」')
    if w > SRC_LIMIT:
        errs.append(f'출처 제목이 폰(360px)에서 두 줄로 나뉠 수 있습니다 ({w:.1f} > {SRC_LIMIT}): {m.group(1)}')
    if not re.search(r'\]\(https?://[^)\s]+\)', m.group(3)):
        errs.append('"내 블로그 :" 줄에 링크가 없습니다 (기본 주소 https://m.blog.naver.com/kgu3405/)')
    if s.rstrip().splitlines()[-1].startswith('내 블로그 :') is False:
        errs.append('출처 블록이 글의 맨 마지막이 아닙니다')
    return errs


def check(path):
    errs = []
    s = open(path, encoding='utf-8').read()
    if re.search(r'^categories:\s*\[study\]', s, re.M):
        errs += check_source(s)
    m = re.match(r'---\n.*?\n---\n\s*(.*)', s, re.S)
    if not m:
        return ['front matter를 찾지 못했습니다']
    body = m.group(1)
    if body.startswith('<div class="tldr"'):
        rest = body  # 도입 문단 없이 3줄 요약으로 시작
    else:
        m2 = re.match(r'(.*?)\n\n(.*)', body, re.S)
        if not m2:
            return ['본문이 너무 짧습니다']
        intro, rest = m2.group(1), m2.group(2)
        if '\n' in intro:
            errs.append('도입 부분이 한 문단이 아닙니다 (도입 문단 뒤에 빈 줄이 필요)')
    t = re.match(r'<div class="tldr" markdown="1">\n\n## 3줄 요약\n\n(.*?)\n</div>', rest, re.S)
    if not t:
        return errs + ['도입 문단 바로 다음에 3줄 요약 블록이 없습니다']
    items = re.findall(r'^\d+\. (.+)$', t.group(1), re.M)
    if len(items) != 3:
        errs.append(f'요약 줄이 {len(items)}개입니다 (정확히 3개)')
    for i, it in enumerate(items, 1):
        w = units(it)
        if w > LIMIT:
            errs.append(f'{i}번 줄이 너무 깁니다 ({w:.1f} > {LIMIT}): {it}')
    return errs


def main():
    paths = sys.argv[1:] or sorted(glob.glob('_posts/*.md'))
    bad = 0
    for p in paths:
        e = check(p)
        if e:
            bad += 1
            print(f'[실패] {p}')
            for x in e:
                print('   -', x)
    print(f'검사 {len(paths)}편, 실패 {bad}편')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
