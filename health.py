"""
Utility functions for calculations related to calories and energe expenditure.


A formula used for determining calories burnt is:

(1+0.0276*(HR-100))*(3.5+0.0887*(W-40))*T
HR: average heart rate
W:  weight in kg
T:  length of workout in minutes

It appears to give results quite similar to my Timex watch.

The Harris-Benedict formula for Basal Metabolic Rate is:

Men: BMR = 66 + (13.7 X wt in kg) + (5 X ht in cm) - (6.8 X age in years)
         = 66 + (6.23 x wt in lbs) + (12.7 x height in inches) -
           (6.8 x age in years)
Women: BMR = 655 + (9.6 X wt in kg) + (1.8 X ht in cm) - (4.7 X age in years)

It should be accurate unless extremely muscular or extremely overfat.

This gives the number of calories required to support just basic life processes
(not including digestion).

To get total daily energe expenditure (TDEE), multiply the bmr by one of the
following activity multipliers:

Sedentary = BMR X 1.2 (little or no exercise, desk job)
Lightly active = BMR X 1.375 (light exercise/sports 1-3 days/wk)
Mod. active = BMR X 1.55 (moderate exercise/sports 3-5 days/wk)
Very active = BMR X 1.725 (hard exercise/sports 6-7 days/wk)
Extr. active = BMR X 1.9 (hard daily exercise/sports & physical job or
    2X day training, i.e marathon, contest etc.)
"""


def calories(avg_heart_rate, weight_lbs, workout_mins):
    return calories_per_min(avg_heart_rate, weight_lbs) * workout_mins


def calories_per_min(avg_heart_rate, weight_lbs):
    return ((1 + 0.0276 * (avg_heart_rate - 100))
            * (3.5 + 0.0887 * (pounds_to_kg(weight_lbs) - 40)))


def bmr_male(weight_lbs, height_inches, age_years):
    return (66 + (13.7 * pounds_to_kg(weight_lbs))
            + (5 * inches_to_cm(height_inches)) - (6.8 * age_years))


def bmr_female(weight_lbs, height_inches, age_years):
    return (655 + (9.6 * pounds_to_kg(weight_lbs))
            + (1.8 * inches_to_cm(height_inches)) - (4.7 * age_years))


def pounds_to_kg(pounds):
    return pounds * 0.45359237


def kg_to_pounds(kg):
    return kg * 2.20462262


def inches_to_cm(inches):
    return inches * 2.54


def cm_to_inches(cm):
    return cm * 0.393700787
