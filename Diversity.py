'''***********************************************************
This Program was made by Patrick Gourley for the purpose of
calculating Diversity of Thought given a csv file of answers
from a group of X participants, sorted into groups of size
Y either Most or Least diverse first.
***********************************************************'''

#Imports 
from itertools import * 
import operator     
import time           
import cProfile
import multiprocessing



#Main Application
'''******************************************
Here is where all the pre-calc stuff happens.
******************************************'''
def run (group_size, participant_answers, big_or_small):  
  start_time = time.time()                                                                   
  participants = []                                                                                                                                                        
  groups = []                                                                                        
  final = []                                                                                       
  final_gender = []
  final_range = []
  final_options = []
  final_balance = []
  group_questions = {}
  question_name_counter = 1
  group_name_counter = 1
  a = participant_answers.values()
  for i in a:
    num_of_q = len(i)
    break
  gender_question = 0                               
  group_counter = 0                                                                                     
  gender_question = False
  participants.extend(range(1, len(participant_answers)+1))                                            
  for group in combinations(participants, group_size):                                                       
    groups.append(group)                                                                               

  while group_counter < len(groups):                                                                           
    question_track = 0                                                                                         
    while question_track < num_of_q:                                                                       
      question = []     
      question_real = []                                                                                      
      test = 1                                                                                                
      temp = 0                                                                                 
      
      b = participant_answers.values()
      
      for each in groups[group_counter]:                                   
        values = participant_answers.get(each)                                                          
        question.append((values[question_track]))       
      if question_name_counter <= 10:
        group_questions["Group " + str(group_name_counter) + " Question " + str(question_name_counter)] = question
        question_name_counter+=1
        if question_name_counter > 10:
          group_name_counter+=1
          question_name_counter = 1
      while test <= group_size:                                                      
        temp = question.count(test)                                                              
        question_real.append(temp)                                                               
        test+=1                                                                                
      
      if question_track == 0:                                                            
        gender_question = True                                                        
        getting_result = (diversity(question_real, gender_question, group_size))       
        final.append(getting_result)
        final_gender.append(getting_result)
      
      
      if gender_question == True:                                                     
        gender_question = False                                                               
      else:                                                                                            
        getting_result = (diversity(question_real, gender_question, group_size))                   
        final.append(getting_result[0])
        final_range.append(getting_result[1])
        final_options.append(getting_result[2])
        final_balance.append(getting_result[3])
      question_track+=1                                                                    
    group_counter+=1                                                                              
  result = (figure(final, groups, participants, big_or_small, final_gender, final_range, final_options, final_balance))         
  similar = intra(group_questions, result[0], group_size, start_time)
  return (result, similar)




#Main Calculation
'''******************************************
This is used as a front end to send the data
between different calculators and return a
combined result.
It takes an input of numbers 0-5 for a group
of size (x) and pushes this list through
R(ange) O(ption) and B(alance) calculators 
to extract the end ROB score for that group 
for that question
******************************************'''
def diversity(table, gender_question, group_size):
    result = []       
    final = 0                  
    if gender_question == True:        
      gender = get_gender(table, group_size) 
      result.append(gender)         
      return (sum(result))                 
    r = get_r(table, group_size)   
    o = get_o(table)                
    b = get_b(table, o)        
    result.append(r + o + b)                
    return (sum(result), r, o, b)                 



#Calculate R(ange) score
'''******************************************
This is used to calculate the R(ange) score.
It takes an input of numbers 0-5 for a group
of size (x) outputs a single range score for 
that group for that question
******************************************'''
def get_r (group_question, num_participants):
  max_option = 0
  min_option = 0
  run = 0
  run_max = 1
  
  for i in group_question:
    run+=1
    if i > 0:
      min_option = run
      break
  
  for i in group_question:
    if group_question[-run_max] > 0:
      max_option = (num_participants - (run_max-1))
    else:
      run_max+=1
  a_range = max_option - min_option
  
  if a_range - 1 >= 0:
    return a_range-1
  else:
    return 0

#Calculate O(ptions) Score
'''******************************************
This is used to calculate the O(ptions) 
score. It takes an input of numbers 0-5 for a 
group of size (x) outputs a single options 
score for that group for that question
******************************************'''
def get_o (group_question):
    option_score = 0         
    for each in group_question:  
        if each > 0:             
            option_score += 1    
    option_score-=1              
    return (option_score)         
  
