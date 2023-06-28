# Sphere Strike !

# How to launch
## Launch the Game
**Install conda and pypi**  
- ### First setup
Create a conda environment  
> conda create -n SphereStrike python=3.9

Activate environment
> conda activate SphereStrike  

Install requirements  
> pip install -r requirements.txt

- ### Lauch after setup
Make sure you have conda environment enabled.  
> conda activate SphereStrike  

Execute launch script  
> bash launch.sh

## Launch tensorboard
**Install docker and docker-compose**  

Edit .env with values you need  
> nano .env

Launch tensorboard by executing this command:  
> docker-compose up -d