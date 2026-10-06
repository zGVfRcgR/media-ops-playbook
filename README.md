# media-ops-playbook

## 概要

このリポジトリは、YouTube Shorts・Instagram Reels などの短尺メディアを企画・台本化・レビュー・改善して運用するための **運用設計書（プレイブック）** です。

コンテンツ本文やネタの元になる情報はこのリポジトリ内で管理し、以下をまとめて扱います。

- YouTube 動画の台本・草案・レビュー済み稿
- Copilot の動作ルールとペルソナ定義
- 台本化・コンプライアンス・分析などの運用ワークフロー
- チェックリストとKPIテンプレート
- 投稿前の最終確認ルール

> これまでのように「本体」と「運用」を別リポジトリで分ける運用はやめ、台本や関連資料はこのリポジトリ内で一貫して管理する。

---

## ディレクトリ構成

```
media-ops-playbook/
├── README.md                          # このファイル
├── instructions/
│   └── copilot-instructions.md        # Copilot の動作ルール
├── personas/
│   ├── personas.md                    # ペルソナ定義一覧
│   └── persona_template.md            # ペルソナ作成テンプレート
├── workflows/
│   └── README.md                      # 運用ワークフロー
├── youtube/
│   ├── README.md                      # YouTube 台本の保存ルール
│   ├── fields.md                      # YouTube API 取得フィールド定義
│   └── scripts/                       # 台本・草案・レビュー済み稿を保存
│       ├── README.md                  # 台本の命名ルールと保存方針
│       ├── draft/                    # 下書き
│       ├── review/                    # レビュー中
│       └── published/                 # 確定済み
├── compliance/
│   └── checklist.md                   # コンプライアンス確認チェックリスト
├── analytics/
│   └── kpi_template.md                # 分析・KPIテンプレート
├── data/
│   └── ...                            # YouTube 収集データ
├── python/
│   └── youtube_collector.py           # データ収集スクリプト
├── integration/
│   └── portfolio-masterplan.md        # 連携ルール（必要時のみ）
└── .env.example                       # API キーのサンプル
```

---

## 役割分担

| 担当 | 役割 |
|------|------|
| Copilot | 台本案・返信案・チェックリスト案・分析案の作成 |
| 人間（あなた） | 最終承認・公開判断・法務税務の確認 |
| 専門家 | 必要な場面での税務・法務・金融の判断 |
| 企画担当 | ネタの選定・優先順位・公開判断 |

---

## 基本原則

- **Copilot は補助する。人間が最終判断する。**
- 法務・税務・金融・著作権に関わる判断は必ず人間が行う。
- コンテンツと運用ルールをこのリポジトリ内で一貫して管理する。
- 1本の動画は1テーマに絞る。

---

## はじめかた

1. [`instructions/copilot-instructions.md`](instructions/copilot-instructions.md) でCopilotの動作ルールを確認する
2. [`personas/personas.md`](personas/personas.md) でペルソナを選ぶ
3. [`youtube/README.md`](youtube/README.md) で台本の保存場所と命名規則を確認する
4. [`workflows/README.md`](workflows/README.md) でワークフローを確認する
5. [`compliance/checklist.md`](compliance/checklist.md) で公開前チェックを行う
6. [`analytics/kpi_template.md`](analytics/kpi_template.md) で結果を記録する

---

## YouTube API 利用準備（最短）

1. 依存パッケージをインストールする
    ```bash
    pip install -r python/requirements.txt
    ```
2. `.env.example` を `.env` にコピーする
    ```bash
    cp .env.example .env
    ```
3. `.env` に以下を設定する
    - `YOUTUBE_API_KEY`（Google Cloud で発行した API キー）
    - `YOUTUBE_CHANNEL_ID`（分析対象チャンネル ID）
    - `MAX_COMMENTS_PER_VIDEO`（任意、既定値: 100）
4. 収集スクリプトを実行する
    ```bash
    python python/youtube_collector.py
    ```
5. `data/` に生成された JSON / CSV を分析に使う

---
