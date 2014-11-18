
# coding: utf-8

# In[1]:

import svgwrite


# In[2]:




# In[3]:

methods_and_scores = {
    'BR': 3,
    'LP': 4,
    'mlg-lp-unweighted': 2.4444,
    'mlg-lp': 1.7778,
    'RAKEL1': 7,
    'RAKEL2': 5.8889,
    'MLkNN': 6.1111,
    'BPMLL': 6.7778,
    'CLR': 8,
}


# In[7]:

method_count = len(methods_and_scores)
# well we have to compare more than one method
assert (method_count > 1) 


# In[584]:

sorted_methods[4]


# In[575]:

critical_lines = [[1,4], [2,6]]


# In[576]:

sorted_methods = sorted(methods_and_scores, key=lambda x: methods_and_scores[x])


# In[598]:

font_height = 14
margin_ltbr = [70, 4*font_height, font_height, font_height]
main_line_color = svgwrite.rgb(10, 10, 16, '%')
text_color = 'red'
critical_line_color = 'orange'

# interval between methods
line_height = 1.5*font_height
interval_size = font_height*1.5
interval_height = font_height*0.33
# assume that 100px = 100%
size = interval_size*(method_count-1)

number_of_critical_lines = len(critical_lines)
critical_line_space = number_of_critical_lines*line_height
item_space = 1.5*line_height


# In[681]:

critical_distance_value = max([methods_and_scores[sorted_methods[x[1]]]-methods_and_scores[sorted_methods[x[0]]] for x in critical_lines])/float(method_count)
critical_distance = size * critical_distance_value


# In[682]:

dwg = svgwrite.Drawing('test.svg', profile='tiny')


# In[683]:

for interval_line_number in range(method_count):
    x_i = int(interval_size * interval_line_number)
    rank = method_count - interval_line_number
    text_element = svgwrite.text.Text(
            str(rank), 
            x = [margin_ltbr[0] + x_i],
            y = [margin_ltbr[1] + font_height], fill=text_color)
    text_element["text-anchor"] = "middle"
    dwg.add(text_element)

    dwg.add(
        svgwrite.shapes.Line(
            (x_i+margin_ltbr[0], 4+font_height+margin_ltbr[1]), 
            (x_i+margin_ltbr[0], 4.5+font_height+interval_height+margin_ltbr[1]), 
            stroke=main_line_color))
    
    method_position = size * methods_and_scores[sorted_methods[interval_line_number]]/float(method_count)
    method_vertical_end = (method_position+margin_ltbr[0], 4+font_height+margin_ltbr[1])
    anchor = "start"
    if (rank > ceil(0.5*method_count)):
        method_horizontal_end = 0+margin_ltbr[0]
        method_junction = critical_line_space+(rank-ceil(0.5*method_count))*item_space+margin_ltbr[1]
        anchor = "end"
    else:
        method_horizontal_end = size+margin_ltbr[0]
        method_junction = critical_line_space+rank*item_space+margin_ltbr[1]
        anchor = "start"
    
    
    dwg.add(
            svgwrite.shapes.Line(
                method_vertical_end, 
                (method_vertical_end[0], method_junction), 
                stroke=main_line_color))

    dwg.add(
            svgwrite.shapes.Line(
                (method_horizontal_end, method_junction), 
                (method_vertical_end[0], method_junction), 
                stroke=main_line_color))
    
    text_element = svgwrite.text.Text(
            str(sorted_methods[rank-1]), 
            x = [method_horizontal_end],
            y = [method_junction], fill=text_color)
    text_element["text-anchor"] = anchor
    dwg.add(text_element)

for i in xrange(len(critical_lines)):
    critical_line = critical_lines[i]
    method_position_left = 0+margin_ltbr[0] + size * methods_and_scores[sorted_methods[method_count-critical_line[0]]]/float(method_count)
    method_position_right = 0+margin_ltbr[0] +  size * methods_and_scores[sorted_methods[method_count-critical_line[1]]]/float(method_count)
    
    dwg.add(
            svgwrite.shapes.Line(
                (method_position_left, 4+font_height+interval_height+margin_ltbr[1]+(i+.5)*line_height*.5), 
                (method_position_right, 4+font_height+interval_height+margin_ltbr[1]+(i+.5)*line_height*.5), 
                stroke=critical_line_color))
    
    dwg.add(
    svgwrite.shapes.Line(
        (method_position_left, 4+font_height+interval_height+margin_ltbr[1]+(i+.25)*line_height*.5), 
        (method_position_left, 4+font_height+interval_height+margin_ltbr[1]+(i+.75)*line_height*.5), 
        stroke=critical_line_color))

    dwg.add(
        svgwrite.shapes.Line(
            (method_position_right, 4+font_height+interval_height+margin_ltbr[1]+(i+.25)*line_height*.5), 
            (method_position_right, 4+font_height+interval_height+margin_ltbr[1]+(i+.75)*line_height*.5), 
            stroke=critical_line_color))
    

text_element = svgwrite.text.Text(
            "Critical distance {0:.5f}".format(critical_distance_value), 
            x = [0+margin_ltbr[0]],
            y = [2.5*font_height], fill=critical_line_color)
dwg.add(text_element) 
    
dwg.add(
    svgwrite.shapes.Line(
        (0+margin_ltbr[0], 3*font_height), 
        (critical_distance+margin_ltbr[0], 3*font_height),
        stroke=critical_line_color))
dwg.add(
    svgwrite.shapes.Line(
        (0+margin_ltbr[0], 2.75*font_height), 
        (0+margin_ltbr[0], 3.25*font_height),
        stroke=critical_line_color))

dwg.add(
    svgwrite.shapes.Line(
        (critical_distance+margin_ltbr[0], 2.75*font_height), 
        (critical_distance+margin_ltbr[0], 3.25*font_height),
        stroke=critical_line_color))


dwg.add(
    svgwrite.shapes.Line(
        (0+margin_ltbr[0], 4+font_height+interval_height+margin_ltbr[1]), 
        (size+margin_ltbr[0], 4+font_height+interval_height+margin_ltbr[1]),
        stroke=main_line_color))


# In[684]:

dwg.save()


# In[612]:




# In[527]:




# In[469]:




# In[517]:




# In[517]:




# In[517]:




# In[ ]:




# In[ ]:



