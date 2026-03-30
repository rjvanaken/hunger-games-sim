# The Hunger Games Multi-Agent Simulator
Welcome welcome, to the annual Hunger Games event!
May the odds be ever in your favor

## Running Modes
The model has been trained and can be run with the existing model or training can be executed

### Train the Model
To train the model, run:
```
python main.py --train > filename.txt
```
Best to add > `filename.txt`, as it will be many lines


### Run with the Model
To run the simulator and evaluate the model over 10k episodes:
```
python main.py --eval
```

To run the simulator a single time and see what each tribute chose at every turn:
```
python main.py --robot
```

#### Flags

To run the single run game and show the map of the arena, add the `--show` flag

To see the arena diagram with different color tributes to easily spot them, add the `--color` flag

Note: If you are running this to an output file, the colors will not work and will cause visual disruptions