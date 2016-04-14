import numpy as np
import pandas as pd
import os
from dataloader import loader
from judgebioextractor import mergeWriteJudgeToClean
from data_cleaning import Clean_Data

def main():
    mergeWriteJudgeToClean()
    Clean_Data()

if __name__ == "__main__":
    main()
