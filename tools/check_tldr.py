#!/usr/bin/env python3
"""모든 글(_posts/*.md)이 '3줄 요약' 규칙을 지키는지 검사한다.

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


def check(path):
    errs = []
    s = open(path, encoding='utf-8').read()
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
