import logging
import concurrent.futures
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import io
import uvicorn
import asyncio
from PIL import Image, ImageDraw

app = FastAPI()


def process_image(file):
    # Open the file as an image
    input_image = Image.open(file.file)

    # Create a watermark image
    watermark = Image.new("RGBA", (500, 100), (255, 255, 255, 255))
    draw = ImageDraw.Draw(watermark)
    draw.text((10, 10), "watermark", fill="black", font_size=80)

    # Composite the watermark onto the input image
    input_image.paste(watermark, (0, 0), watermark)

    # Save the processed image to bytes
    output_image = io.BytesIO()
    input_image.save(output_image, format="JPEG")
    output_image.seek(0)

    return output_image.read()


@app.post("/watermark/")
async def set_watermark(file: UploadFile):

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        result_image = await asyncio.to_thread(process_image, file)

    return StreamingResponse(io.BytesIO(result_image), media_type="image/jpeg")


if __name__ == '__main__':
    # uvicorn main:app --host 0.0.0.0 --port 8080 --reload --workers 2
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
