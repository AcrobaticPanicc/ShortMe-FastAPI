from setup.setup_app import create_app

application = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:application", port=8080, reload=True)
