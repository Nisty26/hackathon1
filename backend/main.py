from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from color_utils import dominant_rgb, rgb_to_hsv_deg
from logic import classify_undertone, harmony_type, PALETTES

app = FastAPI(title="AI Color Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SkinResult(BaseModel):
    rgb: List[int]
    hsv: List[float]
    undertone: str
    recommended_palette: List[str]

class OutfitResult(BaseModel):
    outfit1_rgb: List[int]
    outfit2_rgb: List[int]
    outfit1_hsv: List[float]
    outfit2_hsv: List[float]
    harmony: str
    hue_diff: float

class AllResult(BaseModel):
    skin: SkinResult
    outfits: OutfitResult

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze/skin", response_model=SkinResult)
async def analyze_skin(file: UploadFile = File(...)):
    data = await file.read()
    rgb = dominant_rgb(data)
    h, s, v = rgb_to_hsv_deg(rgb)
    undertone = classify_undertone(rgb)
    return SkinResult(
        rgb=list(rgb),
        hsv=[h, s, v],
        undertone=undertone,
        recommended_palette=PALETTES[undertone],
    )

@app.post("/analyze/outfits", response_model=OutfitResult)
async def analyze_outfits(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    b1 = await file1.read()
    b2 = await file2.read()
    rgb1 = dominant_rgb(b1)
    rgb2 = dominant_rgb(b2)
    h1, s1, v1 = rgb_to_hsv_deg(rgb1)
    h2, s2, v2 = rgb_to_hsv_deg(rgb2)
    diff = abs((h1 - h2 + 180) % 360 - 180)
    return OutfitResult(
        outfit1_rgb=list(rgb1),
        outfit2_rgb=list(rgb2),
        outfit1_hsv=[h1, s1, v1],
        outfit2_hsv=[h2, s2, v2],
        harmony=harmony_type(h1, h2),
        hue_diff=diff,
    )

@app.post("/analyze/all", response_model=AllResult)
async def analyze_all(selfie: UploadFile = File(...),
                      outfit1: UploadFile = File(...),
                      outfit2: UploadFile = File(...)):
    skin = await analyze_skin(selfie)   # type: ignore
    outfits = await analyze_outfits(outfit1, outfit2)  # type: ignore
    return AllResult(skin=skin, outfits=outfits)
