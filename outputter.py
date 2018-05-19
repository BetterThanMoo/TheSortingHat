'''***********************************************************
This is one of the dependencies to the Diversity application
written by Patrick Gourley to output the calculated 
information into an excel spreadsheet
***********************************************************'''

#Imports 
import cvsimport
import os
from datetime import datetime
from xlwt import *
import getpass
import itertools


'''***********************************************************
Initialise relevant information, and setup styles for the
excel document before saving the output file to a folder named
Tests.
***********************************************************'''   
def get_print(output, big_or_small, number, filepath):
    r_group = output[0]
    m_group = output[1]
    s_group = output[2]
    range_groups = output[3]
    gender_groups = output[4]
    option_groups = output[5]
    balance_groups = output[6]
    per_question_result = output[7]
    similar = output[8]
    group_size = number
    wb = Workbook()
    sheet1 = wb.add_sheet('Answers')
    sheet2 = wb.add_sheet('Breakdown')
    
    #Styles
    headingstyle = easyxf('font: name Calibri (Body); font: height 320; font: bold on; align: horiz center')
    totalstyle = easyxf('font: name Calibri (Body); font: height 320; font: bold on; font: color_index blue; align: horiz center')
    groupstyle = easyxf('font: name Calibri (Body); font: height 240; align: horiz center')
    namestyle = easyxf('font: name Calibri (Body); font: height 240; font: bold on; align: horiz center')  
    question_score_style = easyxf('font: name Calibri (Body); font: height 240; font: bold on; font: color_index red; align: horiz center')  
    question_total_style = easyxf('font: name Calibri (Body); font: height 240; font: bold on; font: color_index blue; align: horiz center')  
    questiontitlestyle = easyxf('font: name Calibri (Body); font: height 240; font: bold on; font: italic on; align: horiz center') 
    scorestyle = easyxf('font: name Calibri (Body); font: height 560; font: bold on; font: color_index red; align: horiz center')
    lscorestyle = easyxf('font: name Calibri (Body); font: height 320; font: bold on; font: color_index red; align: horiz center')
    
    row_count = 0
    position_count = 0
    other_count = 0
    ingroup = True
   
    while position_count < len(r_group):
        if other_count == 0:
            if (r_group[position_count]) != 'Not in Group':  
                if big_or_small == True:
                    sheet1.write(row_count, 0, 'MOST DIVERSE', headingstyle)
                    big_or_small = False
                else:
                    sheet1.write(row_count, 0, 'LEAST DIVERSE', headingstyle)
                    big_or_small = True
                    
                sheet1.write(row_count, 2, 'TOTAL SCORE', namestyle)
                sheet1.write(row_count+1, 0, r_group[position_count], groupstyle)
                sheet1.write(row_count, 3, 'RANGE', namestyle)
                sheet1.write(row_count, 4, 'GENDER', namestyle)
                sheet1.write(row_count, 5, 'OPTIONS', namestyle)
                sheet1.write(row_count, 6, 'BALANCE', namestyle)
                
                row_count+=1
                if type(s_group[position_count]) == int:
                    sheet1.write(row_count, 2, s_group[position_count], scorestyle)
                    sheet1.write(row_count, 3, range_groups[position_count], lscorestyle)
                    sheet1.write(row_count, 4, gender_groups[position_count], lscorestyle)
                    sheet1.write(row_count, 5, option_groups[position_count], lscorestyle)
                    sheet1.write(row_count, 6, balance_groups[position_count], lscorestyle)
                else:
                    sheet1.write(row_count, 2, 'N/A', scorestyle)
                    sheet1.write(row_count, 3, 'N/A', lscorestyle)
                    sheet1.write(row_count, 4, 'N/A', lscorestyle)
                    sheet1.write(row_count, 5, 'N/A', lscorestyle)
                    sheet1.write(row_count, 6, 'N/A', lscorestyle)
                    
                row_count+=1  
                sheet1.write(row_count, 2, 100, totalstyle)
                sheet1.write(row_count, 3, 27, totalstyle)
                sheet1.write(row_count, 4, 10, totalstyle)
                sheet1.write(row_count, 5, 36, totalstyle)
                sheet1.write(row_count, 6, 27, totalstyle)
                
                row_count+=2
                other_count+=1
    
                intra_row_count = row_count
                sheet1.write(intra_row_count, 3, 'Intra-Group Diversity', namestyle)
                intra_row_count+=1
                
                sheet1.write(intra_row_count, 2, 'Question', questiontitlestyle)
                sheet1.write(intra_row_count, 3, 'Score', questiontitlestyle) 
                sheet1.write(intra_row_count, 4, 'Total', questiontitlestyle)
                
                intra_row_count+=1
                count = 0
                while count < 10:
                    sheet1.write((intra_row_count+count), 2, count+1, namestyle)
                    count+=1

                count = 0  
                while count < 10:
                    if len(per_question_result) > position_count:
                        for i in per_question_result[position_count]:
                            sheet1.write((intra_row_count+count), 3, i, question_score_style)
                            count+=1  
                    else:
                        sheet1.write((intra_row_count+count), 3, 'N/A', question_score_style)
                        count+=1

                count = 0
                while count < 10:
                    sheet1.write((intra_row_count+count), 4, 10, question_total_style)    
                    count+=1
                
                row_count+=10

            else:
                if ingroup == True:
                    sheet1.write(row_count-9, 0, r_group[position_count], lscorestyle)
                    ingroup = False
                for i in m_group[position_count]:
                    sheet1.write(row_count-8, 0, i, namestyle)
                    row_count+=1
                other_count = 0
                position_count += 1
        else:
            for i in m_group[position_count]:
                sheet1.write(row_count-11, 0, i, namestyle)
                row_count+=1
            other_count = 0
            position_count += 1

    col_width = 234 * 20    
    try:
        for i in itertools.count():
            sheet1.col(i).width = col_width
            sheet2.col(i).width = col_width
    except ValueError:
        pass    

    magic = int((group_size-1) * (group_size / 2))
    count = 0
    group_count = 0
    group_divider = []
    while count < len(similar):
        for i in similar:
            group_divider.append(i)
            if count-1 == -1:
                sheet2.write(count, 4, "Group " + str(r_group[group_count]), groupstyle)
                count+=1
                sheet2.write(count, 4, "", namestyle)
                sheet2.write(count, 5, "", namestyle)  
                count+=1
            if len(r_group) > 1:   
                if group_count+1 < len(r_group) and (r_group[group_count+1]) != 'Not in Group':
                    if len(group_divider) % magic == 0:
                        sheet2.write(count, 4, "", namestyle)
                        sheet2.write(count, 5, "", namestyle)  
                        count+=1
                        sheet2.write(count, 4, "Group " + str(r_group[group_count]), groupstyle)
                        count+=1
                        sheet2.write(count, 4, "", namestyle)
                        sheet2.write(count, 5, "", namestyle)  
                        count+=1
                        group_count+=1
            sheet2.write(count, 4, i, namestyle)
            sheet2.write(count, 5, similar[i], lscorestyle)      
            count+=1  
            
    filepath.append(filepath[0])
    l = list(filepath[1])
    for i in reversed(l):
        if i == '/':
            break
        else:
            del(l[-1])
    filepath.append("".join(l))
    if not os.path.exists(str(filepath[-1]) + '/Tests/'):
        os.makedirs(str(filepath[-1]) + '/Tests/')        
    wb.save(str(filepath[-1]) + '/Tests/' + 'test_results' + str(datetime.now()) + '.xls')