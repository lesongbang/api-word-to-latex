# Bu?c 1: Ch?n image n?n
# S? d?ng m?t image Python nh?
FROM python:3.9-slim

# Bu?c 2: C�i d?t c�c g�i h? th?ng c?n thi?t
# Bao g?m pandoc d? chuy?n d?i v� texlive-full d? t?o PDF t? LaTeX (h? tr? Unicode t?t)
# C?nh b�o: texlive-full r?t l?n (~5GB), di?u n�y s? l�m image c?a b?n l?n theo.
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Bu?c 3: Thi?t l?p m�i tru?ng l�m vi?c
WORKDIR /app

# Bu?c 4: Sao ch�p m� ngu?n v�o container
COPY app.py /app/

# Bu?c 5: C�i d?t c�c thu vi?n Python
RUN pip install --no-cache-dir Flask Werkzeug

# Bu?c 6: M? port d? b�n ngo�i c� th? giao ti?p v?i server
EXPOSE 5000

# Bu?c 7: L?nh d? kh?i ch?y ?ng d?ng khi container b?t d?u
CMD ["python", "app.py"]