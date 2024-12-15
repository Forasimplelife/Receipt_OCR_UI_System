
# 領収書の分類、認識とOCRをシステム

## Summary

<div style="max-width: 600px; word-wrap: break-word;">

この記事は、UI OCRシステムの構築について紹介しています。このシステムは、レシート画像から店舗名、日時、金額などの重要な情報を迅速かつ正確に抽出するために設計された自動化ソリューションです。具体的には、私が独自に訓練した2つのAIモデル（分類モデルと物体検出モデル）とEasyOCR、さらにStreamlitを用いたUIを統合して構築されています。

分類モデル Receipt Classification Model はレシート画像の回転角度（0度、90度、180度、270度）を自動的に判別し、どの向きの画像でも正しく処理できるように設計されています。物体検出モデル Receipt Detection Model は、レシート内の店舗名や日時、金額などの情報が記載された領域を効率的に特定し、文字認識に最適なデータを提供します。さらに、文字認識部分にはEasyOCRを採用し、多言語対応で高精度なテキスト抽出を実現しました。

これらのAIモデル を基盤に、Streamlitを用いてシンプルで直感的なUIを開発し、ユーザーが専門知識を必要とせずに簡単に利用できる環境を提供しています。このシステムは、手作業でのデータ入力を大幅に削減し、効率化と正確性の向上を図ることを目的としています。

</div>

##  システムの概要


<div style="max-width: 600px; word-wrap: break-word;">
本システムは以下のコンポーネントで構成されています：
	1.	分類モデル (Classification Model)
ResNetを基盤とした分類モデルを使用し、レシート画像の回転角度（0°, 90°, 180°, 270°）を判別します。このステップにより、画像の向きを統一し、後続の処理を最適化します。
	2.	物体検出モデル (Detection Model)
YOLOv9を基盤とした物体検出モデルを使用して、レシート内の重要情報が記載されている領域（店舗名、日時、金額など）を検出します。これにより、特定の領域を効率よく抽出します。
	3.	文字認識モデル (OCR)
EasyOCRを使用して、検出された領域内のテキストを多言語対応で高精度に認識します。日本語と英語を含む複数言語に対応しています。
	4.	UI (Streamlit)
Streamlitを用いて、簡単かつ直感的に操作できるユーザーインターフェースを提供します。専門知識がなくても利用可能です。
</div>


##  システムの構造と運用フロー

project/
├── models/                # 訓練済みの分類モデルと物体検出モデルの重み
├── data/                  # サンプルデータセット
├── src/
│   ├── classify.py        # 分類モデルのコード
│   ├── detect.py          # 物体検出モデルのコード
│   ├── ocr.py             # OCR処理のコード
│   ├── app.py             # Streamlitで動作するUIコード
├── requirements.txt       # 必要なパッケージ
└── README.md              # このファイル

<div style="max-width: 600px; word-wrap: break-word;">


1. 画像の入力
ユーザーがレシート画像をアップロードします。

2. 分類 (Classification)
ResNetベースの分類モデルが画像の回転角度を判定し、適切な方向に調整します。
	

3. 物体検出 (Object Detection)
YOLOv9を用いて、レシート内の重要領域を検出します。検出された領域はOCRモデルに渡されます。

4. 文字認識 (OCR)
EasyOCRが検出領域内の文字を認識し、結果をテキスト形式で出力します。

5. 結果の表示
抽出された情報（店舗名、日時、金額など）がStreamlitのUIに表示されます。

### データ準備

#### 1. 領収書データを収集

自分で買い物の領収書が200枚以上の領収書を収集して、その中は、比較的綺麗なと折り目ないの125枚を選び、訓練に行きます。

#### 2. Roboflowでアノテーションに

アノテーションツールにはいくつかの選択肢がありますが、最初にLabelImgとLabelmeを試しました。しかし、比較した結果、ウェブベースのRoboflowが非常に使いやすいことが分かりました。今回はRoboflowを使用してアノテーションを行いました。

Roboflowについて
Roboflowはデータセットのアノテーションを簡単かつ迅速に行い、さまざまなモデルのトレーニングに適した形式に変換できるソリューションを提供しています。無料で利用可能なRoboflowのパブリックバージョンを使用することができます。https://app.roboflow.com/


#### 3. データアップロード
ここでは、125枚の領収書サンプルをRoboflowアカウントにアップロードしてアノテーションを行います。


<div align="medium">
    <img src="images/dataset1.png" alt="YOLO" width="100%">
</div>


#### 4. アノテーションを作ります
このプロジェクトでは、領収書から以下の3つのラベルを抽出します：『合計』、『日付』、『電話番号』。そのため、それぞれのラベル名を入力し、各領収書サンプルのアノテーションを作ります。


