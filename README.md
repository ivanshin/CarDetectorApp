
# CarDetectorApp

This app was created in research goals. How does this work?:

 - Open webpage of this app 
 - Upload street with cars image
 - Wait for result (see Demo section)

Kaggle research and used model (implimented SegNet architecture) training process: [link](https://www.kaggle.com/code/ivanshingel/cars-segmentation-research)

STACK: Fastapi (Python 3.10) + HTML + CSS + JS


## Features

CNN for this task was trained with lack of data (train dataset ~2500 segmented images). The expirement was to improve segmentation result with some "tricks". Main feature:

![Image processing schema](https://github.com/ivanshin/CarDetectorApp/blob/master/webp/assets/img_proc_scheme.png)

## Run Locally

Clone the project:

```bash
  git clone https://github.com/ivanshin/CarDetectorApp.git
```

Switch to project directory:

```bash
  cd CarDetectorApp
```

Create virtual enviroment and activate:

```bash
  python -m venv .venv
```

```bash
  . .venv\Scripts\activate
```

Install requirements:

```bash
  pip install -r requirements.txt
```

Start uvicorn server:

```bash
  uvicorn app.main:app
```

Check if it works:

 Visit: [127.0.0.1:8000](http://127.0.0.1:8000)


## Demo
