## Python Codebase

Detect_Segemnt...  is main working code containing functions to detect segment and classify code as well as develop and export machine learning models and also produce necessary graphs- definitely should have split this up tbf.

Raw data folder contains motion signals and the files are named based on the person the shot was collected from , type of shot and amount of shots made - different from how many will be detected.

Processed data contains the segmented and classififed data categorised into their relevant shots- useful for training with apple coreml. better to start from raw data however and use the scripts i have in main python file to create your own training and test data sets for apple coreml.


