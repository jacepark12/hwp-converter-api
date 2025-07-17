import os
import aiofiles.os
from logger import logger

SUPPORTED_EXTENSIONS = (".hwp", ".hwpx")


def is_supported_file(filename: str) -> bool:
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1]


async def cleanup_file(file_path: str):
    try:
        if await aiofiles.os.path.exists(file_path):
            await aiofiles.os.unlink(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
        else:
            logger.debug(f"File not found for deletion: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {str(e)}")