<div align="medium">
    <img src="images/dataset2.png" alt="YOLO" width="100%">
</div>


#### 5. 前処理

アノテーションが完了したら、いくつかの前処理を行います。例えば、データセットを訓練用、検証用、テスト用に分割りします。また、画像を640x640サイズにリサイズします（現在のYOLO v9は640x640サイズの画像しか処理できないため、このステップは必須です）。

これらの前処理を行った結果、データセットの87枚が訓練用、26枚を検証用、12枚はテスト用として準備されました。

<div align="medium">
    <img src="images/dataset3.png" alt="YOLO" width="100%">

</div>


データセットの作成が完了したら、Roboflowの「Export Dataset」オプションを使用して、YOLO v9モデル用のデータセットをエクスポートできます。エクスポートしたデータセットコードを取得し、このコードをColab上で使用してモデルの訓練を行います。


## トーレニングの流れ

それでは、Colab上でYOLO v9モデルを使用してデータセットをどのように訓練するかを見ていきましょう。
まず、Colabの「ランタイムのタイプを変更」オプションからハードウェアアクセラレータをT4 GPUに変更します。その後、YOLOv9のリポジトリをGithubからGoogleドライブにクローンする必要があります。そのために、Googleドライブをマウントしてリポジトリをクローンし、以下のコードを使用して必要なファイルやパッケージをすべてインストールします。

###  Google Driveを接続に

```python
from google.colab import drive
drive.mount('/content/drive')
```

### YOLOv9のリポジトリをクローンと必要なパッケージをインストール

Clone YOLO v9 repository into your Google Drive.

```python
!git clone https://github.com/WongKinYiu/yolov9
%cd yolov9
!pip install -r requirements.txt -q
```

## モデルをダウンロード

リポジトリをクローンして必要なファイルをインストールした後、ディレクトリを作成し、以下のコードを実行してすべての重み（モデル）をダウンロードして保存することができます。

```python
!wget -P {HOME}/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt
!wget -P {HOME}/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e.pt
!wget -P {HOME}/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-c.pt
!wget -P {HOME}/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-e.pt
```

## Roboflowからデータセットをインポート
次に、Roboflowで作成したデータセットをインポートします，その前に、Roboflowパッケージをインストールする必要があります。

```python
!pip install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="xxxxxxx")
project = rf.workspace().project("projectname")
version = project.version(version number)
dataset = version.download("yolov9")
```

## トーレニング

その後、データセットを使ってYOLOモデルを訓練するためのトレーニングコードを実行します。ここでは、gelan-c weight.ptを使用してデータセットを訓練します。訓練を始める前に、モデルの設定ファイル（ここでは gelan-c.yaml）内のアンカー数を、データセットでアノテーションしたラベルの数に変更してください（この記事は３と使います）。モデルをより正確にするために、100エポックで訓練を行いました。ただし、必要に応じてエポック数を変更することも可能です。

```python
%cd {HOME}/yolov9

!python train.py \
--batch 8 --epochs 100 --img 640 --device 0 --min-items 0 --close-mosaic 15 \
--data invoice_extraction-3/data.yaml \
--weights {HOME}/weights/gelan-c.pt \
--cfg models/detect/gelan-c.yaml \
--hyp hyp.scratch-high.yaml
```

## トーレニングの結果

これでモデルの訓練が完了しました。モデルを100エポックで訓練した結果、全クラスにおいて平均適合率（mean average precision）が0.9という良好な精度を達成しました。

 <div align="medium">
    <img src="images/results1.png" alt="YOLO" width="100%">
</div>
Accuracy and Precision of the trained YOLO-v9 model

 <div align="medium">
    <img src="images/results2.png" alt="YOLO" width="100%">
</div>
Graph showing the model performance


## テストイメージを使って検証
   
```python
!python detect.py \
--img 640 --conf 0.5 --device 0 \
--weights {HOME}/yolov9/runs/train/exp2/weights/best.pt \
--source {HOME}/yolov9/test/images

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/yolov9/runs/detect/exp2/*.jpg')[:3]:
      display(Image(filename=image_path, width=600))
      print("\n")
```
 <div align="medium">
    <img src="images/testresult1.jpeg" alt="YOLO" width="50%">
</div>

 <div align="medium">
    <img src="images/testresult2.jpeg" alt="YOLO" width="50%">
</div>

## Reference

<details><summary> <b>Expand</b> </summary>

* [https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)
* [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9)
* [https://github.com/VDIGPKU/DynamicDet](https://github.com/VDIGPKU/DynamicDet)
* [https://github.com/DingXiaoH/RepVGG](https://github.com/DingXiaoH/RepVGG)
