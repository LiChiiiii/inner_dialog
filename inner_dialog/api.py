import os
from dotenv import load_dotenv
from inner_dialog.auth import auth
from inner_dialog.model import Model
from inner_dialog.run_model import run_model
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
# http://xxx.xxx.xxx.xxx
production_frontend_url = os.getenv("FRONTEND_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Allow any port from localhost.
    allow_origin_regex=f"http://localhost:\d+|{production_frontend_url}:\d+",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/gen_mindmap/")
def gen_mindmap(
    question: str,
    model: Model,
    token: str,
    use_cache: bool = True,
    foce_write_cache: bool = False,
):
    is_verified, msg = auth(token=token, api_id="37")

    if not is_verified:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource, contact admin for API token.",
        )

    output_content = run_model(
        question=question,
        model=model,
        use_cache=use_cache,
        force_write_cache=foce_write_cache,
    )
    output_dict = {question: output_content}

    return output_dict
