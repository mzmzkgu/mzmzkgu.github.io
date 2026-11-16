#!/usr/bin/env python3
"""IndexNow: 새 글이 배포되면 검색엔진(Bing, 네이버 등)에 주소를 알려 준다.

- 기본: 방금 배포된 커밋에서 새로 생기거나 고쳐진 글(_posts/*.md)의 주소와, 홈·전체 글·해당 게시판 주소를 보낸다.
- --all : 사이트 전체 주소를 보낸다. (처음 한 번이나 문제가 있을 때)
- --dry-run : 실제로 보내지 않고 보낼 내용만 출력한다. (시험용)
- --ref <커밋> : 이 커밋의 변경을 기준으로 한다. (기본 HEAD)

키 파일(저장소 루트의 <키>.txt)은 비밀이 아니다. 이 사이트가 주인임을 검색엔진에 증명하는 공개 파일이다.
구글은 IndexNow 를 쓰지 않는다. (구글은 Search Console 사이트맵으로 알린다)
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

HOST = "mzmzkgu.github.io"
BASE = "https://" + HOST
KEY = "c79de37461ced32f097fd26092b83d52"
KEY_LOCATION = f"{BASE}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
BOARDS = ["/ipo/", "/infinity/", "/study/"]            # 글 분야 → 목록 주소 (categories 값과 같다)
FIXED_PAGES = ["/", "/posts/", "/ipo/", "/infinity/", "/study/", "/fearbuy/", "/market/", "/contact/", "/privacy/"]


def post_url(filename):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", os.path.basename(filename))
    return f"{BASE}/posts/{m.group(1)}/{m.group(2)}/{m.group(3)}/{m.group(4)}/" if m else None


def categories_of(path):
    try:
        head = open(path, encoding="utf-8").read(2000)
    except OSError:
        return []
    m = re.search(r"^categories:\s*\[([^\]]*)\]", head, re.M)
    return [c.strip() for c in m.group(1).split(",")] if m else []


def changed_posts(ref):
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AM", f"{ref}^", ref, "--", "_posts"],
        capture_output=True, text=True, check=False,
    ).stdout.split()
    return [p for p in out if p.endswith(".md")]


def build_urls(args):
    if args.all:
        posts = sorted(glob.glob("_posts/*.md"))
        urls = [BASE + p for p in FIXED_PAGES] + [u for u in map(post_url, posts) if u]
        return urls
    posts = changed_posts(args.ref)
    if not posts:
        return []
    urls = [BASE + "/", BASE + "/posts/"]
    for p in posts:
        u = post_url(p)
        if u:
            urls.append(u)
        for c in categories_of(p):
            board = f"/{c}/"
            if board in BOARDS:
                urls.append(BASE + board)
    seen, uniq = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def send(urls):
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]
    except Exception as e:  # 네트워크 오류 등: 배포를 막지 않는다
        return 0, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", default="HEAD")
    args = ap.parse_args()

    urls = build_urls(args)
    if not urls:
        print("새로 올라온 글이 없어서 보내지 않습니다.")
        return 0
    print(f"IndexNow 로 보낼 주소 {len(urls)}개:")
    for u in urls:
        print("  ", u)
    if args.dry_run:
        print("(dry-run: 실제로 보내지 않음)")
        return 0
    for i in range(0, len(urls), 10000):
        status, text = send(urls[i:i + 10000])
        print(f"응답: HTTP {status} {text}")
        # 200/202 = 접수됨. 그 외는 경고만 남기고 끝낸다(사이트 배포에는 영향 없음)
        if status not in (200, 202):
            print(f"::warning::IndexNow 전송이 정상 접수되지 않았습니다 (HTTP {status}). 키 파일 주소와 배포 상태를 확인하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
