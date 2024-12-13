!python detect.py \
--img 640 --conf 0.5 --device cpu \
--weights runs/train/exp/weights/best.pt \
--source data/corrected_images\
--save-txt --save-conf