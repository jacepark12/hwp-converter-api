# hwp-converter-api

[LibreOffice Extension](https://github.com/ebandal/H2Orestart)을 사용하여, LibreOffice를 headless 모드로 실행하고 HWP 파일을 PDF 및 DOCX 형식으로 변환하는 API 서버입니다.

[Palantir Foundry](https://www.palantir.com/platforms/foundry/)내에서의 HWP 파일 처리를 위해 개발하였습니다. Palantir Foundry의 [Container Transforms](https://www.palantir.com/docs/foundry/transforms-python/container-overview)에서 사용할 수 있도록 [Image Requirements](https://www.palantir.com/docs/foundry/transforms-python/container-overview#image-requirements)를 준수합니다.

## 지원 형식

### 입력 포맷
- `.hwp`
- `.hwpx`

### 출력 포맷
- `.pdf`
- `.docx`

## Docker 컨테이너 실행 방법

### Docker

1. **Docker 이미지 빌드**:
   ```bash
   docker build -t hwp-converter-api .
   ```

2. **컨테이너 실행**:
   ```bash
   docker run -p 8800:8800 hwp-converter-api
   ```

3. **Health Check**:
   ```bash
   curl http://localhost:8800/health
   ```

## API Endpoints

### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### Convert File
```http
POST /convert
```

**Parameters**:
- `file` (required): HWP/HWPX file to convert
- `output_format` (optional): Output format - `pdf` or `docx` (default: `pdf`)

**Example using curl**:
```bash
curl -X POST "http://localhost:8800/convert" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.hwp" \
  -F "output_format=pdf" \
  --output converted.pdf
```

**Example using Python**:
```python
import requests

url = "http://localhost:8800/convert"
files = {"file": open("document.hwp", "rb")}
data = {"output_format": "pdf"}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open("converted.pdf", "wb") as f:
        f.write(response.content)
    print("Conversion successful!")
else:
    print(f"Error: {response.json()}")
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Unsupported file type or invalid output format
- `500 Internal Server Error`: Conversion failure or file processing error

Error responses include detailed information:
```json
{
  "error": "Unsupported file type",
  "detail": "Only .hwp, .hwpx files are supported"
}
```
