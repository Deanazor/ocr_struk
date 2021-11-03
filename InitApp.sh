git clone https://github.com/PaddlePaddle/PaddleOCR.git

pip install requirements.txt

wget https://nodeflux-intern-ai.s3.ap-southeast-1.amazonaws.com/Ai-models/ocr-sruk/rec_crnn_inference.zip
wget https://nodeflux-intern-ai.s3.ap-southeast-1.amazonaws.com/Ai-models/ocr-sruk/det_r50_vd_inference.zip

!unzip det_r50_vd_inference.zip
!unzip rec_crnn_inference.zip