# YouTube 台本の保存ルール

YouTube 動画の台本は、このリポジトリ内の `youtube/` 配下で一元管理する。

## 保存先

- `youtube/scripts/draft/` — 下書き
- `youtube/scripts/review/` — レビュー中
- `youtube/scripts/published/` — 確定済み

## 命名規則

`YYYY-MM-DD_<テーマ>_v1.md`

例:

- `2026-10-06_short-term-investing_v1.md`
- `2026-10-06_short-term-investing_v2.md`
- `2026-10-06_short-term-investing_final.md`

## 保存する内容

- 1本ごとの台本
- フック
- 本論
- CTA
- 公開前チェックのメモ
- レビューコメント

## 方針

- 1本の動画につき1ファイルを原則とする
- 版管理は `v1`, `v2`, `final` などで管理する
- 承認前後の状態が分かるように保存先を分ける
- このリポジトリ内で完結させて、別リポジトリへ本体を分離しない

## 参考

- [README.md](../README.md)
- [workflows/README.md](../workflows/README.md)
- [youtube/fields.md](fields.md)
