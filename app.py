import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from typing import Annotated
from fastapi import UploadFile, File, Depends
from src.api.schemas.predict_schema import PredictionResponce
from src.api.routes import api_router
from src.api.schemas.auth_schema import UserLogin, UserRegister, UserLoginResponse, User, Balance
from src.infrastructure.core.security import get_current_user
from src.infrastructure.database.utils import init_db
from src.infrastructure.services.auth_service import AuthService, get_auth_service
from src.infrastructure.services.predict_service import PredictionService, get_prediction_service

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get_webui():
    return FileResponse("index2.html")


@app.post("/api/auth/register", response_model=UserLoginResponse)
async def register(user_info: UserRegister,
                   service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.register(user_info)
    return response


@app.post("/api/auth/login", response_model=UserLoginResponse)
async def login(user_info: UserLogin,
                service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.login(user_info)
    return response


@app.get("/api/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/api/auth/balance", response_model=Balance)
async def get_balance(service: Annotated[AuthService, Depends(get_auth_service)],
                      current_user: User = Depends(get_current_user)):
    response = await service.get_balance(current_user)
    return response


@app.post("/api/predict/SVC")
async def send_data_for_prediction(model_name: str,
                                   prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                   file: UploadFile = File(...), user: User = Depends(get_current_user)):
    prediction_id = await prediction_service.register_prediction(user_id=user.id, model=model_name, file=file)
    return prediction_id


@app.post("/api/predict/1")
async def get_prediction_results(prediction_id: str,
                                 prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                 user: User = Depends(get_current_user)):
    prediction = await prediction_service.get_predictions(user_id=user.id,
                                                          prediction_id=prediction_id)
    responce = PredictionResponce.get_from_db(prediction)

    return responce


def start_service(port="8002", host="127.0.0.1", resetdb=False):
    host = os.getenv("HOST", host)
    port = int(os.getenv("PORT", port))
    if resetdb:
        init_db(drop_all=True)
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    start_service
