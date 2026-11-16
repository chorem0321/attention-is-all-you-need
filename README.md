# Attention Is All You Need — manim 발표자료

Vaswani et al., NeurIPS 2017 논문 리뷰 — **Transformer 1팀** 발표자료, 슬라이드 31장.
라이브: https://chorem0321.github.io/attention-is-all-you-need/

문장 "Allen walks dog" 가 출력이 될 때까지의 8단계를 순서대로 따라갑니다.

| 단계 | 슬라이드 |
|---|---|
| 도입 (표지 · 배경 · 전체 구조 · 로드맵) | 1–4 |
| ① Tokenize + Embedding | 5 |
| ② Positional Encoding (순서 문제 · 다중 주파수 · 10000 과 상대 위치) | 6–8 |
| ③ Multi-Head Self-Attention | 9–21 |
| ④ Add & Norm ① (Residual · LayerNorm) | 22–23 |
| ⑤ FFN (구조 · 비선형성의 원리) | 24–25 |
| ⑥ Add & Norm ② + ⑦ Stack × 6 | 26 |
| ⑧ 디코더 attention · Linear + Softmax 출력 | 27–28 |
| 결과 · 한계 · 정리 | 29–31 |
각 슬라이드 = manim 씬 1개 → mp4 → `index.html` 에서 재생.

```
Transformer/
├─ NIPS-2017-attention-is-all-you-need-Paper.pdf   원문 (수치 근거)
├─ scenes/
│   ├─ common.py            공통 색·폰트·헬퍼 (Q=노랑, K=파랑, V=초록, weight=주황)
│   └─ s01_title.py … s31_summary.py   슬라이드별 씬 (파일당 클래스 1개)
├─ transformer_ppt.py       전체 렌더링 → media/slides/sNN.mp4 로 모음
├─ media/
│   ├─ videos/…             manim 원본 출력
│   └─ slides/sNN.mp4       index.html 이 읽는 영상 + render_report.json
├─ index.html               발표자료 (오프라인, 외부 CDN 없음)
└─ README.md
```

## 1. 준비

```powershell
pip install manim          # Manim Community Edition
ffmpeg -version            # manim 이 사용 (이미 PATH 에 있으면 OK)
```

- **LaTeX 는 필수가 아닙니다.** `scenes/common.py` 의 `M()` 은 LaTeX(`latex` 명령)가 있으면
  `MathTex`, 없으면 Pango `MarkupText`(`<sub>`, `<sup>`)로 수식을 그립니다.
  현재 씬들은 색 구분을 위해 대부분 MarkupText 경로를 씁니다.
- 한글 폰트: 씬은 `Malgun Gothic`, HTML 은 `Pretendard → 맑은 고딕` 순서로 사용합니다.
  Pretendard 는 번들되어 있지 않으므로 PC 에 설치되어 있을 때만 적용됩니다.

## 2. 렌더링

```powershell
python transformer_ppt.py            # 빠른 확인: -ql (480p15), 3개 병렬
python transformer_ppt.py -q h       # 발표용: -qh (1080p60)
python transformer_ppt.py -q h 5 12  # 특정 슬라이드만 (5번, 12번)
python transformer_ppt.py -j 1       # 메모리가 부족하면 직렬로
```

- 결과는 `media/slides/s01.mp4 … s31.mp4` 로 복사됩니다 (`-ql` 후 `-qh` 를 돌리면 덮어씀).
- 실패한 씬은 콘솔과 `media/slides/render_report.json` 에 로그 끝부분이 남습니다.
- 씬 하나만 직접 미리 보려면: `manim -pql scenes/s16_scaled_dot_product.py S16ScaledDotProduct`

## 3. 발표

`index.html` 을 브라우저(Chrome/Edge)로 엽니다. 파일을 더블클릭해서 열어도 됩니다.

| 키 | 동작 |
|---|---|
| `→` `Space` `PageDown` `Enter` | 다음 |
| `←` `PageUp` `Backspace` | 이전 |
| `Home` / `End` | 처음 / 마지막 |
| `S` | 발표자 노트 열기/닫기 |
| `R` | 현재 영상 처음부터 다시 |
| `F` | 전체화면 |

- 영상은 자동재생(muted)되고, 끝나면 마지막 프레임에 멈춰 있습니다.
- URL 끝의 `#7` 처럼 슬라이드 번호로 바로 이동할 수 있습니다.
- 영상이 없으면 그 자리에 "영상을 불러오지 못했습니다" 안내가 표시됩니다.
- `index.html?autotest` 로 열면 31장을 자동으로 넘기며 각 영상이 로드·재생되는지 검사하고
  결과를 화면 왼쪽 위와 탭 제목에 표시합니다.

## 4. 원문 대조 메모

- **EN→FR BLEU 는 41.0**: 이 폴더의 NeurIPS 판 PDF(Abstract, Table 2)에는 41.0 으로 나옵니다.
  41.8 은 이후 arXiv 개정판의 수치라서 슬라이드에는 41.0 을 쓰고, 발표자 노트에 따로 적어 두었습니다.
- **Head 수 실험(Table 3 A)** 은 test 가 아니라 **dev set(newstest2013)** BLEU 이고,
  d_k = d_v = 512/h 로 연산량을 고정한 결과입니다. 슬라이드에도 그렇게 표기했습니다.
- 9·17·18번 슬라이드의 attention 가중치, 16번의 score 행렬, 28번의 다음 토큰 확률은 **설명용 예시 값**입니다 (논문 수치 아님).
- **Positional Encoding**: 파장이 2π → 10000·2π 등비수열, "PE(pos+k) 는 PE(pos) 의 선형함수", 학습형 위치 임베딩과
  거의 동일(Table 3 E: 25.7 vs 25.8), 외삽 가능성 — 모두 3.5절 원문 그대로입니다.
  **10000 이라는 값 자체를 비교한 실험은 논문에 없으므로** 슬라이드에서 "경험적 선택"으로 표기했습니다.
- **FFN 활성화는 원문상 ReLU** 입니다. GELU 는 BERT/GPT 등 후속 모델의 선택이라 별도로 표기했습니다.
- 원문은 Post-LN: `LayerNorm(x + Dropout(Sublayer(x)))`, P_drop = 0.1 (base).
- 임베딩: 학습되는 임베딩 × √d_model, 입력/출력 임베딩과 pre-softmax Linear 가 가중치 공유 (3.4절).
- 층별 역할(하위 = 구문, 상위 = 의미)과 [CLS] 분류는 논문이 아닌 후속 연구 내용이라 슬라이드에 그렇게 표기했습니다.
