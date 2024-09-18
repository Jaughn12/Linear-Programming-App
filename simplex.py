from fractions import Fraction
import copy
def simplex_solver(constraint_inputs:list,obj_inputs:list,rhs_inputs:list,const_num:int,var_num:int):
    simplex_question = []
    simplex_question.append(obj_inputs)
    constraint_inputs = [constraint_inputs[i:i+var_num] for i in range(0, len(constraint_inputs), var_num)]
    simplex_question.extend(constraint_inputs)
    constraint_inequal = ['<=' for i in range(1,const_num+1)]
    col_list = [f'x{i}' for i in range(1,var_num+1)]
    row_list = ['z']
    row_list.extend([f'S{i}' for i in range(1,const_num+1)])
    row_list_1 = copy.deepcopy(row_list)
    basic_var = []
    for i in range(const_num+1):
        simplex_question[0].append(0)
    for x in range(1,const_num+1):
        for y in range(1,const_num+1):
            if x == y:
                if constraint_inequal[x-1] == '<=':   
                    simplex_question[x].append(1)
                    basic_var.append(var_num+y-1)
                else:
                    simplex_question[x].append(-1)
            else:
                simplex_question[x].append(0)
    for i in range(1,const_num+1):
        simplex_question[i].append(rhs_inputs[i-1])
    simplex_initial = copy.deepcopy(simplex_question)
    row_index = 0
    for row in simplex_initial:
        row_str = []
        for elem in row:
            if isinstance(elem, Fraction):
                numerator, denominator = elem.numerator, elem.denominator
            else:
                numerator, denominator = float_to_fraction(elem)
            row_str.append(format_fraction(numerator, denominator))
        simplex_initial[row_index]=row_str
        row_index+=1
    index = 2
    store = {}
    store[f'tableau_1']=simplex_initial
    store[f'tableau_1_basis']=row_list_1
    return tableau_generator(simplex_question,[1],basic_var,var_num,index,store,col_list,row_list)
def float_to_fraction(decimal):
    f = Fraction(decimal).limit_denominator()
    return f.numerator, f.denominator


def format_fraction(numerator, denominator):
    if numerator % denominator == 0:
        return str(numerator // denominator)
    else:
        return f"{numerator}/{denominator}"

def print_tableau(simplex_table):
    for row in simplex_table:
        row_str = []
        for elem in row:
            if isinstance(elem, Fraction):
                numerator, denominator = elem.numerator, elem.denominator
            else:
                numerator, denominator = float_to_fraction(elem)
            row_str.append(format_fraction(numerator, denominator))
        print("\t".join(row_str))
def tableau_generator(simplex_table:list,entering_index:list,basic_var:list,var_num:int,index:int,store:dict,col_list:list,row_list:list):
    obj_var_non_basic = []
    for i in range(len(simplex_table[0])-1):
        obj_var_non_basic.append(simplex_table[0][i])
    if not any(num > 0 for num in obj_var_non_basic):
        return (store,"Optimal Solution Found")
    max_obj = max(obj_var_non_basic)
    max_index = obj_var_non_basic.index(max_obj)
    entering_var_col = [simplex_table[i][max_index] for i in range(1,len(simplex_table))]
    entering_index = entering_var_col
    rhs_col = [simplex_table[i][-1] for i in range(1,len(simplex_table))]
    ratio = []
    for i in range(len(rhs_col)):
        try:
            if rhs_col[i] >= 0 and entering_var_col[i]>=0:
                ratio.append((rhs_col[i])/(entering_var_col[i]))
            else:
                ratio.append(-1)
                
        except ZeroDivisionError:
            ratio.append(-1)
    int_ratio = [i for i in ratio if i >= 0]
    if not int_ratio:
        return (store,"Problem is unbounded")
    min_ratio = min(int_ratio)
    leaving_row_index = ratio.index(min_ratio)+1
    pivot = simplex_table[leaving_row_index][max_index]
    simplex_table[leaving_row_index] = [i/(pivot) for i in simplex_table[leaving_row_index]]

    result = []
    for rows in range(len(simplex_table)):
        if rows == leaving_row_index:
            continue
        else:
            multiplier = simplex_table[rows][max_index]
            for elem1,elem2 in zip(simplex_table[rows],simplex_table[leaving_row_index]):
                result.append(elem1-(multiplier)*elem2)
            simplex_table[rows]=result
            result = []
    row_list[leaving_row_index]= col_list[max_index]
    
    store_simplex = copy.deepcopy(simplex_table)
    row_list_cp = copy.deepcopy(row_list)
    row_index = 0
    for row in store_simplex:
        row_str = []
        for elem in row:
            if isinstance(elem, Fraction):
                numerator, denominator = elem.numerator, elem.denominator
            else:
                numerator, denominator = float_to_fraction(elem)
            row_str.append(format_fraction(numerator, denominator))
        store_simplex[row_index]=row_str
        row_index+=1
    store[f'tableau_{index}']=store_simplex
    store[f'tableau_{index}_basis']=row_list_cp
    index+=1
    return tableau_generator(simplex_table,entering_index,basic_var,var_num,index,store,col_list,row_list)
if __name__ == "__main__":
   print(simplex_solver([2,3,1,1],[-2,-1],[12,6],2,2))
    
    
        
    


    
