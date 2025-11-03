from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_routes import router as auth_router
from routers.email_routes import router as email_router
from routers.cover_routes import router as cover_router
from routers.sendmail_routes import router as mail_router
from routers.name_update import router as email_router
from routers import security_settings as security_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# ✅ Include routers
app.include_router(auth_router)
app.include_router(email_router)
app.include_router(cover_router)
app.include_router(mail_router) 
app.include_router(email_router)
app.include_router(security_router.router)

@app.get("/")
def root():
    return {"message": "Backend running successfully!"}