#Calculate (B)alance Score
'''******************************************
This is used to calculate the B(alance) 
score. It takes an input of numbers 0-5 for a 
group of size (x) outputs a single balance
score for that group for that question
******************************************'''
def get_b (group_question, option_score):
  active_check = []
  option = 0
  
  for i in group_question:
    if round(i*100/len(group_question)) != 0:
      active_check.append(round(i*100/len(group_question)))
    
    
  for j in active_check:
    if j >= 15: 
      if j < 80:
        option+=1
  if option -1 >= 0:
    if option -1 == 4:
      return option-2
    else:
      return option-1
  else:
    return 0

  
#Calculate Gender Score
'''******************************************
This is used to calculate the Gender score.
It takes an input of numbers 0-5 for a group
of size (x) outputs a single gender score for 
that group for that question. This is only
relevant to question 2 of each group
******************************************'''
def get_gender(group_question, group_size):
  other_count = 0
  if group_question[2] > 0:
    other_count = group_question[2]
    
  if other_count > 0:
    group_question[0] += (other_count/2)
    group_question[1] += (other_count/2)
    
  male_percent = int ((group_question[0]/ group_size) * 100)
  female_percent = int ((group_question[1]/ group_size) * 100)
  
  if male_percent >= female_percent:
    difference = male_percent - female_percent
  else:
    difference = female_percent - male_percent
    
  if difference in range (0, 18):
    return 10
  elif difference in range (18, 34):
    return 8
  elif difference in range (34, 51):
    return 6
  elif difference in range (51, 68):
    return 4
  elif difference in range (68, 85):
    return 2
  else:
    return 0

#Extract final scores per group  
'''******************************************
This is used to extract the final ordered 
groups based on diversity. It takes the list
of completed ROB scores per question and then 
calculates the final ROB score overall per
group. It will return a list of all the
calculated groups from Most diverse to Least
diverse.
******************************************'''
def figure(final, groups, participants, big_or_small, final_gender, final_range, final_options, final_balance):
  per_question = {}
  per_gender = {}
  per_range = {}
  per_options = {}
  per_balance = {}
  groups_final = {}                                                                                          
  result = []
  not_in_list = []
  remove_list = []
  sorting_count = 0
  question_diversity_count = 0                            
  question_gender_count = 0
  question_rob_count = 0
  group_count = 1                                                
  while question_diversity_count < len(final):    
    if question_diversity_count % 10 == 0:                                                                        
      groups_final["Group " + str(group_count)] = sum(final[question_diversity_count:question_diversity_count+10])
      per_question["Group " + str(group_count)] = (final[question_diversity_count:question_diversity_count+10])
      per_gender["Group " + str(group_count)] = (final_gender[question_gender_count])
      per_range["Group " + str(group_count)] = sum(final_range[question_rob_count:question_rob_count+9])
      per_options["Group " + str(group_count)] = sum(final_options[question_rob_count:question_rob_count+9])
      per_balance["Group " + str(group_count)] = sum(final_balance[question_rob_count:question_rob_count+9])
      question_diversity_count+=10                                                                                   
      question_gender_count+=1
      question_rob_count += 9
      group_count+=1                                                                                                
  groups_final = sorted(groups_final.items(), key=operator.itemgetter(1), reverse=True)
  big = sorted(groups_final, key=operator.itemgetter(1), reverse=True)                       
  small = sorted(groups_final, key=operator.itemgetter(1), reverse=False) 
  

  while sorting_count < len(groups_final):
    unique = True
    group_checker = []
    if big_or_small == True:
      groups_final = big
    else:
      groups_final = small
    who = str(groups_final[sorting_count][0])                                                                    
    group_number = [int(s) for s in who if s.isdigit()]                                                          
    group_number = int(''.join(str(i) for i in group_number))                                                     
    
    for i in groups[(group_number)-1]:
      group_checker.append(i)
    if len(remove_list) > 0:
      for i in group_checker:
        if i in remove_list:
          unique = False
    if unique == True:
      result.append("Group " + str(group_number) + ": " + ((str(groups[(group_number)-1])) + " Score: " + str(groups_final[sorting_count][1])))
      for i in group_checker:
          remove_list.append(i)
      remove_list = sorted(remove_list)
      if big_or_small == False:
        big_or_small = True
      else:
        big_or_small = False
      sorting_count+=1
    if unique == False:
      sorting_count+=1
  for i in participants:
    if i not in remove_list:
      result.append("Not in Group: " + '(' + (str(i)) + ')')
  
  little_groups = []
  count = 0
  little_count = 0
  smaller_count = 0
  while count < len(result):
    if result[little_count][0:3] == 'Not':
      break
    for i in result[little_count]:
      if i == ':':
        little_groups.append(result[little_count][0:smaller_count])
        break
      else:
        smaller_count+=1
    little_count+=1
    smaller_count = 0
    count+=1
  per_question_result = []
  gender_groups = []
  range_groups = []
  option_groups = []
  balance_groups = []

  for i in little_groups:
    per_question_result.append(per_question[i])
    gender_groups.append(per_gender[i])
    range_groups.append(per_range[i])
    option_groups.append(per_options[i])
    balance_groups.append(per_balance[i])
    

  return (result, range_groups, gender_groups, option_groups, balance_groups, per_question_result)

