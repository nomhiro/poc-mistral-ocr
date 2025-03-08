from mistralai import Mistral, DocumentURLChunk
from pathlib import Path
import json
import os

from util.markdown_utils import get_combined_markdown

# APIキーを設定して、Mistralクライアントを作成
api_key = os.getenv("MISTRALAI_API_KEY")
client = Mistral(api_key=api_key)

# OCR対象のPDFファイル
pdf_file = Path("./Society5.0の実現に向けた科学技術・イノベーション政策 .pdf")
assert pdf_file.is_file()

# PDFファイルをアップロード
uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

# アップロードしたファイルに対して、署名付きURLを取得
signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

# PDFファイルをOCR
pdf_response = client.ocr.process(document=DocumentURLChunk(
    document_url=signed_url.url), model="mistral-ocr-latest", include_image_base64=True)

# OCR結果を表示
response_dict = json.loads(pdf_response.model_dump_json())
json_string = json.dumps(response_dict, indent=4, ensure_ascii=False)
# OCR結果をファイルに保存。
result_file = Path("./result/ocr_result.json")
result_file.write_text(json_string, encoding="utf-8")

# Markdown形式でファイルに保存
markdown_string = get_combined_markdown(pdf_response)
markdown_file = Path("./result/ocr_result.md")
markdown_file.write_text(markdown_string, encoding="utf-8")
