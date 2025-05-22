"""
Authors: Nicole Huang & Kelli Eng
Date: 5/15/25
Description: Main class which initiates and runs all analysis files in repository.
"""
##### imports #####
import conan_analysis
import conf_matrix
import context_analysis
import pilot_analysis

##### main class #####
def main():
    print("\nRunning pilot data collection and scoring...")
    try:
        pilot_analysis.main()
    except Exception as e:
        print("Error running pilot.py:", e)

    print("\nRunning GC context-based scoring analysis...")
    try:
        context_analysis.main()
    except Exception as e:
        print("Error running context_analysis.py:", e)

    print("\nRunning confusion matrix analysis...")
    try:
        conf_matrix.main()
    except Exception as e:
        print("Error running conf_matrix.py:", e)

    print("Running DIALOCONAN context analysis...")
    try:
        conan_analysis.main()
    except Exception as e:
        print("Error running dialoconan_analysis.py:", e)

    print("\nAll analysis steps done")

if __name__ == "__main__":
    main()
