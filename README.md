# The Sorting Hat

The Sorting Hat analyses survey information in order to determine how diverse a group of survey respondents are, in terms of the answers they have provided.

It achieves this by comparing each individual's responses with every other individual's response and applying a proprietorial calculation as outlined below. Sub-group calculations can made in order to determine most, and least, diverse sub-groups.

## Client Problem (Calculation and Combinations)
From surveys completed on Survey Monkey, where each survey has 10 questions, with 5 response options per question, from a total sample size of ‘x’ individuals:
- 1/  Identify the “Most diverse group” possible. 
    - That is, given a group size ‘y’, from the total sample size ‘x’, identify the combination of individuals who, when grouped together, exhibit the **greatest** variety of selected response options. 
    - Greatest variety being defined as the most response options chosen per question with the most even distribution across all selected response options.
    ![most diverse](https://i.imgur.com/5We3zMm.png)
- 2/ Identify “Least diverse group” possible. 
    - That is, given a group size ‘y’, from the total sample size ‘x’, identify the combination of individuals who, when grouped together, exhibit the **least** variety of selected response options.
    - Least variety being defined as the fewest options chosen per question with the least even distribution across all selected response options.
    ![least diverse](https://i.imgur.com/ejVmqpn.png)

## The Sorting Hat Program 
### Features:
- Import csv files
- Toggle between a *greatest diversity first* or *least diversity first* group output
- Select variable group sizes ranging from minimum of 5 to maximum of total sample size ‘x’ (that is, all those who completed the survey)
- Output in an easy to read *excel* format:
    - Page one documents ‘Most diverse’ and ‘Least diverse’ group combinations Provides:
        - total ‘diversity / variety’ score out of 100 (that is score of 10 per question x 10 questions)    
        - subcategory sub-total scores for subcategories below

* Page two documents intragroup comparisons:
    * Identifies degree of similarity / difference between all possible pairs of individuals within each group (Out of 900)
    ![intra](https://i.imgur.com/WJ0u485.png)


## Working with the survey answers:

To calculate group ‘diversity / variety’ three primary subcategory totals – **Range**, **Options**, **Balance** – and a fourth optional subcategory total – **Gender** – were defined.

The three primary subcategory totals are associated to questions that have 5 possible response options. The fourth (optional) subtotal is associated with questions that have only 3 possible response options.

For each question the **group** can get a maximum possible “variety / diversity” score of 10 (great variety / very diverse) and a minimum possible “variety / diversity” score of 0 (no variety / not diverse).

The question score out of 10 is the total of the Range, Options, Balance, Gender subtotal scores.
* Range: Measures the range of options selected by the group per question (Score 0-3)
* Options: Measures the number of options selected by the group per question (Score 0-4)
* Balance: Measures the distribution of group members across each selected option per question (Score 0-3)
* *Optional* Gender: Measures the spread of gender within the group (Score 0 - 10)
The maximum possible score a group can achieve over all ten questions is 100 (greatest variety), the minimum possible score a group can achieve over all ten questions is 0 (least variety)

## Example:
##### Problem - If 30 people take a survey, which 5 of the 30 people exhibit the greatest variety of options selected

- Step 1: Determine all the groups (all the combinations of 5 people from the 30 sample)
- Step 2: Run each group through the *Sorting Hat* algorithm to calculate the necessary scores
- Step 3: Total the *Sorting Hat* scores for each group
- Step 4: Return the group with the highest score

*This example can be found [here]*

### Tech:
*The Sorting Hat* requires the following dependencies:
* [Python 3] - The coding language
* [Kivy] - For the GUI
* [xlwt] - An excel module for python

### Installation:
A pre-built version with an example can be downloaded in the [releases] section for MacOS, Windows, and Linux.
The source code is also available which can be compiled independently

### Running the source code:
- Install the dependencies
- cd to the location of the files
- Open your favourite Terminal and run the following:
```sh
$ kivy kivygui.py
```
### Todo:
- Multiprocessing support
- General optimization

[//]: #
[Python 3]: <https://www.python.org/downloads/>
[Kivy]: <https://kivy.org/#home>
[xlwt]: <https://pypi.org/project/xlwt/#description>
[releases]: <https://github.com/BetterThanMoo/TheSortingHat/releases>
[here]: <https://github.com/BetterThanMoo/TheSortingHat/blob/master/Example%20csv.csv>
