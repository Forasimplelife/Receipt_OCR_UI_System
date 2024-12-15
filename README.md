
# 領収書の分類、認識とOCRのUIシステム

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

<div style="max-width: 600px; word-wrap: break-word;">


1. 画像の入力
ユーザーがレシート画像をアップロードします。
<div align="medium">
    <img src="Figures/UI1.png" alt="YOLO" width="100%">

</div>


2. 分類 (Classification)
ResNetベースの分類モデルが画像の回転角度を判定し、適切な方向に調整します。

<div align="medium">
    <img src="Figures/UI2.png" alt="YOLO" width="100%">
</div>	


<div align="medium">
    <img src="Figures/UI3.png" alt="YOLO" width="100%">
</div>	

3. 物体検出 (Object Detection)
YOLOv9を用いて、レシート内の重要領域を検出します。検出された領域はOCRモデルに渡されます。

<div align="medium">
    <img src="Figures/UI4.png" alt="YOLO" width="100%">
</div>	

<div align="medium">
    <img src="Figures/UI5.png" alt="YOLO" width="100%">
</div>	


4. 文字認識 (OCR)
EasyOCRが検出領域内の文字を認識し、結果をテキスト形式で出力します。

<div align="medium">
    <img src="Figures/UI6.png" alt="YOLO" width="100%">
</div>	


5. 結果の表示
抽出された情報（店舗名、日時、金額など）がStreamlitのUIに表示されます。

<div align="medium">
    <img src="Figures/UI7.png" alt="YOLO" width="100%">
</div>	


## Reference

<details><summary> <b>Expand</b> </summary>

* [https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)
* [https://github.com/WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9)
* [https://github.com/VDIGPKU/DynamicDet](https://github.com/VDIGPKU/DynamicDet)
* [https://github.com/DingXiaoH/RepVGG](https://github.com/DingXiaoH/RepVGG)
