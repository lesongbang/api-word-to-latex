# Bu?c 1: Ch?n image n?n
# S? d?ng m?t image Python nh?
FROM python:3.9-slim

# Bu?c 2: Cài d?t các gói h? th?ng c?n thi?t
# Bao g?m pandoc d? chuy?n d?i và texlive-full d? t?o PDF t? LaTeX (h? tr? Unicode t?t)
# C?nh báo: texlive-full r?t l?n (~5GB), di?u này s? làm image c?a b?n l?n theo.
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Bu?c 3: Thi?t l?p môi tru?ng làm vi?c
WORKDIR /app

# Bu?c 4: Sao chép mã ngu?n vào container
COPY app.py /app/

# Bu?c 5: Cài d?t các thu vi?n Python
RUN pip install --no-cache-dir Flask Werkzeug

# Bu?c 6: M? port d? bên ngoài có th? giao ti?p v?i server
EXPOSE 5000

# Bu?c 7: L?nh d? kh?i ch?y ?ng d?ng khi container b?t d?u
CMD ["python", "app.py"]