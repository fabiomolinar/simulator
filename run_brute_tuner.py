from simulator.tuner.brute import BruteTuner
from simulator.tuner.brute import RecurringBruteTuner

def run():
    brute = RecurringBruteTuner()
    brute.run()
    
if __name__ == "__main__":
    run()