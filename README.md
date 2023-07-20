# RAG powered by Amazon Kendra & Rinna

[こちらのブログ](https://github.com/kenicazu/apprunner-sample-app/issues/3)で公開されているソリューションをベースにしており、
rinna の japanese-gpt-neox-3.6b-instruction-ppo モデルを、SageMaker でリアルタイム推論エンドポイントを Hostingして
そちらを利用したRAGのデモアプリケーションになります。

このサンプルアプリケーションでは以下のリソースが必要になります。
- Amazon Kendra
- SageMaker 推論エンドポイント（rinna japanese-gpt-neox-3.6b-instruction-ppo）

## アーキテクチャイメージ

![全体のアーキテクチャ図](./images/architecture.png)

## 画面イメージ

![イメージ図1](./images/image1.png)

## ディレクトリ構成

```shell
.
├── README.md                           # 本READMEファイル
├── /images                             # READMEで使用しているイメージファイル
└── /source                             # RAGアプリケーションのソースコードやREADME

```

## デプロイ準備

上記のリソースをAWSにデプロイする方法をまとめます。
デプロイを実行する端末には、下記のソフトウェアが必要です。

- AWS CLI v2
- Node.js 14以上
- Docker

```shell
# CDKプロジェクト配下に移動
cd infra

# IaCの依存関係をインストール
npm ci

# CDKをデプロイ先のリージョンで使えるように初期化する（以下コマンドはap-northeast-1の例）
AWS_REGION=ap-northeast-1 npx cdk bootstrap
```
## デプロイ手順

**エラーとなった場合はコマンドを実行しているディレクトリが正しいことを確認してください**
### BaseStackのデプロイ

まずはじめにBaseStackをデプロイし、App Runnerでサービスを実行するために必要なVPCやDB（Aurora Serverless V2）、コンテナイメージを格納するためのECRプライベートリポジトリを作成します。

```shell
# cdk-base-stackのデプロイ
npx cdk deploy BaseStack --require-approval never
```
なお、CDKのOutputsとして **BaseStack.RepositoryURI** が出力されると思うので、メモしておいてください。  
これは作成したECRリポジトリのURIになります。 この後の手順でこちらのリポジトリにコンテナをプッシュします。 

```shell
# 出力例
BaseStack.RepositoryURI = *******.dkr.ecr.ap-northeast-1.amazonaws.com/app-runner
```
