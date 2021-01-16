# DECA Judging Simulator

The DECA Judging Simulator simulates scores in a DECA conference and analyzes the impact of normalizing scores using two methods. Calculates the threshold for judge bias where not normalizing yields better results than normalizing. Assumes that scores follow a normal distribution. 

### Parameters
**relevant_scores:** how many scores do you care about? (top 4 qualify, for example).

**trials:** how many trials to calculate the average error? Balance speed with accuracy.

**judges:** how many judges do you have?

**kids_per_judge:** how many kids will each judge evaluate?

**avg_score:**  The average true score on a roleplay

**st_score:** The standard deviation in participant ability (of the true scores)    

**min_bias_tested:** The minimum judge bias to be tested in the simulation

**max_bias_tested:** The maximum judge bias to be tested in the simulation

How well trained are your judges? These refer to the standard deviation for a single judged score. For instance, if 95% of your judges would judge within 14 points of a 70 (true score) role-play, your standard deviation would be: (14 / 2) / 70 = 0.10.
*From 2020 DECA Launch Judging Data, this value seems to be around 0.13 in the real world.*

### Usage
Inspired by debate over whether to normalize scores at DECA Launch 2020 at The Harker School. Can be used to simulate any similar competition-based system that includes biased judging and potential normalization. 








