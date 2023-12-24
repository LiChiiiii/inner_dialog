FROM python:3.10-slim
ARG FRONTEND_URL
ENV FRONTEND_URL $FRONTEND_URL
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-directory
COPY inner_dialog/ ./inner_dialog
COPY data/ ./data
EXPOSE 80
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "inner_dialog.api:app"]