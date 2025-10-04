import os, pathlib, uuid
from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'any-secret-string'

FILES_FOLDER = pathlib.Path(__file__).with_name('hashim1')
FILES_FOLDER.mkdir(exist_ok=True)

ADMIN_KEY = "1234"   # رمز سادهٔ خودتان

# ---------- چک کردن کلید ادمین ----------
def is_admin():
    return request.args.get("key") == ADMIN_KEY

# ---------- صفحهٔ اصلی ----------
@app.route('/')
def index():
    return render_template("links.html")

# ---------- API لیست فایل‌ها ----------
@app.route('/api/files')
def api_files():
    zips = [f for f in os.listdir(FILES_FOLDER) if f.lower().endswith('.zip')]
    return jsonify(zips)

# ---------- دانلود ----------
@app.route('/download/hashim1/<path:filename>')
def download(filename):
    return send_from_directory(FILES_FOLDER, filename, as_attachment=True)

# ---------- آپلود سریع (همان صفحه) ----------
@app.route('/add', methods=["POST"])
def add_zip():
    if not is_admin():
        return "Access denied", 403
    file = request.files['file']
    if file and file.filename.lower().endswith('.zip'):
        save_name = f"{uuid.uuid4().hex}.zip"
        file.save(FILES_FOLDER / save_name)
        flash("✅ اضافه شد.", "success")
    else:
        flash("❌ فقط ZIP.", "danger")
    return redirect(url_for('index'))

# ---------- حذف یک فایل ----------
@app.route('/del/<path:filename>')
def del_zip(filename):
    if not is_admin():
        return "Access denied", 403
    try:
        (FILES_FOLDER / filename).unlink()
        flash("❌ حذف شد.", "success")
    except FileNotFoundError:
        flash("فایل یافت نشد.", "danger")
    return redirect(url_for('index'))