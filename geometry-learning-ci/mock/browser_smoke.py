#!/usr/bin/env python3
"""Public-safe browser smoke for synthetic geometry player mock.

Checks responsive layout and interaction behavior, not private problem geometry,
canonical correctness, learner data, cognitive evidence or physical devices.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil

from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
INDEX=HERE/"index.html"
VIEWPORTS=[
    ("small_portrait",320,568),
    ("mobile_portrait",360,800),
    ("mobile_landscape",823,384),
    ("tablet_portrait",768,1024),
    ("desktop",1280,850),
]


def assert_no_canvas_overlay(page, label):
    a=page.locator(".canvas-holder").bounding_box()
    b=page.locator(".controls-card").bounding_box()
    assert a and b
    horizontally=a["x"]+a["width"]<=b["x"]+1 or b["x"]+b["width"]<=a["x"]+1
    vertically=a["y"]+a["height"]<=b["y"]+1 or b["y"]+b["height"]<=a["y"]+1
    assert horizontally or vertically, f"{label}: controls obscure canvas"
    has_hscroll=page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2")
    assert not has_hscroll,f"{label}: horizontal overflow"
    for btn in page.locator("button:visible").all():
        box=btn.bounding_box()
        if box:
            assert box["height"]>=44, f"{label}: min touch height failure {btn.inner_text()}"
    return {"width":int(a["width"]),"height":int(a["height"]),
            "canvasToControls":"side-by-side" if horizontally else "stacked",
            "pageScrollHeight":page.evaluate("document.documentElement.scrollHeight") }


def run():
    chrome=(shutil.which("google-chrome") or shutil.which("chromium")
            or shutil.which("chromium-browser"))
    if not chrome:
        raise RuntimeError("Expected system Chrome/Chromium on public runner")
    report={}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=chrome,headless=True,
                                   args=["--no-sandbox","--disable-dev-shm-usage"])
        page=browser.new_page()
        browser_errors=[]
        page.on("pageerror",lambda err:browser_errors.append(str(err)))
        page.goto(INDEX.as_uri(),wait_until="load")
        assert page.locator(".tab").count()==3
        assert page.locator(".canvas-holder svg").count()==1
        for name,width,height in VIEWPORTS:
            page.set_viewport_size({"width":width,"height":height})
            page.wait_for_timeout(50)
            report[name]=assert_no_canvas_overlay(page,name)
            action=page.locator("#actions button").first.bounding_box()
            assert action, f"{name}: missing main action"
            report[name]["mainActionBottom"]=round(action["y"]+action["height"])
            if name in ("small_portrait","mobile_portrait","mobile_landscape"):
                assert action["y"]+action["height"]<=height+2, (
                    f"{name}: key action needs scrolling before use")
        # Direct handling and allowed action isolation.
        page.set_viewport_size({"width":360,"height":800})
        assert page.get_by_role("heading",name="돌리면 무엇이 바뀔까?").is_visible()
        page.get_by_role("button",name="90° 돌리기").click()
        assert "변화를 살펴보세요" in page.locator("#status").inner_text()
        page.get_by_role("button",name="되돌리기").click()

        # Mental mode: choice required before commit. Replay only after commit.
        page.locator("#mode-predict").click()
        commit=page.get_by_role("button",name="선택 확정")
        assert commit.is_disabled()
        assert page.locator("button",has_text="변화 보기").count()==0
        page.get_by_role("button",name="가 보기").click()
        assert commit.is_enabled()
        page.get_by_role("button",name="나 보기").click()
        assert "처음 고른 가" in page.locator("#status").inner_text()
        page.get_by_role("button",name="선택 확정").click()
        assert "처음 고른 가 · 확정한 나" in page.locator("#status").inner_text()
        assert page.get_by_role("button",name="변화 보기").is_visible()
        assert page.get_by_role("button",name="가 보기").is_disabled()
        page.get_by_role("button",name="변화 보기").click()
        assert "정답·오답을 채점하지 않고" in page.locator("#status").inner_text()

        # Switch reflection: reset source and keep mental replay locked.
        page.get_by_role("tab",name="회전").focus()
        page.keyboard.press("ArrowRight")
        assert page.get_by_role("tab",name="반사·대칭").get_attribute("aria-selected") == "true"
        assert page.get_by_role("button",name="좌우 뒤집기").is_visible()
        page.get_by_role("button",name="좌우 뒤집기").click()
        page.get_by_role("button",name="되돌리기").click()
        page.locator("#mode-predict").click()
        assert page.get_by_role("button",name="선택 확정").is_disabled()

        # Synthetic G6 has placement only; no solver or positive-process claims.
        page.get_by_role("tab",name="공간 제약").click()
        assert page.get_by_role("button",name="배치 바꾸기").is_visible()
        page.get_by_role("button",name="배치 바꾸기").click()
        assert "배치 A" in page.locator("#geometry").text_content()
        page.get_by_role("button",name="배치 바꾸기").click()
        assert "배치 B" in page.locator("#geometry").text_content()
        page.get_by_role("button",name="되돌리기").click()
        assert "먼저 조각을 놓아 보세요" in page.locator("#geometry").text_content()
        assert not browser_errors, f"JS runtime exceptions: {browser_errors}"
        browser.close()
    return {"status":"PASS_PUBLIC_MOCK_BROWSER_ONLY",
            "viewports":report,"lessonTabs":3,"modes":2,
            "checks":["no_canvas_control_overlap","no_horizontal_overflow",
                      "mental_first_choice_commit_guard","first_choice_retained_across_selection_change",
                      "keyboard_tab_arrow_navigation","after_commit_replay",
                      "non_scored_synthetic_place_and_undo","no_JS_pageerrors"],
            "noPrivateSource":"confirmed by isolated public CI file scope"}


if __name__=="__main__":
    print("GEOMETRY_PLAYER_MOCK_SMOKE="+json.dumps(run(),sort_keys=True))
