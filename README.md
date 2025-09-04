dùng xóa docker cũ dùng các lênh sau:

docker stop my-converter-app

docker rm my-converter-app

đầu tiên tải dự án về vào build docker chạy thôi
*build docker mới

docker build -t converter-api .

*chạy

docker run -d -p 5000:5000 --name my-converter-app converter-api

vídu api

curl -X POST \
  -F "file=@thu.docx" \
  http://localhost:5000/word-to-latex-zip \
  --output result.zip


curl -X POST \
  -F "file=@result.zip" \
  http://localhost:5000/latex-zip-to-word \
  --output final_document.docx


 curl -X POST -F "file=@thu.docx" -F "format=latex" http://localhost:5000/convert -o thu.tex


 curl -X POST -F "file=@thu.tex" -F "format=docx" http://localhost:5000/convert -o ket.docx
