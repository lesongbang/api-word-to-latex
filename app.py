import os
import subprocess
import uuid
import tempfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import shutil
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/word-to-latex-zip', methods=['POST'])
def word_to_latex_zip():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file trong request"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.docx'):
        return jsonify({"error": "Vui lòng chọn một file .docx"}), 400

    work_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
    zip_path = None

    try:
        filename = secure_filename(file.filename)
        input_path_abs = os.path.join(work_dir, filename)
        file.save(input_path_abs)

        base_name = os.path.splitext(filename)[0]
        output_tex_filename = f"{base_name}.tex"
        media_dir_relative = 'images' # Sử dụng đường dẫn tương đối

        command = [
            'pandoc',
            filename, # Input file (tương đối với work_dir)
            '--to', 'latex',
            '-o', output_tex_filename, # Output file (tương đối với work_dir)
            '--extract-media', media_dir_relative # Thư mục media (tương đối)
        ]
        
        # Chạy pandoc BÊN TRONG thư mục tạm để nó tạo đường dẫn tương đối
        subprocess.run(
            command, 
            check=True, 
            timeout=30,
            capture_output=True,
            text=True,
            cwd=work_dir # Đây là chìa khóa!
        )

        zip_filename_base = f"{base_name}.zip"
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename_base)
        
        output_tex_path_abs = os.path.join(work_dir, output_tex_filename)
        media_dir_abs = os.path.join(work_dir, media_dir_relative)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(output_tex_path_abs, os.path.basename(output_tex_filename))
            if os.path.isdir(media_dir_abs):
                for root, dirs, files in os.walk(media_dir_abs):
                    for f in files:
                        file_path = os.path.join(root, f)
                        archive_name = os.path.relpath(file_path, work_dir)
                        zipf.write(file_path, archive_name)

        return send_file(zip_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Lỗi trong quá trình chuyển đổi của Pandoc",
            "details": f"Exit Code: {e.returncode}, Stderr: {e.stderr}"
        }), 500
    except Exception as e:
        return jsonify({"error": "Đã xảy ra lỗi không mong muốn", "details": str(e)}), 500
    finally:
        if os.path.isdir(work_dir):
            shutil.rmtree(work_dir)
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)


@app.route('/latex-zip-to-word', methods=['POST'])
def latex_zip_to_word():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file trong request"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.zip'):
        return jsonify({"error": "Vui lòng chọn một file .zip"}), 400
    
    work_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])

    try:
        zip_path = os.path.join(work_dir, secure_filename(file.filename))
        file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(work_dir)

        tex_file = None
        for item in os.listdir(work_dir):
            if item.endswith('.tex'):
                tex_file = item
                break
        
        if not tex_file:
            raise ValueError("Không tìm thấy file .tex trong file zip.")

        output_filename = f"{os.path.splitext(tex_file)[0]}.docx"
        
        command = [
            'pandoc',
            tex_file,
            '-o', output_filename
        ]

        subprocess.run(
            command, 
            check=True, 
            timeout=30, 
            cwd=work_dir,
            capture_output=True,
            text=True
        )

        final_output_path = os.path.join(work_dir, output_filename)
        return send_file(final_output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Lỗi trong quá trình chuyển đổi của Pandoc (ZIP to Word)",
            "details": f"Exit Code: {e.returncode}, Stderr: {e.stderr}"
        }), 500
    except Exception as e:
        return jsonify({"error": "Đã xảy ra lỗi không mong muốn", "details": str(e)}), 500
    finally:
        if os.path.isdir(work_dir):
            shutil.rmtree(work_dir)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)