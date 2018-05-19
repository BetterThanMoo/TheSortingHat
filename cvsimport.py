'''***********************************************************
This is one of the dependencies to the Diversity application
written by Patrick Gourley to import survey monkey csvs
and strip away unncessessary information
***********************************************************'''

#Imports 
import csv
import Diversity
import re

'''***********************************************************
This function firstly reads how many participants are featured
in the survey. And secondly, passes stripped information into
the diversity calculator.
***********************************************************'''
def get_num_people(questionaire_answers, number=None, big_or_small=None):
  with open(questionaire_answers, 'r') as f:
    reader = csv.reader(f)
    answers_as_list = list(reader)

  del([answers_as_list[0]])
  del ([answers_as_list[0]])

  main_count = 0
  first_inside = 0
  second_inside = 0  
  while main_count < len(answers_as_list)+1:
    while first_inside < main_count:
      while second_inside < 9:
        del([answers_as_list[first_inside][0]])
        second_inside +=1
      first_inside+=1
      second_inside = 0
    main_count+=1   
    insder = 0
       
  main_count = 0
  first_inside = 0
  second_inside = 0  
  
  while main_count < len(answers_as_list):
    while first_inside <= main_count:
      while second_inside < 1:
        del([answers_as_list[main_count][2]])     
        second_inside +=1
      first_inside+=1
      second_inside = 0
    insider = 0
    main_count+=1     

  with_numbers = []
  with_numbers_final = {}
  count = 0
  name_count = 1
  whoiswho = {}
  for i in answers_as_list:
    for j in i:
      if j.isdigit():
        with_numbers.append(int(j))
      else:
        if j != '':
          with_numbers.append(j)
     
  while len(with_numbers) > count:
    if count % 11 == 0:
      with_numbers_final[name_count] = with_numbers[count+1:count+11]
      whoiswho[name_count] = with_numbers[count]
      name_count+=1
      count+=11
      
  if number!= None and number > 0:
    return main(with_numbers_final, number, big_or_small, whoiswho)
  else:
    return (len(answers_as_list))  
  

'''***********************************************************
This function takes the diversity calculation and formats
it for use in the output 
***********************************************************'''
def main(with_numbers_final, number, big_or_small, whoiswho):
  resulting1 =  Diversity.run(number, with_numbers_final, big_or_small)
  resulting = resulting1[0]
  resultington = resulting[0]
  
  range_groups = resulting[1]
  gender_groups = resulting[2]
  option_groups = resulting[3]
  balance_groups = resulting[4]
  per_question_result = resulting[5]
  similar = resulting1[1]
  similar_temp = resulting1[1]
  
  
  other_similar =[]
  for i in similar:
    other_similar.append(i)  
  
  for k, v in whoiswho.items():
    resultington = [w.replace('({},'.format(k), '({},'.format(v)) for w in resultington]
    resultington = [w.replace(' {},'.format(k), ' {},'.format(v)) for w in resultington]
    resultington = [w.replace(' {})'.format(k), ' {})'.format(v)) for w in resultington]
    resultington = [w.replace('({})'.format(k), '({})'.format(v)) for w in resultington]
    
  for k, v in whoiswho.items():
    similar_temp = [w.replace('({},'.format(k), '({},'.format(v)) for w in similar_temp]
    similar_temp = [w.replace(' {},'.format(k), ' {},'.format(v)) for w in similar_temp]
    similar_temp = [w.replace(' {})'.format(k), ' {})'.format(v)) for w in similar_temp]
    similar_temp = [w.replace('({})'.format(k), '({})'.format(v)) for w in similar_temp]  

  
  similar_real = {}
  count = 0
  for i in similar_temp:
    similar_real[i] = similar[other_similar[count]]
    count+=1
  
    
  r_group = []
  o_count = 0
  for i in resultington:
    count = 0
    while count < len(resultington[o_count]):
      if i[count] == ':':
        r_group.append(i[0:count])
        break
      else:
        count+=1
    o_count+=1
    
  m_group = []
  o_count = 0
  count_start = 0
  count_end = 0
  for i in resultington:
    count = 0
    while count < len(resultington[o_count]):
      if i[count] == '(':
        count_start = count+1
      if i[count] == ')':
        count_end = count
        m_group.append(i[count_start:count_end])
        break
      else:
        count+=1
    o_count+=1   
    
    
  s_group = []
  o_count = 0
  for i in resultington:
    count = 0
    while count < len(resultington[o_count]):
      if i[-count] == ':':
        s_group.append(i[-count+2::])
        break
      else:
        count+=1
    o_count+=1 
  
  m_group_real = []
  for i in m_group:
    i = i.split(',')
    m_group_real.append(i)
    
  s_group_real = []
  for i in s_group:
    i = i.split(',')
    if i[0].isdigit() == True:
      s_group_real.append(int(i[0]))
    else:
      s_group_real.append(i[0])
  
  return (r_group, m_group_real, s_group_real, range_groups, gender_groups, option_groups, balance_groups, per_question_result, similar_real)