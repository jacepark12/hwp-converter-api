import aiofiles.os
from logger import logger

async def cleanup_file(file_path: str):
    try:
        if await aiofiles.os.path.exists(file_path):
            await aiofiles.os.unlink(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
        else:
            logger.debug(f"File not found for deletion: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {str(e)}")
