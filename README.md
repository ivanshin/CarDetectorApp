
# CarDetectorApp

This app was created in research goals. How it's work:

 - Open webpage of this app 
 - Upload street with cars image
 - Wait for result (see Demo section)

Kaggle research and used model (implimented SegNet architecture) training process: [link](https://www.kaggle.com/code/ivanshingel/cars-segmentation-research)

Fastapi + HTML + CSS + JS


## Features

CNN for this task was trained with lack of data (train dataset ~2500 semented images). The expirement was to improve segmentation result with some "tricks". Main feature:

![Image processing schema](/webp/assets/images/san-juan-mountains.jpg "San Juan Mountains")

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
  pip istall -r requirements.txt
```

Start uvicorn server:

```bash
  uvicorn app.main:app
```

Check it's work:

 - [127.0.0.1:8000](/127.0.0.1:8000)



## Demo


