import subprocess
import uuid
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse
from logger import logger
from utils import cleanup_file, is_supported_file, get_file_extension

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Server is running"}


@app.post("/convert")
async def convert_hwp(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    output_format: str = Form("pdf"),
):
    """
    Convert an HWP file to the specified output format (pdf or docx).
    """
    if not is_supported_file(file.filename):
        logger.error(f"Unsupported file type: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Unsupported file type",
                "detail": "Only .hwp, .hwpx files are supported",
            },
        )

    if output_format not in ["pdf", "docx"]:
        logger.error(f"Invalid output format: {output_format}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid output format",
                "detail": "Supported formats: pdf, docx",
            },
        )

    file_extension = get_file_extension(file.filename)
    file_uid = uuid.uuid4()

    input_filename = f"/tmp/{file_uid}{file_extension}"
    output_filename = f"/app/{file_uid}.{output_format}"

    logger.info(
        f"Converting {file.filename} to {output_format}, output_filename: {output_filename}"
    )

    try:
        with open(input_filename, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"error": "Failed to save file", "detail": str(e)}
        )

    try:
        result = subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                output_format,
                input_filename,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.info(f"Conversion successful: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Conversion failed: {e.stderr.decode()}")
        background_tasks.add_task(cleanup_file, input_filename)
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to convert HWP to {output_format.upper()}",
                "detail": e.stderr.decode(),
            },
        )

    if not os.path.exists(output_filename):
        logger.error(f"Output file not created: {output_filename}")
        background_tasks.add_task(cleanup_file, input_filename)
        raise HTTPException(
            status_code=500,
            detail={"error": "Conversion failed", "detail": "Output file not created"},
        )

    media_type = (
        "application/pdf"
        if output_format == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response_filename = f"converted.{output_format}"

    background_tasks.add_task(cleanup_file, input_filename)
    background_tasks.add_task(cleanup_file, output_filename)

    return FileResponse(
        output_filename, media_type=media_type, filename=response_filename
    )
