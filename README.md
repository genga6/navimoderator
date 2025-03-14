# NaviModerator

NaviModerator は、Twitch のコメントモデレーションを自動化するツールです。現在開発中であり、主要機能の実装を進めています。

## 概要
NaviModerator は、Twitch のコメントを取得し、AI による自動翻訳や誹謗中傷検出を行うことで、配信者のモデレーション作業をサポートします。

## 主な機能（開発中）
- **コメントの取得**: Twitch API を利用してリアルタイムでコメントを取得
- **誹謗中傷の検出**: LLM（大規模言語モデル）を活用して不適切なコメントをフィルタリング
- **自動翻訳**: コメントを自動翻訳し、配信者が内容を理解しやすくする
- **クラウド・ローカル推論**: ONNX Runtime Web によるローカル推論とクラウド処理の両方をサポート
- **Twitch Extension 連携**: OAuth 認証を用いた配信者向けインターフェースを提供予定

## システム構成
- **バックエンド**: FastAPI + LangGraph による LLM ワークフロー構築
- **フロントエンド（予定）**: TypeScript を用いた UI 実装
- **推論エンジン**: ONNX Runtime Web による WebGPU 推論
- **データフロー**:
  - Twitch API <-> FastAPI（LangGraph）<-> LLM（ONNX Runtime Web）

以下は LangGraph によるワークフローです。

![LangGraph ワークフロー](/workspaces/navimoderator/images/Navimoderator-2025-03-14.png)

## インストール & セットアップ（開発中）
リポジトリをクローンし、環境をセットアップしてください。

```bash
git clone https://github.com/your-repo/NaviModerator.git
cd NaviModerator
pip install -r requirements.txt
```

※ 現在、開発途中のため、環境構築や実行方法は変更される可能性があります。

## ライセンス
Apache License 2.0

## 開発状況
本プロジェクトは現在開発中であり、フィードバックやコントリビューションを歓迎しています。

---

今後のアップデートや機能追加については、適宜 README を更新していきます。

