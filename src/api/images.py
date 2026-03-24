from fastapi import APIRouter, File, UploadFile
import shutil
from src.tasks.tasks import save_resized_images


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post('')
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}.jpg"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    save_resized_images.delay(image_path)