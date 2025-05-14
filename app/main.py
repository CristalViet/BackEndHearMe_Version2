from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import course, dictionary, user, routes

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production, nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes

app.include_router(course.router, prefix="/api/course", tags=["course"])
app.include_router(dictionary.router, prefix="/api/dictionary", tags=["dictionary"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(routes.router, prefix="/api", tags=["lesson"])
