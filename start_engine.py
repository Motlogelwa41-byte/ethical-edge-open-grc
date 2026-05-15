import uvicorn

if __name__ == "__main__":
    print("Launching Ethical Edge Cognitive Engine...")
    print("UNICEF & SOCIETY Modules Loading...")
    print("Please go to http://127.0.0.1:8000 in your browser")
    # This points to the 'app' folder and the 'main' file
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
