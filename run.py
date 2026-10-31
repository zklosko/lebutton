import sys

import uvicorn

if __name__ == "__main__":
    dev = "--dev" in sys.argv
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=dev, workers=1)