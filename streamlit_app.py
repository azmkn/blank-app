import streamlit as st
n=st.number_input('数',1)
or_n=n
exp=0
b=1
while n%2==0:
  n//=2
while n%5==0:
  n//=5
if n==1:
  st.text(str(or_n)+":"+str(exp))
while True:
  b*=10
  exp+=1
  b%=n
  if b==1:

    if st.button("表示"):
      st.text(str(or_n)+"   :   "+str(exp))
      st.text("(1/or_n)={:.100f}")
      exit()