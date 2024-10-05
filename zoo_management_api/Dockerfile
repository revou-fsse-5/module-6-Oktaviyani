# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-dev  # You can also use --only main

# Copy the application code
COPY . .

# Set environment variable to use the virtual environment
ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose the port the app runs on
EXPOSE 5000

# Set the command to run the application
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
