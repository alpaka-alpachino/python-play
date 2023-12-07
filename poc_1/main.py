from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import io
import uvicorn
from PIL import Image, ImageDraw

app = FastAPI()
watermark = Image.new("RGBA", (500, 100), (255, 255, 255, 255))


async def process_image(file):
    # Open the file as an image
    input_image = Image.open(file.file)

    # Composite the watermark onto the input image
    input_image.paste(watermark, (0, 0), watermark)

    # Save the processed image to bytes
    output_image = io.BytesIO()
    input_image.save(output_image, format="JPEG")
    output_image.seek(0)

    return output_image.read()


@app.post("/watermark/")
async def set_watermark(file: UploadFile):
    result_image = await process_image(file)

    return StreamingResponse(io.BytesIO(result_image), media_type="image/jpeg")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=False, workers=16)
