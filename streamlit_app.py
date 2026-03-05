import streamlit as st

import pandas as pd

excel_file=st.file_uploader("Excelファイルを選択してください",type=['xlsx'])
if excel_file:
  df=pd.read_excel(excel_file)
  class_list=df['学級']
  your_class=st.selectbox('クラスを選択してください',class_list)
  class_dict={}
  for i in range(len(class_list)):
    class_dict[class_list[i]]=i
  from random import choice

  if st.button("Start!"):
    class_number=class_dict[your_class]
    class_data=df.iloc[class_number]
    n=class_data['人数']
    attendance_number_start=class_data['最初の出席番号']
    h,w=class_data['縦の長さ'],class_data['横の長さ']
    g=class_data['席'].split()
    grid=[]
    for i in g:
      grid.append(list(i))
    l = [i for i in range(1, n+1)]
    name = class_data['名前(出席番号順)'].split()
    max_name_length=max([len(i)for i in name])
    for i in range(len(name)):
      if i+attendance_number_start<=9:p=str(i+attendance_number_start)+" "
      else:p=str(i+attendance_number_start)
      name[i]=p+"."+name[i]+"  "*(max_name_length-len(name[i]))
    fix_number=class_data['固定人数']
    if fix_number!=0:
      fix_data=list(map(int,class_data['固定者の番号、位置'].split()))
    for i in range(fix_number):
      grid[fix_data[3*i+1]-1][fix_data[3*i+2]-1]=name[fix_data[3*i]-attendance_number_start]
      l.remove(fix_data[3*i]-attendance_number_start+1)
    tf=True
    for i in range(0,h):
      for j in range(0,w):
        if grid[i][j]=="x":
          grid[i][j]="   "+"  "*max_name_length
          continue
        if grid[i][j]=="o":
          c=choice(l)
          grid[i][j]=name[c - 1]
          l.remove(c)
    st.text("")
    data={}
    for i in range(w):
      newl=[]
      for j in range(h):
        newl.append(grid[j][i])
      data[i]=newl
    df_seat=pd.DataFrame(data)
    st.markdown(df_seat.to_html(index=False, header=False), unsafe_allow_html=True)