# The Hunger Games Multi-Agent Simulator
Welcome welcome, to the annual Hunger Games event!
May the odds be ever in your favor

## Dependencies

```
pip install numpy gymnasium stable-baselines3 pillow tqdm
```

## Running Modes
The model has been trained and can be run with the existing model or training can be executed.

### Train the Model
To train the model from the start with survival and gamemaker bombs, run:
```
python main.py --train
```
It will output a `results.txt` file that will be overwritten when it gets too long

To fine tune train the model with the addition of the hazardous wall, run:
```
python main.py --train --tune
```
It will output a `results_tune.txt` file that will be overwritten when it gets too long

### Run with the Model
You can run it with the model in 2 different ways:

#### Evaluation Mode

To run the simulator and evaluate the model over 10k episodes:
```
python main.py --eval
```

#### Single Run Mode
In your single run, a `games.gif` file will be generated containing the arena frames for each turn (48 per day)

To show tqdm progress bar:
```
python main.py --robot
```

To print out each tribute's move instead:
```
python main.py --robot --print
```

#### Additional Flags

To run the single run game and show the map of the arena in the terminal, add the `--display` flag

To see the arena diagram with different color tributes to easily spot them, add the `--color` flag

Note: If you are running this to an output file, the colors will not work and will cause visual disruptions