#Intra-group calculations
'''******************************************
This is used to determine who in each group
is most similar to one another. E.g. if
person 1 and person 2 both put option 3 (of
5 options) for a particular question, their
comparison would be scored as 0, as there
is no diversity in their option selection.
If person 1 and person 2 put options 1, and 5
then they would score 100, as there is the
maximum level of diversity between their 
selections.
******************************************'''
def intra(group_questions, winners, group_size, start_time):
  r_group = []
  o_count = 0
  for winner in winners:
    count = 0
    while count < len(winners[o_count]):
      if winner[count] == ':':
        r_group.append(winner[0:count])
        break
      else:
        count+=1
    o_count+=1


  correct_group_answers = []
  count = 0
  q_count = 2
  while count < len(r_group):
    if r_group[count] != 'Not in Group':
      while q_count <= 10:
        tack = ' question ' + str(q_count)
        search_for = r_group[count].lower() + tack
        calcld = [value for key, value in group_questions.items() if search_for in key.lower()]
        correct_group_answers.append(calcld)
        q_count+=1
      count+=1
      q_count=2
    else:
      count+=1


  test = []
  gender_q = 0
  for correct_group_answer in correct_group_answers:
    for correct_answer in correct_group_answer:
      test.append(correct_answer)
      
  magic = int((group_size-1) * (group_size / 2))  
  count_total = 0
  question_count = 0
  count_first = 0
  count_second = 1
  score = []
  while count_total < (magic * 9 * len(winners)):
    scoretest = ((test[question_count][count_first], test[question_count][count_second]))
    if scoretest in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]:
      score.append(0)
    elif scoretest in [(1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)]:
      score.append(25)
    elif scoretest in [(1, 3), (2, 4), (3, 1), (3, 5), (4, 2), (5, 3)]:
      score.append(50)
    elif scoretest in [(1, 4), (2, 5), (4, 1), (5, 2)]:
      score.append(75)
    elif scoretest in [(1, 5), (5, 1)]:
      score.append(100)
    else:
      print ("ERROR ERROR ERORR")
      break
    count_second+=1
    if count_second >= len(test[question_count]):
      count_total +=1
      count_first +=1
      count_second = (count_first+1)
      if count_second >= len(test[question_count]):
        if question_count+1 < len(test):
          question_count+=1
          count_total = 0
          count_first = 0
          count_second = count_first + 1
        else:
          break
        
    
  testing = 0
  count = 0
  comparison = 0
  
  final_list = []
  while comparison < magic:
    testing+=score[count]
    count+= magic
    if count >= magic * 9:
      count = comparison + 1
      comparison+=1
      final_list.append(testing)
      testing = 0
      if comparison == magic:
        del score[0:magic*9]
        if len(score) > magic:
          count = 0
          comparison = 0
        else:
          break

  m_group = []
  o_count = 0
  count_start = 0
  count_end = 0
  for i in winners:
    count = 0
    while count < len(winners[o_count]):
      if i[count] == '(':
        count_start = count+1
      if i[count] == ')':
        count_end = count
        m_group.append(i[count_start:count_end])
        break
      else:
        count+=1
    o_count+=1    
    
  m_group_real = []
  for i in m_group:
    i = i.split(',')
    m_group_real.append(i)
  m_group_real = [list(map(int, x)) for x in m_group_real]
  

  final = {}
  list_count = 0
  count = 0
  count2 = 1
  sumtracker = 0
  while list_count < len(m_group_real):
    while count2 < len(m_group_real[list_count]):
      final["("+ str(m_group_real[list_count][count]) + ", " + str(m_group_real[list_count][count2])+")"] = final_list[sumtracker]
      if count2+1 >= group_size:
        count+=1
        count2 = count + 1
      else:
        count2+=1
      sumtracker+=1
    if list_count+1 >= len(m_group_real):
      break
    else:
      list_count+=1
    count = 0
    count2 = 1    

  return (final)