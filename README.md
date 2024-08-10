# FungalFrequencies
visualierung für Fungal Frequencies


## Run
 
 ### build Website
 ``` 
cd FungalFrequencies
cd client 
npm run build
```

For autobuild use
``` 
npm run autobuild
```
 ### Run Python

 DEV:
 ``` 
cd FungalFrequencies
source .venv/bin/activate
python3 server.py
```

 ``` 
waitress-serve --host 127.0.0.1 server:app
```

## Install

### clone
``` 
git clone https://github.com/4ndreas/FungalFrequencies.git
```

### install python 

``` 
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### install npm 

``` 
cd FungalFrequencies
cd client 
npm install
```