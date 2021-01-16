import numpy as np
import math

# USER DEFINED CONSTANTS ---------------------------------------------------------------

# does not significantly impact reliance on normalization
relevant_scores = 10    # how many scores do you care about? (top 4 qualify, for example)

# more trials = increased accuracy, at the cost of more time to calculate
trials = 1000           # how many trials to calculate the average errors?

# higher num of judges usually SLIGHTLY increases reliance on normalization (not significant)
judges = 18             # how many judges do you have?

# higher num of kids leads to increased reliance on normalization (lower cutoff)
kids_per_judge = 3     # how many kids will each judge judge?

# how well trained are your judges? This refers to the standard
# deviation for a single judged score. For instance, if 95% of your judges would
# judge within 14 points of a 70 role-play, your standard deviation would be (14/2)/70 = 0.1
# from 2020 DECA Launch Judging Data, seems to be around 0.13
# not actually used in current program
standard_judge_bias = 0.13     # Higher bias leads to a need for normalization

avg_score = 68.5      # Higher avg leads to increased reliance on normalization (lower cutoff)
st_score = 11.5       # Higher stdev for the scores leads to lower reliance on normalization (higher cutoff)
# DECA LAUNCH 2020: avg 68.5, stdev 11.5

min_bias_tested = 0.01
max_bias_tested = 0.20


# HELPER METHODS ---------------------------------------------------------------------------

# Given a list of scores, returns a list of the original indices in descending order
def rank_top(scores):
    return [name for (score, name) in sorted([(x, i) for (i, x) in list(enumerate(scores))], reverse=True)]


# calculates standard deviation of a list
def st_dev(arr):
    mean = sum(arr)/len(arr)
    variance = 0
    for i in arr:
        variance += (i - mean) ** 2
    return math.sqrt(variance/len(arr))


# MAIN SIMULATION ---------------------------------------------------------------------------
#
def run_simulation(relevant_scores, trials, judges, kids_per_judge, avg_score, st_score):
    cutoff = -1
    cutoff_found = False

    for bias in range(int(min_bias_tested*100), int(max_bias_tested*100) + 1, 1):
        st_judge_bias = bias/100.0

        points = round((st_judge_bias * 2) * avg_score)

        judged_error = []
        normalized_error = []
        adding_error = []

        for trial in range(trials):
            true_scores = np.random.normal(avg_score, st_score, judges * kids_per_judge)
            judge_bias = np.random.normal(1, st_judge_bias, judges)
            judged_scores = []
            normalized_scores = []
            added_scores = []

            overall_avg = sum(true_scores) / len(true_scores)

            for i in range(judges):
                bias = judge_bias[i]
                kids = [(bias * x) for x in true_scores[kids_per_judge * i: kids_per_judge * (i + 1)]]
                judged_scores += kids
                judged_avg = sum(kids) / len(kids)

                norm_factor = overall_avg / judged_avg
                norm_kids = [norm_factor * x for x in kids]
                normalized_scores += norm_kids

                add_factor = overall_avg - judged_avg
                added_kids = [add_factor + x for x in kids]
                added_scores += added_kids

            true_places = rank_top(true_scores)
            judged_places = rank_top(judged_scores)
            normalized_places = rank_top(normalized_scores)
            added_places = rank_top(added_scores)

            # print(true_places)
            # print(judged_places)
            # print(normalized_places)
            # print(added_places)

            # computes the judged/normalized errors for this trial
            j_error = 0
            n_error = 0
            a_error = 0
            for i in range(relevant_scores):
                j_error += (i - judged_places.index(true_places[i])) ** 2
                n_error += (i - normalized_places.index(true_places[i])) ** 2
                a_error += (i - added_places.index(true_places[i])) ** 2

            judged_error += [math.sqrt(j_error)]
            normalized_error += [math.sqrt(n_error)]
            adding_error += [math.sqrt(a_error)]
        # END TRIAL LOOP

        print("Bias:", st_judge_bias, "--> Points:", points)
        # average judged_error per trial
        print("Judged Error:", sum(judged_error) / trials, " ± ", st_dev(judged_error))
        # average normalized_error per trial
        print("Normalized Error:", sum(normalized_error) / trials, " ± ", st_dev(normalized_error))
        print("Added Error:", sum(adding_error) / trials, " ± ", st_dev(adding_error), "\n")

        if (not cutoff_found) and sum(judged_error) > sum(normalized_error):
            cutoff_found = True
            cutoff = st_judge_bias
    # END MODELING LOOP

    print("Modeling complete. Cutoff was found at bias level:", cutoff)
    print("This means that if your estimated bias level is at or below this number, you shouldn't normalize.")
    print("Add refers to adding a constant to judged scores to normalize.")
    print("Normalized refers to multiplying a constant with judged scores to normalize.")
# END OF SIMULATION METHOD


# Runs actual simulation ---------------------------------------------------------
run_simulation(relevant_scores, trials, judges, kids_per_judge, avg_score, st_score)
